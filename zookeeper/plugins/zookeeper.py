import time
from outlyer_agent.collection import Status, Plugin, PluginTarget
import sys
import socket
import re
import subprocess

class ZookeeperPlugin(Plugin):
    def get_stats(self):
        """ Get ZooKeeper server stats as a map """
        data = self._send_cmd('mntr')
        stuff={}
        decoded_data = data.decode('utf-8')
        for line in decoded_data.split('\n'):
            if len(line) > 1:
                stuff[line.split()[0]] = line.split()[1]
        return stuff
    def _create_socket(self):
        return socket.socket()

    def _send_cmd(self, cmd):
        """ Send a 4letter word command to the server """
        s = self._create_socket()
        s.settimeout(self._timeout)
        s.connect(self._address)
        s.send(str.encode('mntr'))
        data = s.recv(2048)
        s.close()
        return data

    def collect(self, target: PluginTarget) -> Status:
        HOST = target.get('host')
        PORT = target.get('port')
        self.zk_version = target.get('version')
        self._address = (HOST, int(PORT))
        self._timeout = 10
        output = self.get_stats()
        status = Status.OK
        if output['zk_version'] != (self.zk_version + ','):
            status = Status.CRITICAL
        del output['zk_version']
        del output['zk_server_state']
        for key, value in output.items():
            target.gauge(key, {'zookeeper': key}).set(int(value))
        return Status.OK
