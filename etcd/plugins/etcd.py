#!/usr/bin/env python3

import sys
import requests
import os

from outlyer_plugin import Plugin, Status
from prometheus_client.parser import text_string_to_metric_families


GAUGE_METRICS = [
    'etcd_server_has_leader',
    'etcd_server_proposals_pending',
    'etcd_server_proposals_committed_total',
    'etcd_server_proposals_applied_total',
    'etcd_debugging_mvcc_watcher_total',
    'etcd_debugging_mvcc_slow_watcher_total',
    'etcd_debugging_mvcc_keys_total',
    'process_resident_memory_bytes',
    'etcd_debugging_mvcc_db_total_size_in_bytes',
    'process_open_fds',
    'process_max_fds',
    ''
]

COUNTER_METRICS = [
    'etcd_server_leader_changes_seen_total',
    'etcd_server_proposals_failed_total',
    'etcd_debugging_mvcc_put_total',
    'etcd_debugging_mvcc_delete_total',
    'etcd_debugging_mvcc_txn_total',
    'etcd_debugging_mvcc_range_total',
    'etcd_network_client_grpc_received_bytes_total',
    'etcd_network_client_grpc_sent_bytes_total',
    'etcd_network_peer_received_bytes_total',
    'etcd_network_peer_sent_bytes_total',
]


class EtcdMetricsPlugin(Plugin):
  
  def collect(self, _):
    HOST = os.environ['ip'] if 'ip' in os.environ else 'localhost'
    if 'ETCD_HOST' in os.environ:
      HOST = os.environ['ETCD_HOST']
    PORT = os.environ['ETCD_CLIENT_PORT'] if 'ETCD_CLIENT_PORT' in os.environ else '2379'
    PATH = 'metrics'
    
    try:
      res = requests.get(f'http://{HOST}:{PORT}/{PATH}', timeout=20).text
      labels = {}
      for family in text_string_to_metric_families(res):
        for sample in family.samples:
          if sample[0] in COUNTER_METRICS:
            self.counter(sample[0], sample[1]).set(sample[2])
          elif sample[0] in GAUGE_METRICS:
            self.gauge(sample[0], sample[1]).set(sample[2])
      
      return Status.OK
    except Exception as ex:
      self.logger.error('Unable to scrape metrics from etcd: %s', str(ex))
      return Status.CRITICAL


if __name__ == '__main__':
    sys.exit(EtcdMetricsPlugin().run())
