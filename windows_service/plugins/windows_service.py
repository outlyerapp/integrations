#!/usr/bin/env python3

import os; os.chdir('c:\\outlyer\\embedded\\bin')
import psutil
import sys
from outlyer_plugin import Plugin, Status



SERV_STATE = {
    'running': Status.OK,
    'stopped': Status.CRITICAL,
    'start pending': Status.WARNING,
    'stop pending': Status.WARNING,
    'continue pending': Status.WARNING,
    'pause pending': Status.WARNING,
    'paused': Status.WARNING,
    'unknown': Status.UNKNOWN
}


class WinServPlugin(Plugin):

    def collect(self, _) -> Status:
    
        win_serv = self.get('win_serv', '')
        service = self.getService(win_serv)
        serv_status = service['status']
        status = self.getStatus(serv_status)
        #print(win_serv)
        #print(serv_status)
        #print (status)
        return status

    def getService(self, name):
        win_serv = self.get('win_serv', '')
        service = None
        try:
            service = psutil.win_service_get(name)
            service = service.as_dict()
        except Exception as ex:
            print (str(ex))
            return Status.CRITICAL
        return service

    def getStatus(self, val):

        value = None
        for key in SERV_STATE:
            if key in val:
                value = SERV_STATE[key]
                #self.counter('win_service').set(int(2))
                break
        return value
        
if __name__ == '__main__':
    sys.exit(WinServPlugin().run())
