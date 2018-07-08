import unittest

from outlyer_plugin import OutlyerPluginTest

class TestPlugin(unittest.TestCase):

    def test_awsdynamodb_plugin(self):
        variables = {'AWS_REGION': 'us-east-1'}
        output = OutlyerPluginTest.run_plugin("../plugins/aws-dynamodb.py", variables, timeout=30)
        output.print_output()

if __name__ == '__main__':
    unittest.main()
