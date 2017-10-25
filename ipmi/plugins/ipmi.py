from outlyer_agent.collection import Status, Plugin, PluginTarget, DEFAULT_PLUGIN_EXEC
from typing import AnyStr
import logging
import sys
import pyghmi
import pyghmi.exceptions
from pyghmi.ipmi import command

logger = logging.getLogger(__name__)


class HttpRequestPlugin(Plugin):

    def collect(self, target: PluginTarget):

        def sanitize_string(s: AnyStr) -> str:
            if isinstance(s, bytes):
                s = s.decode('utf-8', 'ignore')
            return s.translate(str.maketrans(' -.', '___', '+'))

        try:
            host = target.get('host')
            username = target.get('username')
            password = target.get('password')

            if not host or not username or not password:
                logger.error('Configuration is incomplete.')
                return Status.UNKNOWN

            cmd = command.Command(bmc=host, userid=username, password=password)
            for sensor in cmd.get_sensor_data():
                if sensor.value:
                    type = sanitize_string(sensor.type)
                    name = sanitize_string(sensor.name)
                    unit = sensor.units
                    target.gauge(name, {'sensor_type': type, 'uom': unit}).set(float(sensor.value))

            return Status.OK

        except pyghmi.exceptions.IpmiException as ex:
            logger.error('Error connecting to IPMI server')
            return Status.UNKNOWN
