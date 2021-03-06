import unittest

from outlyer_plugin import OutlyerPluginTest

class TestPlugin(unittest.TestCase):

    def test_awssns_plugin(self):
        variables = {
            'AWS_REGION': 'us-west-2',
        }
        output = OutlyerPluginTest.run_plugin("../plugins/aws-sns.py", variables)
        output.print_metrics_md()

if __name__ == '__main__':
    unittest.main()
