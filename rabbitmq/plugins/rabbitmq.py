import requests
import requests.exceptions
import urllib.parse
import urllib3

from typing import Iterable

from outlyer_agent.collection import Status, Plugin, PluginTarget, DEFAULT_PLUGIN_EXEC


NODE_COUNTERS = ['context_switches', 'gc_bytes_reclaimed', 'gc_num',
                 'io_file_handle_open_attempt_count''io_read_bytes', 'io_read_count',
                 'io_reopen_count', 'io_seek_count', 'io_sync_count',
                 'io_write_bytes', 'io_write_count', 'mnesia_disk_tx_count',
                 'mnesia_ram_tx_count', 'msg_store_read_count', 'msg_store_write_count',
                 'queue_index_journal_write_count', 'queue_index_read_count', 'queue_index_write_count',
                 'uptime']

NODE_GAUGES = ['disk_free', 'fd_total', 'fd_used',
               'io_file_handle_open_attempt_avg_time''io_read_avg_time', 'io_seek_avg_time',
               'io_sync_avg_time', 'io_write_avg_time', 'mem_used',
               'proc_total', 'proc_used', 'sockets_total', 'sockets_used']


class RabbitMQPlugin(Plugin):


    def __init__(self, name, deployments, host, logger, executor=DEFAULT_PLUGIN_EXEC):
        self.host = self.port = self.protocol = self.verify_ssl = None
        self.url = self.username = self.password = None
        super().__init__(name, deployments, host, logger, executor)

    def collect(self, target: PluginTarget) -> Status:

        try:
            self.host = target.get('host', 'localhost')
            self.port = target.get('port', '15672')
            self.protocol = target.get('protocol', 'http')
            self.verify_ssl = target.get('verify_ssl', True)
            self.username = target.get('username', 'guest')
            self.password = target.get('password', 'guest')

            self.url = f'{self.protocol}://{self.host}:{self.port}'

            # suppress requests/urllib3 ssl warnings when ignoring
            if not self.verify_ssl:
                urllib3.disable_warnings()

            # Overview stats

            overview = self.get_url('/api/overview')
            node_name = overview['node']

            self.overview_stats(target, overview)
            self.node_stats(target, node_name)

            vhost_names = list()
            for vhost in self.get_url('/api/vhosts'):
                vhost_name = vhost['name']
                vhost_names.append(vhost_name)
                if target.get('vhost_stats', False):
                    self.vhost_stats(target, vhost)

            if target.get('queue_stats', False):
                self.queue_stats(target, vhost_names)

            if target.get('exchange_stats', False):
                self.exchange_stats(target, vhost_names)

            return Status.OK

        except requests.exceptions.HTTPError as ex:
            self.logger.error('HTTP error connecting to RabbitMQ: %s', str(ex))
            return Status.CRITICAL

    def get_url(self, url: str) -> any:
        r = requests.get(self.url + url, auth=(self.username, self.password),
                         timeout=10, verify=self.verify_ssl)
        r.raise_for_status()
        return r.json()

    def queue_stats(self, target: PluginTarget, vhost_names: Iterable[str]) -> None:
        for vhost_name in vhost_names:
            n = urllib.parse.quote(vhost_name, safe='')
            for queue in self.get_url(f'/api/queues/{n}'):
                queue_name = queue['name']
                labels = {'queue_name': queue_name,
                          'vhost_name': 'root' if vhost_name == '/' else vhost_name}
                if 'message_stats' in queue:
                    for k, v in queue['message_stats'].items():
                        if isinstance(v, int) and not '_details' in k:
                            target.counter(f'rabbitmq.queue_{k}', labels).set(float(v))
                for k in ['messages', 'messages_unacknowledged', 'messages_ready', 'reductions']:
                    if k in queue:
                        if isinstance(queue[k], int) and not '_details' in k:
                            target.counter(f'rabbitmq.queue_{k}', labels).set(float(queue[k]))

    def exchange_stats(self, target: PluginTarget, vhost_names: Iterable[str]) -> None:
        for vhost_name in vhost_names:
            n = urllib.parse.quote(vhost_name, safe='')
            for exchange in self.get_url(f'/api/exchanges/{n}'):
                exch_name = exchange['name']
                labels = {'exchange_name': exch_name,
                          'vhost_name': 'root' if vhost_name == '/' else vhost_name,
                          'type': exchange['type']}
                if 'message_stats' in exchange:
                    for k, v in exchange['message_stats'].items():
                        if isinstance(v, int):
                            target.counter(f'rabbitmq.exchange_{k}', labels).set(float(v))

    def vhost_stats(self, target: PluginTarget, vhost: dict) -> None:
        vhost_name = vhost['name']
        labels = {'vhost_name': 'root' if vhost_name == '/' else vhost_name}
        if 'message_stats' in vhost:
            for k, v in vhost['message_stats'].items():
                if isinstance(v, int):
                    target.counter(f'rabbitmq.vhost_{k}', labels).set(float(v))
            for k in ['messages', 'messages_unacknowledged', 'messages_ready',
                      'recv_oct', 'send_oct']:
                target.counter(f'rabbitmq.vhost_{k}', labels).set(float(vhost[k]))

    def node_stats(self, target: PluginTarget, node_name: str) -> None:
        node = self.get_url(f'/api/nodes/{node_name}')
        labels = {'node_name': node_name}
        target.gauge('rabbitmq.partition_count', labels).set(len(node['partitions']))

        for k in NODE_COUNTERS:
            if k in node:
                target.counter(f'rabbitmq.node_{k}', labels).set(float(node[k]))

        for k in NODE_GAUGES:
            if k in node:
                target.gauge(f'rabbitmq.node_{k}', labels).set(float(node[k]))

    def overview_stats(self, target: PluginTarget, overview: dict) -> None:
        for section in ['message_stats', 'queue_totals', 'object_totals']:
            for k, v in overview[section].items():
                if isinstance(v, int):
                    target.gauge(f'rabbitmq.{section}_{k}').set(float(v))
                elif isinstance(v, dict):
                    for l, w in v.items():
                        target.gauge(f'rabbitmq.{section}_{k}_{l}').set(float(w))
