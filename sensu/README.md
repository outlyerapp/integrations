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
label `service=sensu.<check_name>` added so you can easily filter all your metrics
for a particular check in Outlyer using the `service` label. 

In addition the status code of each check is sent as the `service.status` metric
to Outlyer with the label `service: sensu.<check_name>`. You will be able to use this
metric to configure dashboad status widgets and service check alerts in Outlyer.

All metrics will also get the `environment` label pulled from the client's environment 
field that ran the check. If this field is an array, all parts of the array will be 
combined into a single string with `-` joining them so you can filter to specific metrics 
in your environments.

## Nagios Checks

For Nagios checks, the timestamp of when the check was executed is used for all the
metric data points. 

## Graphite Metric Checks

For Graphite metric checks the timestamp of each metric data
point is used, apart from the service.status which uses the check execution time
like Nagios checks. In addition if you configure `schemes` in your Outlyer handler
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
* **-d**: Set this to `true` to enable debugging output of the handler. This will show you
the final payload being posted to Outlyer to help debug if you don't see metrics in Outlyer
after the check runs successfully.

Finally add your Outlyer API configuration at `/etc/sensu/conf.d/outlyer.json`:

```json
{
    "outlyer": {
       "api_key": "<API_KEY>",
       "account": "<ACCOUNT_NAME>",
       "schemes": {
            "default": {
                "metric_name_length": 2,
                "scheme": "businessunit.applicationenv.alertgroup.applicationrole.sensuserver.owneremail.runningschedule.host"
            }
    }
}
```

Where:

* **api_key**: Your user's API key generated under user settings
* **account**: The unique account name of the account you want to push metrics too (you will see this in the URL when using the app)
* **schemes**: (Optional) Define your Graphite naming schemes here to transform your metric name schemes into labels for outlyer. 
Read more on schemes below. If this is removed all Graphite metrics will be sent as-is. However if your Graphite metric names are longer
than 80 characters they will be truncated to the last 80 characters. Using Schemes is recommended to ensure all your metrics are sent
with labels so they are easily discoverable in Outlyer.

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

For example if you encode all your metrics with the following path:

```
{environment}.{region}.{team}.{application}.{hostname}.{metric_name}
```

then Outlyer will transform the metric name into just {metric_name} with the labels
environment, region, team, application and host for the rest of the path. This means
you can then use the labels in Outlyer to filter metrics to the specific environment, 
team or host, and then select the metric_name for graphing and alerting.

In order for the metric names to be parsed correctly you need to define schemes in your
Outlyer handler configuration. A `default` configuration can be provided that will be used
across all your checks if you use the same scheme for all your metrics. However additional
configurations can be defined using the check's name in Sensu to define specific schemes
for specific checks. For example if you have a Sensu check with name `metrics_cpu` you can
add the `metrics_cpu` scheme to the list of schemes in the Outlyer configuration with its 
own scheme. If a specific check scheme isn't defined, it will always use the `default` scheme.

The handler will remove the hostname (as these usually contain full-stops in the name) and then
split the metric name into parts broken by full-stops, the same way Graphite splits metrics into
a browsable tree. In your scheme you then define two variables:

* **metric_name_length**: This is the number of parts from the end that are used by the actual metric name. These will be combined to form the final metric name in Outlyer.
* **scheme**: This is the full-stop seperated scheme for the rest of the metric so they can be transformed into labels. The name of the label will be the string provided in the scheme part.

In the example above the following scheme would transform the metrics into labels:
environment, region, team, application, hostname with the metric name being the last 2
parts of the metric name:

```json
"schemes": {
            "default": {
                "metric_name_length": 2,
                "scheme": "environment.region.team.application.hostname"
            }
```

When parsing the metric names in the handler, if the length of the Graphite metric
name differs from the scheme + metric_name_length no metrics will be parsed and sent
to Outlyer and you will see a warning in the Handler output. You can then fix the 
scheme definition for the Handler to start seeing metrics again.

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
tail -f /var/log/sensu/sensu-server.log | grep outlyer
```
You can also set the handler command line option `-d true` to enable debug output
for the handler to see the actual payload of metrics being sent to Outlyer.

== Changelog ==

|Version|Release Date|Description                                          |
|-------|------------|-----------------------------------------------------|
|1.0    |12-Jul-2018 |Initial version of the Outlyer Sensu Handler.        |