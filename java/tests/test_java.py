import unittest

from outlyer_plugin import OutlyerPluginTest

class TestPlugin(unittest.TestCase):

    def test_javaplugin(self):
        variables = {}
        output = OutlyerPluginTest.run_plugin("../plugins/java.py", variables)
        output.print_output()

if __name__ == '__main__':
    unittest.main()
