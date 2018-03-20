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

        # Make request to NTP Host
        try:
            buf = 1024
            msg = bytes('\x1b' + 47 * '\0', "utf-8")
            time_1970 = 2208988800
            client = socket.socket(AF_INET, SOCK_DGRAM)
            client.sendto(msg, address)
            msg, address = client.recvfrom(buf)
            t = struct.unpack("!12I", msg)[10]
            t -= time_1970
            ntp_clock = datetime.strptime(time.ctime(t).replace("  ", " "), '%a %b %d %H:%M:%S %Y').date()

            time_delta = datetime.now().date() - ntp_clock
            self.gauge('ntp_drift', {"uom": "s"}).set(time_delta.seconds)
            if int(time_delta.seconds) < drift:
                return Status.OK
            else:
                return Status.CRITICAL
        except Exception as e:
            return Status.CRITICAL


if __name__ == '__main__':
    sys.exit(NTPCheckPlugin().run())