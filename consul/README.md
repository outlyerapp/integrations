Consul Integration
==================

== Description ==

Consul is a distributed, highly available, and data center aware solution to connect and configure applications across dynamic, distributed infrastructure.

This integration will monitor your Consul cluster by collecting metrics from its RESTful HTTP API and the agent `/metrics` endpoint.

Once enabled you will get a default Consul dashboard and alert rules template to help you get started monitoring your key Consul metrics.

== Metrics Collected ==

| Metric Name                   |Type |Labels                                       |Unit|Description                                                                     |
|-------------------------------|-----|---------------------------------------------|----|--------------------------------------------------------------------------------|
|consul_catalog_services        |Gauge|                                             |    |Total number of services.                                                       |
|consul_client_agents           |Gauge|                                             |    |Total number of agents running in client mode.                                  |
|consul_datacenters             |Gauge|                                             |    |Total number of datacenters.                                                    |
|consul_health_failure_tolerance|Gauge|                                             |    |Number of voting servers that the cluster can lose while continuing to function.|
|consul_health_node_status      |Gauge|check, node, status                          |    |Node checks status.                                                             |
|consul_health_service_status   |Gauge|check, node, status, service_id, service_name|    |Service checks status.                                                          |
|consul_raft_leader             |Gauge|                                             |    |Indicates whether the cluster has a raft leader.                                |
|consul_raft_peers              |Gauge|                                             |    |Total number of agents running in server mode.                                  |
|consul_runtime_alloc_bytes     |Gauge|                                             |byte|Number of bytes allocated by the Consul process.                                |
|consul_runtime_heap_objects    |Gauge|                                             |    |Number of objects allocated on the heap.                                        |
|consul_runtime_num_goroutines  |Gauge|                                             |    |Rumber of running goroutines.                                                   |
|consul_serf_lan_members        |Gauge|                                             |    |Total number of members in the cluster.                                         |

== Installation ==

Run the Consul plugin against your Consul instances and it will start collecting the metrics. If your cluster is secured with RPC encryption using TLS or ACL tokens, you must provide additional plugin configurations via environment variables.

### Plugin Environment Variables

The Consul plugin can be customized via environment variables.

|Variable        |Default              |Description                                                                  |
|----------------|---------------------|-----------------------------------------------------------------------------|
|protocol        |http                 |Consul REST API protocol. Use `https` when TLS is enabled.                   |
|host            |localhost            |Consul host.                                                                 |
|port            |8500                 |Consul REST API port.                                                        |
|client_cert_file|                     |Path to a client cert file to use for TLS when `verify_incoming` is enabled. |
|private_key_file|                     |Path to a client key file to use for TLS when `verify_incoming` is enabled.  |
|ca_bundle_file  |                     |Path to the CA file to use for TLS when communicating with Consul.           |
|acl_token       |                     |The token ID used in each RPC request to the servers when ACL system is used.|

== Changelog ==

|Version|Release Date|Description                                          |
|-------|------------|-----------------------------------------------------|
|1.0    |31-May-2018 |Initial version of our Consul monitoring integration.|
