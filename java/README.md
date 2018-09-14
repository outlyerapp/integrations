Java Integration
================

== Description ==

A Java virtual machine (JVM) is a virtual machine that enables a computer to run Java programs as well as programs written in other languages and compiled to Java bytecode.

This integration will monitor your JVM by collecting metrics via JMX.

Once enabled you will get a default JVM dashboard to help you get started monitoring your key JVM metrics.

== Metrics Collected ==

|Metric Name                                  |Type   |Labels|Unit       |Description                                         |
|---------------------------------------------|-------|------|-----------|----------------------------------------------------|
|java_lang_classloading_loadedclasscount      |Gauge  |      |           |The number of loaded classes.                       |
|java_lang_garbagecollector_collectiontime    |Counter|name  |           |The rate of time spent on garbage collection.       |
|java_lang_garbagecollector_collectioncount   |Counter|name  |           |The rate of garbage collections.                    |
|java_lang_memory_heapmemoryusage_committed   |Gauge  |      |byte       |The total Java heap memory committed to be used.    |
|java_lang_memory_heapmemoryusage_init        |Gauge  |      |byte       |The initial Java heap memory allocated.             |
|java_lang_memory_heapmemoryusage_max         |Gauge  |      |byte       |The maximum Java heap memory available.             |
|java_lang_memory_heapmemoryusage_used        |Gauge  |      |byte       |The total Java heap memory used.                    |
|java_lang_memory_nonheapmemoryusage_committed|Gauge  |      |byte       |The total Java non-heap memory committed to be used.|
|java_lang_memory_nonheapmemoryusage_init     |Gauge  |      |byte       |The initial Java non-heap memory allocated.         |
|java_lang_memory_nonheapmemoryusage_max      |Gauge  |      |byte       |The maximum Java non-heap memory available.         |
|java_lang_memory_nonheapmemoryusage_used     |Gauge  |      |byte       |The total Java non-heap memory used.                |
|java_lang_runtime_uptime                     |Gauge  |      |millisecond|The total time the JVM is running.                  |
|java_lang_threading_threadcount              |Gauge  |      |           |The number of live threads.                         |
|java_lang_threading_peakthreadcount          |Gauge  |      |           |The number of peak threads.                         |
|java_lang_threading_daemonthreadcount        |Gauge  |      |           |The number daemon threads.                          |

== Installation ==

This integration requires that JMX be enabled on the JVM. To enable JMX on a the JVM you can add the additional options to your
Java command when starting the JVM:

```
-Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.port=9999
-Dcom.sun.management.jmxremote.rmi.port=9999
-Dcom.sun.management.jmxremote.ssl=false
-Dcom.sun.management.jmxremote.authenticate=false
-Dcom.sun.management.jmxremote.local.only=false
```

### Plugin Environment Variables

The Java plugin can be customized via environment variables.

|Variable|Default  |Description|
|--------|---------|-----------|
|host    |localhost|JMX host.  |
|port    |9999     |JMX port.  |

== Changelog ==

|Version|Release Date|Description                                        |
|-------|------------|---------------------------------------------------|
|1.0    |12-Jun-2018 |Initial version of our Java monitoring integration.|
