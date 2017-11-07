Tomcat Server Integration
=========================

This integration requires JMX to be enabled on the Tomcat JVM. 
How you do this depends on the version of Tomcat you have and how 
you're running it.

If you're using the [official Tomcat container][hub], you can 
enable JMX by passing options in the `CATALINA_OPTS` environment
variable, for example:

```bash
CATALINA_OPTS=""
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.port=9010"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.rmi.port=9010"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.ssl=false"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.authenticate=false"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.local.only=false"

docker run -d -e CATALINA_OPTS=$CATALINA_OPTS tomcat:7.0-jre7-alpine
```

If you run Tomcat directly via `catalina.sh`, you can put the JMX
options into a file called `setenv.sh` in the same folder. 

```bash
CATALINA_OPTS=""
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.port=9010"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.rmi.port=9010"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.ssl=false"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.authenticate=false"
CATALINA_OPTS="${CATALINA_OPTS} -Dcom.sun.management.jmxremote.local.only=false"
```

If you already have `CATALINA_OPTS` defined, skip the first line and
paste the rest.

Once Tomcat starts, you should configure the integration with the
port number you specified for `com.sun.management.jmxremote.port`
(not the HTTP port Tomcat normally listens on).

[hub]: https://hub.docker.com/_/tomcat/