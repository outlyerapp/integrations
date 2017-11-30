import re

import requests
import requests.exceptions

from outlyer_agent.collection import Status, Plugin, PluginTarget, DEFAULT_PLUGIN_EXEC


class NginxStatusPlugin(Plugin):

    def collect(self, target: PluginTarget):

        url = target.get('url', None)
        if not url:
            self.logger.error('Nginx server status URL not specified in configuration file')
            return Status.UNKNOWN

        try:

            response = requests.get(url)
            response.raise_for_status()

            text = response.content.decode('utf-8')

            m = re.search(r'Active connections:\s+(\d+)', text)
            if m:
                target.gauge('nginx.active').set(int(m.group(1)))

            m = re.search(r'server accepts handled requests\n\s+(\d+)\s+(\d+)\s+(\d+)', text)
            if m:
                target.counter('nginx.accepted').set(int(m.group(1)))
                target.counter('nginx.handled').set(int(m.group(2)))
                target.counter('nginx.requests').set(int(m.group(3)))

            m = re.search(r'Reading:\s+(\d+)\s+Writing:\s+(\d+)\s+Waiting:\s+(\d+)', text)
            if m:
                target.gauge('nginx.reading').set(int(m.group(1)))
                target.gauge('nginx.writing').set(int(m.group(2)))
                target.gauge('nginx.waiting').set(int(m.group(3)))

            return Status.OK

        except requests.exceptions.RequestException as ex:
            self.logger.error('Unable to connect to Nginx server: ' + str(ex))
            return Status.CRITICAL

        except Exception as ex:
            self.logger.exception('Error in plugin', exc_info=ex)
            return Status.UNKNOWN
