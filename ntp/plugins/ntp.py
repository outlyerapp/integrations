#!/usr/bin/env python3

import random
import sys
from datetime import datetime
from outlyer_agent import __version__ as agent_version
from outlyer_plugin import Plugin, Status
from distutils.version import StrictVersion


class NTPCheckPlugin(Plugin):

    def collect(self, _):

        if StrictVersion(agent_version) >= StrictVersion("1.4.6"):
            from ntplib import NTPClient
        else:
            self.logger.warning("This plugin requires agent version 1.4.6 or newer")
            return Status.CRITICAL

        # Set how much drift is acceptable before failing, by default 5 mins (300 secs)
        drift = int(self.get("drift", "300"))
        hosts = self.get("ntp-hosts", "0.pool.ntp.org,1.pool.ntp.org,2.pool.ntp.org").split(",")
        random.shuffle(hosts)

        for h in hosts:
            try:
                ntp_ts = NTPClient().request(h).orig_time
                if ntp_ts:
                    break
            except Exception as e:
                self.logger.warning(f"NTP host request '{h}' failed")
                ntp_ts = None
                continue

        if not ntp_ts:
            return Status.CRITICAL
        delta_seconds = int(datetime.now().timestamp() - ntp_ts)
        self.gauge('ntp_drift', {}).set(delta_seconds)
        if abs(delta_seconds) < drift:
            return Status.OK
        else:
            return Status.CRITICAL


if __name__ == '__main__':
    sys.exit(NTPCheckPlugin().run())
