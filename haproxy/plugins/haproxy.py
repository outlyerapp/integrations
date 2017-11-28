import csv
import io
import socket
import requests

from outlyer_agent.collection import Status, Plugin, PluginTarget

class HAProxyPlugin(Plugin):

    STATUS_MAP = {'UP': 0, 'DOWN': 1}

    COUNTER_METRICS = [
        'stot', 'bin', 'bout', 'dreq', 'dresp', 'ereq', 'econ', 'eresp',
        'wretr', 'wredis', 'chkfail', 'chkdown', 'downtime', 'lbtot',
        'hrsp_1xx', 'hrsp_2xx', 'hrsp_3xx', 'hrsp_4xx', 'hrsp_5xx', 'hrsp_other',
        'hanafail', 'req_tot', 'cli_abrt', 'srv_abrt',
        'comp_in', 'comp_out', 'comp_byp', 'comp_rsp'
    ]

    GAUGE_METRICS = [
        'qcur', 'qmax', 'scur', 'smax', 'slim', 'status', 'weight', 'act', 'bck', 'lastchg',
        'qlimit', 'throttle', 'type', 'rate', 'rate_lim', 'rate_max', 'req_rate', 'req_rate_max',
        'lastsess', 'qtime', 'ctime', 'rtime', 'ttime'
    ]

    def connect_socket(self, path):
        in_buf = io.StringIO()
        try:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.connect(path)
            s.send(b'show stat\n')
            while True:
                data = s.recv(4096)
                in_buf.write(data)
                if not data:
                    break
            s.close()
        except OSError as ex:
            self.logger.error('Unable to open %s: %s', path, str(ex))
        finally:
            return in_buf.getvalue()

    def connect_http(self, url, username=None, password=None):
        r = requests.get(url, auth=(username, password))
        return r.content


    def translate_status(self, status):
        return self.STATUS_MAP.get(status, 2)

    def collect(self, target: PluginTarget) -> Status:

        data = None
        if target.get('mode', 'socket') == 'socket':
            sock_path = target.get('haproxy_sock', '/var/run/haproxy.sock')
            data = self.connect_socket(sock_path)
        else:
            url = target.get('url')
            username = target.get('username')
            password = target.get('password')

            if not url:
                self.logger.error('HTTP mode specified but no URL provided')
                return Status.UNKNOWN

            if ';csv' not in url:
                url += ';csv;norefresh'

            response = self.connect_http(url, username, password)
            data = response.content

        if data is None:
            return Status.CRITICAL

        in_buf = io.StringIO(data.decode('utf-8'))

        x = csv.DictReader(in_buf)
        for row in x:
            row.pop('')
            pxname = row.pop('# pxname')
            svname = row.pop('svname')
            row['status'] = self.translate_status(row['status'])

            labels = {'pxname': pxname, 'svname': svname}
            for k in self.COUNTER_METRICS:
                try:
                    val = float(row[k])
                    target.counter(f'haproxy.{k}', labels).set(val)
                except KeyError:
                    pass
                except ValueError:
                    pass

            for k in self.GAUGE_METRICS:
                try:
                    val = float(row[k])
                    target.gauge(f'haproxy.{k}', labels).set(val)
                except KeyError:
                    pass
                except ValueError:
                    pass

        return Status.OK
