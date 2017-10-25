import logging
import time

import MySQLdb
import _mysql_exceptions
from MySQLdb.constants import CR

from outlyer_agent.collection import Status, Plugin, PluginTarget, DEFAULT_PLUGIN_EXEC

# TODO: add bool parameter showCommandCounts


logger = logging.getLogger(__name__)

RATE_METRICS = [
    "bytes_received",
    "bytes_sent",
    "connection_errors_accept",
    "connection_errors_internal",
    "connection_errors_max_connections",
    "connection_errors_peer_address",
    "connection_errors_select",
    "connection_errors_tcpwrap",
    "connections",
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
    "sort_range",
    "sort_rows",
    "sort_scan",
]

PERCENTAGE_METRICS = [
    ("table_open_cache_ratio", "table_open_cache_hits", "table_open_cache_misses"),
]

GAUGE_METRICS = [
    "open_files",
    "open_streams",
    "open_table_definitions",
    "open_tables",
    "threads_connected",
    "threads_running",
    "innodb_data_pending_fsyncs",
    "innodb_data_pending_reads",
    "innodb_data_pending_writes",
    "innodb_os_log_pending_fsyncs",
    "innodb_os_log_pending_writes",
    "innodb_row_lock_time",
    "innodb_row_lock_time_avg",
    "innodb_row_lock_time_max",
    "innodb_row_lock_waits",
    "innodb_num_open_files",
    "open_tables",
]

COUNTER_METRICS = [
    "opened_files",
    "opened_table_definitions",
    "opened_tables",
    "table_locks_waited",
]


class MysqlPlugin(Plugin):
    def __init__(self, name, deployments, host, executor=DEFAULT_PLUGIN_EXEC):
        super().__init__(name, deployments, host, executor)
        self.last_collect = None

    def collect(self, target: PluginTarget):

        time_now = time.monotonic()

        try:
            conn = MySQLdb.connect(host=target.get('host', '127.0.0.1'),
                                   port=target.get('port', 3306),
                                   user=target.get('username', 'root'),
                                   passwd=target.get('passwd', 'mysql'),
                                   db=target.get('database', 'mysql'))  # type: MySQLdb.Connection

            cursor = conn.cursor()
            stats = dict()
            cursor.execute('SHOW GLOBAL STATUS')
            for row in cursor:
                stats[row[0].lower()] = row[1]
            cursor.close()

            for k in RATE_METRICS:
                if self.last_collect:
                    elapsed_sec = time_now - self.last_collect
                    per_second = (float(stats[k]) - target.counter(k).get()) / elapsed_sec
                    target.gauge(k + '_per_sec').set(per_second)
                target.counter(k).set(float(stats[k]))

            for k, top, bottom in PERCENTAGE_METRICS:
                percent = 0.0
                if float(stats[bottom]) > 0:
                    percent = float(stats[top]) / float(stats[bottom]) * 100.0
                target.counter(top).set(float(stats[top]))
                target.counter(bottom).set(float(stats[bottom]))
                target.gauge(k, {'uom': '%'}).set(percent)

            for k in GAUGE_METRICS:
                target.gauge(k).set(float(stats[k]))

            for k in COUNTER_METRICS:
                target.counter(k).set(float(stats[k]))

            self.last_collect = time_now
            return Status.OK

        except _mysql_exceptions.MySQLError as ex:

            if ex.args[0] >= CR.ERROR_FIRST:
                logger.error('Unable to connect to MySQL: ' + ex.args[1])
                self.last_collect = None
                return Status.CRITICAL
            else:
                logger.error('Unable to collect from MySQL: ' + ex.args[1])
                self.last_collect = None
                return Status.UNKNOWN

        except Exception as ex:
            logger.exception('Error in plugin', exc_info=ex)

            self.last_collect = None
            return Status.UNKNOWN
