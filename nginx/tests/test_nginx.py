import unittest

from outlyer_plugin import OutlyerPluginTest

class TestPlugin(unittest.TestCase):

    def test_nginxplugin(self):
        variables = {
          "nginx_plus": "true",
          "access_log": "/var/log/nginx/access.log",
        }
        output = OutlyerPluginTest.run_plugin("../plugins/nginx.py", variables)
        output.print_output()
        output.print_metrics_md()

if __name__ == '__main__':
    unittest.main()
