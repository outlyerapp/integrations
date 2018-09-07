#!/usr/bin/env python3

import sys
from outlyer_plugin import Plugin, Status
import re
import glob
import os
from datetime import datetime


class LogrotatePlugin(Plugin):

    def collect(self, _):
        logrotate_state = self.get('logrotate_state', '/var/lib/logrotate/status')

        try:
            logs_info = []
            with open(logrotate_state) as file:
                for line in file.readlines()[1:]:
                    m = re.search(r'"(.+?)" (.*)', line)
                    log_file = m.group(1)
                    last_rotation_str = m.group(2)
                    last_rotation_datetime = datetime.strptime(last_rotation_str, '%Y-%m-%d-%H:%M:%S')
                    delta_seconds = int((datetime.now() - last_rotation_datetime).total_seconds())
                    if '*' in log_file:
                        listing = glob.glob(log_file)
                        for file in listing:
                            if os.path.isfile(file):
                                logs_info.append((file, delta_seconds, os.path.getsize(file)))
                    else:
                        if os.path.isfile(log_file):
                            logs_info.append((log_file, delta_seconds, os.path.getsize(log_file)))

            for log_info in logs_info:
                self.gauge('logrotate.last_rotation', {"log_file":log_info[0]}).set(log_info[1])
                self.gauge('logrotate.size_bytes', {"log_file":log_info[0]}).set(log_info[2])

            return Status.OK

        except Exception as ex:
            self.logger.error('Error collecting logrotate metrics: %s', str(ex))
            return Status.CRITICAL


if __name__ == '__main__':
    sys.exit(LogrotatePlugin().run())
