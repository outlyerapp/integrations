#!/usr/bin/env python3

import re
import sys

from typing import Sequence

import psycopg2
import psycopg2.errorcodes

from outlyer_plugin import Plugin, Status


# TODO: replication stats


# noinspection SqlResolve,SqlDialectInspection,SqlNoDataSourceInspection
class PostgreSQLPlugin(Plugin):


    def collect(self, _) -> Status:

        self.host = self.get('host', 'localhost')
        self.port = self.get('port', 5432)
        self.dbname = self.get('dbname', 'postgres')
        self.user = self.get('username', None)
        self.password = self.get('password', None)

        try:
            self.conn = psycopg2.connect(self.dsn)
            self.cursor = self.conn.cursor()

            pg_ver = self.pg_version()

            self.pg_connection_count(self)
            self.pg_activity(pg_ver, self)
            self.pg_lock_stats(self)
            self.pg_bgwriter_stats(self)
            self.pg_db_stats(self)

            if self.get('table_stats', False):
                self.pg_table_stats(self)
                self.pg_table_io_stats(self)

            if self.get('index_stats', False):
                self.pg_index_stats(self)
                self.pg_index_io_stats(self)

            self.cursor.close()

        except psycopg2.OperationalError as ex:
            print(ex)
            self.logger.error('Unable to connect to PostgreSQL: %s', str(ex))
            return Status.CRITICAL

        except psycopg2.ProgrammingError as ex:
            print(ex)
            self.logger.error('Error executing PostgreSQL plugin: %s', str(ex))
            return Status.UNKNOWN

        return Status.OK

    @property
    def dsn(self) -> str:
        pg_dsn = f'host={self.host} port={self.port} dbname={self.dbname}'
        if self.user:
            pg_dsn += f' user={self.user}'
        if self.password:
            pg_dsn += f' password={self.password}'

        return pg_dsn

    def fetchall(self, sql: str):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def pg_version(self) -> float:
        r = self.fetchall('select version();')[0][0]
        ver_match = re.match(r'^PostgreSQL (?P<ver>\d+\.\d+)', r)
        return float(ver_match.group('ver'))

    def pg_connection_count(self, _) -> None:
        self.logger.info('fetching PG connection count')
        r = self.fetchall('SELECT sum(numbackends) FROM pg_stat_database;')
        self.gauge('postgres.connections').set(float(r[0][0]))

    def pg_activity(self, pg_ver: float, _) -> None:
        self.logger.info('fetching PG activity stats')
        # single session state query avoids multiple scans of pg_stat_activity
        # state is a different column name in postgres 9.2, previous versions will have to update this query accordingly
        if pg_ver >= 9.6:
            q_activity = '''
            SELECT state, (CASE wait_event WHEN NULL THEN FALSE ELSE TRUE END) AS waiting,
                coalesce(extract(EPOCH FROM current_timestamp - xact_start)::INT, 0),
                coalesce(extract(EPOCH FROM current_timestamp - query_start)::INT, 0)
            FROM pg_stat_activity
            '''
        else:
            q_activity = '''
            SELECT state, waiting,
                coalesce(extract(EPOCH FROM current_timestamp - xact_start)::INT, 0),
                coalesce(extract(EPOCH FROM current_timestamp - query_start)::INT, 0)
            FROM pg_stat_activity
            '''

        results = self.fetchall(q_activity)

        active_results = []
        active_count = self.gauge('postgres.sessions.active').set(0)
        idle_count = self.gauge('postgres.sessions.idle').set(0)
        idle_in_txn_count = self.gauge('postgres.sessions.idle_in_transaction').set(0)
        waiting_count = self.gauge('postgres.sessions.waiting').set(0)

        for state, waiting, xact_start_sec, query_start_sec in results:
            if state == 'active':
                active_count.inc()
                # build a list of query start times where query is active
                active_results.append(query_start_sec)
            if state == 'idle':
                idle_count.inc()
            if state == 'idle in transaction':
                idle_in_txn_count.inc()
            if waiting:
                waiting_count.inc()

        # determine longest transaction in seconds
        sorted_by_xact = sorted(results, key=lambda tup: tup[2], reverse=True)
        self.gauge('postgres.sessions.longest_transaction', {'uom': 'seconds'}).set((sorted_by_xact[0])[2])

        # determine longest active query in seconds
        sorted_by_query = sorted(active_results, reverse=True)
        self.gauge('postgres.sessions.longest_query', {'uom': 'seconds'}).set(sorted_by_query[0])

    def pg_lock_stats(self, _) -> None:
        self.logger.info('fetching PG lock stats')

        results = self.fetchall('SELECT mode, locktype FROM pg_locks')

        access_exclusive = self.gauge('postgres.locks.accessexclusive').set(0)
        other_exclusive = self.gauge('postgres.locks.otherexclusive').set(0)
        shared = self.gauge('postgres.locks.shared').set(0)

        for mode, lock_type in results:
            if mode == 'AccessExclusiveLock' and lock_type != 'virtualxid':
                access_exclusive.inc()
            if mode != 'AccessExclusiveLock' and lock_type != 'virtualxid':
                if 'Exclusive' in mode:
                    other_exclusive.inc()
            if 'Share' in mode and lock_type != 'virtualxid':
                shared.inc()

    def pg_bgwriter_stats(self, _) -> None:
        self.logger.info('fetching PG bgwriter stats')
        self.pg_run_metric_query('''
          SELECT checkpoints_timed, checkpoints_req, checkpoint_write_time,
                 checkpoint_sync_time, buffers_checkpoint, buffers_clean,
                 buffers_backend, buffers_alloc
          FROM pg_stat_bgwriter
          ''',
                                 (),
                                 ('postgres.bgwriter.checkpoints_timed',
                                  'postgres.bgwriter.checkpoints_req',
                                  'postgres.bgwriter.checkpoint_write_time',
                                  'postgres.bgwriter.checkpoint_sync_time',
                                  'postgres.bgwriter.buffers_checkpoint',
                                  'postgres.bgwriter.buffers_clean',
                                  'postgres.bgwriter.buffers_backend',
                                  'postgres.bgwriter.buffers_alloc'))

    def pg_db_stats(self, _) -> None:
        self.logger.info('fetching PG database stats')
        self.pg_run_metric_query('''
            SELECT datname, xact_commit, xact_rollback, tup_inserted,
                   tup_updated, tup_deleted, tup_returned, tup_fetched,
                   blks_read, blks_hit, temp_files, temp_bytes, deadlocks,
                   blk_read_time, blk_write_time
            FROM pg_stat_database
            ''',
                                 ('database',),
                                 ('postgres.database.commits',
                                  'postgres.database.rollbacks',
                                  'postgres.database.rows_inserted',
                                  'postgres.database.rows_updated',
                                  'postgres.database.rows_deleted',
                                  'postgres.database.rows_returned',
                                  'postgres.database.rows_fetched',
                                  'postgres.database.blocks_read',
                                  'postgres.database.blocks_hit',
                                  'postgres.database.temp_files',
                                  'postgres.database.temp_bytes',
                                  'postgres.database.deadlocks',
                                  'postgres.database.block_read_time',
                                  'postgres.database.block_write_time'))

    def pg_table_stats(self, _) -> None:
        self.logger.info('fetching PG table stats')
        self.pg_run_metric_query('''
            SELECT schemaname, relname, seq_scan, seq_tup_read, idx_scan, idx_tup_fetch,
              n_tup_ins, n_tup_upd, n_tup_del, vacuum_count, autovacuum_count,
              analyze_count, autoanalyze_count, n_live_tup, n_dead_tup,
              extract(EPOCH FROM now() - last_vacuum)::INT/60/60,
              extract(EPOCH FROM now() - last_analyze)::INT/60/60
            FROM pg_stat_all_tables
            ''',
                                 ('schema', 'rel'),
                                 ('postgres.table.sequential_scans',
                                  'postgres.table.sequential_scan_rows',
                                  'postgres.table.index_scans',
                                  'postgres.table.index_scan_rows',
                                  'postgres.table.rows_inserted',
                                  'postgres.table.rows_updated',
                                  'postgres.table.rows_deleted',
                                  'postgres.table.vacuum_count',
                                  'postgres.table.auto_vacuum_count',
                                  'postgres.table.analyze_count',
                                  'postgres.table.auto_analyze_count',
                                  'postgres.table.live_rows',
                                  'postgres.table.dead_rows',
                                  'postgres.table.time_since_vacuum',
                                  'postgres.table.time_since_analyze'))

    def pg_table_io_stats(self, _) -> None:
        self.logger.info('fetching PG table IO stats')
        self.pg_run_metric_query('''
          SELECT schemaname, relname, heap_blks_read, heap_blks_hit,
            idx_blks_read, idx_blks_hit, toast_blks_read, toast_blks_hit,
            tidx_blks_read, tidx_blks_hit
          FROM pg_statio_all_tables
          ''',
                                 ('schema', 'rel'),
                                 ('postgres.table_io.heap_blocks_read',
                                  'postgres.table_io.heap_blocks_hit',
                                  'postgres.table_io.index_blocks_read',
                                  'postgres.table_io.index_blocks_hit',
                                  'postgres.table_io.toast_blocks_read',
                                  'postgres.table_io.toast_blocks_hit',
                                  'postgres.table_io.toast_index_blocks_read',
                                  'postgres.table_io.toast_index_blocks_hit',
                                  ))

    def pg_index_stats(self, _) -> None:
        self.logger.info('fetching PG index stats')
        self.pg_run_metric_query('''
          SELECT schemaname, relname, indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
          FROM pg_stat_all_indexes
          ''',
                                 ('schema', 'rel', 'index'),
                                 ('postgres.index.scans',
                                  'postgres.index.rows_read',
                                  'postgres.index.rows_fetched',
                                  ))

    def pg_index_io_stats(self, _) -> None:
        self.logger.info('fetching PG index IO stats')
        self.pg_run_metric_query('''
          SELECT schemaname, relname, indexrelname, idx_blks_read, idx_blks_hit
          FROM pg_statio_all_indexes
          ''',
                                 ('schema', 'rel', 'index'),
                                 ('postgres.index_io.blocks_read',
                                  'postgres.index_io.blocks_hit'))


    def pg_run_metric_query(self, sql: str,
                            label_names: Sequence[str],
                            metric_names: Sequence[str]) -> None:
        for row in self.fetchall(sql):
            assert len(label_names) + len(metric_names) == len(row)

            row = list(row)
            labels = {x: row.pop(0) for x in label_names}
            counters = {x: row.pop(0) or 0 for x in metric_names}

            for c_name, c_val in counters.items():
                self.counter(c_name, labels).set(float(c_val))


if __name__ == '__main__':
    sys.exit(PostgreSQLPlugin().run())
