from outlyer_agent.collection import Status, Plugin, PluginTarget, DEFAULT_PLUGIN_EXEC
from datetime import datetime, timezone
import re
import os
import logging
import tzlocal

logger = logging.getLogger(__name__)


def reverse_readline(filename, buf_size=8192):
    """a generator that returns the lines of a file in reverse order"""
    with open(filename) as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        file_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(file_size, offset + buf_size)
            fh.seek(file_size - offset)
            buffer = fh.read(min(remaining_size, buf_size))
            remaining_size -= buf_size
            lines = buffer.split('\n')
            # the first line of the buffer is probably not a complete line so
            # we'll save it and append it to the last line of the next buffer
            # we read
            if segment is not None:
                # if the previous chunk starts right from the beginning of line
                # do not concact the segment to the last line of new chunk
                # instead, yield the segment first
                if buffer[-1] is not '\n':
                    lines[-1] += segment
                else:
                    yield segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                if len(lines[index]):
                    yield lines[index]
        # Don't yield None if the file was empty
        if segment is not None:
            yield segment


var_pattern = re.compile(r'\$(\w+)|(.)')


def find_vars(text):
    return var_pattern.findall(text)


def log_format_2_regex(text):
    return '^' + ''.join('(?P<' + g + '>.*?)' if g else re.escape(c) for g, c in find_vars(text)) + '$'


class NginxLogsPlugin(Plugin):

    LOG_FORMATS = [
        '$remote_addr - $remote_user [$time_local] "$request" $status '
        '$body_bytes_sent "$http_referer" "$http_user_agent"',

        '$remote_addr - $remote_user [$time_local] "$request" $status '
        '$body_bytes_sent $request_time "$http_referer" "$http_user_agent"',

        '$remote_addr - $remote_user [$time_local] "$request" $status '
        '$body_bytes_sent "$http_referer" "$http_user_agent" "$request_time"',

        '$remote_addr - $remote_user [$time_local] "$request" $status '
        '$body_bytes_sent "$http_referer" "$http_user_agent" "$request_time "'
        '"$upstream_connect_time" "$upstream_header_time" "$upstream_response_time"',

        '$remote_addr - $remote_user [$time_local] "$request" $status '
        '$body_bytes_sent "$http_referer" "$http_user_agent" $request_time '
        '$upstream_response_time $pipe'
    ]

    TIME_FIELDS = [
        'request_time', 'upstream_connect_time', 'upstream_header_time', 'upstream_response_time'
    ]

    def collect(self, target: PluginTarget):

        log_path = target.get('access_log')
        if not log_path:
            self.logger.error('Log path not specified in configuration file')
            return Status.UNKNOWN

        interval = target.get('interval', 60)
        interval = 3600
        count = 0
        total = 0.0
        warned = False

        metrics = dict()

        for code in '1xx', '2xx', '3xx', '4xx', '5xx', 'requests':
            metrics[f'nginx.{code}'] = 0

        for k in self.TIME_FIELDS:
            metrics[f'nginx.total_{k}'] = 0
            metrics[f'nginx.count_{k}'] = 0
            metrics[f'nginx.min_{k}'] = 0
            metrics[f'nginx.max_{k}'] = 0

        log_formats = [re.compile(log_format_2_regex(x)) for x in self.LOG_FORMATS]

        start_time = datetime.now(tzlocal.get_localzone())

        try:
            for line in reverse_readline(log_path):

                m = None
                for pattern in log_formats:
                    m = pattern.match(line)
                    if m:
                        break
                if not m:
                    if not warned:
                        self.logger.warn('log file does not match any known format')
                    warned = True
                    continue

                data = m.groupdict()

                line_time = datetime.strptime(data['time_local'], '%d/%b/%Y:%H:%M:%S %z')
                if (start_time - line_time).total_seconds() >= interval:
                    break

                code = data['status']
                metrics[f'nginx.{code}'] = metrics.get(f'nginx.{code}', 0) + 1
                metrics[f'nginx.{code[0]}xx'] += 1
                metrics[f'nginx.requests'] += 1

                for k in self.TIME_FIELDS:
                    try:
                        val = float(data[k])
                        if metrics[f'nginx.count_{k}'] == 0 or val > metrics[f'nginx.max_{k}']:
                            metrics[f'nginx.max_{k}'] = val
                        if metrics[f'nginx.count_{k}'] == 0 or val < metrics[f'nginx.min_{k}']:
                            metrics[f'nginx.min_{k}'] = val
                        metrics[f'nginx.count_{k}'] += 1
                        metrics[f'nginx.total_{k}'] += val

                    except KeyError:
                        pass

        except FileNotFoundError:
            self.logger.error('Nginx log file not found: %s', log_path)
            return Status.UNKNOWN

        for k in self.TIME_FIELDS:
            if metrics[f'nginx.count_{k}'] > 0:
                metrics[f'nginx.avg_{k}'] = metrics[f'nginx.total_{k}'] / metrics[f'nginx.count_{k}']
            del metrics[f'nginx.total_{k}']
            del metrics[f'nginx.count_{k}']

        for code in '1xx', '2xx', '3xx', '4xx', '5xx', 'requests':
            metrics[f'nginx.{code}_per_sec'] = metrics[f'nginx.{code}'] / interval

        for k, v in metrics.items():
            target.gauge(k).set(v)

        return Status.OK
