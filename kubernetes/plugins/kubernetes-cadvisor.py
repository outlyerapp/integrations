#!/usr/bin/env python3

import sys
import requests
import math

from outlyer_plugin import Plugin, Status
from prometheus_client.parser import text_string_to_metric_families

requests.packages.urllib3.disable_warnings()

GAUGE_METRICS = [
    'container_memory_usage_bytes',
]

COUNTER_METRICS = [
    'container_cpu_usage_seconds_total',
    'container_network_receive_bytes_total',
    'container_network_transmit_bytes_total',
    'container_network_receive_errors_total',
    'container_network_transmit_errors_total',
    'container_fs_writes_bytes_total',
    'container_fs_reads_bytes_total',
]

class CAdvisorPlugin(Plugin):

    def collect(self, _):
        PROTOCOL = self.get('protocol', 'http')
        HOST = self.get('ip', '127.0.0.1')
        PORT = self.get('port', '10255')
        ENDPOINT = self.get('endpoint', 'metrics/cadvisor')
        TOKEN_PATH = self.get('token_path', '/var/run/secrets/kubernetes.io/serviceaccount/token')
        header = token = ""
        
        if PROTOCOL == "https":
            with open(TOKEN_PATH) as token_file: 
                token = token_file.read()
                header = {"authorization": "bearer " + token}
        
        # Get cluster name to apply as label to all metrics
        cluster_name = self.get('k8s.cluster')
        metric_labels = {'k8s.cluster': 'unknown'}
        if cluster_name:
            metric_labels['k8s.cluster'] = cluster_name

        try:
            res = requests.get(f'{PROTOCOL}://{HOST}:{PORT}/{ENDPOINT}', timeout=20, verify=False, headers=header).text

            for family in text_string_to_metric_families(res):
                for sample in family.samples:
                    if sample[0] in COUNTER_METRICS:
                        sample[1]["container"] = sample[1].pop("container_name", None)
                        sample[1]["pod"] = sample[1].pop("pod_name", None)
                        labels = {**metric_labels, **sample[1]}
                        value = sample[2]
                        if not math.isnan(value):
                            self.counter(sample[0], labels).set(value)
                    elif sample[0] in GAUGE_METRICS:
                        sample[1]["container"] = sample[1].pop("container_name", None)
                        sample[1]["pod"] = sample[1].pop("pod_name", None)
                        labels = {**metric_labels, **sample[1]}
                        value = sample[2]
                        if not math.isnan(value):
                            self.gauge(sample[0], labels).set(value)

            return Status.OK

        except Exception as ex:
            self.logger.error('Unable to scrape metrics from cAdvisor: %s', str(ex))
            return Status.CRITICAL

if __name__ == '__main__':
    sys.exit(CAdvisorPlugin().run())
