#!/usr/bin/env python3

import sys
import requests
import requests.exceptions
import urllib.parse
import urllib3

from typing import Iterable

from outlyer_plugin import Plugin, Status

NODE_COUNTERS = ['context_switches']

NODE_GAUGES = ['disk_free', 'fd_used', 'mem_used', 'run_queue', 'sockets_used', 'running', 'mem_alarm',
               'disk_free_alarm']

QUEUE_GAUGES = ['active_consumers', 'bindings_count', 'consumers', 'consumer_utilisation', 'memory', 'messages',
                'messages_details/rate',
                'messages_ready', 'messages_ready_details/rate', 'messages_unacknowledged',
                'messages_unacknowledged_details/rate',
                'message_stats/ack', 'message_stats/ack_details/rate', 'message_stats/deliver',
                'message_stats/deliver_details/rate',
                'message_stats/deliver_get', 'message_stats/deliver_get_details/rate', 'message_stats/publish',
                'message_stats/publish_details/rate',
                'message_stats/redeliver', 'message_stats/redeliver_details/rate']

EXCHANGE_GAUGES = ['ack', 'ack_details/rate', 'confirm', 'confirm_details/rate', 'deliver_get',
                   'deliver_get_details/rate', 'publish', 'publish_details/rate', 'publish_in',
                   'publish_in_details/rate', 'publish_out', 'publish_out_details/rate', 'return_unroutable',
                   'return_unroutable_details/rate', 'redeliver', 'redeliver_details/rate']


class RabbitMQ(Plugin):

    def collect(self, _) -> Status:

        try:
            self.host = self.get('ip', '127.0.0.1')
            self.port = self.get('port', '15672')
            self.protocol = self.get('protocol', 'http')
            self.verify_ssl = False
            if self.get('verify_ssl', None):
                self.verify_ssl = True
            self.username = self.get('username', 'guest')
            self.password = self.get('password', 'guest')

            self.url = f'{self.protocol}://{self.host}:{self.port}'

            # suppress requests/urllib3 ssl warnings when ignoring
            if not self.verify_ssl:
                urllib3.disable_warnings()

            # Overview stats

            overview = self.get_data('/api/overview')
            node_name = overview['node']

            self.overview_stats(overview)
            self.node_stats(node_name)

            vhost_names = []
            for vhost in self.get_data('/api/vhosts'):
                vhost_name = vhost['name']
                vhost_names.append(vhost_name)
                self.vhost_stats(vhost)

            self.queue_stats(vhost_names)
            self.exchange_stats(vhost_names)

            return Status.OK

        except requests.exceptions.HTTPError as ex:
            raise ex
            return Status.CRITICAL

    def get_data(self, url: str) -> any:
        r = requests.get(self.url + url, auth=(self.username, self.password),
                         timeout=10, verify=self.verify_ssl)
        r.raise_for_status()
        return r.json()

    def queue_stats(self, vhost_names: Iterable[str]) -> None:
        for vhost_name in vhost_names:
            n = urllib.parse.quote(vhost_name, safe='')
            for queue in self.get_data(f'/api/queues/{n}'):
                queue_name = queue['name']
                labels = {'queue_name': queue_name,
                          'vhost_name': 'root' if vhost_name == '/' else vhost_name}
                if 'message_stats' in queue:
                    for k, v in queue['message_stats'].items():
                        if isinstance(v, int) and not '_details' in k:
                            self.counter(f'rabbitmq.queue_{k}', labels).set(float(v))
                for k in QUEUE_GAUGES:
                    if k in queue:
                        if isinstance(queue[k], int) and not '_details' in k:
                            self.counter(f'rabbitmq.queue_{k}', labels).set(float(queue[k]))

    def exchange_stats(self, vhost_names: Iterable[str]) -> None:
        for vhost_name in vhost_names:
            n = urllib.parse.quote(vhost_name, safe='')
            exchanges
            for exchange in self.get_data(f'/api/exchanges/{n}'):
                exch_name = exchange['name']
                labels = {'exchange_name': exch_name,
                          'vhost_name': 'root' if vhost_name == '/' else vhost_name,
                          'type': exchange['type']}
                if 'message_stats' in exchange:
                    for k, v in exchange['message_stats'].items():
                        if isinstance(v, int):
                            self.counter(f'rabbitmq.exchange_{k}', labels).set(float(v))
                for k in EXCHANGE_GAUGES:
                    if k in exchange:
                        if isinstance(exchange[k], int) and not '_details' in k:
                            self.counter(f'rabbitmq.exchange_{k}', labels).set(float(exchange[k]))

    def vhost_stats(self, vhost: dict) -> None:
        vhost_name = vhost['name']
        labels = {'vhost_name': 'root' if vhost_name == '/' else vhost_name}
        if 'message_stats' in vhost:
            for k, v in vhost['message_stats'].items():
                if isinstance(v, int):
                    self.counter(f'rabbitmq.vhost_{k}', labels).set(float(v))
            for k in ['messages', 'messages_unacknowledged', 'messages_ready',
                      'recv_oct', 'send_oct']:
                self.counter(f'rabbitmq.vhost_{k}', labels).set(float(vhost[k]))

    def node_stats(self, node_name: str) -> None:
        node = self.get_data(f'/api/nodes/{node_name}')
        labels = {'node_name': node_name}
        self.gauge('rabbitmq.partition_count', labels).set(len(node['partitions']))

        for k in NODE_COUNTERS:
            if k in node:
                self.counter(f'rabbitmq.node_{k}', labels).set(float(node[k]))

        for k in NODE_GAUGES:
            if k in node:
                self.gauge(f'rabbitmq.node_{k}', labels).set(float(node[k]))

    def overview_stats(self, overview: dict) -> None:
        for section in ['message_stats', 'queue_totals', 'object_totals']:
            for k, v in overview[section].items():
                if isinstance(v, int):
                    self.gauge(f'rabbitmq.{section}_{k}').set(float(v))
                elif isinstance(v, dict):
                    for l, w in v.items():
                        self.gauge(f'rabbitmq.{section}_{k}_{l}').set(float(w))


if __name__ == '__main__':
    sys.exit(RabbitMQ().run())