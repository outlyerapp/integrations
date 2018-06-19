#!/usr/bin/env python3

import sys
import requests

from outlyer_plugin import Plugin, Status
from prometheus_client.parser import text_string_to_metric_families

GAUGE_METRICS = [
    'kube_node_status_condition',
    'kube_node_spec_unschedulable',
    'kube_daemonset_status_number_available',
    'kube_daemonset_status_number_unavailable',
    'kube_pod_info',
    'kube_node_status_capacity_pods',
    'kube_pod_status_phase',
    'kube_pod_container_status_waiting_reason',
    'kube_deployment_spec_replicas',
    'kube_deployment_status_replicas_updated',
    'kube_deployment_status_replicas',
    'kube_deployment_status_replicas_available',
    'kube_deployment_status_replicas_unavailable',
    'kube_deployment_status_observed_generation',
    'kube_deployment_metadata_generation',
]

COUNTER_METRICS = [
    'kube_pod_container_status_restarts_total',
]


class KubeStateMetricsPlugin(Plugin):

    def collect(self, _):
        HOST = self.get('ip', 'kube-state-metrics.kube-system')
        PORT = self.get('port', '8080')
        PATH = self.get('endpoint', 'metrics')

        try:
            res = requests.get(f'http://{HOST}:{PORT}/{PATH}', timeout=20).text

            for family in text_string_to_metric_families(res):
                for sample in family.samples:
                    if sample[0] in COUNTER_METRICS:
                        self.counter(sample[0], sample[1]).set(sample[2])
                    elif sample[0] in GAUGE_METRICS:
                        self.gauge(sample[0], sample[1]).set(sample[2])

            return Status.OK
        except Exception as ex:
            self.logger.error('Unable to scrape metrics from kube-state-metrics: %s', str(ex))
            return Status.CRITICAL


if __name__ == '__main__':
    sys.exit(KubeStateMetricsPlugin().run())