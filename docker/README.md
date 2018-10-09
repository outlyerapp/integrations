Docker Integration
==================

== Description ==

Docker is a tool designed to make it easier to create, deploy, and run applications by using containers.

This integration will monitor your containers using metrics automatically collected by the Outlyer agent and the Docker plugin.

Once enabled you will get a default Docker dashboard to help you get started monitoring your containers.

== Metrics Collected ==

|Metric Name             |Type |Labels                    |Unit|Description                                                             |
|------------------------|-----|--------------------------|----|------------------------------------------------------------------------|
|container.cpu.cores     |Gauge|container, container.image|    |Number of CPU cores.                                                    |
|container.cpu.system    |Gauge|container, container.image|    |System space CPU usage.                                                 |
|container.cpu.total     |Gauge|container, container.image|    |Total CPU usage.                                                        |
|container.cpu.user      |Gauge|container, container.image|byte|User space CPU usage.                                                   |
|container.io.read.bytes |Gauge|container, container.image|    |The number of bytes read from disk                                      |
|container.io.read.count |Gauge|container, container.image|    |The number of disk read operations.                                     |
|container.io.write.bytes|Gauge|container, container.image|byte|The number of bytes written to disk.                                    |
|container.io.write.count|Gauge|container, container.image|    |The number of disk write operations.                                    |
|container.mem.active    |Gauge|container, container.image|byte|Amount of active memory.                                                |
|container.mem.cached    |Gauge|container, container.image|byte|Amount of cached memory.                                                |
|container.mem.inactive  |Gauge|container, container.image|byte|Amount of inactive memory.                                              |
|container.mem.swap      |Gauge|container, container.image|byte|Amount of swap memory.                                                  |
|container.mem.used      |Gauge|container, container.image|byte|Amount of used memory.                                                  |
|container.net.rx.bytes  |Gauge|container, container.image|byte|The number of received bytes.                                           |
|container.net.rx.drop   |Gauge|container, container.image|byte|The number of received packages dropped.                                |
|container.net.rx.errs   |Gauge|container, container.image|byte|The number of received packages error.                                  |
|container.net.rx.packets|Gauge|container, container.image|byte|The total number of received packages.                                  |
|container.net.tx.bytes  |Gauge|container, container.image|byte|The number of transmitted bytes.                                        |
|container.net.tx.drop   |Gauge|container, container.image|byte|The number of transmitted packages dropped.                             |
|container.net.tx.errs   |Gauge|container, container.image|    |The number of transmitted packages error.                               |
|container.net.tx.packets|Gauge|container, container.image|    |The total number of transmitted packages.                               |
|container.count         |Gauge|status                    |    |The number of containers by status (running, exited, restarting, paused)|

== Installation ==

Run the Docker plugin against your instances to start collecting the number of containers by status. All other Docker metrics are automatically collected by the Outlyer agent.

== Changelog ==

|Version|Release Date|Description                                          |
|-------|------------|-----------------------------------------------------|
|1.1.0  |03-Oct-2018 |Creates scoped Docker dashboard and renames plugin.  |
|1.0    |06-Jun-2018 |Initial version of our Docker monitoring integration.|
