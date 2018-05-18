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

TODO

| Metric Name              |Type   | Labels            |Description                                 |
|--------------------------|-------|-------------------|--------------------------------------------|
|solr.jvm_classes_loaded   |Gauge  |                   |                                            |
|solr.jvm_classes_unloaded |Gauge  |                   |                                            |

== Installation ==

Simply deploy the plugin using a check that selects all your Solr instances via labels. The plugin can
override the following settings with variables:

* `solr_scheme`: The http scheme to connect with (default 'http')
* `port`: The port that the Solr admin is running on (default '8080')
* `solr_admin_url`: The URL to access the Solr Admin APIs without any leading or tailing slashes (default 'solr/admin')
* `username`: If the Admin is behind authentication, the username to connect with (default None)
* `password`: If the Admin is behind authentication, the password to connect with (default None)

== Changelog ==

|Version|Release Date|Description                                         |
|-------|------------|----------------------------------------------------|
|1.0    |17-May-2018 |Initial version                                     |