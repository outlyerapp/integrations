Apache2 Integration
===================

== Description ==

The Apache HTTP Server, colloquially called Apache, is a free and open source cross-platform web server.

This integration will monitor your Apache web server by collecting metrics from its status module, [mod_status](https://httpd.apache.org/docs/current/mod/mod_status.html).

Once enabled you will get a default Apache dashboard to help you get started monitoring your key Apache metrics.

== Metrics Collected ==

|Metric Name                  |Type   |Labels|Unit          |Description                                       |
|-----------------------------|-------|------|--------------|--------------------------------------------------|
|apache2.total_accesses       |Gauge  |      |              |The total number of accesses.                     |
|apache2.uptime               |Gauge  |      |second        |The amount of time the server has been running.   |
|apache2.req_per_sec          |Gauge  |      |request/second|The number of requests performed per second.      |
|apache2.bytes_per_sec        |Gauge  |      |byte/second   |The number of bytes served per second.            |
|apache2.bytes_per_req        |Gauge  |      |byte/second   |The number of bytes served per request.           |
|apache2.busy_workers         |Gauge  |      |worker        |The number of workers serving requests.           |
|apache2.idle_workers         |Gauge  |      |worker        |The number of idle workers.                       |
|apache2.conns_total          |Gauge  |      |connection    |The total number of connections performed.        |
|apache2.conns_async_writing  |Gauge  |      |connection    |The number of asynchronous writes connections.    |
|apache2.conns_async_keepalive|Gauge  |      |connection    |The number of asynchronous keep alive connections.|
|apache2.conns_async_closing  |Gauge  |      |connection    |The number of asynchronous closing connections.   |
|apache2.stats.open           |Gauge  |      |              |Open slot with no current process.                |
|apache2.stats.waiting        |Gauge  |      |worker        |Idle workers waiting for connection.              |
|apache2.stats.starting       |Gauge  |      |worker        |The number of busy workers starting up.           |
|apache2.stats.reading        |Gauge  |      |worker        |The number of busy workers reading request.       |
|apache2.stats.sending        |Gauge  |      |worker        |The number of busy workers sending reply.         |
|apache2.stats.keepalive      |Gauge  |      |worker        |The number of workers busy with keepalive (read). |
|apache2.stats.dnslookup      |Gauge  |      |worker        |The number of workers busy with DNS Lookup.       |
|apache2.stats.closing        |Gauge  |      |worker        |The number of busy workers closing connection.    |
|apache2.stats.logging        |Gauge  |      |worker        |The number of busy workers logging.               |
|apache2.stats.finishing      |Gauge  |      |worker        |The number of busy workers gracefully finishing.  |
|apache2.stats.idle_cleanup   |Gauge  |      |              |The number of idle cleanup of workers.            |

== Installation ==

If `mod_status` is enabled and the `ExtendedStatus` is on (follow the instructions below if it is not), just run the plugin against your Apache web server to start collecting metrics.

### Enable mod_status on Debian

Edit the status module's configuration file `/etc/apache2/mods-enabled/status.conf` and add the following configuration snippet:

```
<IfModule mod_status.c>
...
	ExtendedStatus On

	<Location /server-status>
	    SetHandler server-status
	    Require local
	    Require ip 127.0.0.1
	</Location>
...
</IfModule>
```

Restart Apache to make sure the configuration is applied.

### Enable mod_status on other UNIX-like platforms

Find the Apache main configuration file at `/etc/apache2/apache2.conf`, `/etc/httpd/conf/httpd.conf`, or `/etc/apache2/httpd.conf` (depending on your platform) and make sure the module is loaded by uncommenting the following line:

```
LoadModule status_module libexec/apache2/mod_status.so
```

Also, add the following configuration snippet:

```
<IfModule mod_status.c>
...
	ExtendedStatus On

	<Location /server-status>
	    SetHandler server-status
	    Require local
	    Require ip 127.0.0.1
	</Location>
...
</IfModule>
```

Restart Apache to make sure the configuration is applied.

### Plugin Environment Variables

The Apache plugin can be customized via environment variables.

|Variable       |Default            |Description                          |
|---------------|-------------------|-------------------------------------|
|protocol       |http               |The protocol used (http or https).   |
|port           |80                 |The Apache port.                     |
|status_location|/server-status?auto|The configured `mod_status` location.|

== Changelog ==

|Version|Release Date|Description                                          |
|-------|------------|-----------------------------------------------------|
|1.0    |15-Jun-2018 |Initial version of our Apache monitoring integration.|
