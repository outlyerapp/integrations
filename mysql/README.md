MySQL Integration
=================

== Description ==

MySQL is an open source relational database management system (RDBMS) based on Structured Query Language (SQL). 

This integration will monitor your MySQL database by collecting metrics from MySQL [server status](https://dev.mysql.com/doc/refman/5.5/en/show-status.html).

Once enabled you will get a default MySQL dashboard to help you get started monitoring your key MySQL metrics.

== Metrics Collected ==

|Metric Name                            |Type   |Labels|Unit        |Description                                                                                                                                                                            |
|---------------------------------------|-------|------|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|mysql.threads_connected                |Gauge  |      |            |The number of currently open connections.                                                                                                                                              |
|mysql.threads_running                  |Gauge  |      |            |The number of threads that are not sleeping.                                                                                                                                           |
|mysql.innodb_buffer_pool_pages_total   |Gauge  |      |            |The total number of pages in the InnoDB Buffer Pool.                                                                                                                                   |
|mysql.innodb_buffer_pool_pages_free    |Gauge  |      |            |The number of free pages in the InnoDB Buffer Pool.                                                                                                                                    |
|mysql.table_locks_waited               |Counter|      |            |The total number of times that a request for a table lock could not be granted immediately and a wait was needed.                                                                      |
|mysql.bytes_received                   |Counter|      |byte/second |The rate of bytes received from all clients.                                                                                                                                           |
|mysql.bytes_sent                       |Counter|      |byte/second |The rate of bytes sent to all clients.                                                                                                                                                 |
|mysql.connection_errors_accept         |Counter|      |error/second|The rate of errors that occurred during calls to `accept()` on the listening port.                                                                                                     |
|mysql.connection_errors_internal       |Counter|      |error/second|The rate of connections refused due to internal errors in the server, such as failure to start a new thread or an out-of-memory condition.                                             |
|mysql.connection_errors_max_connections|Counter|      |error/second|The rate of connections refused because the server max_connections limit was reached.                                                                                                  |
|mysql.connection_errors_peer_address   |Counter|      |error/second|The rate of errors that occurred while searching for connecting client IP addresses.                                                                                                   |
|mysql.connection_errors_select         |Counter|      |error/second|The rate of errors that occurred during calls to `select()` or `poll()` on the listening port. (Failure of this operation does not necessarily means a client connection was rejected.)|
|mysql.connection_errors_tcpwrap        |Counter|      |error/second|The rate of connections refused by the libwrap library.                                                                                                                                |
|mysql.created_tmp_disk_tables          |Gauge  |      |table/second|The rate of internal on-disk temporary tables created by the server while executing statements.                                                                                        |
|mysql.created_tmp_files                |Gauge  |      |file/second |The rate of temporary files mysqld has created.                                                                                                                                        |
|mysql.com_commit                       |Counter|      |query/second|The rate of commits.                                                                                                                                                                   |
|mysql.com_insert                       |Counter|      |query/second|The rate of insert statements.                                                                                                                                                         |
|mysql.com_rollback                     |Counter|      |query/second|The rate of rollbacks.                                                                                                                                                                 |
|mysql.com_select                       |Counter|      |query/second|The rate of select statements.                                                                                                                                                         |
|mysql.com_update                       |Counter|      |query/second|The rate of update statements.                                                                                                                                                         |
|mysql.com_delete                       |Counter|      |query/second|The rate of delete statements.                                                                                                                                                         |
|mysql.innodb_buffer_pool_read_requests |Counter|      |read/second |The rate of logical read requests.                                                                                                                                                     |
|mysql.innodb_buffer_pool_reads         |Counter|      |read/second |The rate of logical reads that InnoDB could not satisfy from the buffer pool, and had to read directly from disk.                                                                      |
|mysql.innodb_pages_read                |Counter|      |read/second |The rate of pages read from the InnoDB buffer pool by operations on InnoDB tables.                                                                                                     |
|mysql.innodb_pages_written             |Counter|      |write/second|The rate of pages written by operations on InnoDB tables.                                                                                                                              |
|mysql.innodb_row_lock_time             |Counter|      |            |The rate of time spent in acquiring row locks for InnoDB tables.                                                                                                                       |
|mysql.innodb_row_lock_waits            |Counter|      |ops/second  |The rate of operations on InnoDB tables had to wait for a row lock.                                                                                                                    |
|mysql.select_scan                      |Counter|      |join/second |The rate of joins that did a full scan of the first table.                                                                                                                             |
|mysql.slow_queries                     |Counter|      |query/second|The rate of queries that have taken more than `long_query_time` seconds.                                                                                                               |
|mysql.questions                        |Counter|      |query/second|The rate of statements executed by the server.                                                                                                                                         |

== Installation ==

This plugin runs `mysql show global status` on the command line with some options. By default it will use the user name `root` with "mysql" as the password.

To create a new user specifically for this integration with a minimum set of privileges use the following command:

```
GRANT USAGE ON *.* TO 'outlyer'@'localhost' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;
```

Then configure the `username` and `password` plugin environment variables to match and run the MySQL plugin against your MySQL instance to start collecting metrics.

### Plugin Environment Variables

The MySQL plugin can be customized via environment variables.

|Variable|Default  |Description    |
|--------|---------|---------------|
|ip      |127.0.0.1|MySQL host.    |
|port    |3306     |MySQL port.    |
|username|root     |MySQL username.|
|password|mysql    |MySQL password.|

== Changelog ==

|Version|Release Date|Description                                         |
|-------|------------|----------------------------------------------------|
|1.0    |14-Jun-2018 |Initial version of our MySQL monitoring integration.|
