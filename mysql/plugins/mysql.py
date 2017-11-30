import time

import MySQLdb
import _mysql_exceptions
from MySQLdb.constants import CR

from outlyer_agent.collection import Status, Plugin, PluginTarget, DEFAULT_PLUGIN_EXEC

# TODO: add bool parameter showCommandCounts


GAUGE_METRICS = [
    "innodb_buffer_pool_pages_dirty",
    "innodb_data_pending_fsyncs",
    "innodb_data_pending_reads",
    "innodb_data_pending_writes",
    "innodb_os_log_pending_fsyncs",
    "innodb_os_log_pending_writes",
    "innodb_page_size",
    "innodb_num_open_files",
    "ongoing_anonymous_transaction_count",
    "open_files",
    "open_streams",
    "open_table_definitions",
    "open_tables",
    "threads_connected",
    "threads_running",
]

COUNTER_METRICS = [
    "opened_files",
    "opened_table_definitions",
    "opened_tables",
    "table_locks_waited",
    "table_open_cache_hits",
    "table_open_cache_misses",
    "bytes_received",
    "bytes_sent",
    "connection_errors_accept",
    "connection_errors_internal",
    "connection_errors_max_connections",
    "connection_errors_peer_address",
    "connection_errors_select",
    "connection_errors_tcpwrap",
    "connections",
    "created_tmp_disk_tables",
    "created_tmp_files",
    "created_tmp_tables",
    "table_locks_immediate",
    "table_open_cache_hits",
    "table_open_cache_misses",
    "table_open_cache_overflows",
    "threads_created",
    "com_commit",
    "com_insert",
    "com_rollback",
    "com_select",
    "com_update",
    "com_delete",
    "created_tmp_disk_tables",
    "created_tmp_files",
    "created_tmp_tables",
    "innodb_buffer_pool_read_requests",
    "innodb_buffer_pool_reads",
    "innodb_buffer_pool_write_requests",
    "innodb_data_fsyncs",
    "innodb_data_read",
    "innodb_data_reads",
    "innodb_data_writes",
    "innodb_data_written",
    "innodb_os_log_written",
    "innodb_pages_created",
    "innodb_pages_read",
    "innodb_pages_written",
    "innodb_row_lock_time",
    "innodb_row_lock_waits",
    "innodb_rows_deleted",
    "innodb_rows_inserted",
    "innodb_rows_read",
    "innodb_rows_updated",
    "opened_tables",
    "opened_files",
    "select_full_join",
    "select_full_range_join",
    "select_range",
    "select_range_check",
    "select_scan",
    "slow_launch_threads",
    "slow_queries",
    "sort_merge_passes",
    "sort_range",
    "sort_rows",
    "sort_scan",
    "table_locks_waited",
    "table_open_cache_hits",
    "table_open_cache_misses",
    "table_open_cache_overflows",
]


class MysqlPlugin(Plugin):

    def collect(self, target: PluginTarget):

        host = target.get('host', '127.0.0.1')
        port = target.get('port', 3306)
        user = target.get('username', 'root')
        password = target.get('password', 'mysql')
        db = target.get('database', 'mysql')

        try:
            conn = MySQLdb.connect(host=host, port=port, user=user, password=password, db=db)

            cursor = conn.cursor()
            stats = dict()
            cursor.execute('SHOW GLOBAL STATUS')
            for row in cursor:
                stats[row[0].lower()] = row[1]
            cursor.close()

            labels = {
                'host': host,
                'port': str(port),
                'username': user,
                'db': db
            }

            for k in GAUGE_METRICS:
                try:
                    val = float(stats[k])
                    target.gauge(f'mysql.{k}', labels).set(val)
                except ValueError:
                    pass

            for k in COUNTER_METRICS:
                try:
                    val = float(stats[k])
                    target.counter(f'mysql.{k}', labels).set(val)
                except ValueError:
                    pass

            return Status.OK

        except _mysql_exceptions.MySQLError as ex:

            if ex.args[0] >= CR.ERROR_FIRST:
                self.logger.error('Unable to connect to MySQL: ' + ex.args[1])
                return Status.CRITICAL
            else:
                self.logger.error('Unable to collect from MySQL: ' + ex.args[1])
                return Status.UNKNOWN

        except Exception as ex:
            self.logger.exception('Error in plugin', exc_info=ex)
            return Status.UNKNOWN
