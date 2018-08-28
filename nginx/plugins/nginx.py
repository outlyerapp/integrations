#!/usr/bin/env python3

import re
import os
import sys
import psutil
import requests
import requests.exceptions
from datetime import datetime
import tzlocal
from outlyer_plugin import Plugin, Status


class NginxPlugin(Plugin):

    def collect(self, _):
        is_nginx_plus = self.get('nginx_plus', False)
        
        if is_nginx_plus == 'True':
            self.__collect_nginx_plus()
        else:
            self.__collect_nginx_open_source()

        self.__collect_process_metrics()
        return Status.OK


    def __collect_nginx_plus(self):
        """
        Collect metrics from Nginx plus (module: ngx_http_status_module)
        """
        try:
            # Connection metrics
            res = self.__get_nginx_plus_data("/connections")
            self.gauge('nginx_plus.connections_accepted_total').set(res['accepted'])
            self.gauge('nginx_plus.connections_dropped_total').set(res['dropped'])
            self.counter('nginx_plus.connections_dropped_per_sec').set(res['dropped'])
            self.gauge('nginx_plus.connections_active_current').set(res['active'])
            self.gauge('nginx_plus.connections_idle_current').set(res['idle'])

            # Request Metrics
            res = self.__get_nginx_plus_data("/http/requests")
            self.gauge('nginx_plus.requests_current').set(res['current'])
            self.gauge('nginx_plus.requests_total').set(res['total'])
            self.counter('nginx_plus.requests_per_sec').set(res['total'])

            # SSL metrics
            res = self.__get_nginx_plus_data("/ssl")
            self.gauge('nginx_plus.ssl_handshakes').set(res['handshakes'])
            self.gauge('nginx_plus.ssl_handshakes_failed').set(res['handshakes_failed'])
            self.gauge('nginx_plus.ssl_session_reuses').set(res['session_reuses'])
            
            # Server Zone metrics
            res = self.__get_nginx_plus_data('/http/server_zones')
            for server_zone_name, server_zone in res.items():
                labels = {'server_zone': server_zone_name}
                responses = server_zone['responses']
                self.gauge('nginx_plus.server_zone_requests', labels).set(server_zone['requests'])
                self.gauge('nginx_plus.server_zone_responses_1xx', labels).set(responses['1xx'])
                self.gauge('nginx_plus.server_zone_responses_2xx', labels).set(responses['2xx'])
                self.gauge('nginx_plus.server_zone_responses_3xx', labels).set(responses['3xx'])
                self.gauge('nginx_plus.server_zone_responses_4xx', labels).set(responses['4xx'])
                self.gauge('nginx_plus.server_zone_responses_5xx', labels).set(responses['5xx'])
                self.gauge('nginx_plus.server_zone_responses_total', labels).set(responses['total'])
                self.counter('nginx_plus.server_zone_requests_per_sec', labels).set(server_zone['requests'])
                self.counter('nginx_plus.server_zone_responses_1xx_per_sec', labels).set(responses['1xx'])
                self.counter('nginx_plus.server_zone_responses_2xx_per_sec', labels).set(responses['2xx'])
                self.counter('nginx_plus.server_zone_responses_3xx_per_sec', labels).set(responses['3xx'])
                self.counter('nginx_plus.server_zone_responses_4xx_per_sec', labels).set(responses['4xx'])
                self.counter('nginx_plus.server_zone_responses_5xx_per_sec', labels).set(responses['5xx'])
                self.counter('nginx_plus.server_zone_responses_total_per_sec', labels).set(responses['total'])
                
            # Upstream metrics
            res = self.__get_nginx_plus_data("/http/upstreams")
            self.gauge('nginx_plus.upstream_count').set(len(res.items()))
            for upstream_name, upstream in res.items():
                labels = {'upstream': upstream_name}
                for peer in upstream['peers']:
                    labels.update({'peer': peer['name']})
                    self.gauge('nginx_plus.upstream_peer_id', labels).set(peer['id'])
                    self.gauge('nginx_plus.upstream_peer_weight', labels).set(peer['weight'])
                    self.gauge('nginx_plus.upstream_peer_active', labels).set(peer['active'])
                    self.gauge('nginx_plus.upstream_peer_requests', labels).set(peer['requests'])
                    self.gauge('nginx_plus.upstream_peer_responses_1xx', labels).set(peer['responses']['1xx'])
                    self.gauge('nginx_plus.upstream_peer_responses_2xx', labels).set(peer['responses']['2xx'])
                    self.gauge('nginx_plus.upstream_peer_responses_3xx', labels).set(peer['responses']['3xx'])
                    self.gauge('nginx_plus.upstream_peer_responses_4xx', labels).set(peer['responses']['4xx'])
                    self.gauge('nginx_plus.upstream_peer_responses_5xx', labels).set(peer['responses']['5xx'])
                    self.gauge('nginx_plus.upstream_peer_responses_total', labels).set(peer['responses']['total'])
                    self.counter('nginx_plus.upstream_peer_requests_per_sec', labels).set(peer['requests'])
                    self.counter('nginx_plus.upstream_peer_responses_1xx_per_sec', labels).set(peer['responses']['1xx'])
                    self.counter('nginx_plus.upstream_peer_responses_2xx_per_sec', labels).set(peer['responses']['2xx'])
                    self.counter('nginx_plus.upstream_peer_responses_3xx_per_sec', labels).set(peer['responses']['3xx'])
                    self.counter('nginx_plus.upstream_peer_responses_4xx_per_sec', labels).set(peer['responses']['4xx'])
                    self.counter('nginx_plus.upstream_peer_responses_5xx_per_sec', labels).set(peer['responses']['5xx'])
                    self.counter('nginx_plus.upstream_peer_responses_total_per_sec', labels).set(peer['responses']['total'])
                    self.gauge('nginx_plus.upstream_peer_sent', labels).set(peer['sent'])
                    self.gauge('nginx_plus.upstream_peer_received', labels).set(peer['received'])
                    self.gauge('nginx_plus.upstream_peer_fails', labels).set(peer['fails'])
                    self.gauge('nginx_plus.upstream_peer_unavailable', labels).set(peer['unavail'])
                    self.gauge('nginx_plus.upstream_peer_health_checks_checks', labels).set(peer['health_checks']['checks'])
                    self.gauge('nginx_plus.upstream_peer_health_checks_fails', labels).set(peer['health_checks']['fails'])
                    self.gauge('nginx_plus.upstream_peer_health_checks_unhealthy', labels).set(peer['health_checks']['unhealthy'])
                    last_passed = peer['health_checks'].get('last_passed')
                    
                    if last_passed == False:
                        self.gauge('nginx_plus.upstream_peer_health_checks_last_passed', labels).set(1)
                    elif last_passed == True:
                        self.gauge('nginx_plus.upstream_peer_health_checks_last_passed', labels).set(0)

                    # Collect peer state
                    up = 0
                    draining = 0
                    down = 0
                    unavail = 0
                    checking = 0
                    unhealthy = 0

                    if peer['state'] == 'up':
                        up = 1
                    elif peer['state'] == 'draining':
                        draining = 1
                    elif peer['state'] == 'down':
                        down = 1
                    elif peer['state'] == 'unavail':
                        unavail = 1
                    elif peer['state'] == 'checking':
                        checking = 1
                    elif peer['state'] == 'unhealthy':
                        unhealthy = 1

                    labels.update({"state": "up"})
                    self.gauge('nginx_plus.upstream_peer_state', labels).set(up)
                    labels.update({"state": "draining"})
                    self.gauge('nginx_plus.upstream_peer_state', labels).set(draining)
                    labels.update({"state": "down"})
                    self.gauge('nginx_plus.upstream_peer_state', labels).set(down)
                    labels.update({"state": "unavail"})
                    self.gauge('nginx_plus.upstream_peer_state', labels).set(unavail)
                    labels.update({"state": "checking"})
                    self.gauge('nginx_plus.upstream_peer_state', labels).set(checking)
                    labels.update({"state": "unhealthy"})
                    self.gauge('nginx_plus.upstream_peer_state', labels).set(unhealthy)

        except requests.exceptions.HTTPError as ex:
            self.logger.error('Unable to connect to Nginx Plus server: ' + ex.args[0])
            self.last_collect = None
            sys.exit(2)

        except Exception as ex:
            self.logger.exception('Error in plugin', exc_info=ex)
            self.last_collect = None
            sys.exit(2)


    def __get_nginx_plus_data(self, endpoint):
        url = self.get('url_nginx_plus_api', 'http://localhost/api/3')
        response = requests.get(url+endpoint)
        response.raise_for_status()
        return response.json()


    def __collect_process_metrics(self):
        """
        Collect metrics from Nginx process
        """
        master_count = 0
        worker_count = 0

        for proc in psutil.process_iter():
            try:
                arg0 = proc.cmdline()[0]
                if 'nginx: master process' in arg0:
                    master_count += 1
                elif 'nginx: worker process' in arg0:
                    worker_count += 1
            except ProcessLookupError:
                pass
            except psutil.AccessDenied:
                pass
            except psutil.ZombieProcess:
                pass
            except IndexError:
                pass
        self.gauge('nginx.master_proc_count').set(master_count)
        self.gauge('nginx.worker_proc_count').set(worker_count)


    def __collect_nginx_open_source(self):
        """
        Collect metrics from open source Nginx (module: ngx_http_stub_status_module)
        """
        url = self.get('url_nginx_status', 'http://localhost/nginx_status')
        if not url:
            self.logger.error('Nginx server status URL not specified in configuration file')
            sys.exit(2)

        try:
            response = requests.get(url)
            response.raise_for_status()

            text = response.content.decode('utf-8')

            m = re.search(r'Active connections:\s+(\d+)', text)
            if m:
                active = int(m.group(1))
                self.gauge('nginx.connections_active').set(active)

            m = re.search(r'server accepts handled requests\n\s+(\d+)\s+(\d+)\s+(\d+)', text)
            if m:
                accepted = int(m.group(1))
                handled = int(m.group(2))
                total = int(m.group(3))
                self.gauge('nginx.connections_accepted').set(accepted)
                self.gauge('nginx.connections_handled').set(handled)
                self.gauge('nginx.connections_dropped_total').set(accepted - handled)
                self.counter('nginx.connections_dropped_per_sec').set(accepted - handled)
                self.gauge('nginx.requests_total').set(total)
                self.counter('nginx.requests_per_sec').set(total)

            m = re.search(r'Reading:\s+(\d+)\s+Writing:\s+(\d+)\s+Waiting:\s+(\d+)', text)
            if m:
                reading = int(m.group(1))
                writing = int(m.group(2))
                waiting = int(m.group(3))
                self.gauge('nginx.connections_reading').set(reading)
                self.gauge('nginx.connections_writing').set(writing)
                self.gauge('nginx.connections_waiting').set(waiting)

        except requests.exceptions.RequestException as ex:
            self.logger.error('Unable to connect to Nginx server: ' + str(ex))
            sys.exit(2)

        except Exception as ex:
            self.logger.exception('Error in plugin', exc_info=ex)
            sys.exit(2)


if __name__ == '__main__':
    sys.exit(NginxPlugin().run())
