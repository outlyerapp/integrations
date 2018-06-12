#!/usr/bin/env python3

import re
import os
import sys
import psutil
import requests
import requests.exceptions
from datetime import datetime
import tzlocal
from outlyer_plugin import Plugin, Status


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
            # we'll save it and append it to the last line of the next bzuffer
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


class NginxPlugin(Plugin):

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

    def collect(self, _):
        is_nginx_plus = self.get('nginx_plus', False)
        if is_nginx_plus:
            self.__collect_nginx_plus()
        else:
            self.__collect_nginx_open_source()

        self.__collect_process_metrics()
        self.__collect_access_log_metrics()
        return Status.OK


    def __collect_nginx_plus(self):
        """
        Collect metrics from Nginx plus (module: ngx_http_status_module)
        """
        try:
            # Connection metrics
            res = self.__get_nginx_plus_data("/connections")
            self.gauge('nginx.connections_accepted').set(res['accepted'])
            self.gauge('nginx.connections_dropped').set(res['dropped'])
            self.gauge('nginx.connections_active').set(res['active'])
            self.gauge('nginx.connections_idle').set(res['idle'])

            # Request Metrics
            res = self.__get_nginx_plus_data("/http/requests")
            self.gauge('nginx.requests_current').set(res['current'])
            self.gauge('nginx.requests_total').set(res['total'])

            # SSL metrics
            res = self.__get_nginx_plus_data("/ssl")
            self.gauge('nginx_plus.ssl_handshakes').set(res['handshakes'])
            self.gauge('nginx_plus.ssl_handshakes_failed').set(res['handshakes_failed'])
            self.gauge('nginx_plus.ssl_session_reuses').set(res['session_reuses'])

            # Upstream metrics
            res = self.__get_nginx_plus_data("/http/upstreams")
            self.gauge('nginx_plus.upstream_count').set(len(res.items()))
            for upstream_name, upstream in res.items():
                labels = {'upstream': upstream_name}
                for peer in upstream['peers']:
                    labels.update({'peer': peer['name']})
                    self.gauge('nginx_plus.upstream_peer_id', labels).set(peer['id'])
                    self.gauge('nginx_plus.upstream_peer_weight', labels).set(peer['weight'])
                    self.gauge('nginx_plus.upstream_peer_active', labels).set(peer['active'])
                    self.gauge('nginx_plus.upstream_peer_requests', labels).set(peer['requests'])
                    self.gauge('nginx_plus.upstream_peer_responses_1xx', labels).set(peer['responses']['1xx'])
                    self.gauge('nginx_plus.upstream_peer_responses_2xx', labels).set(peer['responses']['2xx'])
                    self.gauge('nginx_plus.upstream_peer_responses_3xx', labels).set(peer['responses']['3xx'])
                    self.gauge('nginx_plus.upstream_peer_responses_4xx', labels).set(peer['responses']['4xx'])
                    self.gauge('nginx_plus.upstream_peer_responses_5xx', labels).set(peer['responses']['5xx'])
                    self.gauge('nginx_plus.upstream_peer_responses_total', labels).set(peer['responses']['total'])
                    self.gauge('nginx_plus.upstream_peer_sent', labels).set(peer['sent'])
                    self.gauge('nginx_plus.upstream_peer_received', labels).set(peer['received'])
                    self.gauge('nginx_plus.upstream_peer_fails', labels).set(peer['fails'])
                    self.gauge('nginx_plus.upstream_peer_unavailable', labels).set(peer['unavail'])
                    self.gauge('nginx_plus.upstream_peer_health_checks_checks', labels).set(peer['health_checks']['checks'])
                    self.gauge('nginx_plus.upstream_peer_health_checks_fails', labels).set(peer['health_checks']['fails'])
                    self.gauge('nginx_plus.upstream_peer_health_checks_unhealthy', labels).set(peer['health_checks']['unhealthy'])
                    if peer['health_checks']['last_passed'] == False:
                        self.gauge('nginx_plus.upstream_peer_health_checks_last_passed', labels).set(1)
                    else:
                        self.gauge('nginx_plus.upstream_peer_health_checks_last_passed', labels).set(0)

                    # Collect peer state
                    up = 0
                    draining = 0
                    down = 0
                    unavail = 0
                    checking = 0
                    unhealthy = 0

                    if peer['state'] == 'up':
                        up = 1
                    elif peer['state'] == 'draining':
                        draining = 1
                    elif peer['state'] == 'down':
                        down = 1
                    elif peer['state'] == 'unavail':
                        unavail = 1
                    elif peer['state'] == 'checking':
                        checking = 1
                    elif peer['state'] == 'unhealthy':
                        unhealthy = 1

                    labels.update({"state": "up"})
                    self.gauge('nginx_plus.upstream_peer_state', labels).set(up)
                    labels.update({"state": "draining"})
                    self.gauge('nginx_plus.upstream_peer_state', labels).set(draining)
                    labels.update({"state": "down"})
                    self.gauge('nginx_plus.upstream_peer_state', labels).set(down)
                    labels.update({"state": "unavail"})
                    self.gauge('nginx_plus.upstream_peer_state', labels).set(unavail)
                    labels.update({"state": "checking"})
                    self.gauge('nginx_plus.upstream_peer_state', labels).set(checking)
                    labels.update({"state": "unhealthy"})
                    self.gauge('nginx_plus.upstream_peer_state', labels).set(unhealthy)

        except requests.exceptions.HTTPError as ex:
            self.logger.error('Unable to connect to Nginx Plus server: ' + ex.args[0])
            self.last_collect = None
            sys.exit(2)

        except Exception as ex:
            self.logger.exception('Error in plugin', exc_info=ex)
            self.last_collect = None
            sys.exit(2)


    def __get_nginx_plus_data(self, endpoint):
        url = self.get('url_nginx_plus_api', 'http://localhost/api/3')
        response = requests.get(url+endpoint)
        response.raise_for_status()
        return response.json()


    def __collect_access_log_metrics(self):
        """
        Collect metrics from Nginx access log file
        """
        log_path = self.get('access_log', '/var/log/nginx/access.log')
        if not log_path:
            self.logger.error('Log path not specified in configuration file')
            sys.exit(2)

        interval = 60
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
            sys.exit(2)

        for k in self.TIME_FIELDS:
            if metrics[f'nginx.count_{k}'] > 0:
                metrics[f'nginx.avg_{k}'] = metrics[f'nginx.total_{k}'] / metrics[f'nginx.count_{k}']
            del metrics[f'nginx.total_{k}']
            del metrics[f'nginx.count_{k}']

        for code in '1xx', '2xx', '3xx', '4xx', '5xx', 'requests':
            metrics[f'nginx.{code}_per_sec'] = metrics[f'nginx.{code}'] / interval

        for k, v in metrics.items():
            self.gauge(k).set(v)


    def __collect_process_metrics(self):
        """
        Collect metrics from Nginx process
        """
        master_count = 0
        worker_count = 0

        for proc in psutil.process_iter():
            try:
                arg0 = proc.cmdline()[0]
                if 'nginx: master process' in arg0:
                    master_count += 1
                elif 'nginx: worker process' in arg0:
                    worker_count += 1
            except ProcessLookupError:
                pass
            except psutil.AccessDenied:
                pass
            except psutil.ZombieProcess:
                pass
            except IndexError:
                pass
        self.gauge('nginx.master_proc_count').set(master_count)
        self.gauge('nginx.worker_proc_count').set(worker_count)



    def __collect_nginx_open_source(self):
        """
        Collect metrics from open source Nginx (module: ngx_http_stub_status_module)
        """
        url = self.get('url_nginx_status', 'http://localhost/nginx_status')
        if not url:
            self.logger.error('Nginx server status URL not specified in configuration file')
            sys.exit(2)

        try:
            response = requests.get(url)
            response.raise_for_status()

            text = response.content.decode('utf-8')

            m = re.search(r'Active connections:\s+(\d+)', text)
            if m:
                active = int(m.group(1))

            m = re.search(r'server accepts handled requests\n\s+(\d+)\s+(\d+)\s+(\d+)', text)
            if m:
                accepted = int(m.group(1))
                handled = int(m.group(2))
                total = int(m.group(3))
                self.gauge('nginx.connections_accepted').set(accepted)
                self.gauge('nginx.connections_dropped').set(accepted - handled)
                self.gauge('nginx.requests_total').set(total)

            m = re.search(r'Reading:\s+(\d+)\s+Writing:\s+(\d+)\s+Waiting:\s+(\d+)', text)
            if m:
                reading = int(m.group(1))
                writing = int(m.group(2))
                waiting = int(m.group(3))
                self.gauge('nginx.connections_active').set(active - waiting)
                self.gauge('nginx.requests_current').set(reading + writing)
                self.gauge('nginx.connections_idle').set(waiting)

        except requests.exceptions.RequestException as ex:
            self.logger.error('Unable to connect to Nginx server: ' + str(ex))
            sys.exit(2)

        except Exception as ex:
            self.logger.exception('Error in plugin', exc_info=ex)
            sys.exit(2)


if __name__ == '__main__':
    sys.exit(NginxPlugin().run())