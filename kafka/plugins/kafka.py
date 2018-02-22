#!/usr/bin/env python3

import sys
from jmxquery import JMXConnection, JMXQuery

from outlyer_plugin import Status, Plugin


class KafkaPlugin(Plugin):
    def collect(self, _):

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

                   ]

        metrics = jmxConnection.query(jmxQuery)

        for metric in metrics:
            try:
                if (metric.value_type != "String") or (metric.value_type != ""):
                    self.gauge(metric.metric_name, metric.metric_labels).set(metric.value)
            except:
                # Ignore if a new type is returned from JMX that isn't a number
                pass


        return Status.OK


if __name__ == '__main__':
    sys.exit(KafkaPlugin().run())
