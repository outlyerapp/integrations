import requests
import requests.exceptions

from outlyer_agent.collection import Status, Plugin, PluginTarget

# TODO: add search for regex/DOM?


class HttpRequestPlugin(Plugin):

    def collect(self, target: PluginTarget) -> Status:

        url = target.get('url')
        if not url:
            self.logger.error('HTTP plugin is not configured')
            return Status.UNKNOWN

        type = target.get('type', 'GET')
        params = target.get('params', None)
        headers = target.get('headers', None)
        data = target.get('data', None)
        pattern = target.get('pattern', None)
        error_on_redirect = target.get('error_on_redirect', False)
        warning_time = target.get('warning_time', 5.0)
        critical_time = target.get('critical_time', 10.0)

        status = Status.OK  # type: Status

        self.logger.info('Sending %s request to %s', type, url)
        response = requests.request(type, url, params=params, headers=headers, data=data)
        content = ''

        target.gauge('status_code').set(float(response.status_code))
        error_min = 300 if error_on_redirect else 400
        if response.status_code >= error_min:
            status = Status.CRITICAL
        else:
            content = response.content.decode('utf-8', 'ignore')
            if pattern and pattern not in content:
                self.logger.info('Pattern "%s" not found in response content', pattern)
                status = Status.CRITICAL

        if 'Content-Length' in response.headers:
            target.gauge('response_size', {'uom': 'bytes'}).set(float(response.headers['Content-Length']))
        elif content:
            target.gauge('response_size', {'uom': 'bytes'}).set(len(content))

        elapsed_time = response.elapsed.total_seconds()
        target.gauge('response_time', {'uom': 'ms'}).set(elapsed_time)
        self.logger.info('Download of %s finished in %f seconds', url, elapsed_time)

        if elapsed_time >= critical_time:
            status = Status.CRITICAL
        elif elapsed_time >= warning_time:
            status = Status.WARNING

        self.logger.info('Result = %s', str(status))

        return status
