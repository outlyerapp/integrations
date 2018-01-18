#!/usr/bin/env python3

import sys

import requests
import requests.exceptions

from outlyer_plugin import Plugin, Status


class NginxPlusPlugin(Plugin):

    def __init__(self, logger):
        super().__init__(logger)

    def collect(self, _):

        url = self.get('url', None)
        if not url:
            self.logger.error('Nginx server status URL not specified in configuration file')
            return Status.UNKNOWN

        try:

            response = requests.get(url)
            response.raise_for_status()
            status = response.json()

            self.gauge('nginx.connections_active').set(float(status['connections']['active']))
            self.gauge('nginx.connections_idle').set(float(status['connections']['idle']))

            self.counter('nginx.connections_accepted', status['connections']['accepted'])
            self.counter('nginx.connections_dropped', status['connections']['dropped'])

            self.counter('nginx.ssl_handshakes', status['ssl']['handshakes'])
            self.counter('nginx.ssl_handshakes_failed', status['ssl']['handshakes_failed'])
            self.counter('nginx.ssl_session_reuses', status['ssl']['session_reuses'])

            self.gauge('nginx.requests_current').set(float(status['requests']['current']))
            self.counter('nginx.requests_total', status['requests']['total'])

            for zone, stats in status['server_zones'].items():

                dim = {'zone': zone}

                self.gauge('nginx.processing', dim).set(float(stats['processing']))

                for key in 'requests', 'discarded', 'received', 'sent':
                    self.counter(key, dim).set(stats[key])

                for key, val in stats['responses'].items():
                    self.counter(key, dim).set(val)

            return Status.OK

        except requests.exceptions.HTTPError as ex:
            self.logger.error('Unable to connect to Nginx Plus server: ' + ex.args[0])
            self.last_collect = None
            return Status.CRITICAL

        except Exception as ex:
            self.logger.exception('Error in plugin', exc_info=ex)
            self.last_collect = None
            return Status.UNKNOWN


if __name__ == '__main__':
    sys.exit(NginxPlusPlugin().run())
