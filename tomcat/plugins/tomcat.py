#!/usr/bin/env python3

import sys
from jmxquery import JMXConnection, JMXQuery

from outlyer_plugin import Status, Plugin

GAUGE_METRICS = [
    'tomcat.threadpool_maxthreads',
    'tomcat.threadpool_current_thread_count',
    'tomcat.threadpool_current_threads_busy',
    'tomcat.global_request_processor_maxTime',
]

class TomcatPlugin(Plugin):

    def collect(self, _):

        jmx_ip = self.get('ip', '127.0.0.1')
        jmx_port = self.get('port', '9012')
        jmx_url = f'service:jmx:rmi:///jndi/rmi://{jmx_ip}:{jmx_port}/jmxrmi'
        jmxConnection = JMXConnection(jmx_url)

        jmxQuery = [

            # Threadpool Metrics
            JMXQuery("Catalina:type=ThreadPool,name=*/maxThreads",
                     metric_name="tomcat.threadpool_maxthreads",
                     metric_labels={"processor": "{name}"}),
            JMXQuery("Catalina:type=ThreadPool,name=*/currentThreadCount",
                     metric_name="tomcat.threadpool_current_thread_count",
                     metric_labels={"processor": "{name}"}),
            JMXQuery("Catalina:type=ThreadPool,name=*/currentThreadsBusy",
                     metric_name="tomcat.threadpool_current_threads_busy",
                     metric_labels={"processor": "{name}"}),

            # Global Request Processor Metrics
            JMXQuery("Catalina:type=GlobalRequestProcessor,name=*",
                     metric_name="tomcat.global_request_processor_{attribute}",
                     metric_labels = {"processor": "{name}"}),

            # Cache Metrics
            JMXQuery("Catalina:type=Cache,host=*,context=*/accessCount",
                     metric_name="tomcat.cache_access_count",
                     metric_labels={"tomcat_host": "{host}",
                                    "context": "{context}"}),
            JMXQuery("Catalina:type=Cache,host=*,context=*/hitsCount",
                     metric_name="tomcat.cache_hits_count",
                     metric_labels={"tomcat_host": "{host}",
                                    "context": "{context}"}),

            # Servlet Metrics
            JMXQuery("Catalina:j2eeType=Servlet,name=*,WebModule=*,*/processingTime",
                     metric_name="tomcat.servlet_processingTime",
                     metric_labels={"webmodule": "{WebModule}",
                                    "servlet": "{name}"}),
            JMXQuery("Catalina:j2eeType=Servlet,name=*,WebModule=*,*/errorCount",
                     metric_name="tomcat.servlet_errorCount",
                     metric_labels={"webmodule": "{WebModule}",
                                    "servlet": "{name}"}),
            JMXQuery("Catalina:j2eeType=Servlet,name=*,WebModule=*,*/requestCount",
                     metric_name="tomcat.servlet_requestCount",
                     metric_labels={"webmodule": "{WebModule}",
                                    "servlet": "{name}"}),

            # JspMonitor Metrics
            JMXQuery("Catalina:type=JspMonitor,name=jsp,WebModule=*,*/jspCount",
                     metric_name="tomcat.jspmonitor_jsp_count",
                     metric_labels={"webmodule": "{WebModule}"}),
            JMXQuery("Catalina:type=JspMonitor,name=jsp,WebModule=*,*/jspReloadCount",
                     metric_name="tomcat.jspmonitor_jsp_reload_count",
                     metric_labels={"webmodule": "{WebModule}"}),
        ]

        metrics = jmxConnection.query(jmxQuery)

        for metric in metrics:
            try:
                if (metric.value_type != "String") and (metric.value_type != ""):
                    if metric.metric_name in GAUGE_METRICS:
                        self.gauge(metric.metric_name, metric.metric_labels).set(metric.value)
                    else:
                        self.counter(metric.metric_name, metric.metric_labels).set(metric.value)
            except:
                # Ignore if a new type is returned from JMX that isn't a number
                pass

        return Status.OK

if __name__ == '__main__':
    sys.exit(TomcatPlugin().run())