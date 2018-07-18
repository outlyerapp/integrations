#!/usr/bin/env python3

import time
import os
import sys
import dns.resolver

from outlyer_plugin import Plugin, Status

# These imports are necessary because otherwise dynamic type
# resolution will fail on windows without it.
# See more here: https://github.com/rthalley/dnspython/issues/39.
if os.name == 'nt':
    from dns.rdtypes.ANY import *  # noqa
    from dns.rdtypes.IN import *  # noqa
    # for tiny time deltas, time.time on Windows reports the same value
    # of the clock more than once, causing the computation of response_time
    # to be often 0; let's use time.clock that is more precise.
    time_func = time.clock
else:
    time_func = time.time

class DNSCheck(Plugin):

  DEFAULT_TIMEOUT = 5

  def collect(self, _):

      hostname = self.get('hostname')
      record_type = self.get('record_type', 'A')
      resolver = dns.resolver.Resolver()

      # If set, will use specified nameserver instead of nameserver
      # configured in local network settings
      nameserver = self.get('nameserver')
      nameserver_port = self.get('nameserver_port')
      if nameserver is not None:
          resolver.nameservers = [nameserver]
      if nameserver_port is not None:
          resolver.port = nameserver_port

      # Set resolver timeout
      resolver.lifetime = float(self.get('timeout', self.DEFAULT_TIMEOUT))

      # Perform the DNS query, and report its duration as a gauge
      start_time = time.time()
      try:
          self.logger.debug(f"Querying '{record_type}' record for hostname '{hostname}'")
          if record_type == "NXDOMAIN":
              try:
                  resolver.query(hostname)
              except dns.resolver.NXDOMAIN:
                  pass
              else:
                  raise AssertionError("Expected an NXDOMAIN, got a result.")
          else:
              answer = resolver.query(hostname, rdtype=record_type)
              assert (answer.rrset.items[0].to_text())

          response_time = time.time() - start_time

          # Create metric labels
          labels = {
              "hostname": hostname,
              "record_type": record_type
          }
          try:
              nameserver = nameserver or dns.resolver.Resolver().nameservers[0]
              labels["nameserver"] = nameserver
          except IndexError:
              self.logger.error('No DNS server was found on this host.')

          self.gauge('dns.response_time', labels).set(response_time)
          self.logger.debug(f"Resolved hostname: {hostname}")

      except dns.exception.Timeout:
          self.logger.error(f"DNS resolution of {hostname} timed out")
          return Status.CRITICAL

      except Exception:
          self.logger.exception(f"DNS resolution of {hostname} has failed.")
          return Status.CRITICAL

if __name__ == '__main__':
    sys.exit(DNSCheck().run())
