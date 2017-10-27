import time
import requests.exceptions
import icontrol.exceptions

from f5.bigip import ManagementRoot
from f5.bigip.resource import Stats

from outlyer_agent.collection import Status, Plugin, PluginTarget, DEFAULT_PLUGIN_EXEC, Metric

# TODO: get F5 system stats (memory, cpu, etc.)

import urllib3
urllib3.disable_warnings()

POOL_GAUGES = {
    'activeMemberCnt': 'active_member_count',
    'curSessions': 'current_sessions',
    'serverside.curConns': 'current_connections',
    'serverside.maxConns': 'max_connections',
    'connqAll.depth': 'conn_queue_depth'
}

POOL_RATES = {
    'totRequests': 'total_requests',
    'serverside.bitsIn': 'bytes_received',
    'serverside.bitsOut': 'bytes_sent',
    'serverside.pktsIn': 'packets_received',
    'serverside.pktsOut': 'packets_sent',
    'serverside.totConns': 'connections',
}

STATE_MAP = {
    'available': 0.0,
    'unavailable': 1.0,
    'unknown': 2.0
}


class F5Plugin(Plugin):
    def __init__(self, name, deployments, host, logger, executor=DEFAULT_PLUGIN_EXEC):
        super().__init__(name, deployments, host, logger, executor)
        self.last_collect = None

    def collect(self, target: PluginTarget) -> Status:

        time_now = time.monotonic()

        hostname = target.get('host')
        username = target.get('username')
        password = target.get('password')
        if not hostname or not username or not password:
            self.logger.error('Incomplete configuration for F5 LTM plugin')
            return Status.UNKNOWN

        try:
            big_ip = ManagementRoot(hostname, username, password)

            def record_io_stats(prefix, stats, labels: dict) -> None:
                assert len(stats.entries.values()) == 1
                stats = list(stats.entries.values())[0]['nestedStats']['entries']  # type: dict

                for k, v in POOL_GAUGES.items():
                    try:
                        value = stats[k]['value']
                        target.gauge(prefix + v, labels=labels).set(value)
                    except KeyError:
                        pass

                for k, v in POOL_RATES.items():
                    try:
                        new_value = stats[k]['value']
                        if self.last_collect:
                            elapsed = time_now - self.last_collect
                            old_value = target.counter(prefix + v, labels=labels).get()
                            target.gauge(prefix + v + '_per_sec', labels=labels).set((new_value - old_value) / elapsed)
                        target.counter(prefix + v, labels=labels).set(new_value)
                    except KeyError:
                        pass

            def record_availability(prefix, stats, labels: dict) -> None:
                assert len(stats.entries.values()) == 1
                stats = list(stats.entries.values())[0]['nestedStats']['entries']  # type: dict
                state = stats['status.availabilityState']['description']
                state_val = STATE_MAP[state]
                target.gauge(prefix + 'available', labels=labels).set(state_val)

            nodes = big_ip.tm.ltm.nodes.get_collection()
            for node in nodes:
                node_stats = node.stats.load()
                record_io_stats('f5_ltm_node_', node_stats, {'node_name': node.name})
                record_availability('f5_ltm_node_', node_stats, {'node_name': node.name})

            pools = big_ip.tm.ltm.pools.get_collection()
            for pool in pools:
                pool_stats = pool.stats.load()  # type: Stats
                record_io_stats('f5_ltm_pool_', pool_stats, {'pool_name': pool.name})
                record_availability('f5_ltm_pool_', pool_stats, {'pool_name': pool.name})

                members = pool.members_s.get_collection()
                for member in members:
                    member_stats = member.stats.load()
                    record_io_stats('f5_ltm_pool_member_', member_stats, {'pool_name': pool.name,
                                                                          'member_name': member.name})
                    record_availability('f5_ltm_pool_member_', member_stats, {'pool_name': pool.name,
                                                                              'member_name': member.name})

            self.last_collect = time_now
            return Status.OK

        except requests.exceptions.ConnectionError as ex:
            self.logger.error('Error connecting to %s: %s', hostname, ex)
            self.last_collect = None
            return Status.CRITICAL

        except icontrol.exceptions.iControlUnexpectedHTTPError as ex:
            self.logger.error('Unexpected iControl error talking to %s: %s', hostname, ex)
            self.last_collect = None
            return Status.CRITICAL
