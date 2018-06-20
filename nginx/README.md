Nginx Integration
=================

== Description ==

Nginx is a software for web serving, reverse proxying, caching, load balancing, media streaming, and more. It has both open source and commercial (Nginx Plus) versions.

This integration will help you monitor both Nginx and Nginx Plus by collecting metrics from as follows:

|Version   |Metrics From                                                                      |
|----------|----------------------------------------------------------------------------------|
|Nginx     |Status page via `ngx_http_stub_status_module` module, access log and process info.|
|Nginx Plus|REST API via `ngx_http_api_module` module, access log and process info.           |

Once enabled you will get a default Nginx/Nginx Plus dashboard to help you get started monitoring your key Nginx metrics.

== Metrics Collected ==

|Metric Name                                       |Type |Labels               |Unit       |Nginx Version    |Description                                                                                                                                                    |
|--------------------------------------------------|-----|---------------------|-----------|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
|nginx.connections_accepted                        |Gauge|                     |           |Open source, Plus|The total number of accepted client connections.                                                                                                               |
|nginx.connections_dropped                         |Gauge|                     |           |Open source, Plus|The total number of dropped connections.                                                                                                                       |
|nginx.connections_active                          |Gauge|                     |           |Open source, Plus|The total number of active connections.                                                                                                                        |
|nginx.connections_idle                            |Gauge|                     |           |Open source, Plus|The total number of idle connections.                                                                                                                          |
|nginx.requests_current                            |Gauge|                     |           |Open source, Plus|The total number of current requests.                                                                                                                          |
|nginx.requests_total                              |Gauge|                     |           |Open source, Plus|The total number of requests.                                                                                                                                  |
|nginx_plus.ssl_handshakes                         |Gauge|                     |           |Plus             |The total number of SSL handshakes.                                                                                                                            |
|nginx_plus.ssl_handshakes_failed                  |Gauge|                     |           |Plus             |The total number of SSL handshakes failed.                                                                                                                     |
|nginx_plus.ssl_session_reuses                     |Gauge|                     |           |Plus             |The total number of session reuses.                                                                                                                            |
|nginx_plus.upstream_count                         |Gauge|                     |           |Plus             |The total number of upstreams.                                                                                                                                 |
|nginx_plus.upstream_peer_id                       |Gauge|upstream, peer       |           |Plus             |The server id.                                                                                                                                                 |
|nginx_plus.upstream_peer_weight                   |Gauge|upstream, peer       |           |Plus             |Weight of the server.                                                                                                                                          |
|nginx_plus.upstream_peer_active                   |Gauge|upstream, peer       |           |Plus             |The current number of active connections to this server.                                                                                                       |
|nginx_plus.upstream_peer_requests                 |Gauge|upstream, peer       |           |Plus             |The total number of client requests forwarded to this server.                                                                                                  |
|nginx_plus.upstream_peer_responses_1xx            |Gauge|upstream, peer       |           |Plus             |The total number of 1xx responses from this server.                                                                                                            |
|nginx_plus.upstream_peer_responses_2xx            |Gauge|upstream, peer       |           |Plus             |The total number of 2xx responses from this server.                                                                                                            |
|nginx_plus.upstream_peer_responses_3xx            |Gauge|upstream, peer       |           |Plus             |The total number of 3xx responses from this server.                                                                                                            |
|nginx_plus.upstream_peer_responses_4xx            |Gauge|upstream, peer       |           |Plus             |The total number of 4xx responses from this server.                                                                                                            |
|nginx_plus.upstream_peer_responses_5xx            |Gauge|upstream, peer       |           |Plus             |The total number of 5xx responses from this server.                                                                                                            |
|nginx_plus.upstream_peer_responses_total          |Gauge|upstream, peer       |           |Plus             |The total number of responses from this server.                                                                                                                |
|nginx_plus.upstream_peer_sent                     |Gauge|upstream, peer       |byte       |Plus             |The total number of bytes sent to this server.                                                                                                                 |
|nginx_plus.upstream_peer_received                 |Gauge|upstream, peer       |byte       |Plus             |The total number of bytes received from this server.                                                                                                           |
|nginx_plus.upstream_peer_fails                    |Gauge|upstream, peer       |           |Plus             |The total number of unsuccessful attempts to communicate with the server.                                                                                      |
|nginx_plus.upstream_peer_unavailable              |Gauge|upstream, peer       |           |Plus             |How many times the server became unavailable for client requests (state `unavail`) due to the number of unsuccessful attempts reaching the max_fails threshold.|
|nginx_plus.upstream_peer_health_checks_checks     |Gauge|upstream, peer       |           |Plus             |The total number of health check requests made.                                                                                                                |
|nginx_plus.upstream_peer_health_checks_fails      |Gauge|upstream, peer       |           |Plus             |The number of failed health checks.                                                                                                                            |
|nginx_plus.upstream_peer_health_checks_unhealthy  |Gauge|upstream, peer       |           |Plus             |How many times the server became unhealthy (state “unhealthy”).                                                                                                |
|nginx_plus.upstream_peer_health_checks_last_passed|Gauge|upstream, peer       |           |Plus             |Indicats if the last health check request was successful and passed tests.                                                                                     |
|nginx_plus.upstream_peer_state                    |Gauge|upstream, peer, state|           |Plus             |Current state, which may be one of `up`, `draining`, `down`, `unavail`, `checking`, and `unhealthy`.                                                           |
|nginx.master_proc_count                           |Gauge|                     |           |Open source, Plus|Number of master processes.                                                                                                                                    |
|nginx.worker_proc_count                           |Gauge|                     |           |Open source, Plus|Number of worker processes.                                                                                                                                    |
|nginx.1xx                                         |Gauge|                     |           |Open source, Plus|The total number of 1xx responses.                                                                                                                             |
|nginx.2xx                                         |Gauge|                     |           |Open source, Plus|The total number of 2xx responses.                                                                                                                             |
|nginx.3xx                                         |Gauge|                     |           |Open source, Plus|The total number of 3xx responses.                                                                                                                             |
|nginx.4xx                                         |Gauge|                     |           |Open source, Plus|The total number of 4xx responses.                                                                                                                             |
|nginx.5xx                                         |Gauge|                     |           |Open source, Plus|The total number of 5xx responses.                                                                                                                             |
|nginx.min_request_time                            |Gauge|                     |millisecond|Open source, Plus|The minimum request time.                                                                                                                                      |
|nginx.max_request_time                            |Gauge|                     |millisecond|Open source, Plus|The maximum request time.                                                                                                                                      |
|nginx.1xx_per_sec                                 |Gauge|                     |req/second |Open source, Plus|The total number of 1xx responses per second.                                                                                                                  |
|nginx.2xx_per_sec                                 |Gauge|                     |req/second |Open source, Plus|The total number of 1xx responses per second.                                                                                                                  |
|nginx.3xx_per_sec                                 |Gauge|                     |req/second |Open source, Plus|The total number of 1xx responses per second.                                                                                                                  |
|nginx.4xx_per_sec                                 |Gauge|                     |req/second |Open source, Plus|The total number of 1xx responses per second.                                                                                                                  |
|nginx.5xx_per_sec                                 |Gauge|                     |req/second |Open source, Plus|The total number of 1xx responses per second.                                                                                                                  |
|nginx.requests_per_sec                            |Gauge|                     |req/second |Open source, Plus|The total number of requests per second.                                                                                                                       |

== Installation ==

To enable calculation of response times, you need to define a new access log format that includes `request_time`. Add this to your `nginx.conf` in the `http` block:

```
log_format timed_combined '$remote_addr - $remote_user [$time_local] '
                          '"$request" $status $body_bytes_sent '
                          '$request_time "$http_referer" '
                          '"$http_user_agent"';
```

Then in your log directives, use the `time_combined` format, for example:

```
access_log /var/log/nginx/access.log timed_combined;
```

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
|access_log        |/var/log/nginx/access.log    |The path to Nginx `access.log` file (required).               |
|nginx_plus        |false                        |Set to `true` when using Nginx Plus.                          |
|url_nginx_status  |http://localhost/nginx_status|Only used for Nginx open source. The URL to Nginx Status page.|
|url_nginx_plus_api|http://localhost/api/3       |Only used for Nginx Plus. The URL to Nginx Plus API.          |

### Running on Docker

When running Nginx on Docker, by default, the `access.log` will only be accessible inside the container. As the Nginx plugin requires access to `access.log`, you must expose it to the host by mounting a [Docker Volume](https://docs.docker.com/storage/volumes/), for example, by running the container with the option `-v /var/log/nginx/access.log:/var/log/nginx/access.log`. Also, make sure to allow the host ip on the `location` block.

== Changelog ==

|Version|Release Date|Description                                         |
|-------|------------|----------------------------------------------------|
|1.0    |11-Jun-2018 |Initial version of our Nginx monitoring integration.|
