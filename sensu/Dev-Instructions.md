# Sensu Outlyer Handler Plugin

This readme includes development instructions for building, packaging and testing the Sensu plugin in Ruby.

## Packaging and Publishing



## Testing

First uncomment the settings config on line 73 to set the test account and API key.
Then you can use the following command to test the handler with example Nagios
output data using the following command:

```bash
cat ./test/test-nagios-data.json | ruby ./bin/outlyer-metrics.rb -f nagios
```

Note you will have to override the check timestamp to the current time so your
metrics will appear in Outlyer using the test above:

```ruby
timestamp =  Time.now.to_i * 1000
```