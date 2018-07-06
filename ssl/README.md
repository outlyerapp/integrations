SSL Integration
===============

== Description ==

Secure Sockets Layer (SSL) is a standard security technology for establishing an encrypted link between a server and a client—typically a web server (website) and a browser, or a mail server and a mail client.

This integration will monitor your SSL certificates by collecting their expiration time.

Once enabled you will get a default SSL dashboard to help you get started monitoring your SSL certificates.

== Metrics Collected ==

|Metric Name       |Type   |Labels         |Unit|Description                                       |
|------------------|-------|---------------|----|--------------------------------------------------|
|ssl.days_remaining|Gauge  |ssl_cert_source|day |The SSL certificate remaining days for expiration.|

== Installation ==

Just run the SSL plugin against your hosts and it will start collecting metrics.

### Plugin Environment Variables

The SSL plugin can be customized via environment variables.

|Variable        |Default|Description                                                                                                                                           |
|----------------|-------|------------------------------------------------------------------------------------------------------------------------------------------------------|
|cert_path       |       |The certificate path in the filesystem, e.g.: /usr/local/nginx/ssl/cert.crt                                                                           |
|host            |       |The remote host where the certificate is installed, e.g.: outlyer.com                                                                                 |
|port            |443    |The host remote port.                                                                                                                                 |
|cert_common_name|       |The certificate CN (Common Name). When specified, it checks whether the CN provided is equal to the CN present in the certificate, e.g.: *.outlyer.com|
|warning_days    |30     |The number of remaining days for a warning condition.                                                                                                 |
|critical_days   |7      |The number of remaining days for a critical condition.                                                                                                |

== Changelog ==

|Version|Release Date|Description                                       |
|-------|------------|--------------------------------------------------|
|1.0    |06-Jul-2018 |Initial version of our SSL monitoring integration.|
