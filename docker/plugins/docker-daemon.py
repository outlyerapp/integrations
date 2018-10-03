#!/usr/bin/env python3

import sys
import docker

from outlyer_plugin import Plugin, Status


class DockerPlugin(Plugin):

    def collect(self, _):
        try:
            client = docker.from_env()
            running_containers = client.containers.list(all=True, filters={"status": "running"})
            restarting_containers = client.containers.list(all=True, filters={"status": "restarting"})
            paused_containers = client.containers.list(all=True, filters={"status": "paused"})
            exited_containers = client.containers.list(all=True, filters={"status": "exited"})
            self.gauge('container.count', {"status": "running"}).set(len(running_containers))
            self.gauge('container.count', {"status": "restarting"}).set(len(restarting_containers))
            self.gauge('container.count', {"status": "paused"}).set(len(paused_containers))
            self.gauge('container.count', {"status": "exited"}).set(len(exited_containers))
            return Status.OK
        except Exception as ex:
            self.logger.error('Error collecting Docker metrics: %s', str(ex))
            return Status.CRITICAL


if __name__ == '__main__':
    sys.exit(DockerPlugin().run())
