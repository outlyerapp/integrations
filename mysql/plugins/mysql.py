#!/usr/bin/env python3

import sys
import pymysql.cursors

from outlyer_plugin import Plugin, Status

GAUGE_METRICS = [
    "Innodb_buffer_pool_pages_dirty",
    "Innodb_data_pending_fsyncs",
    "Innodb_data_pending_reads",
    "Innodb_data_pending_writes",
    "Innodb_os_log_pending_fsyncs",
    "Innodb_os_log_pending_writes",
    "Innodb_page_size",
    "Innodb_num_open_files",
    "Open_files",
    "Open_streams",
    "Open_table_definitions",
    "Open_tables",
    "Threads_connected",
    "Threads_running",
]

COUNTER_METRICS = [
    "Opened_files",
    "Opened_table_definitions",
    "Opened_tables",
    "Table_locks_waited",
    "Table_open_cache_hits",
    "Table_open_cache_misses",
    "Bytes_received",
    "Bytes_sent",
    "Connection_errors_accept",
    "Connection_errors_internal",
    "Connection_errors_max_connections",
    "Connection_errors_peer_address",
    "Connection_errors_select",
    "Connection_errors_tcpwrap",
    "Connections",
    "Created_tmp_disk_tables",
    "Created_tmp_files",
    "Created_tmp_tables",
    "Table_locks_immediate",
    "Table_open_cache_hits",
    "Table_open_cache_misses",
    "Table_open_cache_overflows",
    "Threads_created",
    "Com_commit",
    "Com_insert",
    "Com_rollback",
    "Com_select",
    "Com_update",
    "Com_delete",
    "Created_tmp_disk_tables",
    "Created_tmp_files",
    "Created_tmp_tables",
    "Innodb_buffer_pool_read_requests",
    "Innodb_buffer_pool_reads",
    "Innodb_buffer_pool_write_requests",
    "Innodb_data_fsyncs",
    "Innodb_data_read",
    "Innodb_data_reads",
    "Innodb_data_writes",
    "Innodb_data_written",
    "Innodb_os_log_written",
    "Innodb_pages_created",
    "Innodb_pages_read",
    "Innodb_pages_written",
    "Innodb_row_lock_time",
    "Innodb_row_lock_waits",
    "Innodb_rows_deleted",
    "Innodb_rows_inserted",
    "Innodb_rows_read",
    "Innodb_rows_updated",
    "Opened_tables",
    "Opened_files",
    "Select_full_join",
    "Select_full_range_join",
    "Select_range",
    "Select_range_check",
    "Select_scan",
    "Slow_launch_threads",
    "Slow_queries",
    "Sort_merge_passes",
    "Sort_range",
    "Sort_rows",
    "Sort_scan",
    "Table_locks_waited",
    "Table_open_cache_hits",
    "Table_open_cache_misses",
    "Table_open_cache_overflows",
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