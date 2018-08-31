Agent Integration
=================

== Description ==

This integration is installed by default to provide a dashboard and instructions to install and monitor the Outlyer
agent which is required to run our other monitoring integrations that require plugins on your hosts. 

Your account agent key for installing the agents is:

**{AGENT_KEY}**

== Metrics Collected ==

The agent sends back the following metrics by default so you can get visibility into the agents health and performance 
across your hosts:

|Metric Name                |Type |Labels|Unit   |Description                                                 |
|---------------------------|-----|------|-------|------------------------------------------------------------|
|agent.uptime               |Gauge|      |Seconds|The total uptime since the agent was started                |
|agent.cpu_pct              |Gauge|      |Percent|The CPU utalization of the core agent process               |
|agent.mem_pct              |Gauge|      |Percent|The memory utalization of the core agent process            |
|agent.mem_res              |Gauge|      |Bytes  |                                                            |
|agent.mem_virt             |Gauge|      |Bytes  |                                                            |
|agent.publish_metrics      |Gauge|      |Count  |The number of metrics being published by the agent per flush|
|agent.publish_latency      |Gauge|      |Seconds|The time taken to flush all the metrics to Outlyer per flush|
|agent.request_inprogress   |Gauge|      |Count  |                                                            |
|agent.request_latency_count|Gauge|      |Count  |                                                            |
|agent.request_latency_sum  |Gauge|      |Seconds|                                                            |

== Installation ==

You must install the Outlyer agent for your platform. Full instructions to do this can be found on our docs: 
[https://docs2.outlyer.com/docs/agent/overview](https://docs2.outlyer.com/docs/agent/overview)

Your account agent key for installing the agents is:

**{AGENT_KEY}**

== Changelog ==

|Version|Release Date|Description                                         |
|-------|------------|----------------------------------------------------|
|1.0    |22-May-2018 |Initial version                                     |
