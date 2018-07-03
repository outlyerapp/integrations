import unittest

from outlyer_plugin import OutlyerPluginTest

class TestPlugin(unittest.TestCase):

    def test_pingplugin(self):
        variables = {"hosts": "outlyer.com", "count": "3"}
        output = OutlyerPluginTest.run_plugin("../plugins/ping.py", variables)
        output.print_output()

if __name__ == '__main__':
    unittest.main()
