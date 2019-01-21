#!/usr/bin/env python3

import sys
import requests
import math

from outlyer_plugin import Plugin, Status
from prometheus_client.parser import text_string_to_metric_families
from kubernetes import client, config

requests.packages.urllib3.disable_warnings()

class KubeletPlugin(Plugin):

    def collect(self, _):
        PROTOCOL = self.get('protocol', 'http')
        HOST = self.get('ip', '127.0.0.1')
        PORT = self.get('port', '10255')
        SUMMARY_ENDPOINT = self.get('summary_endpoint', 'stats/summary')
        CADVISOR_ENDPOINT = self.get('cadvisor_endpoint', 'metrics/cadvisor')
        TOKEN_PATH = self.get('token_path', '/var/run/secrets/kubernetes.io/serviceaccount/token')
        header = token = ''

        if PROTOCOL == 'https':
            with open(TOKEN_PATH) as token_file: 
                token = token_file.read()
                header = {'authorization': 'bearer ' + token}

        # Creates cluster global labels
        cluster_name = self.get('k8s.cluster')
        cluster_global_labels = {'k8s.cluster': 'unknown'}
        if cluster_name:
            cluster_global_labels['k8s.cluster'] = cluster_name
        cluster_global_labels['k8s.node.name'] = self.get('k8s.node.name')

        # Creates API Server client for core v1 API
        config.load_incluster_config()
        api_server_client = client.CoreV1Api()

        self.scrape_summary(f'{PROTOCOL}://{HOST}:{PORT}/{SUMMARY_ENDPOINT}', header, cluster_global_labels, api_server_client)
        self.scrape_cadvisor(f'{PROTOCOL}://{HOST}:{PORT}/{CADVISOR_ENDPOINT}', header, cluster_global_labels, api_server_client)

        return Status.OK


    def scrape_summary(self, kubelet_metrics_url, header, cluster_global_labels, api_server_client):
        try:
            # Scrapes Summary API
            res = requests.get(kubelet_metrics_url, timeout=20, verify=False, headers=header)
            res.raise_for_status()
            res = res.json()

            node = res.get('node')

            node_api_server = api_server_client.list_node(field_selector='metadata.name='+cluster_global_labels['k8s.node.name'])

            node_labels = []
            for label_key, label_value in node_api_server.items[0].metadata.labels.items():
                label = f'{label_key}: {label_value}'
                node_labels.append(label)

            for label in node_labels:
                labels = {**cluster_global_labels}
                labels['k8s.node.label'] = label
                node_memory_usage_bytes = node['memory']['workingSetBytes']
                node_allocatable_memory_bytes = self.__to_byte(node_api_server.items[0].status.allocatable['memory'])
                self.gauge('kube_node_memory_usage_pct', labels).set(node_memory_usage_bytes/node_allocatable_memory_bytes*100)
                self.gauge('kube_node_memory_usage_bytes', labels).set(node_memory_usage_bytes)

                node_cpu_usage_cores = node['cpu']['usageNanoCores']/1000000000
                node_allocatable_cpu_cores = self.__to_core(node_api_server.items[0].status.allocatable['cpu'])
                self.gauge('kube_node_cpu_usage_cores', labels).set(node_cpu_usage_cores)
                self.gauge('kube_node_cpu_usage_pct', labels).set(node_cpu_usage_cores/node_allocatable_cpu_cores*100)

                for network_interface in node['network']['interfaces']:
                    labels_network = {**labels}
                    labels_network['interface'] = network_interface['name']
                    self.counter('kube_node_network_rx_bytes', labels_network).set(network_interface['rxBytes'])
                    self.counter('kube_node_network_tx_bytes', labels_network).set(network_interface['txBytes'])
                    self.counter('kube_node_network_rx_errors', labels_network).set(network_interface['rxErrors'])
                    self.counter('kube_node_network_tx_errors', labels_network).set(network_interface['txErrors'])

                node_fs_nodefs_used_bytes = node['fs']['usedBytes']
                node_fs_nodefs_capacity_bytes = node['fs']['capacityBytes']
                node_fs_nodefs_used_pct = node_fs_nodefs_used_bytes/node_fs_nodefs_capacity_bytes*100
                self.gauge('kube_node_fs_nodefs_used_bytes', labels).set(node_fs_nodefs_used_bytes)
                self.gauge('kube_node_fs_nodefs_capacity_bytes', labels).set(node_fs_nodefs_capacity_bytes)
                self.gauge('kube_node_fs_nodefs_used_pct', labels).set(node_fs_nodefs_used_pct)

                # Kubelet eviction policy is based on these metrics
                # https://kubernetes.io/docs/tasks/administer-cluster/out-of-resource/
                self.gauge('kube_node_memory_available_bytes', labels).set(node['memory']['availableBytes'])
                self.gauge('kube_node_fs_nodefs_available_bytes', labels).set(node['fs']['availableBytes'])
                self.gauge('kube_node_fs_nodefs_inodes_free', labels).set(node['fs']['inodesFree'])
                self.gauge('kube_node_fs_imagefs_available_bytes', labels).set(node['runtime']['imageFs']['availableBytes'])
                self.gauge('kube_node_fs_imagefs_inodes_free', labels).set(node['runtime']['imageFs']['inodesFree'])

            return Status.OK

        except Exception as ex:
            self.logger.error('Unable to scrape metrics from Kubelet Summary API: %s', str(ex))
            sys.exit(Status.CRITICAL)

    def scrape_cadvisor(self, cadvisor_metrics_url, header, cluster_global_labels, api_server_client):
        GAUGE_METRICS = [
            'container_memory_working_set_bytes',
            'container_memory_swap',
        ]

        COUNTER_METRICS = [
            'container_cpu_usage_seconds_total',
            'container_cpu_cfs_throttled_seconds_total',
            'container_network_receive_bytes_total',
            'container_network_transmit_bytes_total',
            'container_network_receive_errors_total',
            'container_network_transmit_errors_total',
            'container_fs_writes_bytes_total',
            'container_fs_reads_bytes_total',
        ]

        try:
            res = requests.get(cadvisor_metrics_url, timeout=20, verify=False, headers=header)
            res.raise_for_status()
            res = res.text

            pods_api_server = api_server_client.list_pod_for_all_namespaces(watch=False)
            pod_labels = {}
            for pod in pods_api_server.items:
                label_list = []
                if pod.metadata.labels:
                    for label_key,label_value in pod.metadata.labels.items():
                        label = f'{label_key}: {label_value}'
                        label_list.append(label)
                    pod_labels[pod.metadata.name] = tuple(label_list)

            for family in text_string_to_metric_families(res):
                for sample in family.samples:
                    sample[1]['container'] = sample[1].pop('container_name', None)
                    sample[1]['pod'] = sample[1].pop('pod_name', None)
                    labels = {**cluster_global_labels, **sample[1]}
                    value = sample[2]
                    if not math.isnan(value):
                        if labels['pod']:
                            if pod_labels.get(labels['pod']) != None:
                                for label in pod_labels[labels['pod']]:
                                    labels['k8s.pod.label'] = label
                                    if sample[0] in COUNTER_METRICS:
                                        self.counter(sample[0], labels).set(value)
                                    elif sample[0] in GAUGE_METRICS:
                                        self.gauge(sample[0], labels).set(value)

            return Status.OK

        except Exception as ex:
            self.logger.error('Unable to scrape metrics from cAdvisor: %s', str(ex))
            sys.exit(Status.CRITICAL)

    def __to_byte(self, mem):
        mem_digits = int(''.join([i for i in mem if i.isdigit()]))
        unit = ''.join([i for i in mem if not i.isdigit()])

        if not unit:
            return mem_digits
        else:
            conversion_table = {
                'k': 1000,
                'ki': 1024,
                'm': 1000000,
                'mi': 1048576,
                'g': 1000000000,
                'gi': 1073741824
            }
            return mem_digits * conversion_table.get(unit.lower())

    def __to_core(self, cpu):
        if 'm' not in cpu:
            return float(cpu)
        else:
            return float(cpu[:-1])/1000

if __name__ == '__main__':
    sys.exit(KubeletPlugin().run())
