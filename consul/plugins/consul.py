#!/usr/bin/env python3

"""
 Consul check aligned with Promtheus exporter metrics: https://github.com/prometheus/consul_exporter
"""

import sys, requests

from outlyer_plugin import Plugin, Status


class ConsulPlugin(Plugin):

    def collect(self, _):

        try:

            local_agent = self.__get_agent_config()

            # How many peers (servers) are in the Raft cluster.
            peers = self.__consul_request('/v1/status/peers')
            if peers:
                self.gauge("consul_raft_peers", {}).set(len(peers))
            else:
                self.gauge("consul_raft_peers", {}).set(0)

            # Does Raft cluster have a leader (according to this node).
            if not local_agent['leader_url']:
                self.gauge("consul_raft_leader", {}).set(0)
            else:
                self.gauge("consul_raft_leader", {}).set(1)

            # How many members are in the cluster.
            nodes = self.__consul_request('/v1/catalog/nodes')
            self.gauge("consul_serf_lan_members", {}).set(len(nodes))

            # How many services are in the cluster.
            services = self.__consul_request('/v1/catalog/services')
            self.gauge("consul_catalog_services", {}).set(len(services))

            # Make service checks from health checks for all services in catalog
            health_state = self.__consul_request('/v1/health/state/any')
            # health checks return Status: passing, warning, critical, maintenance
            for check in health_state:

                passing = 0
                warning = 0
                critical = 0
                maintenance = 0

                if check['Status'] == 'passing':
                    passing = 1
                elif check['Status'] == 'warning':
                    warning = 1
                elif check['Status'] == 'critical':
                    critical = 1
                elif check['Status'] == 'maintenance':
                    maintenance = 1

                if check['ServiceID']:
                    # Service Check
                    labels = {'check': check['CheckID'],
                              'node': check['Node'],
                              'service_id': check['ServiceID'],
                              'service_name': check['ServiceName'],
                              'status': ''}
                    labels['status'] = 'passing'
                    self.gauge("consul_health_service_status", labels).set(passing)
                    labels['status'] = 'warning'
                    self.gauge("consul_health_service_status", labels).set(warning)
                    labels['status'] = 'critical'
                    self.gauge("consul_health_service_status", labels).set(critical)
                    labels['status'] = 'maintenance'
                    self.gauge("consul_health_service_status", labels).set(maintenance)
                else:
                    # Node Check
                    labels = {'check': check['CheckID'],
                              'node': check['Node'],
                              'status': ''}
                    labels['status'] = 'passing'
                    self.gauge("consul_health_node_status", labels).set(passing)
                    labels['status'] = 'warning'
                    self.gauge("consul_health_node_status", labels).set(warning)
                    labels['status'] = 'critical'
                    self.gauge("consul_health_node_status", labels).set(critical)
                    labels['status'] = 'maintenance'
                    self.gauge("consul_health_node_status", labels).set(maintenance)

            return Status.OK

        except:
            return Status.CRITICAL

    def __consul_request(self, endpoint):
        """
        Make a request to an endpoint on Consul. Looks up the following check variables
        to override connection settings:

            url: 				The URL to connect to Consul, change to https if using SSL.
                                Defaults to 'http://localhost:8500'
            client_cert_file: 	If using SSL, the public client certificate file
            private_key_file: 	If using SSL, the private key file
            ca_bundle_file: 	If using SSL, a CA bundle file with certificates
            acl_token: 			Access control token to call Consul API if enabled

        :param endpoint:	The endpoint to query, with leading /. i.e. '/v1/agent/self'
        :return: 			Returns the JSON response as json if sucessful
        """
        url = self.get('url', 'http://localhost:8500') + endpoint

        try:
            clientcertfile = self.get('client_cert_file', None)
            privatekeyfile = self.get('private_key_file', None)
            cabundlefile = self.get('ca_bundle_file', None)
            acl_token = self.get('acl_token', None)

            headers = {}
            if acl_token:
                headers['X-Consul-Token'] = acl_token

            if clientcertfile:
                if privatekeyfile:
                    resp = requests.get(url, cert=(clientcertfile, privatekeyfile), verify=cabundlefile,
                                        headers=headers)
                else:
                    resp = requests.get(url, cert=clientcertfile, verify=cabundlefile, headers=headers)
            else:
                resp = requests.get(url, verify=cabundlefile, headers=headers)

        except requests.exceptions.Timeout:
            raise

        resp.raise_for_status()
        return resp.json()

    def __get_agent_config(self):

        local_agent = {}
        local_agent['local_config'] = self.__consul_request('/v1/agent/self')

        # Member key for consul 0.7.x and up; Config key for older versions
        agent_addr = local_agent['local_config'].get('Member', {}).get('Addr') or \
                     local_agent['local_config'].get('Config', {}).get('AdvertiseAddr')
        agent_port = local_agent['local_config'].get('Member', {}).get('Tags', {}).get('port') or \
                     local_agent['local_config'].get('Config', {}).get('Ports', {}).get('Server')

        local_agent['agent_url'] = "{0}:{1}".format(agent_addr, agent_port)
        local_agent['leader_url'] = self.__consul_request('/v1/status/leader')
        local_agent['is_leader'] = (local_agent['agent_url'] == local_agent['leader_url'])
        local_agent['datacenter'] = local_agent['local_config'].get('Config', {}).get('Datacenter')

        return local_agent


if __name__ == '__main__':
    sys.exit(ConsulPlugin().run())