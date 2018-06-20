Elasticsearch Integration
=========================

== Description ==

Elasticsearch is an open source distributed document store and search engine that stores and retrieves data structures in near real-time.

This integration will monitor your Elasticsearch cluster by collecting metrics from its RESTful HTTP APIs.

Once enabled you will get a default Elasticsearch dashboard to help you get started monitoring your key Elasticsearch metrics.

== Metrics Collected ==

|Metric Name                                                         |Type |Labels      |Unit       |Description                                                                    |
|--------------------------------------------------------------------|-----|------------|-----------|-------------------------------------------------------------------------------|
|elasticsearch_cluster_status                                        |Gauge|cluster_name|           |Assumes 0, 1, or 2 if the cluster status is green, yellow or red, respectively.|
|elasticsearch_cluster_active_primary_shards                         |Gauge|cluster_name|           |Number of primary shards active.                                               |
|elasticsearch_cluster_number_of_shards                              |Gauge|cluster_name|           |Total number of shards.                                                        |
|elasticsearch_cluster_relocating_shards                             |Gauge|cluster_name|           |Number of relocating shards.                                                   |
|elasticsearch_cluster_initializing_shards                           |Gauge|cluster_name|           |Number of initializing shards.                                                 |
|elasticsearch_cluster_unassigned_shards                             |Gauge|cluster_name|           |Number of unassigned shards.                                                   |
|elasticsearch_cluster_delayed_unassigned_shards                     |Gauge|cluster_name|           |Number of delayed unassigned shards.                                           |
|elasticsearch_cluster_number_of_pending_tasks                       |Gauge|cluster_name|           |Number of pending tasks.                                                       |
|elasticsearch_cluster_number_of_indices                             |Gauge|cluster_name|           |Number of indices.                                                             |
|elasticsearch_cluster_number_of_docs                                |Gauge|cluster_name|           |Number of indexed documents.                                                   |
|elasticsearch_cluster_number_of_nodes                               |Gauge|cluster_name|           |Number of nodes in the cluster.                                                |
|elasticsearch_cluster_number_of_failed_nodes                        |Gauge|cluster_name|           |Number of failed nodes in the cluster.                                         |
|elasticsearch_cluster_number_of_data_nodes                          |Gauge|cluster_name|           |Number of nodes working as data node.                                          |
|elasticsearch_cluster_number_of_coordinating_only_nodes             |Gauge|cluster_name|           |Number of nodes working as coordinating only.                                  |
|elasticsearch_cluster_number_of_master_elegible_nodes               |Gauge|cluster_name|           |Number of nodes working as master elegible.                                    |
|elasticsearch_cluster_number_of_ingest_nodes                        |Gauge|cluster_name|           |Number of nodes working as ingest node.                                        |
|elasticsearch_node_process_open_file_descriptors                    |Gauge|cluster_name|           |Current number of open file descriptors.                                       |
|elasticsearch_node_process_max_file_descriptors                     |Gauge|cluster_name|           |Max number of file descriptors.                                                |
|elasticsearch_node_jvm_mem_heap_used_in_bytes                       |Gauge|cluster_name|byte       |Amount of JVM heap memory being used.                                          |
|elasticsearch_node_jvm_mem_heap_committed_in_bytes                  |Gauge|cluster_name|byte       |Amount of JVM heap memory committed.                                           |
|elasticsearch_node_jvm_mem_non_heap_used_in_bytes                   |Gauge|cluster_name|byte       |Amount of JVM non-heap memory being used.                                      |
|elasticsearch_node_jvm_mem_non_heap_committed_in_bytes              |Gauge|cluster_name|byte       |Amount of JVM non-heap memory committed.                                       |
|elasticsearch_node_jvm_mem_pools_young_used_in_bytes                |Gauge|cluster_name|byte       |Amount of memory currently used by the Young Generation heap region.           |
|elasticsearch_node_jvm_mem_pools_young_max_in_bytes                 |Gauge|cluster_name|byte       |Maximum amount of memory that can be used by the Young Generation heap region. |
|elasticsearch_node_jvm_mem_pools_old_used_in_bytes                  |Gauge|cluster_name|byte       |Amount of memory in bytes currently used by the Old Generation heap region.    |
|elasticsearch_node_jvm_mem_pools_old_max_in_bytes                   |Gauge|cluster_name|byte       |Maximum amount of memory that can be used by the Old Generation heap region.   |
|elasticsearch_node_jvm_gc_collectors_young_collection_count         |Gauge|cluster_name|           |Total count of Young Generation garbage collections.                           |
|elasticsearch_node_jvm_gc_collectors_young_collection_time_in_millis|Gauge|cluster_name|millisecond|Total time spent on Young Generation garbage collections.                      |
|elasticsearch_node_jvm_gc_collectors_old_collection_count           |Gauge|cluster_name|           |Total count of Old Generation garbage collections.                             |
|elasticsearch_node_jvm_gc_collectors_old_collection_time_in_millis  |Gauge|cluster_name|millisecond|Total time spent on Old Generation garbage collections.                        |
|elasticsearch_node_indices_search_query_total                       |Gauge|cluster_name|           |The total number of queries.                                                   |
|elasticsearch_node_indices_search_query_time_in_millis              |Gauge|cluster_name|millisecond|The total time spent on queries.                                               |
|elasticsearch_node_indices_search_query_current                     |Gauge|cluster_name|           |The number of currently active queries.                                        |
|elasticsearch_node_indices_search_fetch_time_in_millis              |Gauge|cluster_name|millisecond|The total time spent on the search fetch.                                      |
|elasticsearch_node_indices_search_fetch_current                     |Gauge|cluster_name|           |The number of search fetches currently running.                                |
|elasticsearch_node_indices_indexing_index_total                     |Gauge|cluster_name|           |The total number of documents indexed to an index.                             |
|elasticsearch_node_indices_indexing_index_time_in_millis            |Gauge|cluster_name|millisecond|The total time spent indexing documents to an index.                           |
|elasticsearch_node_indices_indexing_index_failed                    |Gauge|cluster_name|           |The number of failed indexing operations.                                      |
|elasticsearch_node_indices_refresh_total_time_in_millis             |Gauge|cluster_name|millisecond|The total time spent on index refreshes on the primary shards.                 |
|elasticsearch_node_indices_flush_total_time_in_millis               |Gauge|cluster_name|millisecond|The total time spent flushing the index to disk.	                              |

== Installation ==

Run the Elasticsearch plugin against your Elasticsearch instances and it will start collecting the metrics. If your cluster is secured with Basic Authentication or TLS/SSL, you must provide additional plugin configurations via environment variables.

### Plugin Environment Variables

The Elasticsearch plugin can be customized via environment variables.

|Variable        |Default              |Description                                           |
|----------------|---------------------|------------------------------------------------------|
|protocol        |http                 |Elasticsearch REST API protocol.                      |
|host            |localhost            |Elasticsearch host.                                   |
|port            |9200                 |Elasticsearch REST API port.                          |
|username        |                     |Basic authentication username.                        |
|password        |                     |Basic authentication password.                        |
|client_cert_file|                     |Path to a client cert file to use when TLS is enabled.|
|private_key_file|                     |Path to a client key file to use when TLS is enabled. |
|ca_bundle_file  |                     |Path to the CA file to use when TLS is enabled.       |

== Changelog ==

|Version|Release Date|Description                                                |
|-------|------------|-----------------------------------------------------------|
|1.0    |05-Jun-2018 |Initial version of our Elasticsearch monitoring integration|
