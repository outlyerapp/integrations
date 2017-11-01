import requests
import requests.exceptions
import urllib.parse

from outlyer_agent.collection import Status, Plugin, PluginTarget


NODE_COUNTERS = ['gc_num', 'gc_bytes_reclaimed', 'context_switches',
                 'io_read_count', 'io_read_bytes', 'io_write_count', 'io_write_bytes',
                 'io_sync_count', 'io_seek_count', 'io_reopen_count',
                 'mnesia_ram_tx_count', 'mnesia_disk_tx_count',
                 'msg_store_read_count', 'msg_store_write_count',
                 'queue_index_journal_write_count', 'queue_index_write_count',
                 'queue_index_read_count', 'io_file_handle_open_attempt_count']

NODE_GAUGES = ['mem_used', 'fd_used', 'sockets_used', 'proc_used',
               'disk_free', 'io_read_avg_time', 'io_write_avg_time', 'io_sync_avg_time',
               'io_seek_avg_time', 'io_file_handle_open_attempt_avg_time']


class RabbitMQPlugin(Plugin):
    def collect(self, target: PluginTarget) -> Status:

        try:
            host = target.get('host', 'localhost')
            port = target.get('port', '15672')
            protocol = target.get('protocol', 'http')
            verify_ssl = target.get('verify_ssl', True)
            username = target.get('username', 'guest')
            password = target.get('password', 'guest')

            url = (f'{protocol}://{host}:{port}')

            # Overview stats

            r = requests.get(f'{url}/api/overview', auth=(username, password), timeout=10, verify=verify_ssl)
            r.raise_for_status()
            overview = r.json()  # type: dict
            node_name = overview['node']

            for section in ['message_stats', 'queue_totals', 'object_totals']:
                for k, v in overview[section].items():
                    if isinstance(v, int):
                        target.gauge(f'rabbitmq_{section}_{k}').set(float(v))
                    elif isinstance(v, dict):
                        for l,w in v.items():
                            target.gauge(f'rabbit_mq{section}_{k}_{l}').set(float(w))

            # Node stats

            r = requests.get(f'{url}/api/nodes/{node_name}', auth=(username, password), timeout=10, verify=verify_ssl)
            r.raise_for_status()
            node = r.json()

            target.gauge('rabbitmq_partition_count').set(len(node['partitions']))

            for k in NODE_COUNTERS:
                if k in node:
                    target.counter(f'rabbitmq_node_{k}').set(float(node[k]))

            for k in NODE_GAUGES:
                if k in node:
                    target.gauge(f'rabbitmq_node_{k}').set(float(node[k]))


            # Vhost stats

            r = requests.get(f'{url}/api/vhosts', auth=(username, password), timeout=10, verify=verify_ssl)
            r.raise_for_status()
            vhosts = r.json()  # type: dict
            vhost_names = list()
            for vhost in vhosts:
                vhost_name = vhost['name']
                vhost_names.append(vhost_name)
                labels = {'vhost_name': vhost_name}
                if 'message_stats' in vhost:
                    for k, v in vhost['message_stats'].items():
                        if isinstance(v, int):
                            target.counter(f'rabbitmq_vhost_{k}', labels).set(float(v))
                    for k in ['messages', 'messages_unacknowledged', 'messages_ready',
                              'recv_oct', 'send_oct']:
                        target.counter(f'rabbitmq_vhost_{k}', labels).set(float(vhost[k]))

            # Queue stats

            for vhost_name in vhost_names:
                n = urllib.parse.quote(vhost_name, safe='')
                r = requests.get(f'{url}/api/queues/{n}', auth=(username, password), timeout=10, verify=verify_ssl)
                r.raise_for_status()
                for queue in r.json():
                    queue_name = queue['name']
                    labels = {'queue_name': queue_name, 'vhost_name': vhost_name}
                    if 'message_stats' in queue:
                        for k, v in queue['message_stats'].items():
                            if isinstance(v, int):
                                target.counter(f'rabbitmq_queue_{k}', labels).set(float(v))
                        for k in ['messages', 'messages_unacknowledged', 'messages_ready', 'reductions']:
                            target.gauge(f'rabbitmq_queue_{k}', labels).set(float(queue[k]))

            # Exchange stats

            for vhost_name in vhost_names:
                n = urllib.parse.quote(vhost_name, safe='')
                r = requests.get(f'{url}/api/exchanges/{n}', auth=(username, password), timeout=10, verify=verify_ssl)
                r.raise_for_status()
                for exchange in r.json():
                    exch_name = exchange['name']
                    labels = {'exchange_name': exch_name, 'vhost_name': vhost_name, 'type': exchange['type']}
                    if 'message_stats' in exchange:
                        for k, v in exchange['message_stats'].items():
                            if isinstance(v, int):
                                target.counter(f'rabbitmq_exchange_{k}', labels).set(float(v))

            return Status.OK

        except requests.exceptions.HTTPError as ex:
            self.logger.error('HTTP error connecting to RabbitMQ: %s', str(ex))
            return Status.CRITICAL
