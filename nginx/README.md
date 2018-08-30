Nginx Integration
=================

== Description ==

Nginx is a software for web serving, reverse proxying, caching, load balancing, media streaming, and more. It has both open source and commercial (Nginx Plus) versions.

This integration will help you monitor both Nginx open source and Nginx Plus by collecting metrics as follows:

|Version   |Metrics From                                                                      |
|----------|----------------------------------------------------------------------------------|
|Nginx     |Status page via `ngx_http_stub_status_module` module, access log and process info.|
|Nginx Plus|REST API via `ngx_http_api_module` module, access log and process info.           |

Once enabled you will get a default Nginx/Nginx Plus dashboard to help you get started monitoring your key Nginx metrics.

== Metrics Collected for Nginx Open Source ==

|Metric Name                                       |Type   |Labels               |Unit             |Nginx Version.   |Description                                                                                                                                                    |
|--------------------------------------------------|-------|---------------------|-----------------|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
|nginx.connections_accepted                        |Gauge  |                     |connection       |Open Source      |The total number of accepted client connections.                                                                                                               |
|nginx.connections_handled                         |Gauge  |                     |connection       |Open Source      |The total number of handled client connections.                                                                                                                |
|nginx.connections_dropped_total                   |Gauge  |                     |connection       |Open Source      |The total number of dropped connections.                                                                                                                       |
|nginx.connections_dropped_per_sec                 |Counter|                     |connection/second|Open Source      |The number of dropped connections per second.                                                                                                                  |
|nginx.connections_active                          |Gauge  |                     |connection       |Open Source      |The current number of active connections.                                                                                                                      |
|nginx.connections_reading                         |Gauge  |                     |connection       |Open Source      |The current number of active connections in reading state.                                                                                                     |
|nginx.connections_writing                         |Gauge  |                     |connection       |Open Source      |The current number of active connections in writing state.                                                                                                     |
|nginx.connections_waiting                         |Gauge  |                     |connection       |Open Source      |The current number of active connections in waiting state.                                                                                                     |
|nginx.requests_current                            |Gauge  |                     |request          |Open Source      |The current number of requests.                                                                                                                                |
|nginx.requests_total                              |Gauge  |                     |request          |Open Source      |The total number of requests.                                                                                                                                  |
|nginx.requests_per_sec                            |Counter|                     |request/sec      |Open Source      |The number of requests per second.                                                                                                                             |
|nginx.master_proc_count                           |Gauge  |                     |process          |Open Source, Plus|The number of master processes.                                                                                                                                |
|nginx.worker_proc_count                           |Gauge  |                     |process          |Open Source, Plus|The number of worker processes.                                                                                                                                |
|nginx_plus.connections_accepted_total             |Gauge  |                     |connection       |Plus             |The total number of accepted client connections.                                                                                                               |
|nginx_plus.connections_dropped_total              |Gauge  |                     |connection       |Plus             |The total number of dropped connections.                                                                                                                       |
|nginx_plus.connections_dropped_per_sec            |Counter|                     |connection/second|Plus             |The number of dropped connections per second.                                                                                                                  |
|nginx_plus.connections_active                     |Gauge  |                     |connection       |Plus             |The current number of active connections.                                                                                                                      |
|nginx_plus.connections_idle                       |Gauge  |                     |connection       |Plus             |The current number of idle connections.                                                                                                                        |
|nginx_plus.requests_current                       |Gauge  |                     |request          |Plus             |The current number of requests.                                                                                                                                |
|nginx_plus.requests_total                         |Gauge  |                     |request          |Plus             |The total number of requests.                                                                                                                                  |
|nginx_plus.requests_per_sec                       |Counter|                     |request/second   |Plus             |The number of requests per second.                                                                                                                             |
|nginx_plus.server_zone_requests_total             |Gauge  |server_zone          |request          |Plus             |The total number of requests by zone.                                                                                                                          |
|nginx_plus.server_zone_requests_per_sec           |Counter|server_zone          |request/second   |Plus             |The number of requests per second by zone.                                                                                                                     |
|nginx_plus.server_zone_responses_1xx              |Gauge  |server_zone          |response         |Plus             |The total number of 1xx responses by zone.                                                                                                                     |
|nginx_plus.server_zone_responses_2xx              |Gauge  |server_zone          |response         |Plus             |The total number of 2xx responses by zone.                                                                                                                     |
|nginx_plus.server_zone_responses_3xx              |Gauge  |server_zone          |response         |Plus             |The total number of 3xx responses by zone.                                                                                                                     |
|nginx_plus.server_zone_responses_4xx              |Gauge  |server_zone          |response         |Plus             |The total number of 4xx responses by zone.                                                                                                                     |
|nginx_plus.server_zone_responses_5xx              |Gauge  |server_zone          |response         |Plus             |The total number of 5xx responses by zone.                                                                                                                     |
|nginx_plus.server_zone_responses_total            |Gauge  |server_zone          |response         |Plus             |The total number of responses by zone.                                                                                                                         |
|nginx_plus.server_zone_responses_per_sec          |Counter|server_zone          |response/second  |Plus             |The number of responses per second by zone.                                                                                                                    |
|nginx_plus.server_zone_responses_1xx_per_sec      |Counter|server_zone          |response/second  |Plus             |The number of 1xx responses per second by zone.                                                                                                                |
|nginx_plus.server_zone_responses_2xx_per_sec      |Counter|server_zone          |response/second  |Plus             |The number of 2xx responses per second by zone.                                                                                                                |
|nginx_plus.server_zone_responses_3xx_per_sec      |Counter|server_zone          |response/second  |Plus             |The number of 3xx responses per second by zone.                                                                                                                |
|nginx_plus.server_zone_responses_4xx_per_sec      |Counter|server_zone          |response/second  |Plus             |The number of 4xx responses per second by zone.                                                                                                                |
|nginx_plus.server_zone_responses_5xx_per_sec      |Counter|server_zone          |response/second  |Plus             |The number of 5xx responses per second by zone.                                                                                                                |
|nginx_plus.ssl_handshakes                         |Gauge  |                     |handshake        |Plus             |The total number of SSL handshakes.                                                                                                                            |
|nginx_plus.ssl_handshakes_failed                  |Gauge  |                     |handshake        |Plus             |The total number of SSL handshakes failed.                                                                                                                     |
|nginx_plus.ssl_session_reuses                     |Gauge  |                     |session          |Plus             |The total number of session reuses.                                                                                                                            |
|nginx_plus.upstream_count                         |Gauge  |                     |upstream         |Plus             |The total number of upstreams.                                                                                                                                 |
|nginx_plus.upstream_peer_id                       |Gauge  |upstream, peer       |peer             |Plus             |The server id.                                                                                                                                                 |
|nginx_plus.upstream_peer_weight                   |Gauge  |upstream, peer       |                 |Plus             |Weight of the server.                                                                                                                                          |
|nginx_plus.upstream_peer_active                   |Gauge  |upstream, peer       |peer             |Plus             |The current number of active connections to this server.                                                                                                       |
|nginx_plus.upstream_peer_requests_total           |Gauge  |upstream, peer       |request          |Plus             |The total number of client requests forwarded to this server.                                                                                                  |
|nginx_plus.upstream_peer_requests_per_sec         |Gauge  |upstream, peer       |request/second   |Plus             |The number of client requests per second forwarded to this server.                                                                                             |
|nginx_plus.upstream_peer_responses_1xx            |Gauge  |upstream, peer       |response         |Plus             |The total number of 1xx responses from this server.                                                                                                            |
|nginx_plus.upstream_peer_responses_2xx            |Gauge  |upstream, peer       |response         |Plus             |The total number of 2xx responses from this server.                                                                                                            |
|nginx_plus.upstream_peer_responses_3xx            |Gauge  |upstream, peer       |response         |Plus             |The total number of 3xx responses from this server.                                                                                                            |
|nginx_plus.upstream_peer_responses_4xx            |Gauge  |upstream, peer       |response         |Plus             |The total number of 4xx responses from this server.                                                                                                            |
|nginx_plus.upstream_peer_responses_5xx            |Gauge  |upstream, peer       |response         |Plus             |The total number of 5xx responses from this server.                                                                                                            |
|nginx_plus.upstream_peer_responses_total          |Gauge  |upstream, peer       |response         |Plus             |The total number of responses from this server.                                                                                                                |
|nginx_plus.upstream_peer_responses_per_sec        |Gauge  |upstream, peer       |response/second  |Plus             |The number of responses per second from this server.                                                                                                           |
|nginx_plus.upstream_peer_responses_1xx_per_sec    |Gauge  |upstream, peer       |response/second  |Plus             |The number of 1xx responses per second from this server.                                                                                                       |
|nginx_plus.upstream_peer_responses_2xx_per_sec    |Gauge  |upstream, peer       |response/second  |Plus             |The number of 2xx responses per second from this server.                                                                                                       |
|nginx_plus.upstream_peer_responses_3xx_per_sec    |Gauge  |upstream, peer       |response/second  |Plus             |The number of 3xx responses per second from this server.                                                                                                       |
|nginx_plus.upstream_peer_responses_4xx_per_sec    |Gauge  |upstream, peer       |response/second  |Plus             |The number of 4xx responses per second from this server.                                                                                                       |
|nginx_plus.upstream_peer_responses_5xx_per_sec    |Gauge  |upstream, peer       |response/second  |Plus             |The number of 5xx responses per second from this server.                                                                                                       |
|nginx_plus.upstream_peer_bytes_sent               |Gauge  |upstream, peer       |byte             |Plus             |The total number of bytes sent to this server.                                                                                                                 |
|nginx_plus.upstream_peer_bytes_received           |Gauge  |upstream, peer       |byte             |Plus             |The total number of bytes received from this server.                                                                                                           |
|nginx_plus.upstream_peer_fails                    |Gauge  |upstream, peer       |fail             |Plus             |The total number of unsuccessful attempts to communicate with the server.                                                                                      |
|nginx_plus.upstream_peer_unavailable              |Gauge  |upstream, peer       |                 |Plus             |How many times the server became unavailable for client requests (state `unavail`) due to the number of unsuccessful attempts reaching the max_fails threshold.|
|nginx_plus.upstream_peer_health_checks_checks     |Gauge  |upstream, peer       |                 |Plus             |The total number of health check requests made.                                                                                                                |
|nginx_plus.upstream_peer_health_checks_fails      |Gauge  |upstream, peer       |                 |Plus             |The number of failed health checks.                                                                                                                            |
|nginx_plus.upstream_peer_health_checks_unhealthy  |Gauge  |upstream, peer       |                 |Plus             |How many times the server became unhealthy (state “unhealthy”).                                                                                                |
|nginx_plus.upstream_peer_health_checks_last_passed|Gauge  |upstream, peer       |                 |Plus             |Indicates if the last health check request was successful and passed tests.                                                                                    |
|nginx_plus.upstream_peer_state                    |Gauge  |upstream, peer, state|                 |Plus             |Current state, which may be one of `up`, `draining`, `down`, `unavail`, `checking`, and `unhealthy`.                                                           |

== Installation ==

For Nginx open source, this plugin collects metrics from the Nginx status page generated by the [ngx_http_stub_status](http://nginx.org/en/docs/http/ngx_http_stub_status_module.html) module. To enable it, add a `location` block to your server:

```
http {
    server {
        location /nginx_status {
            stub_status on;
            access_log off;
            allow 127.0.0.1;
            deny all;
        }
    }
}
```

For Nginx Plus, this plugin collects metrics from the Nginx Plus REST API provided by the [ngx_http_api_module](http://nginx.org/en/docs/http/ngx_http_api_module.html#def_nginx_http_upstream) module. To enable it, add a `location` block to your server:

```
http {
    server {
        location /api {
            api write=on;
            allow 127.0.0.1;
            deny all;
        }
    }
}
```

As soon as your Nginx instance is properly set up as described above, just run the Nginx plugin against your Nginx instance to start collecting metrics. When using Nginx Plus, set the environment variable `nginx_plus: true` to collect Nginx Plus metrics.

### Plugin Environment Variables

The Nginx plugin can be customized via environment variables.

|Variable          |Default                      |Description                                                   |
|------------------|-----------------------------|--------------------------------------------------------------|
|nginx_plus        |false                        |Set to `true` when using Nginx Plus.                          |
|url_nginx_status  |http://localhost/nginx_status|Only used for Nginx open source. The URL to Nginx Status page.|
|url_nginx_plus_api|http://localhost/api/3       |Only used for Nginx Plus. The URL to Nginx Plus API.          |

== Changelog ==

|Version|Release Date|Description                                         |
|-------|------------|----------------------------------------------------|
|1.0    |29-Aug-2018 |Initial version of our Nginx monitoring integration.|
