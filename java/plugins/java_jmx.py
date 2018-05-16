#!/usr/bin/env python3

import sys
from jmxquery import JMXConnection, JMXQuery

from outlyer_plugin import Status, Plugin


class JavaJMXPlugin(Plugin):
    def collect(self, _):

        jmx_url = self.get('jmx_url', 'service:jmx:rmi:///jndi/rmi://localhost:9999/jmxrmi')
        jmxConnection = JMXConnection(jmx_url)

        jmxQuery = [
                    # Class Loading
                    JMXQuery("java.lang:type=ClassLoading/LoadedClassCount",
                             metric_name="java_lang_ClassLoading_LoadedClassCount"),

                    JMXQuery("java.lang:type=ClassLoading/UnloadedClassCount",
                             metric_name="java_lang_ClassLoading_UnloadedClassCount"),

                    JMXQuery("java.lang:type=ClassLoading/UnloadedClassCount",
                             metric_name="java_lang_ClassLoading_TotalLoadedClassCount"),


                    # Garbage Collection

                    JMXQuery("java.lang:type=GarbageCollector,name=*/CollectionTime",
                             metric_name="java_lang_GarbageCollector_CollectionTime",
                             metric_labels={"name": "{name}"}),

                    JMXQuery("java.lang:type=GarbageCollector,name=*/CollectionCount",
                             metric_name="java_lang_GarbageCollector_CollectionCount",
                             metric_labels={"name": "{name}"}),

                    # Memory

                    JMXQuery("java.lang:type=Memory/HeapMemoryUsage",
                             metric_name="java_lang_Memory_HeapMemoryUsage_{attributeKey}"),

                    JMXQuery("java.lang:type=Memory/NonHeapMemoryUsage",
                             metric_name="java_lang_Memory_NonHeapMemoryUsage_{attributeKey}"),

                    JMXQuery("java.lang:type=MemoryPool,name=*/Usage",
                             metric_name="java_lang_MemoryPool_Usage_{attributeKey}",
                             metric_labels={"name": "{name}"}),

                    # Runtime

                    JMXQuery("java.lang:type=Runtime/Uptime",
                             metric_name="java_lang_Runtime_Uptime"),

                    # Threading

                    JMXQuery("java.lang:type=Threading/ThreadCount",
                             metric_name="java_lang_Threading_ThreadCount"),

                    JMXQuery("java.lang:type=Threading/PeakThreadCount",
                             metric_name="java_lang_Threading_PeakThreadCount"),

                    JMXQuery("java.lang:type=Threading/DaemonThreadCount",
                             metric_name="java_lang_Threading_DaemonThreadCount"),

                    JMXQuery("java.lang:type=Threading/TotalStartedThreadCount",
                             metric_name="java_lang_Threading_TotalStartedThreadCount")
                    ]

        metrics = jmxConnection.query(jmxQuery)

        for metric in metrics:
            try:
                if (metric.value_type != "String") and (metric.value_type != ""):
                    self.gauge(metric.metric_name, metric.metric_labels).set(metric.value)
            except:
                # Ignore if a new type is returned from JMX that isn't a number
                pass

        return Status.OK


if __name__ == '__main__':
    sys.exit(JavaJMXPlugin().run())