import unittest

from outlyer_plugin import OutlyerPluginTest

class TestPlugin(unittest.TestCase):

    def test_httpplugin(self):
        variables = {"name": "Outlyer", "url": "https://www.outlyer.com", "pattern": "Analytics & Monitoring for Microservices"}
        output = OutlyerPluginTest.run_plugin("../plugins/http_check.py", variables)
        output.print_output()

if __name__ == '__main__':
    unittest.main()
