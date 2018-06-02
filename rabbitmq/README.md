RabbitMQ Integration
=====================

== Description ==

RabbitMQ is a messaging broker - an intermediary for messaging. It gives your applications a common platform to send and receive messages,
and your messages a safe place to live until received.

This integration will pull out key metrics from your RabbitMQ cluster using the RabbitMQ management plugin APIs.

== Metrics Collected ==

|Metric Name                                 |Type   |Labels                                 |Unit |Description                                       |
|--------------------------------------------|-------|---------------------------------------|-----|--------------------------------------------------|
|rabbitmq.cluster_confirm_count              |counter|cluster                                |     |                                                  |
|rabbitmq.cluster_disk_read_count            |counter|cluster                                |     |                                                  |
|rabbitmq.cluster_disk_write_count           |counter|cluster                                |     |                                                  |
|rabbitmq.cluster_publish_count              |counter|cluster                                |     |                                                  |
|rabbitmq.cluster_return_unroutable_count    |counter|cluster                                |     |                                                  |
|rabbitmq.cluster_channels                   |gauge  |cluster                                |     |                                                  |
|rabbitmq.cluster_connections                |gauge  |cluster                                |     |                                                  |
|rabbitmq.cluster_consumers                  |gauge  |cluster                                |     |                                                  |
|rabbitmq.cluster_exchanges                  |gauge  |cluster                                |     |                                                  |
|rabbitmq.node_context_switches_count        |counter|node, cluster                          |     |                                                  |
|rabbitmq.node_disk_free                     |gauge  |node, cluster                          |     |                                                  |
|rabbitmq.node_fd_used                       |gauge  |node, cluster                          |     |                                                  |
|rabbitmq.node_mem_used                      |gauge  |node, cluster                          |     |                                                  |
|rabbitmq.node_run_queue                     |gauge  |node, cluster                          |     |                                                  |
|rabbitmq.node_sockets_used                  |gauge  |node, cluster                          |     |                                                  |
|rabbitmq.node_running                       |gauge  |node, cluster                          |     |                                                  |
|rabbitmq.node_mem_alarm                     |gauge  |node, cluster                          |     |                                                  |
|rabbitmq.node_disk_free_alarm               |gauge  |node, cluster                          |     |                                                  |
|rabbitmq.node_partitions                    |gauge  |node, cluster                          |     |                                                  |
|rabbitmq.connections                        |gauge  |vhost, cluster                         |     |                                                  |
|rabbitmq.connection_states                  |gauge  |state, cluster                         |     |                                                  |
|rabbitmq.exchange_publish_in_count          |counter|exchange, exchange_type, cluster, vhost|     |                                                  |
|rabbitmq.exchange_publish_out_count         |counter|exchange, exchange_type, cluster, vhost|     |                                                  |
|rabbitmq.queue_consumers                    |gauge  |queue, node, cluster, vhost            |     |                                                  |
|rabbitmq.queue_consumer_utilisation         |gauge  |queue, node, cluster, vhost            |     |                                                  |
|rabbitmq.queue_memory                       |gauge  |queue, node, cluster, vhost            |     |                                                  |
|rabbitmq.queue_messages_count               |counter|queue, node, cluster, vhost            |     |                                                  |
|rabbitmq.queue_messages_ready_count         |counter|queue, node, cluster, vhost            |     |                                                  |
|rabbitmq.queue_messages_unacknowledged_count|counter|queue, node, cluster, vhost            |     |                                                  |
|rabbitmq.queue_messages_ack_count           |counter|queue, node, cluster, vhost            |     |                                                  |
|rabbitmq.queue_messages_deliver_count       |counter|queue, node, cluster, vhost            |     |                                                  |
|rabbitmq.queue_messages_deliver_get_count   |counter|queue, node, cluster, vhost            |     |                                                  |
|rabbitmq.queue_messages_publish_count       |counter|queue, node, cluster, vhost            |     |                                                  |
|rabbitmq.queue_messages_redeliver_count     |counter|queue, node, cluster, vhost            |     |                                                  |

== Installation ==

To enable Outlyer to monitor RabbitMQ you need to enable the management plugin.  The management plugin is included in the
RabbitMQ distribution. To enable it, use rabbitmq-plugins:

`rabbitmq-plugins enable rabbitmq_management`

The Default Web UI is located at: http://server-name:15672/. The Web UI uses an HTTP API provided by the same plugin.
The API's endpoints can be accessed at http://server-host:15672/api/

In the RabbitMQ check you can override the following settings:

* `port`:
* `protocol`:
* `verify_ssl`:
* `username`:
* `password`:

== Changelog ==

|Version|Release Date|Description                                           |
|-------|------------|------------------------------------------------------|
|1.0    |30-May-2018 |Initial version of our RabbitMQ monitoring integration|