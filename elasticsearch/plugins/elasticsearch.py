#!/usr/bin/env python3

import sys
import requests
import jmespath

from outlyer_plugin import Plugin, Status


CLUSTER_HEALTH_METRICS = {
    'active_shards': ('elasticsearch_cluster_number_of_shards', 'gauge'),
    'active_primary_shards': ('elasticsearch_cluster_active_primary_shards', 'gauge'),
    'relocating_shards': ('elasticsearch_cluster_relocating_shards', 'gauge'),
    'initializing_shards': ('elasticsearch_cluster_initializing_shards', 'gauge'),
    'unassigned_shards': ('elasticsearch_cluster_unassigned_shards', 'gauge'),
    'delayed_unassigned_shards': ('elasticsearch_cluster_delayed_unassigned_shards', 'gauge'),
    'number_of_pending_tasks': ('elasticsearch_cluster_number_of_pending_tasks', 'gauge'),
}

CLUSTER_STATS_METRICS = {
    'indices.count': ('elasticsearch_cluster_number_of_indices', 'gauge'),
    'indices.docs.count': ('elasticsearch_cluster_number_of_docs', 'gauge'),
    '_nodes.total': ('elasticsearch_cluster_number_of_nodes', 'gauge'),
    '_nodes.failed': ('elasticsearch_cluster_number_of_failed_nodes', 'gauge'),
    'nodes.count.data': ('elasticsearch_cluster_number_of_data_nodes', 'gauge'),
    'nodes.count.coordinating_only': ('elasticsearch_cluster_number_of_coordinating_only_nodes', 'gauge'),
    'nodes.count.master': ('elasticsearch_cluster_number_of_master_elegible_nodes', 'gauge'),
    'nodes.count.ingest': ('elasticsearch_cluster_number_of_ingest_nodes', 'gauge'),
}

NODE_STATS_METRICS = {
    'process.open_file_descriptors': ('elasticsearch_node_process_open_file_descriptors', 'gauge'),
    'process.max_file_descriptors': ('elasticsearch_node_process_max_file_descriptors', 'gauge'),
    'jvm.mem.heap_used_in_bytes': ('elasticsearch_node_jvm_mem_heap_used_in_bytes', 'gauge'),
    'jvm.mem.heap_committed_in_bytes': ('elasticsearch_node_jvm_mem_heap_committed_in_bytes', 'gauge'),
    'jvm.mem.non_heap_used_in_bytes': ('elasticsearch_node_jvm_mem_non_heap_used_in_bytes', 'gauge'),
    'jvm.mem.non_heap_committed_in_bytes': ('elasticsearch_node_jvm_mem_non_heap_committed_in_bytes', 'gauge'),
    'jvm.mem.pools.young.used_in_bytes': ('elasticsearch_node_jvm_mem_pools_young_used_in_bytes', 'gauge'),
    'jvm.mem.pools.young.max_in_bytes': ('elasticsearch_node_jvm_mem_pools_young_max_in_bytes', 'gauge'),
    'jvm.mem.pools.old.used_in_bytes': ('elasticsearch_node_jvm_mem_pools_old_used_in_bytes', 'gauge'),
    'jvm.mem.pools.old.max_in_bytes': ('elasticsearch_node_jvm_mem_pools_old_max_in_bytes', 'gauge'),
    'jvm.gc.collectors.young.collection_count': ('elasticsearch_node_jvm_gc_collectors_young_collection_count', 'gauge'),
    'jvm.gc.collectors.young.collection_time_in_millis': ('elasticsearch_node_jvm_gc_collectors_young_collection_time_in_millis', 'gauge'),
    'jvm.gc.collectors.old.collection_count': ('elasticsearch_node_jvm_gc_collectors_old_collection_count', 'gauge'),
    'jvm.gc.collectors.old.collection_time_in_millis': ('elasticsearch_node_jvm_gc_collectors_old_collection_time_in_millis', 'gauge'),
    'indices.search.query_total': ('elasticsearch_node_indices_search_query_total', 'gauge'),
    'indices.search.query_time_in_millis': ('elasticsearch_node_indices_search_query_time_in_millis', 'counter'),
    'indices.search.query_current': ('elasticsearch_node_indices_search_query_current', 'gauge'),
    'indices.search.fetch_time_in_millis': ('elasticsearch_node_indices_search_fetch_time_in_millis', 'counter'),
    'indices.search.fetch_current': ('elasticsearch_node_indices_search_fetch_current', 'gauge'),
    'indices.indexing.index_total': ('elasticsearch_node_indices_indexing_index_total', 'gauge'),
    'indices.indexing.index_time_in_millis': ('elasticsearch_node_indices_indexing_index_time_in_millis', 'counter'),
    'indices.indexing.index_failed': ('elasticsearch_node_indices_indexing_index_failed', 'gauge'),
    'indices.refresh.total_time_in_millis': ('elasticsearch_node_indices_refresh_total_time_in_millis', 'gauge'),
    'indices.flush.total_time_in_millis': ('elasticsearch_node_indices_flush_total_time_in_millis', 'gauge'),
}


class ElasticsearchPlugin(Plugin):

  def collect(self, _): 
    try:
      self._config = self.get_config()

      # Get metrics from ES Cluster Health API
      cluster_health_response = self._get_data(self._config.get('cluster_health_api'))

      labels = {'cluster_name': cluster_health_response.get('cluster_name')}
      calc_status = lambda v: {"red": 2, "yellow": 1, "green": 0}.get(v, -1)
      cluster_status = calc_status(cluster_health_response.get('status'))
      self.gauge('elasticsearch_cluster_status', labels).set(cluster_status)
      self._collect_gauge_or_counter(CLUSTER_HEALTH_METRICS, labels, cluster_health_response)
      
      # Get metrics from ES Cluster Stats API
      cluster_stats_response = self._get_data(self._config.get('cluster_stats_api'))
      self._collect_gauge_or_counter_jmespath(CLUSTER_STATS_METRICS, labels, cluster_stats_response)

      # Get metrics from ES Node Stats API
      node_stats_response = self._get_data(self._config.get('node_stats_api'))
      node_stats = next(iter(node_stats_response.get('nodes').values()))
      self._collect_gauge_or_counter_jmespath(NODE_STATS_METRICS, labels, node_stats)

      if cluster_status == 0:
        return Status.OK
      elif cluster_status == 1:
        return Status.WARNING
      else:
        return Status.CRITICAL
    except Exception as ex:
      self.logger.error('Error collecting Elasticsearch metrics: %s', str(ex))
      return Status.CRITICAL

  def get_config(self):
    protocol = self.get('protocol', 'http')
    host = self.get('ip', 'localhost')
    port = self.get('port', 9200)
    username = self.get('username', None)
    password = self.get('password', None)
    client_cert_file = self.get('client_cert_file', None)
    private_key_file = self.get('private_key_file', None)
    ca_bundle_file = self.get('ca_bundle_file', None)
    cluster_health_api = "%s://%s:%s/_cluster/health?pretty" % (protocol, host, port)
    cluster_stats_api = "%s://%s:%s/_cluster/stats?pretty" % (protocol, host, port)
    node_stats_api = "%s://%s:%s/_nodes/_local/stats?pretty" % (protocol, host, port)

    if username and password:
        auth = (username, password)
    else:
        auth = None

    if client_cert_file and private_key_file:
        cert = (client_cert_file, private_key_file)
    elif client_cert_file:
        cert = client_cert_file
    else:
        cert = None

    return {
      'headers': {},
      'timeout': 20,
      'auth': auth,
      'cert': cert,
      'verify': ca_bundle_file,
      'cluster_health_api': cluster_health_api,
      'cluster_stats_api': cluster_stats_api,
      'node_stats_api': node_stats_api,
    }

  def _get_data(self, url):
    res = requests.get(
      url,
      timeout=self._config.get('timeout'),
      headers=self._config.get('headers'),
      auth=self._config.get('auth'),
      verify=self._config.get('verify'),
      cert=self._config.get('cert')
    )
    res.raise_for_status()
    return res.json()

  def _collect_gauge_or_counter(self, metrics, labels, datasource):
    for key, value in datasource.items():
      if key in metrics:
        if metrics[key][1] == 'gauge':
          self.gauge(metrics[key][0], labels).set(value)
        else:
          self.counter(metrics[key][0], labels).set(value)

  def _collect_gauge_or_counter_jmespath(self, metrics, labels, datasource):
    for key, value in metrics.items():
      value = jmespath.search(key, datasource)
      if value:
        if metrics[key][1] == 'gauge':
          self.gauge(metrics[key][0], labels).set(value)
        else:
          self.counter(metrics[key][0], labels).set(value)


if __name__ == '__main__':
    sys.exit(ElasticsearchPlugin().run())

