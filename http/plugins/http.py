from outlyer_agent.collection import Status, Plugin, PluginTarget, DEFAULT_PLUGIN_EXEC
from datetime import datetime
import time
import logging
import requests
import requests.exceptions


# TODO: add parameters for URL, expect_string, etc.
# TODO: add search for regex/DOM?
# TODO: replace timer with time.monotonic()

logger = logging.getLogger(__name__)

URL = 'https://www.google.com'
TYPE = 'GET'
HEADERS = {}
DATA = {}
PARAMS = {}
PATTERN = 'Cloud Services at Scale'
REDIRECT_IS_ERROR = False
CRITICAL_RESPONSE_TIME = 1.0
WARNING_RESPONSE_TIME = 0.750


class HttpRequestPlugin(Plugin):

    def collect(self, target: PluginTarget):

        start_time = datetime.utcnow()
        status = Status.OK  # type: Status

        response = requests.request(TYPE, URL, params=PARAMS, headers=HEADERS, data=DATA)
        content = ''

        target.gauge('status_code').set(float(response.status_code))
        error_min = 300 if REDIRECT_IS_ERROR else 400
        if response.status_code >= error_min:
            status = Status.CRITICAL
        else:
            content = response.content.decode('utf-8', 'ignore')
            if PATTERN and PATTERN not in content:
                status = Status.CRITICAL

        if 'Content-Length' in response.headers:
            target.gauge('response_size', {'uom': 'bytes'}).set(float(response.headers['Content-Length']))
        elif content:
            target.gauge('response_size', {'uom': 'bytes'}).set(len(content))

        end_time = datetime.utcnow()
        elapsed_time = (end_time - start_time).total_seconds()
        target.gauge('response_time', {'uom': 'ms'}).set(elapsed_time)

        if elapsed_time >= CRITICAL_RESPONSE_TIME:
            status = Status.CRITICAL
        elif elapsed_time >= WARNING_RESPONSE_TIME:
            status = Status.WARNING

        return status
