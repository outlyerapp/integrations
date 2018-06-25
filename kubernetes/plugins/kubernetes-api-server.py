#!/usr/bin/env python3

"""
Scrapes the Kubernetes API /healthz and /metrics endpoints using the Kubernetes
client to enable Authentication with the server
"""

import sys
import os
import math
from outlyer_plugin import Plugin, Status
from prometheus_client.parser import text_string_to_metric_families
from kubernetes import client, config

GAUGE_METRICS = [
    'apiserver_request_latencies_summary',
]

COUNTER_METRICS = [
    'apiserver_request_count',
]

class KubeApiServerPlugin(Plugin):

    def collect(self, _):
        config.load_incluster_config()
        v1 = client.CoreV1Api()

        # Authentication setting
        auth_settings = ['BearerToken']

        # Get endpoint, defaults to healthz
        endpoint = '/' + os.environ['endpoint'] if 'endpoint' in os.environ else '/healthz'

        # Get cluster name to apply as label to all metrics
        cluster_name_key = self.get('cluster_name_key', 'k8s.node.cluster')
        cluster_name = self.get(cluster_name_key, None)
        metric_labels = {'k8s.cluster': 'unknown'}
        if cluster_name:
            metric_labels['k8s.cluster'] = cluster_name

        if 'healthz' in endpoint:
            try:
                res = v1.api_client.call_api(endpoint, 'GET',
                                             auth_settings=auth_settings,
                                             _request_timeout=20,
                                             response_type=str)
                if res[1] == 200:
                    return Status.OK
                else:
                    self.logger.error('Expected response code 200 but got: %s', res[1])
                    return Status.CRITICAL
            except Exception as ex:
                self.logger.error('Unable to reach %s: %s', endpoint, str(ex))
                return Status.CRITICAL
        else:
            try:
                # Scrape a Prometheus endpoint
                res = v1.api_client.call_api(endpoint, 'GET',
                                             auth_settings=auth_settings,
                                             _request_timeout=20,
                                             _return_http_data_only=True,
                                             response_type=str)

                # Covert Prometheus response to Outlyer Native format
                for family in text_string_to_metric_families(res):
                    for sample in family.samples:
                        labels = {k: v for k, v in sample[1].items() if v != ''}
                        labels = {**metric_labels, **labels}
                        if sample[0] in COUNTER_METRICS:
                            value = sample[2]
                            if not math.isnan(value):
                                self.counter(sample[0], labels).set(value)
                        elif sample[0] in GAUGE_METRICS:
                            value = sample[2]
                            if not math.isnan(value):
                                self.gauge(sample[0], labels).set(value)

                return Status.OK
            except Exception as ex:
                self.logger.error('API Server is unavailable: %s', str(ex))
                return Status.CRITICAL

if __name__ == '__main__':
    sys.exit(KubeApiServerPlugin().run())
