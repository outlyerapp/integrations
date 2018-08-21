#!/usr/bin/env python3

import sys
import requests
import math

from outlyer_plugin import Plugin, Status
from prometheus_client.parser import text_string_to_metric_families

GAUGE_METRICS = [
    'kube_daemonset_status_number_available',
    'kube_daemonset_status_number_unavailable',
    'kube_pod_info',
    'kube_deployment_spec_replicas',
    'kube_deployment_status_replicas_updated',
    'kube_deployment_status_replicas',
    'kube_deployment_status_replicas_available',
    'kube_deployment_status_replicas_unavailable',
    'kube_deployment_status_observed_generation',
    'kube_deployment_metadata_generation',
    'kube_pod_status_phase',
    'kube_pod_container_resource_requests_cpu_cores',
    'kube_pod_container_resource_limits_cpu_cores',
    'kube_pod_container_resource_requests_memory_bytes',
    'kube_pod_container_resource_limits_memory_bytes',
    'kube_pod_container_status_terminated_reason',
    'kube_pod_container_status_waiting_reason',
    'kube_pod_status_ready',
    'kube_service_info',
    'kube_node_status_allocatable_memory_bytes',
    'kube_node_status_allocatable_cpu_cores',
    'kube_node_status_condition',
    'kube_node_status_capacity_pods',
    'kube_node_spec_unschedulable',
]

COUNTER_METRICS = [
    'kube_pod_container_status_restarts_total',
]

class KubeStateMetricsPlugin(Plugin):

    def collect(self, _):
        HOST = self.get('ip', 'kube-state-metrics.kube-system')
        PORT = self.get('port', '8080')
        PATH = self.get('endpoint', 'metrics')

        # Get cluster name to apply as label to all metrics
        cluster_name = self.get('k8s.cluster')
        metric_labels = {'k8s.cluster': 'unknown'}
        if cluster_name:
            metric_labels['k8s.cluster'] = cluster_name

        try:
            res = requests.get(f'http://{HOST}:{PORT}/{PATH}', timeout=20).text

            for family in text_string_to_metric_families(res):
                for sample in family.samples:
                    labels = {**metric_labels, **sample[1]}
                    value = sample[2]
                    if not math.isnan(value):
                        if sample[0] in COUNTER_METRICS:
                            self.counter(sample[0], labels).set(value)
                        else:
                            self.gauge(sample[0], labels).set(value)

            return Status.OK

        except Exception as ex:
            self.logger.error('Unable to scrape metrics from kube-state-metrics: %s', str(ex))
            return Status.CRITICAL

if __name__ == '__main__':
    sys.exit(KubeStateMetricsPlugin().run())
