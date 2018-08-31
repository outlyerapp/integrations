import unittest
import pprint

from outlyer_plugin import OutlyerPluginTest

class TestPlugin(unittest.TestCase):

    def test_awsrds_discovery_plugin(self):
        variables = {
            'AWS_REGION': 'us-east-1',
        }
        output = OutlyerPluginTest.run_plugin("../collectors/rds-discovery.py", variables)
        pprint.pprint(output.stdout)

if __name__ == '__main__':
    unittest.main()
