#!/usr/bin/env python3

import sys
import pymysql.cursors

from outlyer_plugin import Plugin, Status

GAUGE_METRICS = [
    "Threads_connected",
    "Threads_running",
    "Innodb_buffer_pool_pages_total",
    "Innodb_buffer_pool_pages_free",
]

COUNTER_METRICS = [
    "Table_locks_waited",
    "Bytes_received",
    "Bytes_sent",
    "Connection_errors_accept",
    "Connection_errors_internal",
    "Connection_errors_max_connections",
    "Connection_errors_peer_address",
    "Connection_errors_select",
    "Connection_errors_tcpwrap",
    "Created_tmp_disk_tables",
    "Created_tmp_files",
    "Com_commit",
    "Com_insert",
    "Com_rollback",
    "Com_select",
    "Com_update",
    "Com_delete",
    "Innodb_buffer_pool_read_requests",
    "Innodb_buffer_pool_reads",
    "Innodb_pages_read",
    "Innodb_pages_written",
    "Innodb_row_lock_time",
    "Innodb_row_lock_waits",
    "Select_scan",
    "Slow_queries",
    "Table_locks_waited",
    "Questions",
]


class MySQLPlugin(Plugin):

    def collect(self, _):

        ip = self.get('ip', '127.0.0.1')
        port = int(self.get('port', 3306))
        user = self.get('username', 'root')
        password = self.get('password', 'mysql')

        db = pymysql.connect(
            host=ip,
            port=port,
            user=user,
            passwd=password,
            connect_timeout=10)

        try:
            with db.cursor() as cursor:
                cursor.execute("SHOW GLOBAL STATUS")
                stats = dict(cursor.fetchall())
                labels = {}

                for k in GAUGE_METRICS:
                    if k in stats:
                        val = float(stats[k])
                        self.gauge(f'mysql.{k}', labels).set(val)

                for k in COUNTER_METRICS:
                    if k in stats:
                        val = float(stats[k])
                        self.counter(f'mysql.{k}', labels).set(val)

                return Status.OK

        except (pymysql.err.InternalError, pymysql.err.OperationalError, pymysql.err.NotSupportedError) as e:
            print(f"Privilege error or engine unavailable accessing the INNODB status tables (must grant PROCESS): {e}")
            return Status.UNKNOWN
        except Exception as err:
            print(f"Excpetion while reading database: {err}")
            return Status.UNKNOWN
        finally:
            db.close()


if __name__ == '__main__':
    # To run the collection
    sys.exit(MySQLPlugin().run())
