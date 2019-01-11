#!/usr/bin/env python3

from outlyer_plugin import Status, Plugin
from typing import Dict, Any
import pymongo
import pymongo.errors
import re
import time
import sys


RATE_METRICS = [
    "network.bytes_in",
    "network.bytes_out",
    "network.num_requests",
    "opcounters.delete",
    "opcounters.getmore",
    "opcounters.insert",
    "opcounters.query",
    "opcounters.update",
]

GAUGE_METRICS = [
    "connections.available",
    "connections.current",
    "collections",
    "collections",
    "avg_obj_size",
    "objects",
    "data_size",
    "storage_size",
    "indexes",
    "index_size",
    "fs_used_size",
    "fs_total_size",
    "uptime",
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

        ip = self.get('ip', '127.0.0.1')
        port = self.get('port', 27017)
        username = self.get('username', None)
        password = self.get('password', None)
        auth_db = self.get('auth_source', None)
        connect_timeout = self.get('connect_timeout', 5000)
        socket_timeout = self.get('socket_timeout', 5000)

        try:
            if username:
                uri = f'mongodb://{username}:{password}@{ip}:{port}/'
                if auth_db:
                    uri += f'?authSource={auth_db}'

                c = pymongo.MongoClient(uri,
                                        serverSelectionTimeoutMS=connect_timeout,
                                        connectTimeoutMS=connect_timeout,
                                        socketTimeoutMS=socket_timeout)
            else:
                c = pymongo.MongoClient(host=ip, port=port,
                                        serverSelectionTimeoutMS=connect_timeout,
                                        connectTimeoutMS=connect_timeout,
                                        socketTimeoutMS=socket_timeout)

            for db_name in c.database_names():
                db = c.get_database(db_name)
                stats = uncamel_dict(db.command('dbstats'))
                for k, v in stats.items():
                    if k in GAUGE_METRICS:
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
