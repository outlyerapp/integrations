#!/usr/bin/env python3

import platform
import re
import subprocess
import sys

from outlyer_plugin import Plugin, Status


class PingPlugin(Plugin):

    def collect(self, _):

        count = self.get('count', 3)
        hosts = self.get('hosts', '192.168.1.1')
 
        if isinstance(hosts, str):
            hosts = [x.strip() for x in hosts.split(',')]

        command = 'ping -c {count} {host}'
        parser_1 = r'(?P<sent>\d+) packets transmitted, (?P<rcvd>\d+) (?:packets )?received, ' + \
                   '(?P<loss>[\d.]+)% packet loss(?:, time (?P<time>\d+)\s*ms)?'
        parser_2 = r'(?P<min>[\d.]+)/(?P<avg>[\d.]+)/(?P<max>[\d.]+)/(?P<stddev>[\d.]+) ms'

        if platform.system() == "Windows":
            command = 'ping -n {count} {host}'
            parser_1 = r'Packets: Sent = (?P<sent>\d+), Received = (?P<rcvd>\d+), Lost = \d+ \((?P<loss>[\d.]+)% loss\)'
            parser_2 = r'Minimum = (?P<min>[\d.]+)ms, Maximum = (?P<max>[\d.]+)ms, Average = (?P<avg>[\d.]+)ms'

        status = Status.OK

        for host in hosts:
            result = subprocess.run(command.format(count=count, host=host),
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    timeout=30, shell=True, universal_newlines=True)
            if result.returncode > 0:
                status = Status.CRITICAL

            output = result.stdout

            m = re.search(parser_1, output)
            if not m:
                self.logger.warning('Unable to parse output from ping command:\n' + output)
                return Status.UNKNOWN

            self.gauge('ping.sent', {'ping_host': host}).set(float(m.group('sent')))
            self.gauge('ping.received', {'ping_host': host}).set(float(m.group('rcvd')))
            self.gauge('ping.loss_pct', {'ping_host': host}).set(float(m.group('loss')))

            m = re.search(parser_2, output)
            if not m:
                self.logger.warning('Unable to parse output from ping command:\n' + output)
                return Status.UNKNOWN

            self.gauge('ping.min', {'ping_host': host}).set(float(m.group('min')))
            self.gauge('ping.avg', {'ping_host': host}).set(float(m.group('avg')))
            self.gauge('ping.max', {'ping_host': host}).set(float(m.group('max')))

            try:
                std_dev = float(m.group('stddev'))
                self.gauge('ping.std_dev', {'ping_host': host}).set(std_dev)
            except TypeError:
                pass

        return status


if __name__ == '__main__':
    sys.exit(PingPlugin().run())
