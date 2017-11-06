import re

import psycopg2
import psycopg2.errorcodes

from outlyer_agent.collection import Status, Plugin, PluginTarget


# noinspection SqlResolve
class PostgreSQLPlugin(Plugin):

    def collect(self, target: PluginTarget) -> Status:

        self.host = target.get('host', 'localhost')
        self.port = target.get('port', 5432)
        self.dbname = target.get('dbname', 'postgres')
        self.user = target.get('username', None)
        self.password = target.get('password', None)

        try:
            self.conn = psycopg2.connect(self.dsn)
            self.cursor = self.conn.cursor()

            pg_ver = self.pg_version()

            self.pg_connection_count(target)
            self.pg_activity(pg_ver, target)
            self.pg_lock_stats(target)
            self.pg_bgwriter_stats(target)
            self.pg_db_stats(target)
            self.pg_table_stats(target)

            self.cursor.close()

        except psycopg2.OperationalError as ex:
            self.logger.error('Unable to connect to PostgreSQL: %s', str(ex))
            return Status.CRITICAL

        except psycopg2.ProgrammingError as ex:
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

    def pg_connection_count(self, target: PluginTarget) -> None:
        r = self.fetchall('SELECT sum(numbackends) FROM pg_stat_database;')
        target.gauge('postgres_connections').set(float(r[0][0]))

    def pg_activity(self, pg_ver: float, target: PluginTarget) -> None:
        # single session state query avoids multiple scans of pg_stat_activity
        # state is a different column name in postgres 9.2, previous versions will have to update this query accordingly
        if pg_ver >= 9.6:
            # noinspection SqlResolve
            q_activity = '''
            SELECT state, (CASE wait_event WHEN NULL THEN FALSE ELSE TRUE END) AS waiting,
                coalesce(extract(EPOCH FROM current_timestamp - xact_start)::INT, 0),
                coalesce(extract(EPOCH FROM current_timestamp - query_start)::INT, 0)
            FROM pg_stat_activity
            '''
        else:
            # noinspection SqlResolve
            q_activity = '''
            SELECT state, waiting,
                coalesce(extract(EPOCH FROM current_timestamp - xact_start)::INT, 0),
                coalesce(extract(EPOCH FROM current_timestamp - query_start)::INT, 0)
            FROM pg_stat_activity
            '''

        results = self.fetchall(q_activity)

        active_results = []
        active_count = target.gauge('postgres_active_sessions')
        idle_count = target.gauge('postgres_idle_sessions')
        idle_in_txn_count = target.gauge('postgres_idle_in_transaction_sessions')
        waiting_count = target.gauge('postgres_waiting_sessions')

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
        target.gauge('postgres_longest_xact', {'uom': 'seconds'}).set((sorted_by_xact[0])[2])

        # determine longest active query in seconds
        sorted_by_query = sorted(active_results, reverse=True)
        target.gauge('postgres_longest_query', {'uom': 'seconds'}).set(sorted_by_query[0])

    def pg_lock_stats(self, target: PluginTarget) -> None:
        results = self.fetchall('SELECT mode, locktype FROM pg_locks')

        access_exclusive = target.gauge('postgres_locks_accessexclusive')
        other_exclusive = target.gauge('postgres_locks_otherexclusive')
        shared = target.gauge('postgres_locks_shared')

        for mode, lock_type in results:
            if mode == 'AccessExclusiveLock' and lock_type != 'virtualxid':
                access_exclusive.inc()
            if mode != 'AccessExclusiveLock' and lock_type != 'virtualxid':
                if 'Exclusive' in mode:
                    other_exclusive.inc()
            if 'Share' in mode and lock_type != 'virtualxid':
                shared.inc()

    def pg_bgwriter_stats(self, target: PluginTarget) -> None:
        q_bg_writer = '''
          SELECT checkpoints_timed, checkpoints_req, checkpoint_write_time,
                 checkpoint_sync_time, buffers_checkpoint, buffers_clean,
                 buffers_backend, buffers_alloc
          FROM pg_stat_bgwriter
          '''
        results = self.fetchall(q_bg_writer)[0]
        target.counter('postgres_bgwriter_checkpoints_timed').set(results[0] or 0)
        target.counter('postgres_bgwriter_checkpoints_req').set(results[1] or 0)
        target.counter('postgres_bgwriter_checkpoint_write_time').set(results[2] or 0)
        target.counter('postgres_bgwriter_checkpoint_sync_time').set(results[3] or 0)
        target.counter('postgres_bgwriter_buffers_checkpoint').set(results[4] or 0)
        target.counter('postgres_bgwriter_buffers_clean').set(results[5] or 0)
        target.counter('postgres_bgwriter_buffers_backend').set(results[6] or 0)
        target.counter('postgres_bgwriter_buffers_alloc').set(results[7] or 0)

    def pg_db_stats(self, target: PluginTarget) -> None:
        q_stats = '''
            SELECT datname, xact_commit + xact_rollback, tup_inserted,
                   tup_updated, tup_deleted, tup_returned + tup_fetched,
                   blks_read, blks_hit
            FROM pg_stat_database
            '''
        for row in self.fetchall(q_stats):
            labels = {'database': row[0]}
            target.counter('postgres_transactions', labels).set(row[1] or 0)
            target.counter('postgres_inserts', labels).set(row[2] or 0)
            target.counter('postgres_updates', labels).set(row[3] or 0)
            target.counter('postgres_deletes', labels).set(row[4] or 0)
            target.counter('postgres_reads', labels).set(row[5] or 0)
            target.counter('postgres_blks_diskread', labels).set(row[6] or 0)
            target.counter('postgres_blks_memread', labels).set(row[7] or 0)

    def pg_table_stats(self, target: PluginTarget) -> None:
        q_table_stats = '''
            SELECT schemaname, relname, seq_tup_read, idx_tup_fetch,
              extract(EPOCH FROM now() - last_vacuum)::INT/60/60,
              extract(EPOCH FROM now() - last_analyze)::INT/60/60
            FROM pg_stat_all_tables
            '''
        for row in self.fetchall(q_table_stats):
            labels = {'schema': row[0], 'rel': row[1]}
            target.counter('postgres_tup_seqscan', labels).set(row[2] or 0)
            target.counter('postgres_tup_idxfetch', labels).set(row[3] or 0)
            target.counter('postgres_hours_since_last_vacuum', labels).set(row[4] or 0)
            target.counter('postgres_hours_since_last_analyze', labels).set(row[5] or 0)
