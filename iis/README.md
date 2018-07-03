Internet Information Services (IIS) Integration
===============================================

== Description ==

This integration will monitor your Microsoft Internet Information Services (IIS) web server status and metrics. It relies on
typeperf.exe to get the IIS metrics and appcmd.exe to automatically discover all the sites on your local IIS server, but the list
of sites can be overriden if required to only monitor specific sites you care about.

== Metrics Collected ==

A full list of all the available metrics for IIS can be found
<a href="https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2003/cc786217(v%3dws.10)" target="_blank">here</a>.

|Metric Name                     |Type   |Labels|Unit      |Description                                                                                                           |
|--------------------------------|-------|------|----------|----------------------------------------------------------------------------------------------------------------------|
|iis.service_uptime              |Gauge  |site  |seconds   |The total time since the site was started on IIS.                                                                     |
|iis.bytes_sent_sec              |Gauge  |site  |bytes/s   |The rate, in seconds, at which data bytes have been sent by the WWW service.                                          |
|iis.bytes_received_sec          |Gauge  |site  |bytes/s   |The total bytes of data that have been received by the WWW service since the service started.                         |
|iis.bytes_total_sec             |Gauge  |site  |bytes/s   |The sum of Bytes Sent/sec and Bytes Received/sec.                                                                     |
|iis.current_connections         |Gauge  |site  |count     |The number of active connections to the WWW service.                                                                  |
|iis.files_sent_sec              |Gauge  |site  |files/s   |The rate, in seconds, at which files have been sent.                                                                  |
|iis.files_received_sec          |Gauge  |site  |files/s   |The rate, in seconds, at which files have been received by the WWW service.                                           |
|iis.total_connection_attempts   |Gauge  |site  |count     |The number of connections to the WWW service that have been attempted since the service started.                      |
|iis.maximum_connections         |Gauge  |site  |count     |The maximum number of simultaneous connections made to the WWW service since the service started.                     |
|iis.get_requests_sec            |Gauge  |site  |requests/s|The rate, in seconds, at which HTTP requests that use the GET method have been made to the WWW service.               |
|iis.post_requests_sec           |Gauge  |site  |requests/s|The rate, in seconds, at which HTTP requests that use the POST method have been made to the WWW service.              |
|iis.head_requests_sec           |Gauge  |site  |requests/s|The rate, in seconds, at which HTTP requests that use the HEAD method have been made to the WWW service.              |
|iis.put_requests_sec            |Gauge  |site  |requests/s|The rate, in seconds, at which HTTP requests that use the PUT method have been made to the WWW service.               |
|iis.delete_requests_sec         |Gauge  |site  |requests/s|The rate, in seconds, at which HTTP requests that use the DELETE method have been made to the WWW service.            |
|iis.options_requests_sec        |Gauge  |site  |requests/s|The rate, in seconds, at which HTTP requests that use the OPTIONS method have been made to the WWW service.           |
|iis.trace_requests_sec          |Gauge  |site  |requests/s|The rate, in seconds, at which HTTP requests that use the TRACE method have been made to the WWW service.             |
|iis.not_found_errors_sec        |Gauge  |site  |errors/s  |The rate, in seconds, at which requests were not satisfied by the server because the requested document was not found.|
|iis.locked_errors_sec           |Gauge  |site  |errors/s  |The rate, in seconds, at which requests were not satisfied because the requested document was locked.                 |
|iis.current_anonymous_users     |Gauge  |site  |count     |The number of users who currently have an anonymous request pending with the WWW service.                             |
|iis.current_nonanonymous_users  |Gauge  |site  |count     |The number of users who currently have a nonanonymous request pending with the WWW service.                           |
|iis.cgi_requests_sec            |Gauge  |site  |requests/s|The rate, in seconds, at which CGI requests are being processed simultaneously by the WWW service.                    |
|iis.isapi_extension_requests_sec|Gauge  |site  |requests/s|The rate, in seconds, at which ISAPI extension requests are being processed by the WWW service.                       |

== Installation ==

Just run the IIS plugin on your Windows host.

### Plugin Environment Variables

The IIS plugin can be customized via check variables.

|Variable         |Default     |Description                                                                                                               |
|-----------------|------------|--------------------------------------------------------------------------------------------------------------------------|
|sites            |            |A list of semi-colon seperated sites to monitor if you don't want all the sites on the server monitored.                  |

== Changelog ==

|Version|Release Date|Description                                        |
|-------|------------|---------------------------------------------------|
|1.0    |10-May-2018 |Initial version of our IIS monitoring integration. |
