#!/usr/bin/env python3

import sys
import time

from outlyer_plugin import Plugin, Status
from outlyer_agent.java import MetricType
from outlyer_agent.java.request import JmxQuery, JmxAttribute
from outlyer_agent.java.response import JmxMetric, JmxQueryResponse
from outlyer_agent.java.thread import JvmTask

# TODO: add metrics for each Servlet (controlled by flag)
# TODO: add metrics for each Manager
# TODO: add metrics for each WebModule


class TomcatPlugin(Plugin):

    def collect(self, _):

        host = self.get('host', 'localhost')
        port = self.get('port', 8080)
        jmx_url = f'service:jmx:rmi:///jndi/rmi://{host}:{port}/jmxrmi'

        # These are the metrics we want:
        response = JvmTask().get_metrics(
            jmx_url,
            JmxQuery('tomcat.thread_pool.{attr}',
                     MetricType.GAUGE, 'Catalina:type=ThreadPool,*',
                     JmxAttribute('currentThreadCount'),
                     JmxAttribute('currentThreadsBusy'),
                     JmxAttribute('connectionCount'),
                     JmxAttribute('maxThreads'),
                     JmxAttribute('minSpareThreads'),
                     JmxAttribute('acceptorThreadCount')),
            JmxQuery('tomcat.cache.{attr}',
                     MetricType.GAUGE, 'Catalina:type=Cache,*',
                     JmxAttribute('accessCount'),
                     JmxAttribute('hitsCount')),
            JmxQuery('tomcat.grp.{attr}',
                     MetricType.COUNTER, 'Catalina:type=GlobalRequestProcessor,*',
                     JmxAttribute('bytesReceived'),
                     JmxAttribute('bytesSent'),
                     JmxAttribute('errorCount'),
                     JmxAttribute('processingTime'),
                     JmxAttribute('requestCount'))
        )

        # Calculate derived metrics (rates, percentages, etc.)
        self.do_contexts(response)
        self.do_global_req_procs(response)

        response.upload_target(self)
        return Status.OK

    def do_counter(self, m: JmxMetric) -> None:
        self.counter(m.name, m.labels).set(m.value)

    def do_contexts(self, response: JmxQueryResponse) -> None:

        for context in [x.labels['context'] for x in response.metrics \
                        if x.name.endswith('.access_count')]:

            hits = response.find_one('tomcat.cache.hits_count', context=context)
            access = response.find_one('tomcat.cache.access_count', context=context)
            hit_pct = round((hits.value / access.value) * 100.0, 2)
            labels = hits.labels.copy().update({'uom': '%'})
            self.do_counter(hits)
            self.do_counter(access)
            self.gauge('tomcat.cache.hit_percentage', labels).set(hit_pct)

    def do_global_req_procs(self, response: JmxQueryResponse) -> None:

        for grp in [x.labels['name'] for x in response.metrics \
                    if x.name.startswith('tomcat.grp.')]:

            total_time = response.find_one('tomcat.grp.processing_time', name=grp)
            count = response.find_one('tomcat.grp.request_count', name=grp)

            if count.value > 0:
                avg_time = round(total_time.value / count.value, 3)
                self.gauge('tomcat.grp.average_time').set(avg_time)
            else:
                self.gauge('tomcat.grp.average_time').set(0.0)

            self.do_counter(response.find_one('tomcat.grp.bytes_received', name=grp))
            self.do_counter(response.find_one('tomcat.grp.bytes_sent', name=grp))
            self.do_counter(response.find_one('tomcat.grp.error_count', name=grp))


if __name__ == '__main__':
    sys.exit(TomcatPlugin().run())

