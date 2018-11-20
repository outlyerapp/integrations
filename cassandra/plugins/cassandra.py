#!/usr/bin/env python3

import sys
from jmxquery import JMXConnection, JMXQuery
from outlyer_plugin import Status, Plugin


RATE_METRICS = []

GAUGE_METRICS = [
    'cassandra.reads',
    'cassandra.writes',
    'cassandra.read_latency_99th_percentile',
    'cassandra.write_latency_99th_percentile',
    'cassandra.cache_hits',
    'cassandra.cache_requests',
    'cassandra.storage_load',
    'cassandra.compaction_pending_tasks',
    'cassandra.total_disk_space_used',
    'cassandra.exceptions_read_timeouts',
    'cassandra.exceptions_write_timeouts',
    'cassandra.exceptions_read_unavailables',
    'cassandra.exceptions_write_unavailables',
    'cassandra.threadpool_request_pending_tasks',
    'cassandra.threadpool_request_currently_blocked_tasks',
    'cassandra.open_file_descriptors',
    'cassandra.max_file_descriptors',
]


class CassandraPlugin(Plugin):

    def collect(self, _):
        host = self.get('ip', 'localhost')
        port = self.get('port', 7199)
        jmx_url = f'service:jmx:rmi:///jndi/rmi://{host}:{port}/jmxrmi'

        jmxConnection = JMXConnection(jmx_url)

        jmxQuery = [
            JMXQuery("org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Latency/OneMinuteRate",
              metric_name="cassandra.reads"),

            JMXQuery("org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Latency/OneMinuteRate",
              metric_name="cassandra.writes"),

            JMXQuery("org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Latency/99thPercentile",
              metric_name="cassandra.read_latency_99th_percentile"),

            JMXQuery("org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Latency/99thPercentile",
              metric_name="cassandra.write_latency_99th_percentile"),

            JMXQuery("org.apache.cassandra.metrics:type=Compaction,name=PendingTasks",
              metric_name="cassandra.compaction_pending_tasks"),

            JMXQuery("org.apache.cassandra.metrics:type=ColumnFamily,keyspace=*,scope=*,name=TotalDiskSpaceUsed",
              metric_name="cassandra.total_disk_space_used",
              metric_labels={"keyspace": "{keyspace}"}),

            JMXQuery("org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Timeouts/OneMinuteRate",
              metric_name="cassandra.exceptions_read_timeouts"),

            JMXQuery("org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Timeouts/OneMinuteRate",
              metric_name="cassandra.exceptions_write_timeouts"),

            JMXQuery("org.apache.cassandra.metrics:type=ClientRequest,scope=Read,name=Unavailables/OneMinuteRate",
              metric_name="cassandra.exceptions_read_unavailables"),

            JMXQuery("org.apache.cassandra.metrics:type=ClientRequest,scope=Write,name=Unavailables/OneMinuteRate",
              metric_name="cassandra.exceptions_write_unavailables"),

            JMXQuery("org.apache.cassandra.metrics:type=ThreadPools,path=request,scope=*,name=PendingTasks",
              metric_name="cassandra.threadpool_request_pending_tasks",
              metric_labels={"stage":"{scope}"}),

            JMXQuery("org.apache.cassandra.metrics:type=ThreadPools,path=request,scope=*,name=CurrentlyBlockedTasks/Count",
              metric_name="cassandra.threadpool_request_currently_blocked_tasks",
              metric_labels={"stage":"{scope}"}),

            JMXQuery("java.lang:type=OperatingSystem/OpenFileDescriptorCount",
              metric_name="cassandra.open_file_descriptors"),
            
            JMXQuery("java.lang:type=OperatingSystem/MaxFileDescriptorCount",
              metric_name="cassandra.max_file_descriptors"),
        ]

        metrics = jmxConnection.query(jmxQuery)

        for metric in metrics:
            try:
                if (metric.value_type != "String") and (metric.value_type != ""):
                    if metric.metric_name in RATE_METRICS:
                        self.counter(metric.metric_name, metric.metric_labels).set(metric.value)
                    else:
                        if metric.metric_name == "cassandra.reads" or metric.metric_name == "cassandra.writes":
                            metric.value = "{:.10f}".format(metric.value)
                        
                        self.gauge(metric.metric_name, metric.metric_labels).set(metric.value)
            except:
                # Ignore if a new type is returned from JMX that isn't a number
                pass

        return Status.OK


if __name__ == '__main__':
    sys.exit(CassandraPlugin().run())
