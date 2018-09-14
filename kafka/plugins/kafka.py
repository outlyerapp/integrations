#!/usr/bin/env python3

import sys
from jmxquery import JMXConnection, JMXQuery
from outlyer_plugin import Status, Plugin

COUNTER_METRICS = [
    'kafka_server_brokertopicmetrics_messagesinpersec_count',
    'kafka_server_brokertopicmetrics_bytesoutpersec_count',
    'kafka_server_brokertopicmetrics_bytesinpersec_count',
    'kafka_network_requestmetrics_requestspersec_count',
    'kafka_network_requestmetrics_totaltimems_count',
]

class KafkaPlugin(Plugin):
    def collect(self, _):
        try:
            host = self.get('host', 'localhost')
            port = self.get('port', 9999)
            jmx_url = f'service:jmx:rmi:///jndi/rmi://{host}:{port}/jmxrmi'

            jmxConnection = JMXConnection(jmx_url)

            jmxQuery = [
                    # UnderReplicatedPartitions
                    JMXQuery("kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions/Value",
                              metric_name="kafka_server_ReplicaManager_UnderReplicatedPartitions"),

                    # OfflinePartitionsCount
                    JMXQuery("kafka.controller:type=KafkaController,name=OfflinePartitionsCount/Value",
                             metric_name="kafka_controller_KafkaController_OfflinePartitionsCount"),

                    # ActiveControllerCount
                    JMXQuery("kafka.controller:type=KafkaController,name=ActiveControllerCount/Value",
                             metric_name="kafka_controller_KafkaController_ActiveControllerCount"),

                    # MessagesInPerSec
                    JMXQuery("kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec/Count",
                             metric_name="kafka_server_BrokerTopicMetrics_MessagesInPerSec_Count"),

                    # BytesInPerSec
                    JMXQuery("kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec/Count",
                             metric_name="kafka_server_BrokerTopicMetrics_BytesInPerSec_Count"),

                    # BytesOutPerSec
                    JMXQuery("kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec/Count",
                             metric_name="kafka_server_BrokerTopicMetrics_BytesOutPerSec_Count"),

                    # RequestsPerSec
                    JMXQuery("kafka.network:type=RequestMetrics,name=RequestsPerSec,request=*/Count",
                             metric_name="kafka_network_RequestMetrics_RequestsPerSec_Count",
                             metric_labels={"request": "{request}"}),

                    # TotalTimeMs
                    JMXQuery("kafka.network:type=RequestMetrics,name=TotalTimeMs,request=*",
                             metric_name="kafka_network_RequestMetrics_TotalTimeMs_{attribute}",
                             metric_labels={"request": "{request}"}),

                    # LeaderElectionsPerSec
                    JMXQuery("kafka.controller:type=ControllerStats,name=LeaderElectionRateAndTimeMs/Count",
                              metric_name="kafka_cluster_ControllerStats_LeaderElectionRateAndTimeMs_Count"),

                    # UncleanLeaderElectionsPerSec
                    JMXQuery("kafka.controller:type=ControllerStats,name=UncleanLeaderElectionsPerSec/Count",
                              metric_name="kafka_cluster_ControllerStats_UncleanLeaderElectionsPerSec_Count"),

                    # PartitionCount
                    JMXQuery("kafka.server:type=ReplicaManager,name=PartitionCount/Value",
                             metric_name="kafka_server_ReplicaManager_PartitionCount"),

                    # ISRShrinkRate
                    JMXQuery("kafka.server:type=ReplicaManager,name=IsrShrinksPerSec",
                             metric_name="kafka_server_ReplicaManager_IsrShrinksPerSec_{attribute}"),

                    # ISRExpandRate
                    JMXQuery("kafka.server:type=ReplicaManager,name=IsrExpandsPerSec",
                             metric_name="kafka_server_ReplicaManager_IsrExpandsPerSec_{attribute}"),

                    # NetworkProcessorAvgIdlePercent
                    JMXQuery("kafka.network:type=SocketServer,name=NetworkProcessorAvgIdlePercent/Value",
                             metric_name="kafka_network_SocketServer_NetworkProcessorAvgIdlePercent"),

                    # RequestHandlerAvgIdlePercent
                    JMXQuery("kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent",
                             metric_name="kafka_server_KafkaRequestHandlerPool_RequestHandlerAvgIdlePercent_{attribute}"),

                    # ZooKeeperDisconnectsPerSec
                    JMXQuery("kafka.server:type=SessionExpireListener,name=ZooKeeperDisconnectsPerSec",
                             metric_name="kafka_server_SessionExpireListener_ZooKeeperDisconnectsPerSec_{attribute}"),

                    # ZooKeeperExpiresPerSec
                    JMXQuery("kafka.server:type=SessionExpireListener,name=ZooKeeperExpiresPerSec",
                             metric_name="kafka_server_SessionExpireListener_ZooKeeperExpiresPerSec_{attribute}"),

                    # LeaderCount
                    JMXQuery("kafka.server:type=ReplicaManager,name=LeaderCount/Value",
                             metric_name="kafka_server_ReplicaManager_LeaderCount"),

                    # MaxLag
                    JMXQuery("kafka.server:type=ReplicaFetcherManager,name=MaxLag,clientId=Replica",
                             metric_name="kafka_server_ReplicaFetcherManager_MaxLag"),

                    # OpenFileDescriptorCount
                    JMXQuery("java.lang:type=OperatingSystem/OpenFileDescriptorCount",
                             metric_name="java_lang_OperatingSystem_OpenFileDescriptorCount"),

                    # MaxFileDescriptorCount
                    JMXQuery("java.lang:type=OperatingSystem/MaxFileDescriptorCount",
                             metric_name="java_lang_OperatingSystem_MaxFileDescriptorCount"),

                    # Producer: connection-count
                    JMXQuery("kafka.producer:type=producer-metrics,client-id=*/connection-count",
                             metric_name="kafka_producer_producer-metrics_connection-count"),

                    # Producer: waiting-threads
                    JMXQuery("kafka.producer:type=producer-metrics,client-id=*/waiting-threads",
                             metric_name="kafka_producer_producer-metrics_waiting-threads"),

                    # Producer: record-send-total
                    JMXQuery("kafka.producer:type=producer-metrics,client-id=*/record-send-total",
                             metric_name="kafka_producer_producer-metrics_record-send-total"),

                    # Producer: request-rate
                    JMXQuery("kafka.producer:type=producer-metrics,client-id=*/request-rate",
                             metric_name="kafka_producer_producer-metrics_request-rate"),

                    # Producer: response-rate
                    JMXQuery("kafka.producer:type=producer-metrics,client-id=*/response-rate",
                             metric_name="kafka_producer_producer-metrics_response-rate"),

                    # Producer: outgoing-byte-rate
                    JMXQuery("kafka.producer:type=producer-metrics,client-id=*/outgoing-byte-rate",
                             metric_name="kafka_producer_producer-metrics_outgoing-byte-rate"),

                    # Producer: incoming-byte-rate
                    JMXQuery("kafka.producer:type=producer-metrics,client-id=*/incoming-byte-rate",
                             metric_name="kafka_producer_producer-metrics_incoming-byte-rate"),

                    # Producer: request-latency-avg
                    JMXQuery("kafka.producer:type=producer-metrics,client-id=*/request-latency-avg",
                             metric_name="kafka_producer_producer-metrics_request-latency-avg"),

                    # Producer: io-wait-time-ns-avg
                    JMXQuery("kafka.producer:type=producer-metrics,client-id=*/io-wait-time-ns-avg",
                             metric_name="kafka_producer_producer-metrics_io-wait-time-ns-avg"),

                    # Consumer: records-consumed-total
                    JMXQuery("kafka.consumer:type=consumer-fetch-manager-metrics,client-id=*/records-consumed-total",
                             metric_name="kafka_consumer_consumer-fetch-manager-metrics_records-consumed-total"),

                    # Consumer: records-consumed-rate
                    JMXQuery("kafka.consumer:type=consumer-fetch-manager-metrics,client-id=*/records-consumed-rate",
                             metric_name="kafka_consumer_consumer-fetch-manager-metrics_records-consumed-rate"),

                    # Consumer: records-lag-max
                    JMXQuery("kafka.consumer:type=consumer-fetch-manager-metrics,client-id=*/records-lag-max",
                             metric_name="kafka_consumer_consumer-fetch-manager-metrics_records-lag-max"),

                    # Consumer: bytes-consumed-rate
                    JMXQuery("kafka.consumer:type=consumer-fetch-manager-metrics,client-id=*/bytes-consumed-rate",
                             metric_name="kafka_consumer_consumer-fetch-manager-metrics_bytes-consumed-rate"),

                    # Consumer: fetch-rate
                    JMXQuery("kafka.consumer:type=consumer-fetch-manager-metrics,client-id=*/fetch-rate",
                             metric_name="kafka_consumer_consumer-fetch-manager-metrics_fetch-rate"),

                    # Consumer: fetch-latency-avg
                    JMXQuery("kafka.consumer:type=consumer-fetch-manager-metrics,client-id=*/fetch-latency-avg",
                             metric_name="kafka_consumer_consumer-fetch-manager-metrics_fetch-latency-avg"),

                    # Consumer: assigned-partitions
                    JMXQuery("kafka.consumer:type=consumer-coordinator-metrics,client-id=*/assigned-partitions",
                             metric_name="kafka_consumer_consumer-coordinator-metrics_assigned-partitions"),

                    # Consumer: commit-total
                    JMXQuery("kafka.consumer:type=consumer-coordinator-metrics,client-id=*/commit-total",
                             metric_name="kafka_consumer_consumer-coordinator-metrics_commit-total"),

                    # Consumer: join-total
                    JMXQuery("kafka.consumer:type=consumer-coordinator-metrics,client-id=*/join-total",
                             metric_name="kafka_consumer_consumer-coordinator-metrics_join-total"),

                    # Consumer: sync-total
                    JMXQuery("kafka.consumer:type=consumer-coordinator-metrics,client-id=*/sync-total",
                             metric_name="kafka_consumer_consumer-coordinator-metrics_sync-total"),

                    # Consumer: commit-rate
                    JMXQuery("kafka.consumer:type=consumer-coordinator-metrics,client-id=*/commit-rate",
                             metric_name="kafka_consumer_consumer-coordinator-metrics_commit-rate"),

                    # Consumer: commit-latency-avg
                    JMXQuery("kafka.consumer:type=consumer-coordinator-metrics,client-id=*/commit-latency-avg",
                             metric_name="kafka_consumer_consumer-coordinator-metrics_commit-latency-avg"),

                    # Consumer: join-rate
                    JMXQuery("kafka.consumer:type=consumer-coordinator-metrics,client-id=*/join-rate",
                             metric_name="kafka_consumer_consumer-coordinator-metrics_join-rate"),

                    # Consumer: sync-rate
                    JMXQuery("kafka.consumer:type=consumer-coordinator-metrics,client-id=*/sync-rate",
                             metric_name="kafka_consumer_consumer-coordinator-metrics_sync-rate"),
                   ]

            metrics = jmxConnection.query(jmxQuery)

            for metric in metrics:
                try:
                    if (metric.value_type != "String") and (metric.value_type != ""):
                        if metric.metric_name.lower() in COUNTER_METRICS:
                            self.counter(metric.metric_name, metric.metric_labels).set(metric.value)
                        else:
                            self.gauge(metric.metric_name, metric.metric_labels).set(metric.value)
                except:
                    # Ignore if a new type is returned from JMX that isn't a number
                    pass


            return Status.OK
        except Exception as ex:
            self.logger.error('Unable to scrape metrics from Kafka')
            return Status.CRITICAL


if __name__ == '__main__':
    sys.exit(KafkaPlugin().run())
