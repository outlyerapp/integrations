Cassandra Integration
=====================

== Description ==

Apache Cassandra is a free and open-source distributed wide column store NoSQL database management system designed to handle large amounts of data across many commodity servers, providing high availability with no single point of failure. Cassandra offers robust support for clusters spanning multiple datacenters, with asynchronous masterless replication allowing low latency operations for all clients.

This integration will monitor your Cassandra cluster by collecting metrics via JMX.

Once enabled you will get a default Cassandra overview dashboard to help you get started monitoring your key Cassandra performance metrics.

== Metrics Collected ==

|Metric Name                                         |Type   |Labels    |Unit        |Description                                                           |
|----------------------------------------------------|-------|----------|------------|----------------------------------------------------------------------|
|cassandra.reads                                     |Gauge  |          |read/second |The number of local read requests per second.                         |
|cassandra.writes                                    |Gauge  |          |write/second|The number of local write requests per second.                        |
|cassandra.read_latency_99th_percentile              |Gauge  |          |microsecond |The local read latency - p99.                                         |
|cassandra.write_latency_99th_percentile             |Gauge  |          |microsecond |The local write latency - p99.                                        |
|cassandra.compaction_pending_tasks                  |Gauge  |          |task        |The number of pending compactions.                                    |
|cassandra.total_disk_space_used                     |Gauge  |keyspace  |byte        |The total disk space used by the keyspace in this node.               |
|cassandra.exceptions_read_timeouts                  |Gauge  |          |error/second|Read requests not acknowledged within configurable timeout window.    |
|cassandra.exceptions_write_timeouts                 |Gauge  |          |error/second|Write requests not acknowledged within configurable timeout window.   |
|cassandra.exceptions_read_unavailables              |Gauge  |          |error/second|Read requests for which the required number of nodes was unavailable. |
|cassandra.exceptions_write_unavailables             |Gauge  |          |error/second|Write requests for which the required number of nodes was unavailable.|
|cassandra.threadpool_request_pending_tasks          |Gauge  |stage     |task        |The number of pending tasks for the thread pool.                      |
|cassandra.threadpool_request_currently_blocked_tasks|Gauge  |stage     |task        |The number of currently blocked tasks for the thread pool.            |
|cassandra.open_file_descriptors                     |Gauge  |          |file        |The number of opened file descriptors.                                |
|cassandra.max_file_descriptors                      |Gauge  |          |file        |The maximum number of file descriptors.                               |

== Installation ==

Just run the Cassandra plugin against your Cassandra instances and it will start collecting metrics.

### Plugin Environment Variables

The Cassandra plugin can be customized via environment variables.

|Variable |Default     |Description        |
|---------|------------|-------------------|
|host     |localhost   |Cassandra host.    |
|port     |7199        |Cassandra JMX port.|


== Changelog ==

|Version|Release Date|Description                                             |
|-------|------------|--------------------------------------------------------|
|1.0    |9-Jul-2018  |Initial version of our Cassandra monitoring integration.|
