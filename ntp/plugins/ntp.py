#!/usr/bin/env python3

from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct
import time
from datetime import datetime

from outlyer_plugin import Plugin, Status


class NTPCheckPlugin(Plugin):

    def collect(self, _):

        # Set how much drift is acceptable before failing, by default 5 mins (300 secs)
        drift = int(self.get("drift", "300"))
        # NTP Host to check time against
        host = self.get("ntp-host", "pool.ntp.org")
        port = int(self.get("port", "123"))
        address = (host, port)
        timeout = int(self.get("timeout", "20"))

        # Make request to NTP Host
        try:
            buf = 1024
            msg = bytes('\x1b' + 47 * '\0', "utf-8")
            time_1970 = 2208988800
            client = socket.socket(AF_INET, SOCK_DGRAM)
            client.settimeout(timeout)
            client.sendto(msg, address)
            msg, address = client.recvfrom(buf)
            t = struct.unpack("!12I", msg)[10]
            t -= time_1970
            ntp_dt = datetime.strptime(time.ctime(t).replace("  ", " "), '%a %b %d %H:%M:%S %Y')
            delta_seconds = int((datetime.now() - ntp_dt).total_seconds())
            self.gauge('ntp_drift', {}).set(delta_seconds)
            if abs(delta_seconds) < drift:
                return Status.OK
            else:
                return Status.CRITICAL
        except Exception as e:
            raise e
            return Status.CRITICAL


if __name__ == '__main__':
    sys.exit(NTPCheckPlugin().run())
