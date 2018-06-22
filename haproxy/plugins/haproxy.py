#!/usr/bin/env python3

import csv
import io
import socket
import sys
import requests

from outlyer_plugin import Plugin, Status


#TODO: HAPROXY show info command


class HAProxyPlugin(Plugin):

    STATUS_MAP = {'UP': 0, 'DOWN': 1}

    COUNTER_METRICS = [
        'bin',
        'bout',
        'dreq',
        'dresp',
        'ereq',
        'econ',
        'eresp',
        'wretr',
        'wredis',
        'hrsp_4xx',
        'hrsp_5xx',
    ]

    GAUGE_METRICS = [
        'qcur',
        'scur',
        'status',
        'rate',
        'req_rate',
        'qtime',
        'rtime',
    ]

    def connect_socket(self, path):
        in_buf = io.BytesIO()
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

    def collect(self, _) -> Status:

        data = None
        if self.get('mode', 'socket') == 'socket':
            sock_path = self.get('haproxy_sock', '/var/run/haproxy.sock')
            data = self.connect_socket(sock_path)
        else:
            url = self.get('url')
            username = self.get('username')
            password = self.get('password')

            if not url:
                self.logger.error('HTTP mode specified but no URL provided')
                return Status.UNKNOWN

            if ';csv' not in url:
                url += ';csv;norefresh'

            data = self.connect_http(url, username, password)

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
                    self.counter(f'haproxy.{k}', labels).set(val)
                except KeyError:
                    pass
                except ValueError:
                    pass

            for k in self.GAUGE_METRICS:
                try:
                    val = float(row[k])
                    self.gauge(f'haproxy.{k}', labels).set(val)
                except KeyError:
                    pass
                except ValueError:
                    pass

        return Status.OK


if __name__ == '__main__':
    sys.exit(HAProxyPlugin().run())
