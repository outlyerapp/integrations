import unittest

from outlyer_plugin import OutlyerPluginTest

class TestPlugin(unittest.TestCase):

    def test_sslplugin(self):
        variables = {"host": "outlyer.com"}
        output = OutlyerPluginTest.run_plugin("../plugins/ssl_check.py", variables)
        output.print_output()

if __name__ == '__main__':
    unittest.main()
