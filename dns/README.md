DNS Check Integration
=====================

== Description ==

This integration monitors the resolvability of and lookup times for any DNS records using nameservers of your choosing.

== Metrics Collected ==

|Metric Name      |Type   |Labels                           |Unit   |Description                                          |
|-----------------|-------|---------------------------------|-------|-----------------------------------------------------|
|dns.response_time|gauge  |record, record_type, nameserver|Seconds|The response time of the DNS lookup on the nameserver|

== Installation ==

Just install this integration and create a new check to run this integration from one of your agents. The plugin
takes the following check variables:

|Variable       |Default     |Required?|Description                                                                                                   |
|---------------|------------|---------|--------------------------------------------------------------------------------------------------------------|
|record         |            |Yes      |The hostname to look up.                                                                                      |
|record_type    |A           |         |The DNS record type to look up.                                                                               |
|nameserver     |            |         |Use a specific nameserver otherwise will use the local network settings nameserver. Must be set as IP address.|
|nameserver_port|            |         |Set the port number of the nameserver if specifying a specific nameserver to use.                             |
|timeout        |5           |         |Override the default lookup timeout in seconds.                                                               |

== Changelog ==

|Version|Release Date|Description                                          |
|-------|------------|-----------------------------------------------------|
|1.0    |17-Jul-2018 |Initial version of the DNS Check Integration.        |
