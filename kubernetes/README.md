Kubernetes Integration
======================

== Description ==

Kubernetes is an open source system for automating deployment, scaling, and management of containerized applications.

This integration will monitor your Kubernetes cluster by collecting metrics from API Server and [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics).

Once enabled you will get default dashboards and alert rules to help you get started monitoring your key Kubernetes metrics.

== Metrics Collected ==

### Kubernetes API Server: kubernetes-api-server.py

| Metric Name                       |Type   |Labels                                                   |Unit       |Description                                    |
|-----------------------------------|-------|---------------------------------------------------------|-----------|-----------------------------------------------|
|apiserver_request_count            |Counter|k8s.cluster, verb, resource, client, contentType, code   |           |Total number of API Server requests per second.|
|apiserver_request_latencies_summary|Gauge  |k8s.cluster, resource, scope, subresource, verb, quantile|microsecond|API Server request latency.                    |

### Kube State Metrics: kube-state-metrics.py

| Metric Name                               |Type   |Labels                                                                 |Unit|Description                                                                                                            |
|-------------------------------------------|-------|-----------------------------------------------------------------------|----|-----------------------------------------------------------------------------------------------------------------------|
|kube_daemonset_status_number_available     |Gauge  |daemonset, namespace                                                   |    |The number of nodes that should be running the daemon pod and have one or more of the daemon pod running and available.|
|kube_daemonset_status_number_unavailable   |Gauge  |daemonset, namespace                                                   |    |The number of nodes that should be running the daemon pod and have none of the daemon pod running and available.       |
|kube_deployment_metadata_generation        |Gauge  |deployment, namespace                                                  |    |Sequence number representing a specific generation of the desired state.                                               |
|kube_deployment_spec_replicas              |Gauge  |deployment, namespace                                                  |    |Number of desired pods for a deployment.                                                                               |
|kube_deployment_status_observed_generation |Gauge  |deployment, namespace                                                  |    |The generation observed by the deployment controller.                                                                  |
|kube_deployment_status_replicas            |Gauge  |deployment, namespace                                                  |    |The number of replicas per deployment.                                                                                 |
|kube_deployment_status_replicas_available  |Gauge  |deployment, namespace                                                  |    |The number of available replicas per deployment.                                                                       |
|kube_deployment_status_replicas_unavailable|Gauge  |deployment, namespace                                                  |    |The number of unavailable replicas per deployment.                                                                     |
|kube_deployment_status_replicas_updated    |Gauge  |deployment, namespace                                                  |    |The number of updated replicas per deployment.                                                                         |
|kube_node_spec_unschedulable               |Gauge  |node                                                                   |    |Whether a node can schedule new pods.                                                                                  |
|kube_node_status_capacity_pods             |Gauge  |node                                                                   |    |The total pod resources of the node.                                                                                   |
|kube_node_status_condition                 |Gauge  |node, condition, status                                                |    |The condition of a cluster node.                                                                                       |
|kube_pod_container_status_restarts_total   |Counter|container, namespace, pod                                              |    |The number of container restarts per second.                                                                           |
|kube_pod_container_status_waiting_reason   |Gauge  |container, namespace, pod, reason                                      |    |Describes the reason the container is currently in waiting state.                                                      |
|kube_pod_info                              |Gauge  |pod, namespace, host_ip, pod_ip, node, created_by_kind, created_by_name|    |Information about pod.                                                                                                 |
|kube_pod_status_phase                      |Gauge  |pod, namespace, phase                                                  |    |The pods current phase.                                                                                                |

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

== Changelog ==

|Version|Release Date|Description                                                       |
|-------|------------|------------------------------------------------------------------|
|1.0    |24-May-2018 |Initial version of our Kubernetes monitoring integration.         |
|1.1    |25-Jun-2018 |Adds k8s.cluster label and collects new API Server latency metric.|
