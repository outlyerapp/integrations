import unittest
import pprint
import json

from outlyer_plugin import OutlyerPluginTest

class TestPlugin(unittest.TestCase):

    def test_awsec2_discovery_plugin(self):
        variables = {
            'AWS_REGION': 'us-east-1',
#            'AWS_ACCESS_KEY_ID': '',
#            'AWS_SECRET_ACCESS_KEY': ''
        }
        output = OutlyerPluginTest.run_plugin("../plugins/ec2-discovery.py", variables)
        instances = json.loads(output.stdout)
        pprint.pprint(instances)

    def test_aws_ec2_plugin(self):
        # Run discovery script first to get list of instance in account
        variables = {
            'AWS_REGION': 'us-east-1',
            'INSTANCE_LABELS': 'cloud.instance.image_id, cloud.service',
#            'AWS_ACCESS_KEY_ID': '',
#            'AWS_SECRET_ACCESS_KEY': ''
        }
        output = OutlyerPluginTest.run_plugin("../plugins/ec2-discovery.py", variables)
        instances = json.loads(output.stdout)

        pluginvariables = {**variables, **instances['instances'][0]['labels']}
        pluginvariables['hostname'] = instances['instances'][0]['hostname']
        pluginvariables['ip'] = instances['instances'][0]['ip']
        output = OutlyerPluginTest.run_plugin("../plugins/aws-ec2.py", pluginvariables)
        output.print_output()

if __name__ == '__main__':
    unittest.main()
