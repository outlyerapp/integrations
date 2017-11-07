import re

import requests
import requests.auth
import requests.exceptions

from outlyer_agent.collection import Status, Plugin, PluginTarget


class PrometheusPlugin(Plugin):

    def collect(self, target: PluginTarget) -> Status:

        endpoints = target.get('endpoints')
        if not endpoints:
            self.logger.error('Prometheus plugin is not configured correctly')
            return Status.UNKNOWN
        if isinstance(endpoints, str):
            endpoints = [x.strip() for x in endpoints.split(',')]

        status = Status.OK
        for endpoint in endpoints:  # type: dict
            url = endpoint.get('url', None)
            username = endpoint.get('username', None)
            password = endpoint.get('password', None)

            try:
                auth = requests.auth.HTTPBasicAuth(username, password) if username or password else None
                r = requests.get(url, auth=auth)
                r.raise_for_status()

            except requests.exceptions.ConnectionError as ex:
                self.logger.error('Error fetching %s: %s', url, str(ex))
                status = Status.CRITICAL
                continue

            content_type = r.headers.get('Content-Type')
            if 'text/plain' not in content_type:
                self.logger.error('Invalid response from Prometheus endpoint %s: ' +
                                  'content type is %s (was expecting text/plain)', url, content_type)
                status = Status.UNKNOWN
                continue

            help_t = (None, None)
            type_t = (None, None)
            for line in r.iter_lines(decode_unicode='utf-8'):  # type: str
                if not line.strip():
                    continue
                m = re.match(r'# HELP (?P<name>\w+) (?P<help>.*)', line)
                if m:
                    help_t = (m.group('name'), m.group('help'))
                    continue
                m = re.match(r'# TYPE (?P<name>\w+) (?P<type>.*)', line)
                if m:
                    type_t = (m.group('name'), m.group('type'))
                    continue
                m = re.match(r'(?P<name>\w+)(?:{(?P<labels>.*)})? (?P<value>.*)', line)
                if m:
                    name = m.group('name')
                    help_str = help_t[1] if help_t[0] == name else None
                    type_str = type_t[1] if type_t[0] == name else None
                    value = float(m.group('value'))

                    label_str = m.group('labels')
                    labels = {'url': url}
                    if label_str:
                        labels.update({x[0]: x[1] for x in re.findall(r'(\w+)="([^"]*)"', label_str)})

                    if type_str == 'counter':
                        target.counter(name, labels).set(value)
                    else:
                        target.gauge(name, labels).set(value)

        return status
