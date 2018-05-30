#!/usr/bin/env python3

from outlyer_plugin import Status, Plugin
import sys
import socket


GAUGE_METRICS = [
    'zk_avg_latency',
    'zk_max_latency',
    'zk_min_latency',
    'zk_num_alive_connections',
    'zk_outstanding_requests',
    'zk_znode_count',
    'zk_watch_count',
    'zk_ephemerals_count',
    'zk_approximate_data_size',
    'zk_open_file_descriptor_count',
    'zk_max_file_descriptor_count',
    'zk_followers',
    'zk_synced_followers',
    'zk_pending_syncs',
]

COUNTER_METRICS = [
    'zk_packets_received',
    'zk_packets_sent',
]


class ZookeeperPlugin(Plugin):
    def get_stats(self):
        """ Get ZooKeeper server stats as a map """
        data = self._send_cmd('mntr')
        result={}
        decoded_data = data.decode('utf-8')
        for line in decoded_data.split('\n'):
            if len(line) > 1:
                result[line.split()[0]] = line.split()[1]
        return result

    def _create_socket(self):
        return socket.socket()

    def _send_cmd(self, cmd):
        """ Send a 4letter word command to the server """
        s = self._create_socket()
        s.settimeout(self._timeout)
        s.connect(self._address)
        s.send(str.encode(cmd))
        data = s.recv(2048)
        s.close()
        return data

    def collect(self, _) -> Status:
        HOST = self.get('host', 'localhost')
        PORT = self.get('port', 2181)
        self._address = (HOST, int(PORT))
        self._timeout = 10
        # Test the server is running in a non-error state
        if self._send_cmd('ruok').decode("utf-8") == 'imok':
            status = Status.OK
        else:
            status = Status.CRITICAL
        output = self.get_stats()
        del output['zk_version']
        del output['zk_server_state']
        for key, value in output.items():
            if key in COUNTER_METRICS:
                self.counter(key, {'zookeeper': key}).set(int(value))
            elif key in GAUGE_METRICS:
                self.gauge(key, {'zookeeper': key}).set(int(value))
        return status


if __name__ == '__main__':
    # To run the collection
    sys.exit(ZookeeperPlugin().run())
