ZooKeeper Integration
=====================

== Description ==

ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services.

This integration will monitor your ZooKeeper cluster by collecting ZooKeeper metrics using [four letter words](http://zookeeper.apache.org/doc/r3.4.12/zookeeperAdmin.html#sc_zkCommands) commands.

Once enabled you will get a default ZooKeeper dashboard and alert rules to help you get started monitoring your key ZooKeeper metrics.

== Metrics Collected ==

| Metric Name                 |Type   |Labels|Unit       |Description                                                                                                              |
|-----------------------------|-------|------|-----------|-------------------------------------------------------------------------------------------------------------------------|
|zk_avg_latency               |Gauge  |      |millisecond|The average time it takes for the server to respond to a client request.                                                 |
|zk_max_latency               |Gauge  |      |millisecond|The maximum time it takes for the server to respond to a client request.                                                 |
|zk_min_latency               |Gauge  |      |millisecond|The minimum time it takes for the server to respond to a client request.                                                 |
|zk_packets_received          |Counter|      |           |The number of packets received.                                                                                          |
|zk_packets_sent              |Counter|      |           |The number of packets sent.                                                                                              |
|zk_num_alive_connections     |Gauge  |      |           |The total count of client connections.                                                                                   |
|zk_outstanding_requests      |Gauge  |      |           |The number of queued requests when the server is under load and is receiving more sustained requests than it can process.|
|zk_znode_count               |Gauge  |      |           |The number of znodes in the ZooKeeper namespace (the data).                                                              |
|zk_watch_count               |Gauge  |      |           |Watch count.                                                                                                             |
|zk_ephemerals_count          |Gauge  |      |           |Ephemerals Count.                                                                                                        |
|zk_approximate_data_size     |Gauge  |      |byte       |Approximate data size.                                                                                                   |
|zk_open_file_descriptor_count|Gauge  |      |           |Number of currently open file descriptors.                                                                               |
|zk_max_file_descriptor_count |Gauge  |      |           |Maximum number of open file descriptors.                                                                                 |
|zk_followers                 |Gauge  |      |           |Number of followers.                                                                                                     |
|zk_synced_followers          |Gauge  |      |           |Current number of synced followers.                                                                                      |
|zk_pending_syncs             |Gauge  |      |           |Current number of pending syncs.                                                                                         |


== Installation ==

Run the ZooKeeper plugin against your ZooKeeper instances and it will start collecting metrics.

### Plugin Environment Variables

The ZooKeeper plugin can be customized via environment variables.

|Variable |Default  |Description    |
|---------|---------|---------------|
|ip       |localhost|ZooKeeper host.|
|port     |2181     |ZooKeeper port.|

== Changelog ==

|Version|Release Date|Description                                             |
|-------|------------|--------------------------------------------------------|
|1.0.2  |28-Sep-2018 |Fixes ZooKeeper dashboard logo URL and updates docs.    |
|1.0.1  |28-Sep-2018 |Uses ip environment variable instead of host.           |
|1.0    |25-May-2018 |Initial version of our ZooKeeper monitoring integration.|
