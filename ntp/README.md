Network Time Protocol Drift Check
=================================

== Description ==

The Network Time Protocol (NTP) integration reports the time offset of the server its running on to a NTP server
on the internet. If the offset is too large it means the time of your server is out of sync. with the rest of the world,
and this can cause issues with viewing your metrics and alerts in Outlyer.

This plugin should be deployed to all your hosts running the agent to ensure metric times are being
reported back to Outlyer accurately for dashboards and alerts.

== Metrics Collected ==

| Metric Name              |Type   | Labels            |Unit |Description                                 |
|--------------------------|-------|-------------------|-----|--------------------------------------------|
|ntp_drift                 |Gauge  |                   |sec  |The time offset of the server in seconds.   |

== Installation ==

Just deploy the NTP plugin using a check with selector 'instance.type:host' to ensure this plugin is running
on all of your hosts. You can override the following settings:

|Variable|Default     |Description                                                            |
|--------|------------|-----------------------------------------------------------------------|
|drift   |300         |The drift period in seconds that is acceptable before the plugin alerts|
|ntp-host|pool.ntp.org|The NTP host to connect to                                             |
|port    |123         |The NTP host port to connect to                                        |
|timeout |5           |The timeout period in seconds to connect to the NTP host               |

== Changelog ==

|Version|Release Date|Description                                         |
|-------|------------|----------------------------------------------------|
|1.0    |20-Mar-2018 |Initial version                                     |
|1.1    |30-May-2018 |Added timeout variable to plugin                    |