Java Integration
================

== Description ==

A Java virtual machine (JVM) is a virtual machine that enables a computer to run Java programs as well as programs written in other languages and compiled to Java bytecode.

This integration will monitor your JVM by collecting metrics via JMX.

Once enabled you will get a default JVM dashboard to help you get started monitoring your key JVM metrics.

== Metrics Collected ==

|Metric Name                                  |Type   |Labels|Unit       |Description                                         |
|---------------------------------------------|-----  |------|-----------|----------------------------------------------------|
|java_lang_classloading_loadedclasscount      |gauge  |      |           |The number of loaded classes.                       |
|java_lang_garbagecollector_collectiontime    |gauge  |name  |millisecond|The total time spent on garbage collection.         |
|java_lang_garbagecollector_collectioncount   |counter|name  |byte       |The number of garbage collections.                  |
|java_lang_memory_heapmemoryusage_committed   |gauge  |      |byte       |The total Java heap memory committed to be used.    |
|java_lang_memory_heapmemoryusage_init        |gauge  |      |byte       |The initial Java heap memory allocated.             |
|java_lang_memory_heapmemoryusage_max         |gauge  |      |byte       |The maximum Java heap memory available.             |
|java_lang_memory_heapmemoryusage_used        |gauge  |      |byte       |The total Java heap memory used.                    |
|java_lang_memory_nonheapmemoryusage_committed|gauge  |      |byte       |The total Java non-heap memory committed to be used.|
|java_lang_memory_nonheapmemoryusage_init     |gauge  |      |byte       |The initial Java non-heap memory allocated.         |
|java_lang_memory_nonheapmemoryusage_max      |gauge  |      |byte       |The maximum Java non-heap memory available.         |
|java_lang_memory_nonheapmemoryusage_used     |gauge  |      |byte       |The total Java non-heap memory used.                |
|java_lang_runtime_uptime                     |counter|      |second     |The total time the JVM is running.                  |
|java_lang_threading_threadcount              |gauge  |      |           |The number of live threads.                         |
|java_lang_threading_peakthreadcount          |gauge  |      |           |The number of peak threads.                         |
|java_lang_threading_daemonthreadcount        |gauge  |      |           |The number daemon threads.                          |

== Installation ==

Just run the Java plugin against your JVM instance and it will start collecting JVM metrics.

### Plugin Environment Variables

The Java plugin can be customized via environment variables.

|Variable|Default  |Description|
|--------|---------|-----------|
|host    |localhost|JMX host.  |
|port    |9999     |JMX port.  |

== Changelog ==

|Version|Release Date|Description                                       |
|-------|------------|--------------------------------------------------|
|1.0    |12-Jun-2018 |Initial version of our Java monitoring integration|
