#!/usr/bin/env python

import subprocess
import sys
import re

from outlyer_plugin import Plugin, Status

"""
Monitors Microsoft IIS Web Server. Will automatically get metrics for every site on your server
unless you override the 'sites' variable with semi-colon (;) seperated list of site names.
"""


class IISPlugin(Plugin):

    def collect(self, _):
        listsites = []
        sites = self.get_sites()
        if not sites:
            return Status.UNKNOWN

        for site in sites:
            counters = []
            counters.append(f"\Web Service({site})\Service Uptime")

            # Network
            counters.append(f"\Web Service({site})\Bytes Sent/sec")
            counters.append(f"\Web Service({site})\Bytes Received/sec")
            counters.append(f"\Web Service({site})\Bytes Total/sec")
            counters.append(f"\Web Service({site})\Current Connections")
            counters.append(f"\Web Service({site})\Files Sent/sec")
            counters.append(f"\Web Service({site})\Files Received/sec")
            counters.append(f"\Web Service({site})\Total Connection Attempts (all instances)")
            counters.append(f"\Web Service({site})\Maximum Connections")

            # HTTP Methods
            counters.append(f"\Web Service({site})\Get Requests/sec")
            counters.append(f"\Web Service({site})\Post Requests/sec")
            counters.append(f"\Web Service({site})\Head Requests/sec")
            counters.append(f"\Web Service({site})\Put Requests/sec")
            counters.append(f"\Web Service({site})\Delete Requests/sec")
            counters.append(f"\Web Service({site})\Options Requests/sec")
            counters.append(f"\Web Service({site})\Trace Requests/sec")

            # Errors
            counters.append(f"\Web Service({site})\\Not Found Errors/sec")
            counters.append(f"\Web Service({site})\Locked Errors/sec")

            # Users
            counters.append(f"\Web Service({site})\Current Anonymous Users")
            counters.append(f"\Web Service({site})\Current NonAnonymous Users")

            # Requests
            counters.append(f"\Web Service({site})\CGI Requests/sec")
            counters.append(f"\Web Service({site})\ISAPI Extension Requests/sec")

            listsites += (counters)

        try:
            command = [r'c:\windows\system32\typeperf.exe', '-sc', '1']
            output = subprocess.check_output(command + listsites)

        except:
            return Status.UNKNOWN

        i = 1
        for listsite in listsites:
            metric = listsite.lower()
            siteval = re.search(r'\((.*?)\)', metric).group(1)
            metric = re.sub(r'\([^)]*\)', '', metric)
            metric = re.sub('[^0-9a-zA-Z]+', '_', metric)
            metric = re.sub('web_service_', 'iis.', metric)
            value = output.decode('utf-8').splitlines()[2].split(',')[i].replace('"', '').strip()
            self.gauge(metric, {'site': siteval}).set(float(value))
            i += 1
        return Status.OK

    def get_sites(self):
        """
        Allows user to set list of sites as variable, i.e. 'Default Web Site;Test Site'
        If variable not provided then it will use the appcmd program to list all the
        sites on the server automatically
        """

        if self.get('sites', None):
            return self.get('sites', '').split(';')
        else:
            # Authomatically get sites with appcmd
            try:
                appcmd = [r'c:\windows\system32\inetsrv\appcmd.exe', 'list', 'sites', '/text:name']
                appoutput = subprocess.check_output(appcmd)
                sites = appoutput.decode('utf-8').rstrip().split('\r\n')
                # add total for the server too
                sites.append('_Total')
                return sites
            except:
                return None


if __name__ == '__main__':
    # To run the collection
    sys.exit(IISPlugin().run())
