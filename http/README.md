HTTP Integration
================

== Description ==

This integration will monitor the status of your local or remote HTTP endpoints by issuing HTTP requests and collecting HTTP response data like response code, time and size.

Once enabled you will get a default HTTP dashboard to help you get started monitoring your HTTP endpoints.

== Metrics Collected ==

|Metric Name       |Type   |Labels|Unit       |Description                    |
|------------------|-------|------|-----------|-------------------------------|
|http.status_code  |Gauge  |site  |code       |The HTTP response code.        |
|http.response_size|Gauge  |site  |byte       |The HTTP response size.        |
|http.response_time|Gauge  |site  |millisecond|The HTTP response elapsed time.|

== Installation ==

Just run the HTTP plugin against your HTTP endpoint and it will start collecting metrics.

### Plugin Environment Variables

The HTTP plugin can be customized via environment variables.

|Variable         |Default     |Description                                                                                                               |
|-----------------|------------|--------------------------------------------------------------------------------------------------------------------------|
|name             |            |The name to assign to this check (available as the `site` label in the dashboard scope)                                   |
|url              |            |The URL to check.                                                                                                         |
|method           |GET         |The HTTP request method. Possible values: GET, POST, PUT, HEAD, PATCH, DELETE and OPTIONS.                                |
|params           |            |The parameters to be added as the URL query string, e.g.: key1:value1,key2:value2 (separated by comma with no whitespaces)|
|headers          |            |The HTTP request headers, e.g.: header1:value1,header2:value2 (separated by comma with no whitespaces)                    |
|data             |            |Optional string data to send in the request.                                                                              |
|pattern          |            |Optional text pattern to search for in the response HTML.                                                                 |
|error_on_redirect|false       |If true, redirect responses (3xx) will result in CRITICAL status.                                                         |
|warning_time     |            |Response time threshold to trigger WARNING status.                                                                        |
|critical_time    |            |Response time threshold to trigger CRITICAL status.                                                                       |
|timeout          |10          |Maximum timeout in seconds before the request times out and fails                                                         |

== Changelog ==

|Version|Release Date|Description                                        |
|-------|------------|---------------------------------------------------|
|1.0    |28-Jun-2018 |Initial version of our HTTP monitoring integration.|
