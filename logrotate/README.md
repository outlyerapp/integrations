logrotate Integration
=====================

== Description ==

logrotate is a system utility that manages the automatic rotation and compression of log files.

This integration will monitor log files managed by logrotate by collecting metrics from logrotate state file and the log files themselves.

Once enabled you will get a default logrotate dashboard and alert to help you get started monitoring your log files.

== Metrics Collected ==

|Metric Name            |Type   |Labels  |Unit  |Description                                                                                                                  |
|-----------------------|-------|--------|------|-----------------------------------------------------------------------------------------------------------------------------|
|logrotate.last_rotation|Gauge  |log_file|second|The amount of time in seconds since the last rotation.                                                                       |
|logrotate.size_bytes   |Gauge  |log_file|byte  |The current size in bytes of each log file managed by logrotate (that is, each log file present in the logrotate state file).|

== Installation ==

Just run the logrotate plugin against your instances and it will start collecting metrics.

### Plugin Environment Variables

The logrotate plugin can be customized via environment variables.

|Variable       |Default                  |Description                                                                                                                                          |
|---------------|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
|logrotate_state|/var/lib/logrotate/status|Absolute path to logrotate state file (in some non-Debian based distributions you might have to set the path to `/var/lib/logrotate.status` instead).|

== Changelog ==

|Version|Release Date|Description                                             |
|-------|------------|--------------------------------------------------------|
|1.0    |07-Sep-2018 |Initial version of our logrotate monitoring integration.|
