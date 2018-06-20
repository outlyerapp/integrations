etcd Integration
================

== Description ==

etcd is a distributed, consistent key-value store used for configuration management, service discovery, and coordinating distributed work.

This integration will monitor your etcd cluster by collecting metrics from etcd `/metrics` endpoint.

Once enabled you will get a default etcd cluster overview dashboard and alert rules template to help you get started monitoring your key etcd metrics.

== Metrics Collected ==

| Metric Name                                 |Type   |Labels |Unit|Description                                              |
|---------------------------------------------|-------|-------|----|---------------------------------------------------------|
|etcd_debugging_mvcc_watcher_total            |Gauge  |       |    |Total number of watchers.                                |
|etcd_debugging_mvcc_slow_watcher_total       |Gauge  |       |    |Total number of unsynced slow watchers.                  |
|etcd_debugging_mvcc_keys_total               |Gauge  |       |    |Total number of keys.                                    |
|etcd_debugging_mvcc_db_total_size_in_bytes   |Gauge  |       |byte|Total size of the underlying database in bytes.          |
|etcd_debugging_mvcc_put_total                |Counter|       |    |Total number of puts seen by this member.                |
|etcd_debugging_mvcc_delete_total             |Counter|       |    |Total number of deletes seen by this member.             |
|etcd_debugging_mvcc_txn_total                |Counter|       |    |Total number of txns seen by this member.                |
|etcd_debugging_mvcc_range_total              |Counter|       |    |Total number of ranges seen by this member.              |
|etcd_server_has_leader                       |Gauge  |       |    |Whether or not a leader exists. 1 is existence, 0 is not.|
|etcd_server_proposals_pending                |Gauge  |       |    |The current number of pending proposals to commit.       |
|etcd_server_proposals_committed_total        |Gauge  |       |    |The total number of consensus proposals committed.       |
|etcd_server_proposals_applied_total          |Gauge  |       |    |The total number of consensus proposals applied.         |
|etcd_server_leader_changes_seen_total        |Counter|       |    |The number of leader changes seen.                       |
|etcd_server_proposals_failed_total           |Counter|       |    |The total number of failed proposals seen.               |
|etcd_network_client_grpc_received_bytes_total|Counter|       |byte|The total number of bytes received from grpc clients.    |
|etcd_network_client_grpc_sent_bytes_total    |Counter|       |byte|The total number of bytes sent to grpc clients.          |
|etcd_network_peer_received_bytes_total       |Counter|from   |byte|The total number of bytes received from peers.           |
|etcd_network_peer_sent_bytes_total           |Counter|to     |byte|The total number of bytes sent to peers.                 |
|process_resident_memory_bytes                |Gauge  |       |byte|Resident memory size in bytes.                           |
|process_open_fds                             |Gauge  |       |    |Number of open file descriptors.                         |
|process_max_fds                              |Gauge  |       |    |Maximum number of open file descriptors.                 |

== Installation ==

Just run the etcd plugin against your etcd instances and it will start collecting etcd metrics.

### Plugin Environment Variables

The etcd plugin can be customized via environment variables.

|Variable |Default     |Description                                       |
|---------|------------|--------------------------------------------------|
|ETCD_HOST|            |etcd host. If empty, it will default to localhost.|
|PORT     |2379        |etcd client port.                                 |
|PATH     |metrics     |etcd metrics endpoint.                            |

== Changelog ==

|Version|Release Date|Description                                        |
|-------|------------|---------------------------------------------------|
|1.0    |22-May-2018 |Initial version of our etcd monitoring integration.|
