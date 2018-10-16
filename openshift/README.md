OpenShift Integration
=====================

== Description ==

OpenShift Container Platform is Red Hat's on-premises private platform as a service product, built around a core of application containers powered by Docker, with orchestration and management provided by Kubernetes, on a foundation of Red Hat Enterprise Linux.

This integration will monitor your OpenShift cluster by collecting metrics from OpenShift Kubernetes APIs via API Server.

Once enabled you will get a default OpenShift dashboard to help you get started monitoring your OpenShift metrics.

== Metrics Collected ==

|Metric Name                                               |Type   |Labels                                                                                                                                       |Unit        |Description                                                                          |
|----------------------------------------------------------|-------|---------------------------------------------------------------------------------------------------------------------------------------------|------------|-------------------------------------------------------------------------------------|
|openshift.users                                           |Gauge  |k8s.cluster, username                                                                                                                        |user        |The active users in the OpenShift cluster.                                           |
|openshift.routes                                          |Gauge  |k8s.cluster, route_name, namespace, route_host, to.kind, to.name, to.weight, ingress.host, ingress.conditions.type, ingress.conditions.status|route       |The configured routes in the OpenShift cluster.                                      |
|openshift.clusterquota.cpu.limit                          |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |core        |Hard limit for cpu by cluster resource quota for all namespaces.                     |
|openshift.clusterquota.memory.limit                       |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |byte        |Hard limit for memory by cluster resource quota for all namespaces.                  |
|openshift.clusterquota.pods.limit                         |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |pod         |Hard limit for pods by cluster resource quota for all namespaces.                    |
|openshift.clusterquota.services.limit                     |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |service     |Hard limit for services by cluster resource quota for all namespaces.                |
|openshift.clusterquota.services.nodeports.limit           |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |service     |Hard limit for service node ports by cluster resource quota for all namespaces.      |
|openshift.clusterquota.services.loadbalancers.limit       |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |service     |Hard limit for service load balancers by cluster resource quota for all namespace.   |
|openshift.clusterquota.secrets.limit                      |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |secret      |Hard limit for secrets by cluster resource quota for all namespace.                  |
|openshift.clusterquota.configmaps.limit                   |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |configmap   |Hard limit for config map by cluster resource quota for all namespace.               |
|openshift.clusterquota.persistentvolumeclaims.limit       |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |pvc         |Hard limit for persistent volume claims by cluster resource quota for all namespaces.|
|openshift.clusterquota.cpu.used                           |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |core        |Observed cpu usage by cluster resource quota for all namespaces.                     |
|openshift.clusterquota.memory.used                        |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |byte        |Observed memory usage by cluster resource quota for all namespaces.                  |
|openshift.clusterquota.pods.used                          |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |pod         |Observed pods usage by cluster resource quota for all namespaces.                    |
|openshift.clusterquota.services.used                      |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |service     |Observed services usage by cluster resource quota for all namespaces.                |
|openshift.clusterquota.services.nodeports.used            |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |service     |Observed service node ports usage by cluster resource quota for all namespaces.      |
|openshift.clusterquota.services.loadbalancers.used        |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |service     |Observed service load balancers usage by cluster resource quota for all namespaces.  |
|openshift.clusterquota.secrets.used                       |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |secret      |Observed secret usage by cluster resource quota for all namespaces.                  |
|openshift.clusterquota.configmaps.used                    |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |configmap   |Observed config map usage by cluster resource quota for all namespaces.              |
|openshift.clusterquota.persistentvolumeclaims.used        |Gauge  |k8s.cluster, cluster_quota_name                                                                                                              |pvc         |Observed persistent volume claims usage by cluster resource quota for all namespaces.|
|openshift.appliedclusterquota.cpu.limit                   |Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |core        |Hard limit for cpu by cluster resource quota and namespace.                          |
|openshift.appliedclusterquota.memory.limit                |Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |byte        |Hard limit for memory by cluster resource quota and namespace.                       |
|openshift.appliedclusterquota.pods.limit                  |Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |pod         |Hard limit for pods by cluster resource quota and namespace.                         |
|openshift.appliedclusterquota.services.limit              |Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |service     |Hard limit for services by cluster resource quota and namespace.                     |
|openshift.appliedclusterquota.services.nodeports.limit    |Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |service     |Hard limit for service node ports by cluster resource quota and namespace.           |
|openshift.appliedclusterquota.services.loadbalancers.limit|Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |service     |Hard limit for service load balancers by cluster resource quota and namespace.       |
|openshift.appliedclusterquota.secrets.limit               |Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |secret      |Hard limit for secrets by cluster resource quota and namespace.                      |
|openshift.appliedclusterquota.configmaps.limit            |Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |configmap   |Hard limit for config maps by cluster resource quota and namespace.                  |
|openshift.appliedclusterquota.persistentvolumeclaims.limit|Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |pvc         |Hard limit for persistent volume claims by cluster resource quota and namespace.     |
|openshift.appliedclusterquota.cpu.used                    |Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |core        |Observed cpu usage by cluster resource quota and namespace.                          |
|openshift.appliedclusterquota.memory.used                 |Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |byte        |Observed memory usage by cluster resource quota and namespace.                       |
|openshift.appliedclusterquota.pods.used                   |Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |pod         |Observed pods usage by cluster resource quota and namespace.                         |
|openshift.appliedclusterquota.services.used               |Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |service     |Observed services usage by cluster resource quota and namespace.                     |
|openshift.appliedclusterquota.services.nodeports.used     |Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |service     |Observed service node ports usage by cluster resource quota and namespace.           |
|openshift.appliedclusterquota.services.loadbalancers.used |Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |service     |Observed service load balancers usage by cluster resource quota and namespace.       |
|openshift.appliedclusterquota.secrets.used                |Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |secret      |Observed secrets usage by cluster resource quota and namespace.                      |
|openshift.appliedclusterquota.configmaps.used             |Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |configmap   |Observed config maps usage by cluster resource quota and namespace.                  |
|openshift.appliedclusterquota.persistentvolumeclaims.used |Gauge  |k8s.cluster, cluster_quota_name, namespace                                                                                                   |pvc         |Observed persistent volume claims usage by cluster resource quota and namespace.     |

== Installation ==

Just run the OpenShift plugin against a single Kubernetes node of your cluster and it will start collecting metrics.

### Plugin Environment Variables

The OpenShift plugin can be customized via environment variables.

|Variable  |Default                                            |Description                                              |
|----------|---------------------------------------------------|---------------------------------------------------------|
|api_server|api.openshift-apiserver                            |The full qualified domain name (FQDN) for the API Server.|
|token_path|/var/run/secrets/kubernetes.io/serviceaccount/token|The path to the service account token.                   |

== Changelog ==

|Version|Release Date|Description                                             |
|-------|------------|--------------------------------------------------------|
|1.0    |16-Oct-2018 |Initial version of our OpenShift monitoring integration.|
