Ping Integration
================

== Description ==

The ping utility uses the ICMP protocol's mandatory ECHO_REQUEST datagram to elicit an ICMP ECHO_RESPONSE from a host or gateway.

This integration will monitor the status of your hosts by sending ICMP packets via ping command.

Once enabled you will get a default dashboard to help you get started monitoring your hosts.

== Metrics Collected ==

|Metric Name  |Type   |Labels    |Unit       |Description                            |
|-------------|-------|----------|-----------|---------------------------------------|
|ping.sent    |Gauge  |ping_host |packet     |The number of packets transmitted.     |
|ping.received|Gauge  |ping_host |packet     |The number of packets received.        |
|ping.loss_pct|Gauge  |ping_host |percent    |The percentage of packet loss.         |
|ping.min     |Gauge  |ping_host |millisecond|The minimum round-trip time.           |
|ping.avg     |Gauge  |ping_host |millisecond|The average round-trip time.           |
|ping.max     |Gauge  |ping_host |millisecond|The maximum round-trip time.           |
|ping.std_dev |Gauge  |ping_host |millisecond|The standard deviation for round-trips.|

== Installation ==

Just run the ping plugin against your hosts and it will start collecting metrics.

### Plugin Environment Variables

The ping plugin can be customized via environment variables.

|Variable|Default|Description                                                             |
|--------|-------|------------------------------------------------------------------------|
|hosts   |       |The hosts to be tested separated by comma, e.g.: outlyer.com, google.com|
|count   |3      |The number of ICMP Echo Requests to send.                               |

== Changelog ==

|Version|Release Date|Description                                        |
|-------|------------|---------------------------------------------------|
|1.0    |03-Jul-2018 |Initial version of our ping monitoring integration.|
