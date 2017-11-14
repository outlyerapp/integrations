import time
import sys

from outlyer_agent.collection import Status, Plugin, PluginTarget
from outlyer_agent.java import MetricType
from outlyer_agent.java.request import JmxQuery, JmxAttribute
from outlyer_agent.java.thread import JvmTask


class KafkaPlugin(Plugin):
    def collect(self, target: PluginTarget):
        time_now = time.monotonic()

        host = target.get('host', 'localhost')
        port = target.get('port', 9999)
        jmx_url = f'service:jmx:rmi:///jndi/rmi://{host}:{port}/jmxrmi'

        response = JvmTask().get_metrics(
            jmx_url,

            # Controller metrics
            JmxQuery('kafka.controller.{name}.{attr}',
                     MetricType.GAUGE,
                     'kafka.controller:type=KafkaController,*',
                     JmxAttribute('Value')),
            JmxQuery('kafka.controller.stats.{name}',
                     MetricType.COUNTER,
                     'kafka.controller:type=ControllerStats,*',
                     JmxAttribute('Count')),

            # Network metrics
            JmxQuery('kafka.network.processor.idle.percent.{networkProcessor}',
                     MetricType.GAUGE,
                     'kafka.network:type=Processor,name=IdlePercent,*',
                     JmxAttribute('Value')),
            JmxQuery('kafka.network.processor.avg.idle.percent',
                     MetricType.GAUGE,
                     'kafka.network:type=SocketServer,name=NetworkProcessorAvgIdlePercent',
                     JmxAttribute('Value')),
            JmxQuery('kafka.network.request.metrics.{name}.{request}',
                     MetricType.COUNTER,
                     'kafka.network:type=RequestMetrics,*',
                     JmxAttribute('Count')),
            JmxQuery('kafka.network.request.channel.{name}',
                     MetricType.GAUGE,
                     'kafka.network:type=RequestChannel,name=RequestQueueSize,*',
                     JmxAttribute('Value')),
            JmxQuery('kafka.network.request.channel.{name}.{processor}',
                     MetricType.GAUGE,
                     'kafka.network:type=RequestChannel,name=ResponseQueueSize,*',
                     JmxAttribute('Value')),

            # Server metrics
            JmxQuery('kafka.server.broker.state',
                     MetricType.GAUGE,
                     'kafka.server:type=KafkaServer,name=BrokerState',
                     JmxAttribute('Value')),
            JmxQuery('kafka.server.purgatory.num.delayed.{delayedOperation}',
                     MetricType.COUNTER,
                     'kafka.server:type=DelayedOperationPurgatory,name=NumDelayedOperations,*',
                     JmxAttribute('Value')),
            JmxQuery('kafka.server.purgatory.size.{delayedOperation}',
                     MetricType.GAUGE,
                     'kafka.server:type=DelayedOperationPurgatory,name=PurgatorySize,*',
                     JmxAttribute('Value')),
            JmxQuery('kafka.server.broker.topic.metrics.{name}',
                     MetricType.COUNTER,
                     'kafka.server:type=BrokerTopicMetrics,*',
                     JmxAttribute('Count')),
            JmxQuery('kafka.server.delayed.fetch.{fetcherType}.{name}',
                     MetricType.COUNTER,
                     'kafka.server:type=DelayedFetchMetrics,*',
                     JmxAttribute('Count')),
            JmxQuery('kafka.server.replica.fetcher.manager.{name}.{clientId}',
                     MetricType.GAUGE,
                     'kafka.server:type=ReplicaFetcherManager,*',
                     JmxAttribute('Value')),
            JmxQuery('kafka.server.replica.manager.{name}',
                     MetricType.COUNTER,
                     'kafka.server:type=ReplicaManager,name=*PerSec',
                     JmxAttribute('Count')),
            JmxQuery('kafka.server.replica.manager.{name}',
                     MetricType.GAUGE,
                     'kafka.server:type=ReplicaManager,name=*Count',
                     JmxAttribute('Value')),
            JmxQuery('kafka.server.replica.manager.{name}',
                     MetricType.GAUGE,
                     'kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions',
                     JmxAttribute('Value')),
            JmxQuery('kafka.server.request.handler.pool.avg.idle.percent',
                     MetricType.COUNTER,
                     'kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent',
                     JmxAttribute('Count')),
        )

        response.upload_target(target)
        return Status.OK
