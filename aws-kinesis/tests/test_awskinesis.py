import unittest

from outlyer_plugin import OutlyerPluginTest

class TestPlugin(unittest.TestCase):

    def test_awskinesis_plugin(self):
        variables = {
            'AWS_REGION': 'us-west-2',
        }
        output = OutlyerPluginTest.run_plugin("../plugins/aws-kinesis.py", variables)
        output.print_metrics_md()

if __name__ == '__main__':
    unittest.main()
