import logging
import time

import requests
import requests.exceptions

from outlyer_agent.collection import Status, Plugin, PluginTarget, DEFAULT_PLUGIN_EXEC

logger = logging.getLogger(__name__)
REQUIREMENTS = ['requests==2.18.4']


class NginxPlusPlugin(Plugin):

    def __init__(self, name, deployments, host, executor=DEFAULT_PLUGIN_EXEC):
        super().__init__(name, deployments, host, executor)
        self.last_collect = None

    def collect(self, target: PluginTarget):

        url = target.get('url', None)
        if not url:
            logger.error('Nginx server status URL not specified in configuration file')
            return Status.UNKNOWN

        time_now = time.monotonic()

        def _per_sec(name: str, new_value: float, dims: dict=None):
            if self.last_collect:
                ps_name = name + '_per_sec'
                old_value = target.counter(name, dims).get()
                target.gauge(ps_name, dims).set((new_value - old_value) / (time_now - self.last_collect))
            target.counter(name, dims).set(new_value)

        try:

            response = requests.get(url)
            response.raise_for_status()
            status = response.json()

            target.gauge('connections.active').set(float(status['connections']['active']))
            target.gauge('connections.idle').set(float(status['connections']['idle']))

            _per_sec('connections.accepted', status['connections']['accepted'])
            _per_sec('connections.dropped', status['connections']['dropped'])

            _per_sec('ssl.handshakes', status['ssl']['handshakes'])
            _per_sec('ssl.handshakes_failed', status['ssl']['handshakes_failed'])
            _per_sec('ssl.session_reuses', status['ssl']['session_reuses'])

            target.gauge('requests.current').set(float(status['requests']['current']))
            _per_sec('requests.total', status['requests']['total'])

            for zone, stats in status['server_zones'].items():

                dim = {'zone': zone}

                target.gauge('processing', dim).set(float(stats['processing']))

                for key in 'requests', 'discarded', 'received', 'sent':
                    _per_sec(key, stats[key], dim)
                for key, val in stats['responses'].items():
                    _per_sec(key, val, dim)

            self.last_collect = time_now
            return Status.OK

        except requests.exceptions.HTTPError as ex:
            logger.error('Unable to connect to Nginx Plus server: ' + ex.args[0])

            self.last_collect = None
            return Status.CRITICAL

        except Exception as ex:
            logger.exception('Error in plugin', exc_info=ex)

            self.last_collect = None
            return Status.UNKNOWN
