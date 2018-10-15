#!/usr/bin/env python3
import sys

import os
from outlyer_plugin import Plugin, Status


class TestPlugin(Plugin):

    def collect(self, _) -> Status:
        self.logger.info('loggering')
        mg = self.gauge('test_gauge', labels={'bob': '123'})

        mg.set(134)
        return Status.OK


if __name__ == '__main__':
    sys.exit(TestPlugin().run())