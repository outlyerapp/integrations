import platform
import re
import subprocess

from outlyer_agent.collection import Status, Plugin, PluginTarget


class PingPlugin(Plugin):

    def collect(self, target: PluginTarget):

        count = target.get('count', 3)
        hosts = target.get('hosts', '192.168.1.1')
        if isinstance(hosts, str):
            hosts = [x.strip() for x in hosts.split(',')]

        command = 'ping -c {count} {host}'
        parser_1 = r'(?P<sent>\d+) packets transmitted, (?P<rcvd>\d+) (?:packets )?received, ' + \
                   '(?P<loss>[\d.]+)% packet loss(?:, time (?P<time>\d+)\s*ms)?'
        parser_2 = r'(?P<min>[\d.]+)/(?P<avg>[\d.]+)/(?P<max>[\d.]+)/(?P<stddev>[\d.]+) ms'
        if platform.system() == "Windows":
            # if True:
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

            target.gauge('ping.sent', {'host': host}).set(float(m.group('sent')))
            target.gauge('ping.received', {'host': host}).set(float(m.group('rcvd')))
            target.gauge('ping.loss_pct', {'host': host, 'uom': '%'}).set(float(m.group('loss')))

            try:
                time = float(m.group('time'))
                target.gauge('ping_time', {'host': host, 'uom': 'ms'}).set(time)
            except TypeError:
                pass

            m = re.search(parser_2, output)
            if not m:
                self.logger.warning('Unable to parse output from ping command:\n' + output)
                return Status.UNKNOWN

            target.gauge('ping.min', {'host': host, 'uom': 'ms'}).set(float(m.group('min')))
            target.gauge('ping.avg', {'host': host, 'uom': 'ms'}).set(float(m.group('avg')))
            target.gauge('ping.max', {'host': host, 'uom': 'ms'}).set(float(m.group('max')))

            try:
                std_dev = float(m.group('stddev'))
                target.gauge('ping.std_dev', {'host': host, 'uom': 'ms'}).set(std_dev)
            except TypeError:
                pass

        return status
