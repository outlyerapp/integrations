import csv
import io
import socket

from outlyer_agent.collection import Status, Plugin, PluginTarget, DEFAULT_PLUGIN_EXEC, Metric


class HAProxyPlugin(Plugin):

    def collect(self, target: PluginTarget) -> Status:

        def status_code(status):
            if status == 'UP':
                return 0
            elif status == 'DOWN':
                return 1
            else:
                return 2

        sock_path = target.get('haproxy_sock', '/var/run/haproxy.sock')

        try:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.connect(sock_path)
            s.send(b'show stat \n')
            data = s.recv(32768)
            s.close()
        except OSError as ex:
            self.logger.error('Unable to open %s: %s', sock_path, str(ex))
            return Status.UNKNOWN

        in_buf = io.StringIO(data.decode('utf-8'))

        x = csv.DictReader(in_buf)
        for row in x:
            row.pop('')
            pxname = row.pop('# pxname')
            svname = row.pop('svname')
            row['status'] = status_code(row['status'])
            for k, v in row.items():
                try:
                    v = float(v)
                    target.gauge(f'haproxy_{pxname}_{svname}_k').set(v)
                except ValueError:
                    pass

        return Status.OK
