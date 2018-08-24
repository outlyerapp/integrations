Kubernetes Integration
======================

== Description ==

Kubernetes is an open source system for automating deployment, scaling, and management of containerized applications.

This integration will monitor your Kubernetes cluster by collecting metrics from API Server, [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics), and Kubelet.

Once enabled you will get default dashboards and alert rules to help you get started monitoring your key Kubernetes metrics.

== Metrics Collected ==

### Kubernetes API Server: kubernetes-api-server.py

| Metric Name                       |Type   |Labels                                                   |Unit       |Description                                    |
|-----------------------------------|-------|---------------------------------------------------------|-----------|-----------------------------------------------|
|apiserver_request_count            |Counter|k8s.cluster, verb, resource, client, contentType, code   |           |Total number of API Server requests per second.|
|apiserver_request_latencies_summary|Gauge  |k8s.cluster, resource, scope, subresource, verb, quantile|microsecond|API Server request latency.                    |

### Kube State Metrics: kube-state-metrics.py

| Metric Name                                     |Type   |Labels                                                                                       |Unit|Description                                                                                                            |
|-------------------------------------------------|-------|---------------------------------------------------------------------------------------------|----|-----------------------------------------------------------------------------------------------------------------------|
|kube_daemonset_status_number_available           |Gauge  |k8s.cluster, daemonset, namespace                                                            |    |The number of nodes that should be running the daemon pod and have one or more of the daemon pod running and available.|
|kube_daemonset_status_number_unavailable         |Gauge  |k8s.cluster, daemonset, namespace                                                            |    |The number of nodes that should be running the daemon pod and have none of the daemon pod running and available.       |
|kube_deployment_metadata_generation              |Gauge  |k8s.cluster, deployment, namespace                                                           |    |Sequence number representing a specific generation of the desired state.                                               |
|kube_deployment_spec_replicas                    |Gauge  |k8s.cluster, deployment, namespace                                                           |    |Number of desired pods for a deployment.                                                                               |
|kube_deployment_status_observed_generation       |Gauge  |k8s.cluster, deployment, namespace                                                           |    |The generation observed by the deployment controller.                                                                  |
|kube_deployment_status_replicas                  |Gauge  |k8s.cluster, deployment, namespace                                                           |    |The number of replicas per deployment.                                                                                 |
|kube_deployment_status_replicas_available        |Gauge  |k8s.cluster, deployment, namespace                                                           |    |The number of available replicas per deployment.                                                                       |
|kube_deployment_status_replicas_unavailable      |Gauge  |k8s.cluster, deployment, namespace                                                           |    |The number of unavailable replicas per deployment.                                                                     |
|kube_deployment_status_replicas_updated          |Gauge  |k8s.cluster, deployment, namespace                                                           |    |The number of updated replicas per deployment.                                                                         |
|kube_node_spec_unschedulable                     |Gauge  |k8s.cluster, k8s.node.name                                                                   |    |Whether a node can schedule new pods.                                                                                  |
|kube_node_status_allocatable_cpu_cores           |Gauge  |k8s.cluster, k8s.node.name                                                                   |core|The CPU resources of a node that are available for scheduling.                                                         |
|kube_node_status_allocatable_memory_bytes        |Gauge  |k8s.cluster, k8s.node.name                                                                   |byte|The memory resources of a node that are available for scheduling.                                                      |
|kube_node_status_capacity_pods                   |Gauge  |k8s.cluster, k8s.node.name                                                                   |    |The total pod resources of the node.                                                                                   |
|kube_node_status_condition                       |Gauge  |k8s.cluster, k8s.node.name, condition, status                                                |    |The condition of a cluster node.                                                                                       |
|kube_pod_container_status_restarts_total         |Counter|k8s.cluster, container, namespace, pod                                                       |    |The number of container restarts per second.                                                                           |
|kube_pod_container_status_waiting_reason         |Gauge  |k8s.cluster, container, namespace, pod, reason                                               |    |Describes the reason the container is currently in waiting state.                                                      |
|kube_pod_info                                    |Gauge  |k8s.cluster, pod, namespace, host_ip, pod_ip, k8s.node.name, created_by_kind, created_by_name|    |Information about pod.                                                                                                 |
|kube_pod_status_phase                            |Gauge  |k8s.cluster, pod, namespace, phase                                                           |    |The pods current phase.                                                                                                |
|kube_pod_container_resource_requests_cpu_cores   |Gauge  |k8s.cluster, container, pod, namespace, k8s.node.name                                        |core|The number of requested cpu cores by a container.                                                                      |
|kube_pod_container_resource_limits_cpu_cores     |Gauge  |k8s.cluster, container, pod, namespace, k8s.node.name                                        |core|The limit on cpu cores to be used by a container.                                                                      |
|kube_pod_container_resource_requests_memory_bytes|Gauge  |k8s.cluster, container, pod, namespace, k8s.node.name                                        |byte|The number of requested memory bytes by a container.                                                                   |
|kube_pod_container_resource_limits_memory_bytes  |Gauge  |k8s.cluster, container, pod, namespace, k8s.node.name                                        |byte|The limit on memory to be used by a container in bytes.                                                                |
|kube_pod_container_status_terminated_reason      |Gauge  |k8s.cluster, container, pod, namespace, reason                                               |    |Describes the reason the container is currently in terminated state.                                                   |
|kube_pod_status_ready                            |Gauge  |k8s.cluster, pod, namespace, condition                                                       |    |Describes whether the pod is ready to serve requests.                                                                  |
|kube_service_info                                |Gauge  |k8s.cluster, service, namespace, cluster_ip                                                  |    |Information about service.                                                                                             |


### Kubernetes Kubelet: kubernetes-kubelet.py

| Metric Name                             |Type   |Labels                                                                                          |Unit        |Description                                               |
|-----------------------------------------|-------|------------------------------------------------------------------------------------------------|------------|----------------------------------------------------------|
|container_cpu_cfs_throttled_seconds_total|Gauge  |k8s.cluster, k8s.node.name, container, id, image, name, namespace, pod, k8s.pod.label           |second      |Total time duration the container has been throttled.     |
|container_cpu_usage_seconds_total        |Counter|k8s.cluster, k8s.node.name, container, cpu, id, image, name, namespace, pod, k8s.pod.label      |core/second |Rate of CPU time consumed per cpu in seconds.             |
|container_fs_reads_bytes_total           |Counter|k8s.cluster, k8s.node.name, container, device, id, image, name, namespace, pod, k8s.pod.label   |byte/second |Rate of bytes read.                                       |
|container_fs_writes_bytes_total          |Counter|k8s.cluster, k8s.node.name, container, device, id, image, name, namespace, pod, k8s.pod.label   |byte/second |Rate of bytes written.                                    |
|container_memory_working_set_bytes       |Gauge  |k8s.cluster, k8s.node.name, container, id, image, name, namespace, pod, k8s.pod.label           |byte        |Current working set in bytes.                             |
|container_memory_swap                    |Gauge  |k8s.cluster, k8s.node.name, container, id, image, name, namespace, pod, k8s.pod.label           |byte        |Container swap usage in bytes.                            |
|container_network_receive_bytes_total    |Counter|k8s.cluster, k8s.node.name, container, id, image, interface, name, namespace, pod, k8s.pod.label|byte/second |Rate of bytes received.                                   |
|container_network_receive_errors_total   |Counter|k8s.cluster, k8s.node.name, container, id, image, interface, name, namespace, pod, k8s.pod.label|error/second|Rate of errors encountered while receiving.               |
|container_network_transmit_bytes_total   |Counter|k8s.cluster, k8s.node.name, container, id, image, interface, name, namespace, pod, k8s.pod.label|byte/second |Rate of bytes transmitted.                                |
|container_network_transmit_errors_total  |Counter|k8s.cluster, k8s.node.name, container, id, image, interface, name, namespace, pod, k8s.pod.label|error/second|Rate of errors encountered while transmitting.            |
|kube_node_cpu_usage_cores                |Gauge  |k8s.cluster, k8s.node.name, k8s.node.label                                                      |core        |The total CPU usage (sum of all cores).                   |
|kube_node_cpu_usage_pct                  |Gauge  |k8s.cluster, k8s.node.name, k8s.node.label                                                      |fraction    |The percentage of CPU cores used.                         |
|kube_node_fs_imagefs_available_bytes     |Gauge  |k8s.cluster, k8s.node.name, k8s.node.label                                                      |byte        |The storage space available for the imagefs filesystem.   |
|kube_node_fs_imagefs_inodes_free         |Gauge  |k8s.cluster, k8s.node.name, k8s.node.label                                                      |inode       |The free inodes in the imagefs filesystem.                |
|kube_node_fs_nodefs_available_bytes      |Gauge  |k8s.cluster, k8s.node.name, k8s.node.label                                                      |byte        |The storage space available for the nodefs filesystem.    |
|kube_node_fs_nodefs_capacity_bytes       |Gauge  |k8s.cluster, k8s.node.name, k8s.node.label                                                      |byte        |The total capacity of the nodefs filesystem storage.      |
|kube_node_fs_nodefs_inodes_free          |Gauge  |k8s.cluster, k8s.node.name, k8s.node.label                                                      |inode       |The free inodes in the nodefs filesystem.                 |
|kube_node_fs_nodefs_used_bytes           |Gauge  |k8s.cluster, k8s.node.name, k8s.node.label                                                      |byte        |The bytes used in the nodefs filesystem.                  |
|kube_node_fs_nodefs_used_pct             |Gauge  |k8s.cluster, k8s.node.name, k8s.node.label                                                      |fraction    |The percentage of nodefs filesystem usage.                |
|kube_node_memory_available_bytes         |Gauge  |k8s.cluster, k8s.node.name, k8s.node.label                                                      |byte        |The memory available in the node.                         |
|kube_node_memory_usage_byte              |Gauge  |k8s.cluster, k8s.node.name, k8s.node.label                                                      |byte        |The memory used by the node.                              |
|kube_node_memory_usage_pct               |Gauge  |k8s.cluster, k8s.node.name, k8s.node.label                                                      |fraction    |The percentage of memory used in the node.                |
|kube_node_network_rx_bytes               |Counter|k8s.cluster, k8s.node.name, k8s.node.label                                                      |byte/sec    |Rate of bytes received.                                   |
|kube_node_network_tx_bytes               |Counter|k8s.cluster, k8s.node.name, k8s.node.label                                                      |byte/sec    |Rate of bytes transmitted.                                |
|kube_node_network_rx_errors              |Counter|k8s.cluster, k8s.node.name, k8s.node.label                                                      |error/sec   |Rate of errors encountered while receiving.               |        
|kube_node_network_tx_errors              |Counter|k8s.cluster, k8s.node.name, k8s.node.label                                                      |error/sec   |Rate of errors encountered while transmitting.            |

== Installation ==

### Kubernetes API Server: kubernetes-api-server.py
This plugin can be used not only to check API Server and etcd health, but also to collect metrics from API Server.

1. API Server Health Check: run it against any Kubernetes Node.
2. etcd Health Check: provide the environment variable `endpoint: healthz/etcd` and run it against any Kubernetes Node.
3. API Server Metrics: provide the environment variable `endpoint: metrics` and run it against any Kubernetes Node.

|Variable|Default|Description                       |
|--------|-------|----------------------------------|
|endpoint|healthz|Specifies the API Server endpoint.|

### Kubernetes API Server: kube-state-metrics.py
This plugin is used to scrape metrics from `kube-state-metrics`. If you have deployed kube-state-metrics on your Kubernetes cluster as shown in our [documentation](https://docs2.outlyer.com/agent/kubernetes/), just run it against any Kubernetes Node. Otherwise, provide the environment variable `host` with the FQDN (Fully Qualified Domain Name) of your kube-state-metrics Kubernetes Service.

|Variable |Default                       |Description                                           |
|---------|------------------------------|------------------------------------------------------|
|host     |kube-state-metrics.kube-system|Specifies the FQDN for kube-state-metrics K8s Service.|
|port     |8080                          |kube-state-metrics metrics port.                      |
|endpoint |metrics                       |kube-state-metrics metrics endpoint.                  |

### Kubernetes Kubelet: kubernetes-kubelet.py
This plugin is used to scrape container and pod metrics from the embedded cAdvisor instance that ships with Kubelet and node metrics from the Kubelet Summary API. Just run the plugin against all your Kuberentes Nodes.

|Variable         |Default                                            |Description                                                                                                             |
|-----------------|---------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
|protocol         |http                                               |Kubelet REST API protocol (http or https).                                                                              |
|ip               |127.0.0.1                                          |Kubelet host.                                                                                                           |
|port             |10255                                              |Kubelet REST API port (set it to 10250 when using https protocol).                                                      |
|cadvisor_endpoint|metrics/cadvisor                                   |cAdvisor metrics endpoint.                                                                                              |
|summary_endpoint |stats/summary                                      |Kubelet Summary API endpoint.                                                                                           |
|token_path       |/var/run/secrets/kubernetes.io/serviceaccount/token|The path to the mounted Kubernetes Secret file containing the API token to access Kubelet REST API using https protocol.|

== Changelog ==

|Version|Release Date|Description                                                       |
|-------|------------|------------------------------------------------------------------|
|1.3    |21-Aug-2018 |Creates Nodes Dashboard.                                          |
|1.2    |10-Aug-2018 |Creates Pods Dashboard.                                           |
|1.1    |25-Jun-2018 |Adds k8s.cluster label and collects new API Server latency metric.|
|1.0    |24-May-2018 |Initial version of our Kubernetes monitoring integration.         |
