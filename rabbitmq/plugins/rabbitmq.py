import requests
import requests.exceptions
import urllib.parse

from outlyer_agent.collection import Status, Plugin, PluginTarget


NODE_COUNTERS = ['context_switches','gc_bytes_reclaimed','gc_num',
                 'io_file_handle_open_attempt_count''io_read_bytes','io_read_count',
                 'io_reopen_count','io_seek_count','io_sync_count',
                 'io_write_bytes','io_write_count','mnesia_disk_tx_count',
                 'mnesia_ram_tx_count','msg_store_read_count','msg_store_write_count',
                 'queue_index_journal_write_count','queue_index_read_count','queue_index_write_count',
                 'uptime']

NODE_GAUGES = ['disk_free','fd_total','fd_used',
               'io_file_handle_open_attempt_avg_time''io_read_avg_time','io_seek_avg_time',
               'io_sync_avg_time','io_write_avg_time','mem_used',
               'proc_total','proc_used','sockets_total', 'sockets_used']


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

            # suppress requests/urllib3 ssl warnings when ignoring
            if not verify_ssl:
                requests.packages.urllib3.disable_warnings()

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
                if f'{k}_details' in node:
                    target.gauge(f'rabbitmq_node_{k}_details_rate').set(float(node[f'{k}_details']['rate']))

            for k in NODE_GAUGES:
                if k in node:
                    target.gauge(f'rabbitmq_node_{k}').set(float(node[k]))
                if f'{k}_details' in node:
                    target.gauge(f'rabbitmq_node_{k}_details_rate').set(float(node[f'{k}_details']['rate']))


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
                            if k in queue:
                                if isinstance(v, int):
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
