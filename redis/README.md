Redis Integration
=================

== Description ==

Redis is an open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker.

This integration will monitor your Redis cluster by collecting metrics from Redis `INFO` command.

Once enabled you will get a default Redis dashboard to help you get started monitoring your key Redis metrics.

== Metrics Collected ==

|Metric Name                     |Type   |Labels  |Unit   |Description                                                                                                                                 |
|--------------------------------|-------|--------|-------|--------------------------------------------------------------------------------------------------------------------------------------------|
|redis_connected_slaves          |Gauge  |        |       |Number of connected slaves.                                                                                                                 |
|redis_uptime_in_seconds         |Counter|        |       |Number of seconds since Redis server start.                                                                                                 |
|redis_total_connections_received|Counter|        |       |Total number of connections accepted by the server.                                                                                         |
|redis_total_commands_processed  |Counter|        |       |Total number of commands processed by the server.                                                                                           |
|redis_rejected_connections      |Counter|        |       |Number of connections rejected because of maxclients limit.                                                                                 |
|redis_expired_keys              |Counter|        |       |Total number of key expiration events.                                                                                                      |
|redis_evicted_keys              |Counter|        |       |Number of evicted keys due to maxmemory limit.                                                                                              |
|redis_keyspace_hits             |Counter|        |       |Number of successful lookup of keys in the main dictionary.                                                                                 |
|redis_keyspace_misses           |Counter|        |       |Number of failed lookup of keys in the main dictionary.                                                                                     |
|redis_pubsub_channels           |Gauge  |        |       |Global number of pub/sub channels with client subscriptions.                                                                                |
|redis_used_cpu_sys              |Counter|        |       |System CPU time consumed by the Redis server.                                                                                               |
|redis_used_cpu_user             |Counter|        |second |User CPU time consumed by the Redis server.                                                                                                 |
|redis_connected_clients         |Gauge  |        |       |Number of client connections (excluding connections from slaves).                                                                           |
|redis_blocked_clients           |Gauge  |        |       |Number of clients pending on a blocking call (BLPOP, BRPOP, BRPOPLPUSH).                                                                    |
|redis_used_memory               |Gauge  |        |byte   |Total number of bytes allocated by Redis using its allocator (either standard libc, jemalloc, or an alternative allocator such as tcmalloc).|
|redis_mem_fragmentation_ratio   |Gauge  |        |       |Ratio between the number of bytes Redis allocated as seen by the operating system and `redis_used_memory`.                                  |
|redis_instantaneous_ops_per_sec |Gauge  |        |ops/sec|Number of commands processed per second.                                                                                                    |
|redis_instantaneous_input_kbps  |Gauge  |uom     |KB/sec |The network's read rate per second in KB/sec.                                                                                               |
|redis_instantaneous_output_kbps |Gauge  |uom     |KB/sec |The network's write rate per second in KB/sec.                                                                                              |
|redis_keys                      |Gauge  |database|       |The current number of keys per database.                                                                                                    |
|redis_expires                   |Gauge  |database|       |The current number of keys with an expiration per database.                                                                                 |

== Installation ==

Just run the Redis plugin against your Redis instances and it will start collecting metrics.

### Plugin Environment Variables

The Redis plugin can be customized via environment variables.

|Variable|Default     |Description                                                   |
|--------|------------|--------------------------------------------------------------|
|port    |6379        |Redis port.                                                   |
|password|            |Redis password. Only used in password-protected Redis servers.|

== Changelog ==

|Version|Release Date|Description                                         |
|-------|------------|----------------------------------------------------|
|1.0    |13-Jun-2018 |Initial version of our Redis monitoring integration.|
