# Sensu Outlyer Handler Plugin

This readme includes development instructions for building, packaging and testing the Sensu plugin in Ruby.

## Packaging and Publishing

First build the gem:

```
gem build sensu-plugins-outlyer.gemspec
```

Then publish the sensu-plugins-outlyer gem to the Outlyer account on the RubyGems server 
using the following command:

```bash
gem push sensu-plugins-outlyer-<version_number>.gem
```

## Testing

First copy the example config file under `test/test-config.json` to a path outside your 
project and set the account and your API key in the new file. Then set the path to your 
handler configuration file with your API details as an environment variable:

```bash
export SENSU_CONFIG_FILES='/Users/dgildeh/Development/Outlyer/sensu-config.json'
```

Ensure your handler has execution permissions set:

```bash
chmod +x ./bin/outlyer-metrics.rb
```

To run all the unit tests:

```bash
ruby test/test_outlyer_handler.rb 
```

To run a specific unit test:

```bash
ruby -I test test/test_outlyer_handler.rb -n <test_name>
```