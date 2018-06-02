import unittest

from outlyer_plugin import OutlyerPluginTest, OutlyerPluginOutput

class TestPlugin(unittest.TestCase):

    def test_rabbitmqplugin(self):
        variables = {"port": "32785"}
        output = OutlyerPluginTest.run_plugin("../plugins/rabbitmq.py", variables)
        output.print_output()

if __name__ == '__main__':
    unittest.main()