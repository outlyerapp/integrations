import time

from outlyer_agent.collection import Status, Plugin, PluginTarget
from outlyer_agent.java import MetricType
from outlyer_agent.java.request import JmxQuery, JmxAttribute
from outlyer_agent.java.thread import JvmTask


class KafkaPlugin(Plugin):
    def collect(self, target: PluginTarget):
        time_now = time.monotonic()

        host = target.get('host', 'localhost')
        port = target.get('port', 55555)
        jmx_url = f'service:jmx:rmi:///jndi/rmi://{host}:{port}/jmxrmi'

        response = JvmTask().get_metrics(
            jmx_url,

            # Controller metrics
            JmxQuery('kafka_controller_{name}_{attr}',
                     MetricType.GAUGE,
                     'kafka.controller:type=KafkaController,*',
                     JmxAttribute('Value')),
            JmxQuery('kafka_controller_stats_{name}',
                     MetricType.COUNTER,
                     'kafka.controller:type=ControllerStats,*',
                     JmxAttribute('Count')),

            # Network metrics
            JmxQuery('kafka_network_processor_idle_percent_{networkProcessor}',
                     MetricType.GAUGE,
                     'kafka.network:type=Processor,name=IdlePercent,*',
                     JmxAttribute('Value')),
            JmxQuery('kafka_network_processor_avg_idle_percent',
                     MetricType.GAUGE,
                     'kafka.network:type=SocketServer,name=NetworkProcessorAvgIdlePercent',
                     JmxAttribute('Value')),
            JmxQuery('kafka_network_request_metrics_{name}_{request}',
                     MetricType.COUNTER,
                     'kafka.network:type=RequestMetrics,*',
                     JmxAttribute('Count')),
            JmxQuery('kafka_network_request_channel_{name}',
                     MetricType.GAUGE,
                     'kafka.network:type=RequestChannel,name=RequestQueueSize,*',
                     JmxAttribute('Value')),
            JmxQuery('kafka_network_request_channel_{name}_{processor}',
                     MetricType.GAUGE,
                     'kafka.network:type=RequestChannel,name=ResponseQueueSize,*',
                     JmxAttribute('Value')),

            # Server metrics
            JmxQuery('kafka_server_broker_state',
                     MetricType.GAUGE,
                     'kafka.server:type=KafkaServer,name=BrokerState',
                     JmxAttribute('Value')),
            JmxQuery('kafka_server_purgatory_num_delayed_{delayedOperation}',
                     MetricType.COUNTER,
                     'kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,*',
                     JmxAttribute('Value')),
            JmxQuery('kafka_server_purgatory_size_{delayedOperation}',
                     MetricType.GAUGE,
                     'kafka.server:type=DelayedOperationPurgatory,name=PurgatorySize,*',
                     JmxAttribute('Value')),
            JmxQuery('kafka_server_broker_topic_metrics_{name}',
                     MetricType.COUNTER,
                     'kafka.server:type=BrokerTopicMetrics,*',
                     JmxAttribute('Count')),
            JmxQuery('kafka_server_delayed_fetch_{fetcherType}_{name}',
                     MetricType.COUNTER,
                     'kafka.server:type=DelayedFetchMetrics,*',
                     JmxAttribute('Count')),
            JmxQuery('kafka_server_replica_fetcher_manager_{name}_{clientId}',
                     MetricType.GAUGE,
                     'kafka.server:type=ReplicaFetcherManager,*',
                     JmxAttribute('Value')),
            JmxQuery('kafka_server_replica_manager_{name}',
                     MetricType.COUNTER,
                     'kafka.server:type=ReplicaManager,name=*PerSec',
                     JmxAttribute('Count')),
            JmxQuery('kafka_server_replica_manager_{name}',
                     MetricType.GAUGE,
                     'kafka.server:type=ReplicaManager,name=*Count',
                     JmxAttribute('Value')),
            JmxQuery('kafka_server_replica_manager_{name}',
                     MetricType.GAUGE,
                     'kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions',
                     JmxAttribute('Value')),
            JmxQuery('kafka_server_request_handler_pool_avg_idle_percent',
                     MetricType.COUNTER,
                     'kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent',
                     JmxAttribute('Count')),
        )

        response.upload_target(target)
        return Status.OK