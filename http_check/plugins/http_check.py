#!/usr/bin/env python3

import sys
import requests

from outlyer_plugin import Plugin, Status

class HttpRequestPlugin(Plugin):

    def collect(self, _) -> Status:

        name = self.get('name')
        url = self.get('url')
        if not url or not name:
            self.logger.error('HTTP plugin is not configured')
            return Status.UNKNOWN

        method = self.get('method', 'GET')
        params_str = self.get('params', None)
        headers_str = self.get('headers', None)
        data = self.get('data', None)
        pattern = self.get('pattern', None)
        error_on_redirect = self.get('error_on_redirect', False)
        warning_time = float(self.get('warning_time', 2.5))
        critical_time = float(self.get('critical_time', 5.0))

        params = self._from_key_value_string_to_dict(params_str) if params_str else None
        headers = self._from_key_value_string_to_dict(headers_str) if headers_str else None

        status = Status.OK  # type: Status

        self.logger.info('Sending %s request to %s', method, url)
        response = requests.request(method, url, params=params, headers=headers, data=data)
        content = ''

        self.gauge('http.status_code', {'site': name}).set(float(response.status_code))
        error_min = 400 if not error_on_redirect else 300

        if response.status_code >= error_min:
            status = Status.CRITICAL
        else:
            content = response.content.decode('utf-8', 'ignore')
            if pattern and pattern not in content:
                self.logger.info('Pattern "%s" not found in response content', pattern)
                status = Status.CRITICAL

        if 'Content-Length' in response.headers:
            self.gauge('http.response_size', {'site': name, 'uom': 'bytes'}).set(float(response.headers['Content-Length']))
        elif content:
            self.gauge('http.response_size', {'site': name, 'uom': 'bytes'}).set(len(content))

        elapsed_time = response.elapsed.total_seconds()
        self.gauge('http.response_time', {'site': name, 'uom': 'ms'}).set(elapsed_time)
        self.logger.info('Download of %s finished in %f seconds', url, elapsed_time)

        if elapsed_time >= critical_time:
            status = Status.CRITICAL
        elif elapsed_time >= warning_time:
            status = Status.WARNING

        self.logger.info('Result = %s', str(status))

        return status

    def _from_key_value_string_to_dict(self, xuxa):
        return dict(token.split(':') for token in xuxa.strip().split(","))


if __name__ == '__main__':
    sys.exit(HttpRequestPlugin().run())
