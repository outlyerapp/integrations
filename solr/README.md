Solr Monitoring Integration
===========================

== Description ==

Solr is an open source enterprise search platform, written in Java, from the Apache Lucene project.
Its major features include full-text search, hit highlighting, faceted search, real-time indexing,
dynamic clustering, database integration, NoSQL features and rich document (e.g., Word, PDF) handling.
Providing distributed search and index replication, Solr is designed for scalability and fault tolerance.
Solr is widely used for enterprise search and analytics use cases.

This integration monitors Apache Solr 6.4 and above using the admin REST API endpoints. For earlier versions
please use our Java JMX integration to monitoring Solr via JMX.

The integration collects key JVM metrics as well as index and request metrics for each Solr Core.

== Metrics Collected ==

| Metric Name                         |Type   | Labels            |Unit       |Description                                       |
|-------------------------------------|-------|-------------------|-----------|--------------------------------------------------|
|solr.jvm_classes_loaded              |Gauge  |                   |           |Total number of classes loaded in JVM.            |
|solr.jvm_classes_unloaded            |Gauge  |                   |           |Total number of classes unloaded from JVM.        |
|solr.jvm_gc_concurrentmarksweep_count|Counter|                   |           |Total number of major garbage collection runs.    |
|solr.jvm_gc_concurrentmarksweep_time |Counter|                   |millisecond|Total time spent doing major garbage collection.  |
|solr.jvm_gc_parnew_count             |Counter|                   |           |Total number of minor garbage collection runs.    |
|solr.jvm_gc_parnew_time              |Counter|                   |millisecond|Total time spent doing minor garbage collection.  |
|solr.jvm_memory_heap_committed       |Gauge  |                   |byte       |Total JVM heap memory committed.                  |
|solr.jvm_memory_heap_init            |Gauge  |                   |byte       |Total JVM heap memory initialised.                |
|solr.jvm_memory_heap_max             |Gauge  |                   |byte       |Max JVM heap memory available.                    |
|solr.jvm_memory_heap_used            |Gauge  |                   |byte       |Total JVM heap memory used.                       |
|solr.jvm_memory_nonheap_committed    |Gauge  |                   |byte       |Total JVM non-heap memory committed.              |
|solr.jvm_memory_nonheap_init         |Gauge  |                   |byte       |Total JVM non-heap memory initialised.            |
|solr.jvm_memory_nonheap_max          |Gauge  |                   |byte       |Max JVM non-heap memory available.                |
|solr.jvm_memory_nonheap_used         |Gauge  |                   |byte       |Total JVM non-heap memory used.                   | 
|solr.jvm_threads_blocked_count       |Gauge  |                   |           |Total number of threads currently blocked.        |
|solr.jvm_threads_count               |Gauge  |                   |           |Total number of threads running.                  |
|solr.jvm_threads_daemon_count        |Gauge  |                   |           |Total number of daemon threads running.           |
|solr.jvm_threads_deadlock_count      |Gauge  |                   |           |Total number of threads currently in deadlock.    |
|solr.jvm_threads_new_count           |Gauge  |                   |           |Total number of new threads created.              |
|solr.jvm_threads_runnable_count      |Gauge  |                   |           |Total number of runnable threads created.         |
|solr.jvm_threads_terminated_count    |Gauge  |                   |           |Total number of threads terminated.               |
|solr.jvm_threads_timed_waiting_count |Gauge  |                   |           |Total number of threads currently timed waiting.  |
|solr.core_numdocs                    |Gauge  |core               |           |Total number of docs indexed in core.             |
|solr.core_maxdocs                    |Gauge  |core               |           |Max number of docs indexed in core.               |
|solr.core_deleteddocs                |Gauge  |core               |           |Total number of docs waiting for deletion in core.|
|solr.core_size_in_bytes              |Gauge  |core               |byte       |Total core index size in bytes.                   |
|solr.core_segmentcount               |Gauge  |core               |           |Total number of segments per index core.          |
|solr.core_index_heap_usage_bytes     |Gauge  |core               |byte       |Total index heap memory usage per core.           |
|solr.core_select_errors              |Counter|core               |           |Total number of select errors per core.           |
|solr.core_select_requests            |Counter|core               |           |Total number of select requests per core.         |
|solr.core_select_timeouts            |Counter|core               |           |Total number of select timeouts per core.         |
|solr.core_update_errors              |Counter|core               |           |Total number of update errors per core.           |
|solr.core_update_requests            |Counter|core               |           |Total number of update requests per core.         |
|solr.core_update_timeouts            |Counter|core               |           |Total number of update timeouts per core.         |
|solr.core_count                      |Gauge  |                   |           |Total number of cores.                            |
|solr.last_commit_complete_age        |Gauge  |                   |second     |Number of seconds since last commit complete.     |
|solr.last_soft_commit_complete_age   |Gauge  |                   |second     |Number of seconds since last soft commit complete.|

== Installation ==

Simply deploy the plugin using a check that selects all your Solr instances via labels. The plugin can
override the following settings with variables:

* `solr_scheme`: The http scheme to connect with (default 'http')
* `port`: The port that the Solr admin is running on (default '8080')
* `solr_admin_url`: The URL to access the Solr Admin APIs without any leading or tailing slashes (default 'solr/admin')
* `username`: If the Admin is behind authentication, the username to connect with (default None)
* `password`: If the Admin is behind authentication, the password to connect with (default None)

== Changelog ==

|Version|Release Date|Description                                        |
|-------|------------|---------------------------------------------------|
|1.0    |17-May-2018 |Initial version of our Solr monitoring integration.|
