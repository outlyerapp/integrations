Outlyer Sensu Handler Integration
=================================

== Description ==

This integration provides instructions to install and use the Outlyer Sensu Handler Integration
to push all your check event metrics and status codes from Sensu checks into Outlyer. A Sensu
handler is provided by Outlyer which can be installed following the instructions.

Once installed and enabled you should see all your check metrics and status codes in Outlyer to
use on custom dashboards and alerts.

== Metrics Collected ==

The Sensu integration will psuh any metric collected by your Sensu checks to Outlyer. In addition each check
will also automatically generate a metric `service.status` with the label `service: sensu-{check_name}`
which can be used for Outlyer dashboard Status widgets and Service alerts.

== Installation ==

Firstly install the Outlyer Sensu plugin on your Sensu machine using the following
command:

```bash
gem install sensu-plugins-outlyer
```

Next, we’ll enable the handler by adding it to /etc/sensu/conf.d/handlers.json:

```json
{
  "handlers": {
    "outlyer": {
       "type": "pipe",
       "command": "/opt/sensu/embedded/bin/outlyer-metrics.rb"
    }
  }
}
```

and add a configuration at /etc/sensu/conf.d/outlyer.json:

```json
{
    "outlyer": {
       "api_key": "<API_KEY>",
       "account": "<ACCOUNT_NAME>",
       "tags": []
    }
}
```

Where:

* **api_key**: Your user's API key generated under user settings
* **account**: The unique account name of the account you want to push metrics too (you will see this in the URL when using the app)
* **tags**: An array of tags you want to add to all your metrics from Sensu, i.e. region: us-west-1

Finally restart your Sensu server so the new handler is enabled:

```bash
sudo systemctl restart sensu-{server,api}
```

You should start seeing all your metrics from Sensu checks appearing in Outlyer shortly afterwards.

== Changelog ==

|Version|Release Date|Description                                          |
|-------|------------|-----------------------------------------------------|
|1.0    |11-Jul-2018 |Initial version of the Outlyer Sensu Handler.        |