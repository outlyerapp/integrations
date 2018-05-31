RabbitMQ Integration
=====================

== Description ==

RabbitMQ is a messaging broker - an intermediary for messaging. It gives your applications a common platform to send and receive messages,
and your messages a safe place to live until received.

This integration will pull out key metrics from your RabbitMQ cluster using the RabbitMQ management plugin APIs.

== Metrics Collected ==

**Queue Metrics:**

'active_consumers'
'consumers'
'consumer_utilisation'
'memory'
'messages'
'messages_details/rate'
'messages_ready'
'messages_ready_details/rate'
'messages_unacknowledged'
'messages_unacknowledged_details/rate'

**Exchange Metrics:**

| Metric Name                                 |Type   | Labels            |Unit |Description                                                                          |
|---------------------------------------------|-------|-------------------|-----|-------------------------------------------------------------------------------------|
|ack                                          |       |                   |     |                                                                                     |
|ack_details/rate                             |       |                   |     |                                                                                     |
|confirm                                      |       |                   |     |Count of messages confirmed.                                                         |
|confirm_details/rate                         |       |                   |     |                                                                                     |
|deliver_get                                  |       |                   |     |Count of messages delivered in acknowledgement mode in response to basic.get.        |
|deliver_get_details/rate                     |       |                   |     |                                                                                     |
|publish                                      |       |                   |     |Count of messages published.                                                         |
|publish_details/rate                         |       |                   |     |                                                                                     |
|publish_in                                   |       |                   |     |Count of messages published "in" to an exchange, i.e. not taking account of routing. |
|publish_in_details/rate                      |       |                   |     |                                                                                     |
|publish_out                                  |       |                   |     |Count of messages published "out" of an exchange, i.e. taking account of routing.    |
|publish_out_details/rate                     |       |                   |     |                                                                                     |
|return_unroutable                            |       |                   |     |Count of messages returned to publisher as unroutable.                               |
|return_unroutable_details/rate               |       |                   |     |                                                                                     |
|redeliver                                    |       |                   |     |Count of subset of messages in deliver_get which had the redelivered flag set.       |
|redeliver_details/rate                       |       |                   |     |

**Node Metrics:**

| Metric Name                                 |Type   | Labels            |Unit |Description                                                                          |
|---------------------------------------------|-------|-------------------|-----|-------------------------------------------------------------------------------------|
|disk_free_alarm			                  |       |                   |     |Whether the disk alarm has gone off.                                                               |
|disk_free				                      |       |                   |     |Disk free space in bytes.                                                                          |
|fd_used				    	              |       |                   |     |used file descriptors.                                                                             |
|mem_alarm		                              |       |                   |     |Whether the memory alarm has gone off.                                                             |
|mem_used		    		                  |       |                   |     |Memory used in bytes.                                                                              |
|partitions		   		                      |       |                   |     |List of network partitions this node is seeing.                                                    |
|run_queue				                      |       |                   |     |Average number of Erlang processes waiting to run.                                                 |
|running					                  |       |                   |     |Boolean for whether this node is up. Obviously if this is false, most other stats will be missing. |
|sockets_used			                      |       |                   |     |File descriptors used as sockets.                                                                  |

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