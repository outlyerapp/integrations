# Kafka Integration

== Description ==

Kafka is used for building real-time data pipelines and streaming apps. It is horizontally scalable, fault-tolerant, 
wicked fast, and runs in production in thousands of companies.

This integration collects all Kafka metrics via JMX so JMX must be enabled for the plugin to connect too. It will automatically
get all metrics for the Kafka Broker, Kafka Consumer (Java only) and Kafka Producers (Java only) across your environment with a single
plugin.

== Metrics Collected ==

|Metric Name                                                         |MBean Query                                                                           |Type   |Labels |Unit        |Description                                                                                                                                                 |
|--------------------------------------------------------------------|--------------------------------------------------------------------------------------|-------|-------|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
|kafka_server_brokertopicmetrics_messagesinpersec_count              |kafka.server:type=BrokerTopicMetrics, name=MessagesInPerSec/Count                     |Gauge  |       |message/sec |Aggregate incoming message rate.                                                                                                                            |
|kafka_server_brokertopicmetrics_bytesinpersec_count                 |kafka.server:type=BrokerTopicMetrics, name=BytesInPerSec/Count                        |Gauge  |       |byte/sec    |Aggregate incoming byte rate.                                                                                                                               |
|kafka_server_brokertopicmetrics_bytesoutpersec_count                |kafka.server:type=BrokerTopicMetrics, name=BytesOutPerSec/Count                       |Gauge  |       |byte/sec    |Aggregate outgoing byte rate.                                                                                                                               |
|kafka_server_replicamanager_underreplicatedpartitions               |kafka.server:type=ReplicaManager, name=UnderReplicatedPartitions/Value                |Gauge  |       |            |Number of under-replicated partitions.                                                                                                                      |
|kafka_server_replicamanager_partitioncount                          |kafka.server:type=ReplicaManager, name=PartitionCount/Value                           |Gauge  |       |            |Number of partitions on this broker.                                                                                                                        |
|kafka_server_replicamanager_isrshrinkspersec                        |kafka.server:type=ReplicaManager, name=IsrShrinksPerSec                               |Gauge  |       |node/sec    |If a broker goes down, ISR for some of the partitions will shrink. When that broker is up again, ISR will be expanded once the replicas are fully caught up.|
|kafka_server_replicamanager_isrexpandspersec                        |kafka.server:type=ReplicaManager, name=IsrExpandsPerSec                               |Gauge  |       |node/sec    |When a broker is brought up after a failure, it starts catching up by reading from the leader. Once it is caught up, it gets added back to the ISR.         |
|kafka_server_replicamanager_leadercount                             |kafka.server:type=ReplicaManager, name=LeaderCount/Value                              |Gauge  |       |            |Number of leaders on this broker.                                                                                                                           |
|kafka_server_kafkarequesthandlerpool_requesthandleravgidlepercent   |kafka.server:type=KafkaRequestHandlerPool, name=RequestHandlerAvgIdlePercent          |Gauge  |       |fraction    |Average fraction of time the request handler threads are idle.                                                                                              |
|kafka_server_sessionexpirelistener_zookeeperdisconnectspersec       |kafka.server:type=SessionExpireListener, name=ZooKeeperDisconnectsPerSec              |Gauge  |       |event/sec   |Number of Zookeeper client disconnects per second.                                                                                                          |
|kafka_server_sessionexpirelistener_zookeeperexpirespersec           |kafka.server:type=SessionExpireListener, name=ZooKeeperExpiresPerSec                  |Gauge  |       |event/sec   |Number of Zookeeper session expirations per second.                                                                                                         |
|kafka_server_replicafetchermanager_maxlag                           |kafka.server:type=ReplicaFetcherManager, name=MaxLag,clientId=Replica                 |Gauge  |       |            |Number of messages the consumer lags behind the producer by.                                                                                                |
|kafka_controller_kafkacontroller_offlinepartitionscount             |kafka.controller:type=KafkaController, name=OfflinePartitionsCount/Value              |Gauge  |       |            |Number of partitions that don’t have an active leader and are hence not writable or readable.                                                               |
|kafka_controller_kafkacontroller_activecontrollercount              |kafka.controller:type=KafkaController, name=ActiveControllerCount/Value               |Gauge  |       |            |Number of active controllers in the cluster.                                                                                                                |
|kafka_network_requestmetrics_requestspersec_count                   |kafka.network:type=RequestMetrics, name=RequestsPerSec,request=*/Count                |Gauge  |request|request/sec |Request rate.                                                                                                                                               |
|kafka_network_requestmetrics_totaltimems                            |kafka.network:type=RequestMetrics, name=TotalTimeMs,request=*                         |Gauge  |request|millisecond |Total time in ms to serve the specified request.                                                                                                            |
|kafka_network_socketserver_networkprocessoravgidlepercent           |kafka.network:type=SocketServer, name=NetworkProcessorAvgIdlePercent/Value            |Gauge  |       |fraction    |Average fraction of time the network processor threads are idle.                                                                                            |
|kafka_cluster_controllerstats_leaderelectionrateandtimems_count     |kafka.controller:type=ControllerStats, name=LeaderElectionRateAndTimeMs/Count         |Gauge  |       |millisecond |Leader election rate and latency.                                                                                                                           |
|kafka_cluster_controllerstats_uncleanleaderelectionspersec_count    |kafka.controller:type=ControllerStats, name=UncleanLeaderElectionsPerSec/Count        |Gauge  |       |event/sec   |Unclean leader election rate.                                                                                                                               |
|java_lang_operatingsystem_openfiledescriptorcount                   |java.lang:type=OperatingSystem/ OpenFileDescriptorCount                               |Gauge  |       |            |Current number of open file descriptors.                                                                                                                    |
|java_lang_operatingsystem_maxfiledescriptorcount                    |java.lang:type=OperatingSystem/ MaxFileDescriptorCount                                |Gauge  |       |            |Max number of file descriptors.                                                                                                                             |
|kafka_producer_producer-metrics_connection-count                    |kafka.producer:type=producer-metrics, client-id=*/connection-count                    |Gauge  |       |            |The current number of active connections.                                                                                                                   |
|kafka_producer_producer-metrics_waiting-threads                     |kafka.producer:type=producer-metrics, client-id=*/waiting-threads                     |Gauge  |       |            |The number of user threads blocked waiting for buffer memory to enqueue their records.                                                                      |
|kafka_producer_producer-metrics_record-send-total                   |kafka.producer:type=producer-metrics, client-id=*/record-send-total                   |Counter|       |            |The total number of records sent.                                                                                                                           |
|kafka_producer_producer-metrics_request-rate                        |kafka.producer:type=producer-metrics, client-id=*/request-rate                        |Gauge  |       |request/sec |The average number of requests sent per second.                                                                                                             |
|kafka_producer_producer-metrics_response-rate                       |kafka.producer:type=producer-metrics, client-id=*/response-rate                       |Gauge  |       |response/sec|The average number of responses received per second.                                                                                                        |
|kafka_producer_producer-metrics_outgoing-byte-rate                  |kafka.producer:type=producer-metrics, client-id=*/outgoing-byte-rate                  |Gauge  |       |byte/sec    |The average number of outgoing bytes sent per second to all servers.                                                                                        |
|kafka_producer_producer-metrics_incoming-byte-rate                  |kafka.producer:type=producer-metrics, client-id=*/incoming-byte-rate                  |Gauge  |       |byte/sec    |The average number of incoming bytes received per second from all servers.                                                                                  |
|kafka_producer_producer-metrics_request-latency-avg                 |kafka.producer:type=producer-metrics, client-id=*/request-latency-avg                 |Gauge  |       |millisecond |The average request latency in ms.                                                                                                                          |
|kafka_producer_producer-metrics_io-wait-time-ns-avg                 |kafka.producer:type=producer-metrics, client-id=*/io-wait-time-ns-avg                 |Gauge  |       |millisecond |The average length of time the I/O thread spent waiting for a socket ready for reads or writes in nanoseconds.                                              |
|kafka_consumer_consumer-fetch-manager-metrics_records-consumed-total|kafka.consumer:type=consumer-fetch-manager-metrics, client-id=*/records-consumed-total|Counter|       |            |The total number of records consumed.                                                                                                                       |
|kafka_consumer_consumer-fetch-manager-metrics_records-consumed-rate |kafka.consumer:type=consumer-fetch-manager-metrics, client-id=*/records-consumed-rate |Gauge  |       |message/sec |The average number of records consumed per second.                                                                                                          |
|kafka_consumer_consumer-fetch-manager-metrics_records-lag-max       |kafka.consumer:type=consumer-fetch-manager-metrics, client-id=*/records-lag-max       |Gauge  |       |            |The maximum lag in terms of number of records for any partition in this window.                                                                             |
|kafka_consumer_consumer-fetch-manager-metrics_bytes-consumed-rate   |kafka.consumer:type=consumer-fetch-manager-metrics, client-id=*/bytes-consumed-rate   |Gauge  |       |byte/sec    |The average number of bytes consumed per second.                                                                                                            |
|kafka_consumer_consumer-fetch-manager-metrics_fetch-rate            |kafka.consumer:type=consumer-fetch-manager-metrics, client-id=*/fetch-rate            |Gauge  |       |            |The number of fetch requests per second.                                                                                                                    |
|kafka_consumer_consumer-fetch-manager-metrics_fetch-latency-avg     |kafka.consumer:type=consumer-fetch-manager-metrics, client-id=*/fetch-latency-avg     |Gauge  |       |millisecond |The average time taken for a fetch request.                                                                                                                 |
|kafka_consumer_consumer-coordinator-metrics_assigned-partitions     |kafka.consumer:type=consumer-coordinator-metrics, client-id=*/assigned-partitions     |Gauge  |       |            |The number of partitions currently assigned to this consumer.                                                                                               |
|kafka_consumer_consumer-coordinator-metrics_commit-total            |kafka.consumer:type=consumer-coordinator-metrics, client-id=*/commit-total            |Gauge  |       |            |The total number of commit calls.                                                                                                                           |
|kafka_consumer_consumer-coordinator-metrics_join-total              |kafka.consumer:type=consumer-coordinator-metrics, client-id=*/join-total              |Gauge  |       |            |The total number of group joins.                                                                                                                            |
|kafka_consumer_consumer-coordinator-metrics_sync-total              |kafka.consumer:type=consumer-coordinator-metrics, client-id=*/sync-total              |Gauge  |       |            |The total number of group syncs.                                                                                                                            |
|kafka_consumer_consumer-coordinator-metrics_commit-rate             |kafka.consumer:type=consumer-coordinator-metrics, client-id=*/commit-rate             |Gauge  |       |commit/sec  |The number of commit calls per second.                                                                                                                      |
|kafka_consumer_consumer-coordinator-metrics_commit-latency-avg      |kafka.consumer:type=consumer-coordinator-metrics, client-id=*/commit-latency-avg      |Gauge  |       |millisecond |The average time taken for a commit request.                                                                                                                |
|kafka_consumer_consumer-coordinator-metrics_join-rate               |kafka.consumer:type=consumer-coordinator-metrics, client-id=*/join-rate               |Gauge  |       |event/sec   |The number of group joins per second.                                                                                                                       |
|kafka_consumer_consumer-coordinator-metrics_sync-rate               |kafka.consumer:type=consumer-coordinator-metrics, client-id=*/sync-rate               |Gauge  |       |event/sec   |The number of group syncs per second.                                                                                                                       |

== Installation ==

This integration requires that JMX be enabled on Kafka servers, producers and consumers. To enable JMX on a Kafka broker, first edit the `kafka-run-class.sh` script and add the `-Djava.rmi.server.hostname` parameter with the corresponding server IP:

```
KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false  -Dcom.sun.management.jmxremote.ssl=false -Djava.rmi.server.hostname=<SERVER_IP_HERE> "
```

Then, set the `JMX_PORT` environment variable before starting Kafka, for example:

```
JMX_PORT=55555 \
nohup ~/kafka/bin/kafka-server-start.sh ~/kafka/config/server.properties \
> ~/kafka/kafka.log 2>&1 &
```

To set security on JMX, you can follow the SSL and authentication sections [in this guide](https://docs.oracle.com/javase/8/docs/technotes/guides/management/agent.html).

If you have already setup JMX for Kafka, make sure you supply the correct port number in the configuration.

Similarly, producers and consumers should also have JMX enabled.

### Plugin Environment Variables

The Kafka plugin can be customized via environment variables.

|Variable |Default     |Description                        |
|---------|------------|-----------------------------------|
|host     |localhost   |Broker/Producer/Consumer host.      |
|port     |9999        |Broker/Producer/Consumer JMX port.  |

== Changelog ==

|Version|Release Date|Description                                         |
|-------|------------|----------------------------------------------------|
|1.0    |17-May-2018 |Initial version of our Kafka  monitoring integration|

