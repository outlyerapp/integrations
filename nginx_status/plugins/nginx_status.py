import logging
import re
import time

import requests
import requests.exceptions

from outlyer_agent.collection import Status, Plugin, PluginTarget, DEFAULT_PLUGIN_EXEC

logger = logging.getLogger(__name__)
REQUIREMENTS = ['requests==2.18.4']


class NginxStatusPlugin(Plugin):

    def __init__(self, name, deployments, host, executor=DEFAULT_PLUGIN_EXEC):
        super().__init__(name, deployments, host, executor)
        self.last_collect = None

    def collect(self, target: PluginTarget):

        url = target.get('url', None)
        if not url:
            logger.error('Nginx server status URL not specified in configuration file')
            return Status.UNKNOWN

        try:

            time_now = time.monotonic()
            response = requests.get(url)
            response.raise_for_status()

            text = response.content.decode('utf-8')

            m = re.search(r'Active connections:\s+(\d+)', text)
            if m:
                target.gauge('active').set(int(m.group(1)))

            m = re.search(r'server accepts handled requests\n\s+(\d+)\s+(\d+)\s+(\d+)', text)
            if m:
                if self.last_collect:
                    elapsed_sec = time_now - self.last_collect
                    target.gauge('accepted_per_sec').set((float(m.group(1)) - target.gauge('accepted').get()) / elapsed_sec)
                    target.gauge('handled_per_sec').set((float(m.group(1)) - target.gauge('handled').get()) / elapsed_sec)
                    target.gauge('requests_per_sec').set((float(m.group(1)) - target.gauge('requests').get()) / elapsed_sec)

                target.gauge('accepted').set(int(m.group(1)))
                target.gauge('handled').set(int(m.group(2)))
                target.gauge('requests').set(int(m.group(3)))

            m = re.search(r'Reading:\s+(\d+)\s+Writing:\s+(\d+)\s+Waiting:\s+(\d+)', text)
            if m:
                target.gauge('reading').set(int(m.group(1)))
                target.gauge('writing').set(int(m.group(2)))
                target.gauge('waiting').set(int(m.group(3)))

            self.last_collect = time_now
            return Status.OK

        except requests.exceptions.RequestException as ex:
            logger.error('Unable to connect to Nginx server: ' + str(ex))

            self.last_collect = None
            return Status.CRITICAL

        except Exception as ex:
            logger.exception('Error in plugin', exc_info=ex)

            self.last_collect = None
            return Status.UNKNOWN
