import unittest

from outlyer_plugin import OutlyerPluginTest

class TestPlugin(unittest.TestCase):

    def test_ntpplugin(self):
        variables = {"drift": "300"}
        output = OutlyerPluginTest.run_plugin("../plugins/ntp.py", variables)
        output.print_output()

if __name__ == '__main__':
    unittest.main()