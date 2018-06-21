PostgreSQL Integration
======================

== Description ==

PostgreSQL is a powerful, open source object-relational database system that uses and extends the SQL language combined with many features that safely store and scale the most complicated data workloads.

This integration will monitor your PostgreSQL database by collecting metrics from PostgreSQL internal statistics views.

Once enabled you will get a default PostgreSQL dashboard to help you get started monitoring your key PostgreSQL metrics.

== Metrics Collected ==

|Metric Name                            |Type |Labels  |Unit       |Description                                                                                                           |
|---------------------------------------|-----|--------|-----------|----------------------------------------------------------------------------------------------------------------------|
|postgres.connections                   |Gauge|        |connection |Number of active connections.                                                                                         |
|postgres.sessions.active               |Gauge|        |session    |Number of active sessions.                                                                                            |
|postgres.sessions.idle                 |Gauge|        |session    |Number of idle sessions.                                                                                              |
|postgres.sessions.idle_in_transaction  |Gauge|        |session    |Number of idle sessions in transaction.                                                                               |
|postgres.sessions.waiting              |Gauge|        |session    |Number of waiting sessions.                                                                                           |
|postgres.sessions.longest_transaction  |Gauge|uom     |second     |Longest transaction in seconds.                                                                                       |
|postgres.sessions.longest_query        |Gauge|uom     |second     |Longest query in seconds.                                                                                             |
|postgres.locks.accessexclusive         |Gauge|        |lock       |Number of locks in `AccessExclusiveLock` mode.                                                                        |
|postgres.locks.otherexclusive          |Gauge|        |lock       |Number of exclusive locks different than `AccessExclusiveLock`.                                                       |
|postgres.locks.shared                  |Gauge|        |lock       |Number of locks in `Share` mode.                                                                                      |
|postgres.bgwriter.checkpoints_timed    |Gauge|        |checkpoint |Number of scheduled checkpoints that have been performed.                                                             |
|postgres.bgwriter.checkpoints_req      |Gauge|        |checkpoint |Number of requested checkpoints that have been performed.                                                             |
|postgres.bgwriter.checkpoint_write_time|Gauge|        |millisecond|Total amount of time that has been spent in the portion of checkpoint processing where files are written to disk.     |
|postgres.bgwriter.checkpoint_sync_time |Gauge|        |millisecond|Total amount of time that has been spent in the portion of checkpoint processing where files are synchronized to disk.|
|postgres.bgwriter.buffers_checkpoint   |Gauge|        |buffer     |Number of buffers written during checkpoints.                                                                         |
|postgres.bgwriter.buffers_clean        |Gauge|        |buffer     |Number of buffers written by the background writer.                                                                   |
|postgres.bgwriter.buffers_backend      |Gauge|        |buffer     |Number of buffers written directly by a backend.                                                                      |
|postgres.bgwriter.buffers_alloc        |Gauge|        |buffer     |Number of buffers allocated.                                                                                          |
|postgres.database.commits              |Gauge|database|commit     |Number of transactions in this database that have been committed.                                                     |
|postgres.database.rollbacks            |Gauge|database|rollback   |Number of transactions in this database that have been rolled back.                                                   |
|postgres.database.rows_inserted        |Gauge|database|row        |Number of rows inserted by queries in this database.                                                                  |
|postgres.database.rows_updated         |Gauge|database|row        |Number of rows updated by queries in this database.                                                                   |
|postgres.database.rows_deleted         |Gauge|database|row        |Number of rows deleted by queries in this database.                                                                   |
|postgres.database.rows_returned        |Gauge|database|row        |Number of rows returned by queries in this database.                                                                  |
|postgres.database.rows_fetched         |Gauge|database|row        |Number of rows fetched by queries in this database.                                                                   |
|postgres.database.blocks_read          |Gauge|database|block      |Number of disk blocks read in this database.                                                                          |
|postgres.database.blocks_hit           |Gauge|database|hit        |Number of times disk blocks were found already in the buffer cache, so that a read was not necessary.                 |
|postgres.database.temp_files           |Gauge|database|file       |Number of temporary files created by queries in this database.                                                        |
|postgres.database.temp_bytes           |Gauge|database|byte       |Total amount of data written to temporary files by queries in this database.                                          |
|postgres.database.deadlocks            |Gauge|database|deadlock   |Number of deadlocks detected in this database.                                                                        |
|postgres.database.block_read_time      |Gauge|database|millisecond|Time spent reading data file blocks by backends in this database.                                                     |
|postgres.database.block_write_time     |Gauge|database|millisecond|Time spent writing data file blocks by backends in this database.                                                     |

== Installation ==

This plugin runs queries to collect metrics from PostgreSQL, so you need to provide a valid user with appropriate privileges.

To create a specific user for collecting metrics, log into a `psql` session as a user who has `CREATEROLE` privileges, for example:

```
$ sudo -u postgres psql
```

Create a user and grant the appropriate privileges:

```
create user outlyer with password 'your_password';
grant SELECT ON pg_stat_database to outlyer;
```

Then configure the `username` and `password` plugin environment variables to match and run the PostgreSQL plugin against your PostgreSQL instance to start collecting metrics.

### Plugin Environment Variables

The PostgreSQL plugin can be customized via environment variables.

|Variable|Default  |Description                    |
|--------|---------|-------------------------------|
|host    |localhost|PostgreSQL host.               |
|port    |5432     |PostgreSQL port.               |
|dbname  |postgres |PostgreSQL database name.      |
|username|         |PostgreSQL username (required).|
|password|         |PostgreSQL password (required).|

== Changelog ==

|Version|Release Date|Description                                              |
|-------|------------|---------------------------------------------------------|
|1.0    |19-Jun-2018 |Initial version of our PostgreSQL monitoring integration.|
