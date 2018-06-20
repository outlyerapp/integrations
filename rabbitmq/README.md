RabbitMQ Integration
=====================

== Description ==

RabbitMQ is a messaging broker - an intermediary for messaging. It gives your applications a common platform to send and receive messages,
and your messages a safe place to live until received.

This integration will pull out key metrics from your RabbitMQ cluster using the RabbitMQ management plugin APIs.

== Metrics Collected ==

|Metric Name                                       |Type   |Labels                                 |Unit|Description                                                                                       |
|--------------------------------------------------|-------|---------------------------------------|----|--------------------------------------------------------------------------------------------------|
|rabbitmq.cluster_confirm_count                    |Counter|cluster                                |    |Rate at which cluster is confirming publishes.                                                    |
|rabbitmq.cluster_disk_read_count                  |Counter|cluster                                |    |Rate at which cluster is reading messages from disk.                                              |
|rabbitmq.cluster_disk_write_count                 |Counter|cluster                                |    |Rate at which cluster is writing messages to disk.                                                |
|rabbitmq.cluster_publish_count                    |Counter|cluster                                |    |Rate at which messages are entering the cluster.                                                  |
|rabbitmq.cluster_return_unroutable_count          |Counter|cluster                                |    |Rate at which unroutable messages are entering the cluster.                                       |
|rabbitmq.cluster_channels                         |Gauge  |cluster                                |    |Total number of channels in cluster.                                                              |
|rabbitmq.cluster_connections                      |Gauge  |cluster                                |    |Total number of connections in cluster.                                                           |
|rabbitmq.cluster_consumers                        |Gauge  |cluster                                |    |Total number of consumers in cluster.                                                             |
|rabbitmq.cluster_exchanges                        |Gauge  |cluster                                |    |Total number of exchanges in cluster.                                                             |
|rabbitmq.cluster_queues                           |Gauge  |cluster                                |    |Total number of queues in cluster.                                                                |
|rabbitmq.cluster_messages_queued                  |Gauge  |cluster                                |    |Total number of messages queued on cluster.                                                       |
|rabbitmq.node_context_switches_count              |Counter|node, cluster                          |    |Rate at which runtime context switching takes place on node.                                      |
|rabbitmq.node_disk_free                           |Gauge  |node, cluster                          |byte|Current free disk space.                                                                          |
|rabbitmq.node_fd_used                             |Gauge  |node, cluster                          |    |Used file descriptors.                                                                            |
|rabbitmq.node_mem_used                            |Gauge  |node, cluster                          |byte|Memory used in bytes.                                                                             |
|rabbitmq.node_run_queue                           |Gauge  |node, cluster                          |    |Average number of Erlang processes waiting to run.                                                |
|rabbitmq.node_sockets_used                        |Gauge  |node, cluster                          |    |Number of file descriptors used as sockets.                                                       |
|rabbitmq.node_running                             |Gauge  |node, cluster                          |    |Alarm signal, 0 = Not Running, 1 = Running.                                                       |
|rabbitmq.node_mem_alarm                           |Gauge  |node, cluster                          |    |Alarm signal, 0 = Memory OK, 1 = Memory running out.                                              |
|rabbitmq.node_disk_free_alarm                     |Gauge  |node, cluster                          |    |Alarm signal, 0 = Disk Space OK, 1 = Disk running out.                                            |
|rabbitmq.node_partitions                          |Gauge  |node, cluster                          |    |Number of network partitions this node is seeing.                                                 |
|rabbitmq.connections                              |Gauge  |vhost, cluster                         |    |Number of current connections to a given rabbitmq vhost.                                          |
|rabbitmq.connection_states                        |Gauge  |state, cluster                         |    |Number of connections in the specified connection state.                                          |
|rabbitmq.exchange_messages_ack_count              |Counter|exchange, exchange_type, cluster, vhost|    |Rate of messages delivered to clients and acknowledged.                                           |
|rabbitmq.exchange_messages_confirm_count          |Counter|exchange, exchange_type, cluster, vhost|    |Rate of messages confirmed by exchange.                                                           |
|rabbitmq.exchange_messages_deliver_get.count      |Counter|exchange, exchange_type, cluster, vhost|    |Rate of messages delivered in acknowledgement mode to consumers.                                  |
|rabbitmq.exchange_messages_publish_count          |Counter|exchange, exchange_type, cluster, vhost|    |Rate of messages published by exchange.                                                           |
|rabbitmq.exchange_publish_in_count                |Counter|exchange, exchange_type, cluster, vhost|    |Rate of messages published from channels into this exchange.                                      |
|rabbitmq.exchange_publish_out_count               |Counter|exchange, exchange_type, cluster, vhost|    |Rate of messages published from this exchange into queues.                                        |
|rabbitmq.exchange_messages_return_unroutable_count|Counter|exchange, exchange_type, cluster, vhost|    |Rate of messages returned to publisher as unroutable from this exchange.                          |
|rabbitmq.exchange_messages_redeliver_count        |Counter|exchange, exchange_type, cluster, vhost|    |Rate of subset of messages in deliver_get which had the redelivered flag set from this exchange.  |
|rabbitmq.queue_active_consumers                   |Gauge  |queue, node, cluster, vhost            |    |Number of active consumers, consumers that can immediately receive any messages sent to the queue.|
|rabbitmq.queue_consumers                          |Gauge  |queue, node, cluster, vhost            |    |Number of consumers for queue.                                                                    |
|rabbitmq.queue_consumer_utilisation               |Gauge  |queue, node, cluster, vhost            |    |The ratio of time that a queue's consumers can take new messages.                                 |
|rabbitmq.queue_memory                             |Gauge  |queue, node, cluster, vhost            |byte|Bytes of memory consumed by the Erlang process associated with the queue.                         |
|rabbitmq.queue_messages_count                     |Counter|queue, node, cluster, vhost            |    |Rate of the total messages in the queue.                                                          |
|rabbitmq.queue_messages_ready_count               |Counter|queue, node, cluster, vhost            |    |Rate per second of messages ready to be delivered to clients.                                     |
|rabbitmq.queue_messages_unacknowledged_count      |Counter|queue, node, cluster, vhost            |    |Rate of messages delivered to clients but not yet acknowledged.                                   |
|rabbitmq.queue_messages_ack_count                 |Counter|queue, node, cluster, vhost            |    |Rate of messages delivered to clients and acknowledged.                                           |
|rabbitmq.queue_messages_deliver_count             |Counter|queue, node, cluster, vhost            |    |Rate of messages delivered in acknowledgement mode to consumers.                                  |
|rabbitmq.queue_messages_deliver_get_count         |Counter|queue, node, cluster, vhost            |    |Rate of messages delivered in acknowledgement mode to consumers.                                  |
|rabbitmq.queue_messages_publish_count             |Counter|queue, node, cluster, vhost            |    |Rate of messages published.                                                                       |
|rabbitmq.queue_messages_redeliver_count           |Counter|queue, node, cluster, vhost            |    |Rate of subset of messages in deliver_get which had the redelivered flag set.                     |

== Installation ==

To enable Outlyer to monitor RabbitMQ you need to enable the management plugin.  The management plugin is included in the RabbitMQ distribution. To enable it, use rabbitmq-plugins:

`$ rabbitmq-plugins enable rabbitmq_management`

The Default Web UI is located at: http://server-name:15672/. The Web UI uses an HTTP API provided by the same plugin.
The API's endpoints can be accessed at http://server-host:15672/api/

In the RabbitMQ check you can override the following settings:

|Variable  |Default   |Description                                            |
|----------|----------|-------------------------------------------------------|
|port      |1567      |Port running management plugin APIs.                   |
|protocol  |http      |HTTP Protocol, either http or https.                   |
|verify_ssl|false     |Should SSL verification be disabled or not.            |
|username  |guest     |The username for the RabbitMQ Cluster.                 |
|password  |guest     |The password for the RabbitMQ Cluster.                 |

== Changelog ==

|Version|Release Date|Description                                            |
|-------|------------|-------------------------------------------------------|
|1.0    |30-May-2018 |Initial version of our RabbitMQ monitoring integration.|