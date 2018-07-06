import unittest

from outlyer_plugin import OutlyerPluginTest

class TestPlugin(unittest.TestCase):

    def test_awsrds_discovery_plugin(self):
        variables = {}
        output = OutlyerPluginTest.run_plugin("../plugins/aws-s3.py", variables, timeout=60)
        output.print_output()

if __name__ == '__main__':
    unittest.main()
