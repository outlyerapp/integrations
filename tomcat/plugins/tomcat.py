import time

from outlyer_agent.collection import Status, Plugin, PluginTarget, DEFAULT_PLUGIN_EXEC, Metric
from outlyer_agent.java import MetricType
from outlyer_agent.java.request import JmxQuery, JmxAttribute
from outlyer_agent.java.response import JmxMetric, JmxQueryResponse
from outlyer_agent.java.thread import JvmTask

# TODO: add metrics for each Servlet (controlled by flag)
# TODO: add metrics for each Manager
# TODO: add metrics for each WebModule


class TomcatPlugin(Plugin):
    def __init__(self, name, deployments, host, executor=DEFAULT_PLUGIN_EXEC):
        super().__init__(name, deployments, host, executor)
        self.last_collect = None

    def per_second(self, target: PluginTarget, name: str, time_now: float,
                   new_value: JmxMetric, old_value: Metric) -> None:

        if self.last_collect:
            delta = new_value.value - old_value.get()
            elapsed = time_now - self.last_collect
            rate = round(delta / elapsed, 3)
            labels = new_value.labels.copy()
            target.gauge(name, labels=labels).set(rate)

    def do_contexts(self, target: PluginTarget, response: JmxQueryResponse, time_now: float) -> None:

        for context in [x.labels['context'] for x in response.metrics \
                        if x.name.endswith('.access_count')]:

            hits = response.find_one('tomcat.cache.hits_count', context=context)
            access = response.find_one('tomcat.cache.access_count', context=context)
            hit_pct = round((hits.value / access.value) * 100.0, 2)
            labels = hits.labels.copy().update({'uom': '%'})
            target.gauge('tomcat.cache.hit_percentage', labels).set(hit_pct)

    def do_global_req_procs(self, target: PluginTarget, response: JmxQueryResponse, time_now: float) -> None:

        for grp in [x.labels['name'] for x in response.metrics \
                    if x.name.startswith('tomcat.grp.')]:

            total_time = response.find_one('tomcat.grp.processing_time', name=grp)
            count = response.find_one('tomcat.grp.request_count', name=grp)

            if count.value > 0:
                avg_time = round(total_time.value / count.value, 3)
                target.gauge('tomcat.grp.average_time').set(avg_time)
            else:
                target.gauge('tomcat.grp.average_time').set(0.0)

            self.per_second(target, 'tomcat.grp.bytes_received_per_sec', time_now,
                            response.find_one('tomcat.grp.bytes_received', name=grp),
                            target.gauge('tomcat.grp.bytes_received_per_sec'))
            self.per_second(target, 'tomcat.grp.bytes_sent_per_sec', time_now,
                            response.find_one('tomcat.grp.bytes_sent', name=grp),
                            target.gauge('tomcat.grp.bytes_sent_per_sec'))
            self.per_second(target, 'tomcat.grp.bytes_errors_per_sec', time_now,
                            response.find_one('tomcat.grp.error_count', name=grp),
                            target.gauge('tomcat.grp.errors_sent_per_sec'))

    def collect(self, target: PluginTarget):

        time_now = time.monotonic()

        host = target.get('host', 'localhost')
        port = target.get('port', 8080)
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
        self.do_contexts(target, response, time_now)
        self.do_global_req_procs(target, response, time_now)

        response.upload_target(target)
        self.last_collect = time_now
        return Status.OK
