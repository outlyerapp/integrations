#!/usr/bin/env python3

import sys

from typing import AnyStr

import pyghmi
import pyghmi.exceptions
from pyghmi.ipmi import command

from outlyer_plugin import Status, Plugin


class IPMIPlugin(Plugin):

    def collect(self, _):

        def sanitize_string(s: AnyStr) -> str:
            if isinstance(s, bytes):
                s = s.decode('utf-8', 'ignore')
            return s.translate(str.maketrans(' -.', '___', '+'))

        try:
            host = self.get('host')
            username = self.get('username')
            password = self.get('password')

            if not host or not username or not password:
                self.logger.error('Configuration is incomplete.')
                return Status.UNKNOWN

            cmd = command.Command(bmc=host, userid=username, password=password)
            for sensor in cmd.get_sensor_data():
                if sensor.value:
                    type = sanitize_string(sensor.type)
                    name = sanitize_string(sensor.name)
                    unit = sensor.units
                    self.gauge('ipmi.' + name, {'sensor_type': type, 'uom': unit}).set(float(sensor.value))

            return Status.OK

        except pyghmi.exceptions.IpmiException as ex:
            self.logger.error('Error connecting to IPMI server')
            return Status.UNKNOWN


if __name__ == '__main__':
    sys.exit(IPMIPlugin().run())
