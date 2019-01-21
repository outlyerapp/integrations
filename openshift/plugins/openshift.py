#!/usr/bin/env python3

"""
Scrapes OpenShift Kubernetes APIs via API Server
"""

import sys
from outlyer_plugin import Plugin, Status
import requests

requests.packages.urllib3.disable_warnings()


class OpenShiftPlugin(Plugin):

    def collect(self, _) -> Status:

        try:
            # Creates cluster global labels
            cluster_name = self.get('k8s.cluster')
            cluster_global_labels = {'k8s.cluster': 'unknown'}
            if cluster_name:
                cluster_global_labels['k8s.cluster'] = cluster_name

            users = self.__get_data('/apis/user.openshift.io/v1/users')
            for user in users['items']:
                labels = {**cluster_global_labels}
                labels['username'] = user['metadata']['name']
                self.gauge('openshift.users', labels).set(1)

            routes = self.__get_data('/apis/route.openshift.io/v1/routes')
            for route in routes['items']:
                labels = {**cluster_global_labels}
                labels['route.name'] = route['metadata']['name']
                labels['namespace'] = route['metadata']['namespace']
                labels['route.host'] = route['spec']['host']
                labels['to.kind'] = route['spec']['to']['kind']
                labels['to.name'] = route['spec']['to']['name']
                labels['to.weight'] = str(route['spec']['to']['weight'])
                for ingress in route['status']['ingress']:
                    labels['ingress.host'] = ingress['host']
                    for condition in ingress['conditions']:
                        labels['ingress.type'] = condition['type']
                        labels['ingress.status'] = condition['status']
                        self.gauge('openshift.routes', labels).set(1)

            cluster_resource_quotas = self.__get_data('/apis/quota.openshift.io/v1/clusterresourcequotas')
            for cluster_quota in cluster_resource_quotas['items']:
                labels = {**cluster_global_labels}
                labels['cluster_quota_name'] = cluster_quota['metadata']['name']

                limits = cluster_quota['status']['total']['hard']
                if limits.get('cpu'):
                    self.gauge('openshift.clusterquota.cpu.limit', labels).set(self.__to_core(limits.get('cpu')))
                if limits.get('memory'):
                    self.gauge('openshift.clusterquota.memory.limit', labels).set(self.__to_byte(limits.get('memory')))
                if limits.get('pods'):
                    self.gauge('openshift.clusterquota.pods.limit', labels).set(float(limits.get('pods')))
                if limits.get('services'):
                    self.gauge('openshift.clusterquota.services.limit', labels).set(float(limits.get('services')))
                if limits.get('services.nodeports'):
                    self.gauge('openshift.clusterquota.services.nodeports.limit', labels).set(float(limits.get('services.nodeports')))
                if limits.get('services.loadbalancers'):
                    self.gauge('openshift.clusterquota.services.loadbalancers.limit', labels).set(float(limits.get('services.loadbalancers')))
                if limits.get('secrets'):
                    self.gauge('openshift.clusterquota.secrets.limit', labels).set(float(limits.get('secrets')))
                if limits.get('configmaps'):
                    self.gauge('openshift.clusterquota.configmaps.limit', labels).set(float(limits.get('configmaps')))
                if limits.get('persistentvolumeclaims'):
                    self.gauge('openshift.clusterquota.persistentvolumeclaims.limit', labels).set(float(limits.get('persistentvolumeclaims')))

                used = cluster_quota['status']['total']['used']
                if limits.get('cpu'):
                    self.gauge('openshift.clusterquota.cpu.used', labels).set(self.__to_core(used.get('cpu')))
                if limits.get('memory'):
                    self.gauge('openshift.clusterquota.memory.used', labels).set(self.__to_byte(used.get('memory')))
                if limits.get('pods'):
                    self.gauge('openshift.clusterquota.pods.used', labels).set(float(used.get('pods')))
                if limits.get('services'):
                    self.gauge('openshift.clusterquota.services.used', labels).set(float(used.get('services')))
                if limits.get('services.nodeports'):
                    self.gauge('openshift.clusterquota.services.nodeports.used', labels).set(float(used.get('services.nodeports')))
                if limits.get('services.loadbalancers'):
                    self.gauge('openshift.clusterquota.services.loadbalancers.used', labels).set(float(used.get('services.loadbalancers')))
                if limits.get('secrets'):
                    self.gauge('openshift.clusterquota.secrets.used', labels).set(float(used.get('secrets')))
                if limits.get('configmaps'):
                    self.gauge('openshift.clusterquota.configmaps.used', labels).set(float(used.get('configmaps')))
                if limits.get('persistentvolumeclaims'):
                    self.gauge('openshift.clusterquota.persistentvolumeclaims.used', labels).set(float(used.get('persistentvolumeclaims')))

                namespaces = cluster_quota['status'].get('namespaces')
                if namespaces:
                    for namespace in namespaces:
                        labels = {**cluster_global_labels}
                        labels['cluster_quota_name'] = cluster_quota['metadata']['name']
                        labels['namespace'] = namespace['namespace']

                        limits = namespace['status']['hard']
                        if limits.get('cpu'):
                            self.gauge('openshift.appliedclusterquota.cpu.limit', labels).set(self.__to_core(limits.get('cpu')))
                        if limits.get('memory'):
                            self.gauge('openshift.appliedclusterquota.memory.limit', labels).set(self.__to_byte(limits.get('memory')))
                        if limits.get('pods'):
                            self.gauge('openshift.appliedclusterquota.pods.limit', labels).set(float(limits.get('pods')))
                        if limits.get('services'):
                            self.gauge('openshift.appliedclusterquota.services.limit', labels).set(float(limits.get('services')))
                        if limits.get('services.nodeports'):
                            self.gauge('openshift.appliedclusterquota.services.nodeports.limit', labels).set(float(limits.get('services.nodeports')))
                        if limits.get('services.loadbalancers'):
                            self.gauge('openshift.appliedclusterquota.services.loadbalancers.limit', labels).set(float(limits.get('services.loadbalancers')))
                        if limits.get('secrets'):
                            self.gauge('openshift.appliedclusterquota.secrets.limit', labels).set(float(limits.get('secrets')))
                        if limits.get('configmaps'):
                            self.gauge('openshift.appliedclusterquota.configmaps.limit', labels).set(float(limits.get('configmaps')))
                        if limits.get('persistentvolumeclaims'):
                            self.gauge('openshift.appliedclusterquota.persistentvolumeclaims.limit', labels).set(float(limits.get('persistentvolumeclaims')))

                        used = namespace['status']['used']
                        if limits.get('cpu'):
                            self.gauge('openshift.appliedclusterquota.cpu.used', labels).set(self.__to_core(used.get('cpu')))
                        if limits.get('memory'):
                            self.gauge('openshift.appliedclusterquota.memory.used', labels).set(self.__to_byte(used.get('memory')))
                        if limits.get('pods'):
                            self.gauge('openshift.appliedclusterquota.pods.used', labels).set(float(used.get('pods')))
                        if limits.get('services'):
                            self.gauge('openshift.appliedclusterquota.services.used', labels).set(float(used.get('services')))
                        if limits.get('services.nodeports'):
                            self.gauge('openshift.appliedclusterquota.services.nodeports.used', labels).set(float(used.get('services.nodeports')))
                        if limits.get('services.loadbalancers'):
                            self.gauge('openshift.appliedclusterquota.services.loadbalancers.used', labels).set(float(used.get('services.loadbalancers')))
                        if limits.get('secrets'):
                            self.gauge('openshift.appliedclusterquota.secrets.used', labels).set(float(used.get('secrets')))
                        if limits.get('configmaps'):
                            self.gauge('openshift.appliedclusterquota.configmaps.used', labels).set(float(used.get('configmaps')))
                        if limits.get('persistentvolumeclaims'):
                            self.gauge('openshift.appliedclusterquota.persistentvolumeclaims.used', labels).set(float(used.get('persistentvolumeclaims'))) 

            return Status.OK

        except Exception as ex:
            self.logger.error('Unable to scrape OpenShift metrics API Server: %s', str(ex))
            sys.exit(Status.CRITICAL)

    def __get_data(self, endpoint):
        TOKEN_PATH = self.get('token_path', '/var/run/secrets/kubernetes.io/serviceaccount/token')
        API_SERVER = self.get('api_server', 'kubernetes.default')
        TIMEOUT = self.get('timeout', 20)

        with open(TOKEN_PATH) as token_file: 
            token = token_file.read()
            header = {'authorization': 'bearer ' + token}

        resp = requests.get(
          f'https://{API_SERVER}:443{endpoint}',
          timeout=TIMEOUT,
          verify=False,
          headers=header
        )

        resp.raise_for_status()
        return resp.json()

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
    sys.exit(OpenShiftPlugin().run())
