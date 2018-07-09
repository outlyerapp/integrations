import unittest

from outlyer_plugin import OutlyerPluginTest

class TestPlugin(unittest.TestCase):

    def test_awssqs_plugin(self):
        variables = {
            'AWS_REGION': 'us-west-2',
        }
        output = OutlyerPluginTest.run_plugin("../plugins/aws-sqs.py", variables)
        output.print_output()

if __name__ == '__main__':
    unittest.main()
