from outlyer_agent.collection import Status, Plugin, PluginTarget, DEFAULT_PLUGIN_EXEC
from datetime import datetime
import re
import os
import time


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
    return ''.join('(?P<' + g + '>.*?)' if g else re.escape(c) for g, c in find_vars(text))



class NginxLogsPlugin(Plugin):

    COMBINED_FORMAT = '$remote_addr - $remote_user [$time_local] "$request" $status ' \
                      '$body_bytes_sent "$http_referer" "$http_user_agent"'

    TIMED_COMBINED_FORMAT = '$remote_addr - $remote_user [$time_local] "$request" $status ' \
                            '$body_bytes_sent $request_time "$http_referer" "$http_user_agent"'

    def collect(self, target: PluginTarget):

        log_path = target.get('access_log')
        if not log_path:
            self.logger.error('Log path not specified in configuration file')
            return Status.UNKNOWN

        interval = target.get('interval', 60)
        count = 0
        total = 0.0

        for code in '1xx', '2xx', '3xx', '4xx', '5xx', 'requests':
            target.gauge(code).set(0)

        timed_combined_regex = re.compile(log_format_2_regex(NginxLogsPlugin.TIMED_COMBINED_FORMAT))
        combined_regex = re.compile(log_format_2_regex(NginxLogsPlugin.COMBINED_FORMAT))

        timezone = time.strftime("%z", time.localtime())
        start_time = datetime.now()

        for line in reverse_readline(log_path):

            m = timed_combined_regex.match(line) or combined_regex.match(line)
            data = m.groupdict()

            line_time = datetime.strptime(data['time_local'], '%d/%b/%Y:%H:%M:%S ' + timezone)
            if (start_time - line_time).total_seconds() >= interval:
                break

            code = data['status']
            target.gauge('nginx_' + code).inc(1)
            target.gauge('nginx_' + code[0] + 'xx').inc(1)
            target.gauge('nginx_requests').inc(1)

            if 'request_time' in data:
                rt = float(data['request_time'])
                if count == 0 or rt < target.gauge('nginx_min_response_time', {'uom': 'sec'}).get():
                    target.gauge('min', {'uom': 'sec'}).set(rt)
                if count == 0 or rt > target.gauge('nginx_max_response_time', {'uom': 'sec'}).get():
                    target.gauge('max', {'uom': 'sec'}).set(rt)

                total += rt
                count += 1

        if count > 0:
            avg = total / count
            target.gauge('nginx_avg_response_time', {'uom': 'sec'}).set(avg)

        for code in '1xx', '2xx', '3xx', '4xx', '5xx', 'requests':
            target.gauge('nginx_' + code + '_per_sec').set(target.gauge(code).get() / interval)

        return Status.OK
