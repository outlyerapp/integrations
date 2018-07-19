Outlyer Sensu Handler Integration
=================================

== Description ==

This integration provides instructions to install and use the Outlyer Sensu Handler Integration
to push all your check event metrics and check status's from Sensu checks into Outlyer. It supports
both Nagios checks and Graphite Metric check outputs from Sensu.

For Graphite metric checks, the handler will transform your metric name schemes into 
dimensional key/value metric labels using schemes.

Once installed and enabled you should see all your check metrics and check status's in Outlyer to
use on custom dashboards and alerts.

== Metrics Collected ==

The Sensu integration will push any metric collected by your Sensu checks with the
label `service:<check_name>` and `source:sensu` added so you can easily filter all your metrics
for a particular check in Outlyer using the `service` label. 

In addition the status code of each check is sent as the `service.status` metric
to Outlyer with the same labels. You will be able to use this metric to configure dashboad status
widgets and service check alerts in Outlyer.

## Nagios Checks

For Nagios checks, the timestamp of when the check was executed is used for all the
metric data points. 

## Graphite Metric Checks

For Graphite metric checks the timestamp of each metric data
point is used, apart from the service.status which uses the check execution time
like Nagios checks.

In addition if you configure `schemes` in your Outlyer handler
configuration, your metric paths will be transformed from long Graphite metric names
to a metric name with dimensional key/value labels extracted from the Graphite metric
name path.

Please read the Installation instructions for more information on schemes and how
to use them.

== Installation ==

Firstly install the Outlyer Sensu plugin on your Sensu machine(s) using the following
command:

```bash
sensu-install -p outlyer
```

Next, we’ll enable the handlers by adding it to `/etc/sensu/conf.d/outlyer-handlers.json`:

```json
{
  "handlers": {
    "outlyer-graphite": {
       "type": "pipe",
       "command": "/opt/sensu/embedded/bin/outlyer-metrics.rb"
    },
    "outlyer-nagios": {
       "type": "pipe",
       "command": "/opt/sensu/embedded/bin/outlyer-metrics.rb -f nagios"
    }
  }
}
```

Two handlers have been configured, one for your Nagios checks `outlyer-nagios` and
one for your Graphite metric checks `outlyer-graphite`. You can refer to these handlers
in your check configurations to ensure they are handled by the Outlyer handler with
the correct check output parsing. 

In addition, the optional command line options are accepted by the handler:

* **-t**: Use this to change the API request timeout to Outlyer. This may need increasing
if the volume of metrics being sent per check increases substantially. By default it is 5
seconds which is more than enough for most Sensu checks.
* **-d**: Add this flag to enable debugging output of the handler. This will show you
the final payload being posted to Outlyer and other data to help debug if you don't
see metrics in Outlyer after the check runs successfully. **Do not switch this on in production
unless troubleshooting as it will increase your Sensu logging substantially!**

Finally add your Outlyer API configuration at `/etc/sensu/conf.d/outlyer.json`:

```json
{
    "outlyer": {
       "api_key": "<API_KEY>",
       "account": "<ACCOUNT_NAME>",
       "schemes": [
            {
                "filter": "*.*.*.*.*.*",
                "template": "host.host.host.host.name.name"
            }
       ]
    }
}
```

Where:

* **api_key**: Your user's API key generated under user settings
* **account**: The unique account name of the account you want to push metrics too (you will see this in the URL when using the app)
* **schemes**: (Optional) Define your Graphite naming schemes here to transform your metric name schemes into labels for outlyer. 
Read more on schemes below. If this is removed all Graphite metrics will be sent as-is. However if your Graphite metric names are longer
than 80 characters the metric name will be truncated to the last 80 characters. Using Schemes is recommended to ensure all your metrics
are sent with labels so they are easily discoverable in Outlyer.

Finally restart your Sensu server so the new handler is enabled:

```bash
systemctl restart sensu-{server,api}
```

You will need to add the handler to all the checks you want metrics sent to Outlyer for by adding
`outlyer-nagios` or `outlyer-graphite` to your check handlers configuration as appropriate. Once
your checks have been configured to use the Outlyer handler you should start seeing all your
metrics from your configured Sensu checks appearing in Outlyer shortly afterwards.

Also ensure any Sensu checks that send metrics have type `metric` otherwise the output will not
be processed everytime the check runs.

Please read the Metrics Collected section of this guide to understand how your check metrics
are sent to Outlyer.

## Schemes

Outlyer, like most modern monitoring systems, using dimensional metrics. This means that properties about
the metric such as server, region, environment etc. are encoded as key/value labels on the metric. However
most Sensu metric checks use the older Graphite metric format. Graphite doesn't support metric labels
so instead encodes all the properties of the metric into a very long metric name with properties
separated by full-stops. If you have used the `--scheme` command line option for your Sensu
metric checks to append these properties to your metric names, you will need to define a scheme
for your checks in your Outlyer handler configuration.

The schemes can be optionally added to your `/etc/sensu/conf.d/outlyer.json` configuration file to define
a list of filters and templates for the different metrics being sent from your Sensu Graphite metric checks.

If no schemes are provided, it will send the metric name as-is, truncating to the last 80 characters of the metric
name if its longer than 80 characters. However if schemes is provided and no filter match is found for the metric,
the handler will only return the `service.status` metric with a status code of 3 (UNKNOWN) so you can easily setup
alerts in Outlyer to let you know if the handler is dropping metrics for your checks if the metric parsing is not
setup correctly.

The schemes is an array of scheme objects, which include a filter property and template as below:

```json
{
    "filter": "*.*.*.*.*.*",
    "template": "host.host.host.host.name.name"
}
```

where:

* **filter**: Filter is the format of the metrics to match your metrics against, if multiple filters match, the first scheme filter in the
schemes array will be used.
* **template**: The template used to parse the matched graphite metric into labeled metrics. The `name` label to determine the parts that
include the metric name (i.e. cpu-pcnt-usage.guest) are mandatory, and `host` can be used if the hostname of where the metric is from is in
the metric path. Using `host` will override the host name used to run the sensu check when sending the metric to Outlyer, otherwise it will
use the client name of the client that ran the check as the host.

As an example assume we have the following metric:

```
DEV.us-east-1.emailapp.ip-10-127-222-123.us-east-2.compute.internal.cpu-pcnt-usage.guest 12.3 1531798162
```

The following filters will match:

```
*.*.*.*.*.*.*.*.*               # Any metric with 9 dot seperated parts
DEV.*.*.*.*.*.*.*.*             # Any metric starting with DEV followed by 8 parts
DEV.*.emailapp.*.*.*.*.*.*      # Any metric starting with DEV, followed by anything, then emailapp, then 6 parts
```

Once matched, you can then apply a template to extract the labels from the dot-seperated metric parts:

```
environment.region.application.host.host.host.host.name.name
```

Using the same label name over multiple parts will combine the parts into a single label value. This will create the following data-point
in Outlyer:

```
{
      "host": "ip-10-127-222-123.us-east-2.compute.internal",
      "labels": {
        "environment": "dev",
        "region": "us-east-1",
        "application": "emailapp"
      },
      "name": "cpu-pcnt-usage.guest",
      "timestamp": 1531798162000,
      "type": "gauge",
      "value": 12.3
}
```

You will now be able to filter your Sensu Graphite metrics using the host, metic name or any of the labels to build advanced analytics
queries in Outlyer.

## Upgrading

If you need to upgrade your Outlyer handler to a newer version you can use the following
command which will force Sensu to upgrade the handler to a specific version:

```bash
sensu-install -p outlyer:<VERSION>
```
You can find a list of all the versions <a href="https://rubygems.org/gems/sensu-plugins-outlyer" target="_blank">here</a>.

## Troubleshooting

If you don't see metrics appearing in Outlyer after enabling the handlers and checks 
you should use the following command to view the Sensu server logs to see if any
errors are being output by the hander:

```bash
tail -f /var/log/sensu/sensu-server.log | grep outlyer-metrics
```
You can also set the handler command line option `-d true` to enable debug output
for the handler to see the actual payload of metrics being sent to Outlyer.

== Changelog ==

|Version|Release Date|Description                                          |
|-------|------------|-----------------------------------------------------|
|1.0    |12-Jul-2018 |Initial version of the Outlyer Sensu Handler.        |