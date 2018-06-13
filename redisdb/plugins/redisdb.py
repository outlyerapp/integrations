#!/usr/bin/env python3

import re
from outlyer_plugin import Status, Plugin
from typing import Dict, Any
import redis
import redis.exceptions
import sys


GAUGE_METRICS = [
    'connected_slaves',
    'uptime_in_seconds',
    'total_connections_received',
    'total_commands_processed',
    'rejected_connections',
    'expired_keys',
    'evicted_keys',
    'keyspace_hits',
    'keyspace_misses',
    'pubsub_channels',
    'used_cpu_sys',
    'used_cpu_user',
    'connected_clients',
    'blocked_clients',
    'used_memory',
    'mem_fragmentation_ratio',
    'instantaneous_ops_per_sec',
    'instantaneous_input_kbps',
    'instantaneous_output_kbps',
]


def split_uom(val):
    if isinstance(val, str):
        m = re.match(r'([-0-9.]*)(.*)', val)
        if m:
            return float(m.group(1)), {'uom': m.group(2)}
        else:
            return float(val), {}
    else:
        return float(val), {}


class RedisPlugin(Plugin):

    def collect(self, _):

        def uom(k: str) -> dict:
            if k.endswith('_time_sec'):
                return {'uom': 'sec'}
            elif k.endswith('_kbps'):
                return {'uom': 'kbps'}
            elif k.endswith('_perc'):
                return {'uom': '%'}
            else:
                return {}

        try:
            r = redis.StrictRedis(host=self.get('ip', '127.0.0.1'),
                                  port=self.get('port', 6379),
                                  password=self.get('password', None))

            output = r.info()  # type: Dict[str, Any]

            for key in GAUGE_METRICS:
                if key in output:
                    val, labels = split_uom(output[key])
                    labels.update(uom(key))
                    self.gauge('redis_' + key, labels).set(val)

            for key in output.keys():
                if key.startswith('db'):
                    for db_key, db_val in output[key].items():
                        val, labels = split_uom(output[key][db_key])
                        labels.update(uom(key))
                        labels['database'] = key
                        self.gauge('redis_' + db_key, labels).set(val)

            return Status.OK

        except redis.exceptions.ConnectionError as ex:
            self.logger.error('Unable to connect to Redis: ' + ex.args[0])
            return Status.CRITICAL

        except redis.exceptions.ResponseError as ex:
            self.logger.error('Unexpected response from Redis server: ' + ex.args[0])
            return Status.CRITICAL


if __name__ == '__main__':
  # To run the collection
  sys.exit(RedisPlugin().run())
