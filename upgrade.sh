#!/bin/bash

fixed=$( cat $1 | sed -e "s/target: PluginTarget/_/" -e "s/target\./self\./" -e "s/from outlyer_agent\.collection import.*/from outlyer_plugin import Plugin, Status/" -e "s/__init__(self, name, deployments, host, logger, executor=DEFAULT_PLUGIN_EXEC)/__init__(self, logger)/" -e "s/super()\.__init__(name, deployments, host, logger, executor)/super()\.__init__(logger)/" )

cat << EOF
#!/usr/bin/env python3

import sys
EOF
echo "$fixed"
cat << EOF


if __name__ == '__main__':
    sys.exit(Plugin().run())

EOF

