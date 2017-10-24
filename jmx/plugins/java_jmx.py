import logging

from outlyer_agent.collection import Status, Plugin, PluginTarget
from outlyer_agent.java import load_queries_from_yaml
from outlyer_agent.java.thread import JvmTask

# TODO: calculate derived metrics (rates, percentages, etc.)
# TODO: calculate major/minor GC stats

logger = logging.getLogger(__name__)
REQUIREMENTS = ['JPype1-py3==0.5.5.2']


class JavaJmxPlugin(Plugin):

    def collect(self, target: PluginTarget):

        jmx_url = target.get('service_url')
        if not jmx_url:
            logger.error('JMX service URL not specified in configuration file')
            return Status.UNKNOWN

        queries = load_queries_from_yaml(target.get('queries'))
        with_standards = target.get('standard_metrics', True)

        response = JvmTask().get_metrics(jmx_url, *queries,
                                         include_std_jvm_metrics=with_standards)
        response.upload_target(target)

        return Status.OK


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    task = JvmTask()
    task.get_metrics("service:jmx:rmi:///jndi/rmi://localhost:9010/jmxrmi",
                     include_std_jvm_metrics=True)
    task.shutdown()
