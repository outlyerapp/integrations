Tomcat Server Integration
=========================

== Description ==

Apache Tomcat, often referred to as Tomcat Server, is an open-source Java Servlet Container developed by the
Apache Software Foundation (ASF). Tomcat implements several Java EE specifications including Java Servlet,
JavaServer Pages (JSP), Java EL, and WebSocket, and provides a "pure Java" HTTP web server environment in
which Java code can run.

This integration will monitor your key Tomcat metrics and availability via JMX so your Tomcat server will need
to have JMX enabled as per the integration instructions provided.

Once enabled you will get a host of Tomcat performance metrics out of the box, and a default Dashboard
template to help you get started monitoring your key Tomcat performance metrics.

== Metrics Collected ==

| Metric Name                                  | MBean Query                                                    |Type   | Labels             |Unit       |Description                                                                                                            |
|----------------------------------------------|----------------------------------------------------------------|-------|--------------------|-----------|-----------------------------------------------------------------------------------------------------------------------|
|tomcat.threadpool_maxthreads                  |Catalina:type=ThreadPool, name=*/maxThreads                     |Gauge  |processor           |           |The maximum number of allowed worker threads.                                                                          |
|tomcat.threadpool_current_thread_count        |Catalina:type=ThreadPool, name=*/currentThreadCount             |Gauge  |processor           |           |The number of threads managed by the thread pool.                                                                      |
|tomcat.threadpool_current_threads_busy        |Catalina:type=ThreadPool, name=*/currentThreadsBusy             |Gauge  |processor           |           |The number of threads that are in use.                                                                                 |
|tomcat.global_request_processor_bytessent     |Catalina:type=GlobalRequestProcessor, name=*/BytesSent          |Counter|processor           |byte       |Bytes per second sent per request processor.                                                                           |
|tomcat.global_request_processor_bytesreceived |Catalina:type=GlobalRequestProcessor, name=*/BytesReceived      |Counter|processor           |byte       |Bytes per second received per request processor.                                                                       |
|tomcat.global_request_processor_processingtime|Catalina:type=GlobalRequestProcessor, name=*/ProcessingTime     |Gaugue |processor           |millisecond|The sum of request processing times across all requests handled by the request processors (in milliseconds) per second.|
|tomcat.global_request_processor_requestcount  |Catalina:type=GlobalRequestProcessor, name=*/RequestCount       |Counter|processor           |           |Bytes per second received per request processor.                                                                       |
|tomcat.global_request_processor_errorcount    |Catalina:type=GlobalRequestProcessor, name=*/ErrorCount         |Counter|processor           |           |The number of erroneous requests received by the servlet per second.                                                   |
|tomcat.global_request_processor_maxtime       |Catalina:type=GlobalRequestProcessor, name=*/MaxTime            |Gauge  |processor           |millisecond|The longest request processing time (in milliseconds).                                                                 |
|tomcat.cache_access_count                     |Catalina:type=Cache,host=*, context=*/accessCount               |Counter|tomcat_host, context|           |The number of accesses to the cache per second.                                                                        |
|tomcat.cache_hits_count                       |Catalina:type=Cache,host=*, context=*/hitsCount                 |Counter|tomcat_host, context|           |The number of cache hits per second.                                                                                   |
|tomcat.servlet_processingTime                 |Catalina:j2eeType=Servlet, name=*,WebModule=*, */processingTime |Counter|webmodule, servlet  |millisecond|The sum of request processing times across all requests to the servlet (in milliseconds) per second.                   |
|tomcat.servlet_errorCount                     |Catalina:j2eeType=Servlet, name=*,WebModule=*, */errorCount     |Counter|webmodule, servlet  |           |The number of erroneous requests received by the servlet per second.                                                   |
|tomcat.servlet_requestCount                   |Catalina:j2eeType=Servlet, name=*,WebModule=*, */requestCount   |Counter|webmodule, servlet  |           |The number of requests received by the servlet per second.                                                             |
|tomcat.jspmonitor_jsp_count                   |Catalina:type=JspMonitor, name=jsp,WebModule=*, */jspCount      |Counter|webmodule           |           |The number of JSPs per second that have been loaded in the web module.                                                 |
|tomcat.jspmonitor_jsp_reload_count            |Catalina:type=JspMonitor, name=jsp,WebModule=*, */jspReloadCount|Counter|webmodule           |           |The number of JSPs per second that have been reloaded in the web module                                                |

== Installation ==

This integration requires JMX to be enabled on the Tomcat JVM.
How you do this depends on the version of Tomcat you have and how 
you're running it.

If you already have JMX Enabled then you can skip to the end of these
instructions.

Full instructions for enabling JMX on Tomcat can be found
[here](https://tomcat.apache.org/tomcat-7.0-doc/monitoring.html) for Tomcat 7.

#### Enabling Tomcat JMX on Linux

If you run Tomcat directly via `catalina.sh`, you can put the JMX ptions into a file called `setenv.sh` in the same folder.

```bash
CATALINA_OPTS=""
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.port=9010"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.rmi.port=9010"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.ssl=false"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.authenticate=false"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.local.only=false"
```

#### Enabling Tomcat JMX on Docker

If you're using the [official Tomcat container](https://hub.docker.com/_/tomcat/), you can
enable JMX by passing options in the `CATALINA_OPTS` environment variable, for example:

```bash
CATALINA_OPTS=""
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.port=9012"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.rmi.port=9012"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.ssl=false"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.authenticate=false"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.local.only=false"

docker run -d -e CATALINA_OPTS=$CATALINA_OPTS tomcat:latest
```

Once enabled, remember to ensure the port 9012 is open so the Outlyer agent can access the port from
outside the container.

#### Enabling Tomcat JMX on Windows

Under your Tomcat installation folder, edit the `setenv.bat` to include the following:

```bash
set CATALINA_OPTS= -Dcom.sun.management.jmxremote
  -Dcom.sun.management.jmxremote.port=9012
  -Dcom.sun.management.jmxremote.rmi.port=9012
  -Dcom.sun.management.jmxremote.ssl=false
  -Dcom.sun.management.jmxremote.authenticate=false
  -Dcom.sun.management.jmxremote.local.only=false
```

---------

By default the integration plugin will connect to `service:jmx:rmi:///jndi/rmi://{jmx_ip}:9012/jmxrmi`,
where the `jmx_ip` is passed in dynamically at runtime by the agent to ensure it connects to the intended instance.
However, if your JMX port is not on port 9012, you can easily override the port using a check variable:

* port: The port Tomcat's JMX is running on

== Changelog ==

|Version|Release Date|Description                                          |
|-------|------------|-----------------------------------------------------|
|1.0    |15-May-2018 |Initial version of our Tomcat monitoring integration.|