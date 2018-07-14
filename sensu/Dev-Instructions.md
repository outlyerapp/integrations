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

First set the path to your handler configuration file with your API details as
an environment variable:

```bash
export SENSU_CONFIG_FILES='/Users/dgildeh/Development/Outlyer/integrations/sensu/test/test-config.json'
```

Then you can use the following command to test the handler with example Nagios
output data using the following command:

```bash
cat ./test/test-nagios-data.json | ruby ./bin/outlyer-metrics.rb -f nagios
```
For Graphite metric test:

```bash
cat ./test/test-graphite-data.json | ruby ./bin/outlyer-metrics.rb
```

Note you will have to override the check timestamp to the current time so your
metrics will appear in Outlyer using the test above:

```ruby
timestamp =  Time.now.to_i * 1000
```