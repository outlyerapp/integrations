#!/usr/bin/env python3

import sys
import requests
import requests.exceptions
import urllib3
import operator

from functools import reduce

from outlyer_plugin import Plugin, Status

OVERVIEW_METRICS = [
    # Path, metric name, metric type
    ('message_stats/confirm', 'rabbitmq.cluster_confirm_count', 'counter'),
    ('message_stats/disk_reads', 'rabbitmq.cluster_disk_read_count', 'counter'),
    ('message_stats/disk_writes', 'rabbitmq.cluster_disk_write_count', 'counter'),
    ('message_stats/publish', 'rabbitmq.cluster_publish_count', 'counter'),
    ('message_stats/return_unroutable', 'rabbitmq.cluster_return_unroutable_count', 'counter'),
    ('object_totals/channels', 'rabbitmq.cluster_channels', 'gauge'),
    ('object_totals/connections', 'rabbitmq.cluster_connections', 'gauge'),
    ('object_totals/consumers', 'rabbitmq.cluster_consumers', 'gauge'),
    ('object_totals/exchanges', 'rabbitmq.cluster_exchanges', 'gauge'),
    ('object_totals/queues', 'rabbitmq.cluster_queues', 'gauge'),
    ('queue_totals/messages_ready', 'rabbitmq.cluster_messages_queued', 'gauge'),
]

NODE_METRICS = [
    # Path, metric name, metric type
    ('context_switches', 'rabbitmq.node_context_switches_count', 'counter'),
    ('paritions', 'rabbitmq.node_partitions', 'gauge'),
    ('disk_free', 'rabbitmq.node_disk_free', 'gauge'),
    ('fd_used', 'rabbitmq.node_fd_used', 'gauge'),
    ('mem_used', 'rabbitmq.node_mem_used', 'gauge'),
    ('run_queue', 'rabbitmq.node_run_queue', 'gauge'),
    ('sockets_used', 'rabbitmq.node_sockets_used', 'gauge'),
    ('running', 'rabbitmq.node_running', 'gauge'),
    ('mem_alarm', 'rabbitmq.node_mem_alarm', 'gauage'),
    ('disk_free_alarm', 'rabbitmq.node_disk_free_alarm', 'gauage'),
]

EXCHANGE_METRICS = [
    # Path, metric name, metric type
    ('message_stats/ack', 'rabbitmq.exchange_messages_ack_count', 'counter'),
    ('message_stats/confirm', 'rabbitmq.exchange_messages_confirm_count', 'counter'),
    ('message_stats/deliver_get', 'rabbitmq.exchange_messages_deliver_get.count', 'counter'),
    ('message_stats/publish', 'rabbitmq.exchange_messages_publish_count', 'counter'),
    ('message_stats/publish_in', 'rabbitmq.exchange_publish_in_count', 'counter'),
    ('message_stats/publish_out', 'rabbitmq.exchange_publish_out_count', 'counter'),
    ('message_stats/return_unroutable', 'rabbitmq.exchange_messages_return_unroutable_count', 'counter'),
    ('message_stats/redeliver', 'rabbitmq.exchange_messages_redeliver_count', float),
]

QUEUE_METRICS = [
    # Path, metric name, metric type
    ('active_consumers', 'rabbitmq.queue_active_consumers', 'gauge'),
    ('consumers', 'rabbitmq.queue_consumers', 'gaugue'),
    ('consumer_utilisation', 'rabbitmq.queue_consumer_utilisation', 'gauge'),
    ('memory', 'rabbitmq.queue_memory', 'gauge'),
    ('messages', 'rabbitmq.queue_messages_count', 'counter'),
    ('messages_ready', 'rabbitmq.queue_messages_ready_count', 'counter'),
    ('messages_unacknowledged', 'rabbitmq.queue_messages_unacknowledged_count', 'counter'),
    ('message_stats/ack', 'rabbitmq.queue_messages_ack_count', 'counter'),
    ('message_stats/deliver', 'rabbitmq.queue_messages_deliver_count', 'counter'),
    ('message_stats/deliver_get', 'rabbitmq.queue_messages_deliver_get_count', 'counter'),
    ('message_stats/publish', 'rabbitmq.queue_messages_publish_count', 'counter'),
    ('message_stats/redeliver', 'rabbitmq.queue_messages_redeliver_count', 'counter'),
]


class RabbitMQ(Plugin):

    def __init__(self):
        super().__init__()
        self.host = self.get('ip', '127.0.0.1')
        self.port = self.get('port', '15672')
        self.protocol = self.get('protocol', 'http')
        self.verify_ssl = False
        if self.get('verify_ssl', None):
            self.verify_ssl = True
        self.username = self.get('username', 'guest')
        self.password = self.get('password', 'guest')

        self.url = f'{self.protocol}://{self.host}:{self.port}'

        # For performance reasons we limit number of items we query
        self.max_exchanges = self.get('max_exchanges', '50')

        # suppress requests/urllib3 ssl warnings when ignoring
        if not self.verify_ssl:
            urllib3.disable_warnings()

    def collect(self, _) -> Status:

        try:

            # Overview Stats
            overview = self.get_data('/api/overview')
            # Current node being queried - all metrics should be filtered to this node
            node_name = overview['node']
            # Current cluster being queried
            cluster_name = overview['cluster_name']
            self.get_metrics(OVERVIEW_METRICS, overview, {'cluster': cluster_name})

            # Node Stats for current node only
            node = self.get_data(f"/api/nodes/{node_name}")
            node_labels = {
                'node': node_name,
                'cluster': cluster_name
            }
            self.get_metrics(NODE_METRICS, node, node_labels)
            # Get parition length seperately as its an array
            self.gauge('rabbitmq.node_partitions', node_labels).set(len(node['partitions']))

            # Connection Stats
            connections = self.get_data(f"/api/connections")
            vhost_connections = {}
            connection_states = {}
            for conn in connections:
                if (conn['node'] == node_name):
                    if conn.get('state', 'direct') in connection_states:
                        # 'state' does not exist for direct type connections.
                        connection_states[conn.get('state', 'direct')] += 1
                    else:
                        connection_states[conn.get('state', 'direct')] = 1
                    if conn['vhost'] in vhost_connections:
                        vhost_connections[conn['vhost']] += 1
                    else:
                        vhost_connections[conn['vhost']] = 1

            for key, value in vhost_connections.items():
                label = 'root' if key == '/' else key
                self.gauge("rabbitmq.connections", {'vhost': label, 'cluster': cluster_name}).set(value)
            for key, value in connection_states.items():
                self.gauge("rabbitmq.connection_states", {'state': key, 'cluster': cluster_name}).set(value)

            # Exchange Stats for all nodes in cluster
            exchanges = self.get_data("/api/exchanges?page=1&page_size=" + self.max_exchanges)
            for exchange in exchanges['items']:
                exchange_labels = {
                    'exchange': 'amqp_default' if exchange['name'] == '' else exchange['name'],
                    'exchange_type': exchange['type'],
                    'cluster': cluster_name,
                    'vhost': 'root' if exchange['vhost'] == '/' else exchange['vhost']
                }
                self.get_metrics(EXCHANGE_METRICS, exchange, exchange_labels)

            # Queue Stats - only for queues on the node being currently queried
            queues = self.get_data("/api/queues")
            for queue in queues:
                if queue['node'] == node_name:
                    queue_labels = {
                        'queue': queue['name'],
                        'node': queue['node'],
                        'cluster': cluster_name,
                        'vhost': 'root' if queue['vhost'] == '/' else queue['vhost']
                    }
                    self.get_metrics(QUEUE_METRICS, queue, queue_labels)

            return Status.OK

        except requests.exceptions.HTTPError as ex:
            raise ex
            return Status.CRITICAL

    def get_data(self, url: str) -> any:
        r = requests.get(self.url + url, auth=(self.username, self.password),
                         timeout=10, verify=self.verify_ssl)
        r.raise_for_status()
        return r.json()

    def get_value(self, path, values):
        """
        Get the value from a nested dictionary using a path, i.e. 'key1/key2/key3'

        :param path:        The path to the value using forward slash, i.e. 'key1/key2/key3'
        :param values:      The dictionary to search
        :return:            Value if path found, None if not
        """
        try:
            return reduce(operator.getitem, path.split('/'), values)
        except KeyError:
            return None

    def get_metrics(self, metrics, values: dict, labels: dict = {}):
        """
        Takes an array of metrics in the format below and adds metrics
        to the plugin registry if it finds them in the values dictionary:

            [
                ('metric/path', 'metric_name', 'counter'),
                ('metric/path', 'metric_name', 'gauge'),
            ]

        :param metrics:     Array of metrics in format above
        :param values:      Nested Dictionary of values from a JSON response
        :param labels:      (Optional) Labels to be applied to all the metrics
        """
        for metric in metrics:
            value = self.get_value(metric[0], values)
            if isinstance(value, bool):
                value = 1 if value else 0
            if value is not None:
                if metric[2] == 'counter':
                    self.counter(metric[1], labels).set(value)
                else:
                    self.gauge(metric[1], labels).set(value)


if __name__ == '__main__':
    sys.exit(RabbitMQ().run())