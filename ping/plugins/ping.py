from outlyer_agent.collection import Status, Plugin, PluginTarget
import logging
import subprocess
import re
import platform

logger = logging.getLogger(__name__)


class PingPlugin(Plugin):

    def collect(self, target: PluginTarget):

        hosts = target.get('hosts', ['192.168.1.1'])
        count = target.get('count', 3)

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
                logger.warning('Unable to parse output from ping command:\n' + output)
                return Status.UNKNOWN

            target.gauge('sent', {'host': host}).set(float(m.group('sent')))
            target.gauge('received', {'host': host}).set(float(m.group('rcvd')))
            target.gauge('loss_pct', {'host': host, 'uom': '%'}).set(float(m.group('loss')))

            try:
                target.gauge('time', {'host': host, 'uom': 'ms'}).set(float(m.group('time')))
            except TypeError:
                pass

            m = re.search(parser_2, output)
            if not m:
                logger.warning('Unable to parse output from ping command:\n' + output)
                return Status.UNKNOWN

            target.gauge('min', {'host': host, 'uom': 'ms'}).set(float(m.group('min')))
            target.gauge('avg', {'host': host, 'uom': 'ms'}).set(float(m.group('avg')))
            target.gauge('max', {'host': host, 'uom': 'ms'}).set(float(m.group('max')))

            try:
                target.gauge('stddev', {'host': host, 'uom': 'ms'}).set(float(m.group('stddev')))
            except IndexError:
                pass

        return status
