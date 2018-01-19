#!/usr/bin/env python3

from outlyer_plugin import Status, Plugin
from typing import Dict, Any
import pymongo
import pymongo.errors
import re
import time
import sys

# TODO: add replication stats
# TODO: support authentication
# TODO: add parameter for command metrics (metrics.commands.*.failed|total)
# TODO: MongoClient doesn't seem to be respecting connectTimeoutMS=5000


RATE_METRICS = [
    "network.bytes_in",
    "network.bytes_out",
    "network.num_requests",
    "network.physical_bytes_in",
    "network.physical_bytes_out",
    "opcounters.command",
    "opcounters.delete",
    "opcounters.getmore",
    "opcounters.insert",
    "opcounters.query",
    "opcounters.update",
    "opcounters_repl.command",
    "opcounters_repl.delete",
    "opcounters_repl.getmore",
    "opcounters_repl.insert",
    "opcounters_repl.query",
    "opcounters_repl.update",
    "wired_tiger.block_manager.blocks_read",
    "wired_tiger.block_manager.blocks_written",
    "wired_tiger.block_manager.bytes_read",
    "wired_tiger.block_manager.bytes_written",
    "wired_tiger.block_manager.bytes_written_for_checkpoint",
    "wired_tiger.block_manager.mapped_blocks_read",
    "wired_tiger.block_manager.mapped_bytes_read",
]

GAUGE_METRICS = [
    "connections.available",
    "connections.current",
    "wired_tiger.async.current_work_queue_length",
    "wired_tiger.async.maximum_work_queue_length",
]

COUNTER_METRICS = [
    "connections.total_created",
    "locks._collection.acquire_count.r",
    "locks._database.acquire_count.r",
    "locks._database.acquire_count.w",
    "locks._global.acquire_count.r",
    "locks._global.acquire_count.w",
    "locks._metadata.acquire_count.w",
    "wired_tiger.async.total_allocations",
    "wired_tiger.async.total_compact_calls",
    "wired_tiger.async.total_insert_calls",
    "wired_tiger.async.total_remove_calls",
    "wired_tiger.async.total_search_calls",
    "wired_tiger.async.total_update_calls",
]


def uncamel_name(name: str):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    s3 = s2.translate(str.maketrans(' -', '__', '()'))
    return s3


def uncamel_dict(d: Dict[str, Any]):
    better = {}
    for k, v in d.items():
        better[uncamel_name(k)] = v
    return better


def is_number(val: str):
    try:
        float(val)
        return True
    except ValueError:
        return False


def _recursive_flatten(src: Dict[str, Any], dest: Dict[str, Any], prefix: str):
    prefix = prefix + '.' if prefix != '' else ''
    for k, v in src.items():
        if isinstance(v, dict):
            _recursive_flatten(v, dest, prefix + k)
        else:
            dest[prefix + k] = v
    return dest


def flatten_dict(d: Dict[str, Any]):
    better = {}
    _recursive_flatten(d, better, '')

    return better


class MongoPlugin(Plugin):

    def collect(self, _):

        host = self.get('host', 'localhost')
        port = int(self.get('port', 27017))
        username = self.get('username', None)
        password = self.get('password', None)
        auth_db = self.get('auth_source', None)
        connect_timeout = self.get('connect_timeout', 5000)
        socket_timeout = self.get('socket_timeout', 5000)

        try:
            if username:
                uri = f'mongodb://{username}:{password}@{host}:{port}/'
                if auth_db:
                    uri += f'?authSource={auth_db}'

                self.logger.info('Connecting to MongoDB on %s', uri)
                c = pymongo.MongoClient(uri,
                                        connectTimeoutMS=connect_timeout,
                                        socketTimeoutMS=socket_timeout)
            else:
                self.logger.info('Connecting to MongoDB on %s:%d', host, port)
                c = pymongo.MongoClient(host=host, port=port,
                                        connectTimeoutMS=connect_timeout,
                                        socketTimeoutMS=socket_timeout)

            for db_name in c.database_names():
                db = c.get_database(db_name)
                stats = uncamel_dict(db.command('dbstats'))
                for k, v in stats.items():
                    if is_number(v):
                        self.gauge('mongodb.' + k, {'database': db_name}).set(float(v))

            db = c.get_database('admin')
            stats = uncamel_dict(flatten_dict(db.command('serverStatus')))

            for k in RATE_METRICS:
                try:
                    val = float(stats[k])
                    self.counter('mongodb.' + k).set(val)
                except KeyError:
                    pass

            for k in GAUGE_METRICS:
                try:
                    val = stats[k]
                    self.gauge('mongodb.' + k).set(val)
                except KeyError:
                    pass

            for k in COUNTER_METRICS:
                try:
                    val = stats[k]
                    self.counter('mongodb.' + k).set(val)
                except KeyError:
                    pass

            c.close()
            return Status.OK

        except pymongo.errors.ConnectionFailure as ex:
            self.logger.error('Cannot connect to MongoDB: ' + ex.args[0])
            return Status.CRITICAL

        except pymongo.errors.OperationFailure as ex:
            if ex.details['codeName'] == 'AuthenticationFailed':
                self.logger.error('Error connecting to MongoDB: %s', ex.details['errmsg'])
            else:
                self.logger.error('Error executing MongoDB query: %s', ex)
            return Status.UNKNOWN

        except Exception as ex:
            self.logger.exception('Error in plugin', exc_info=ex)
            return Status.UNKNOWN


if __name__ == '__main__':
    sys.exit(MongoPlugin().run())
