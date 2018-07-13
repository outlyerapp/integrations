Outlyer Sensu Handler Integration
=================================

== Description ==

This integration provides instructions to install and use the Outlyer Sensu Handler Integration
to push all your check event metrics and check status's from Sensu checks into Outlyer. It supports
both Nagios checks and Graphite Metric check outputs from Sensu.

Once installed and enabled you should see all your check metrics and check status's in Outlyer to
use on custom dashboards and alerts.

== Metrics Collected ==

The Sensu integration will push any metric collected by your Sensu checks with metric
names namespaced to the check name as follows:

```
<check_name>.<metric_name>
```

In addition the status code of each check is sent as the `service.status` metric
to Outlyer with the label `service: <check_name>`. You will be able to use this
metric to configure dashboad status widgets and service check alerts in Outlyer.

For Nagios checks, the timestamp of when the check was executed is used for all the
metric data points. For Graphite metric checks the timestamp of each metric data
point is used, apart from the service.status which uses the check execution time
like Nagios checks.

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

You can also add the optional `-t` parameter to the handler command to change the default
timeout for Outlyer API requests from 5 seconds. This is useful if you notice the handler
timing out as your checks send more metrics creating larger payloads.

Finally add your Outlyer API configuration at `/etc/sensu/conf.d/outlyer.json`:

```json
{
    "outlyer": {
       "api_key": "<API_KEY>",
       "account": "<ACCOUNT_NAME>" 
    }
}
```

Where:

* **api_key**: Your user's API key generated under user settings
* **account**: The unique account name of the account you want to push metrics too (you will see this in the URL when using the app)

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

## Troubleshooting

If you don't see metrics appearing in Outlyer after enabling the handlers and checks 
you should use the following command to view the Sensu server logs to see if any
errors are being output by the hander:

```bash
tail -f /var/log/sensu/sensu-server.log | grep outlyer
```

== Changelog ==

|Version|Release Date|Description                                          |
|-------|------------|-----------------------------------------------------|
|1.0    |12-Jul-2018 |Initial version of the Outlyer Sensu Handler.        |