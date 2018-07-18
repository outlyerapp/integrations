import unittest

from outlyer_plugin import OutlyerPluginTest

class TestPlugin(unittest.TestCase):

    def test_dnscheckplugin(self):
        variables = {
            "hostname": "outlyer.com",
            "record_type": "A"
        }
        output = OutlyerPluginTest.run_plugin("../plugins/dns_check.py", variables)
        output.print_output()

if __name__ == '__main__':
    unittest.main()