#!/usr/bin/env python3

import sys

from outlyer_plugin import Status, Plugin
from outlyer_agent.java import load_queries_from_yaml
from outlyer_agent.java.thread import JvmTask

# TODO: calculate major/minor GC stats


class JavaJmxPlugin(Plugin):

    def collect(self, _):

        jmx_url = self.get('service_url')
        if not jmx_url:
            self.logger.error('JMX service URL not specified in configuration file')
            return Status.UNKNOWN

        queries = load_queries_from_yaml(self.get('queries'))
        with_standards = self.get('standard_metrics', True)

        response = JvmTask().get_metrics(jmx_url, *queries,
                                         include_std_jvm_metrics=with_standards)
        response.upload_target(self)

        return Status.OK


if __name__ == '__main__':
    sys.exit(JavaJmxPlugin().run())
