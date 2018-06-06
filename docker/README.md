Docker Integration
==================

== Description ==

Docker is a tool designed to make it easier to create, deploy, and run applications by using containers.

This integration will monitor your containers using metrics automatically collected by the Outlyer agent.

Once enabled you will get a default Docker dashboard to help you get started monitoring your containers.

== Metrics Collected ==

|Metric Name             |Type   |Labels                   |Unit|Description                                |
|------------------------|-------|-------------------------|----|-------------------------------------------|
|container.cpu.cores     |       |container,container.image|    |Number of CPU cores.                       |
|container.cpu.system    |       |container,container.image|    |System space CPU usage.                    |
|container.cpu.total     |       |container,container.image|    |Total CPU usage.                           |
|container.cpu.user      |       |container,container.image|byte|User space CPU usage.                      |
|container.io.read.bytes |       |container,container.image|    |The number of bytes read from disk         |
|container.io.read.count |       |container,container.image|    |The number of disk read operations.        |
|container.io.write.bytes|       |container,container.image|byte|The number of bytes written to disk.       |
|container.io.write.count|       |container,container.image|    |The number of disk write operations.       |
|container.mem.active    |       |container,container.image|byte|Amount of active memory.                   |
|container.mem.cached    |       |container,container.image|byte|Amount of cached memory.                   |
|container.mem.inactive  |       |container,container.image|byte|Amount of inactive memory.                 |
|container.mem.swap      |       |container,container.image|byte|Amount of swap memory.                     |
|container.mem.used      |       |container,container.image|byte|Amount of used memory.                     |
|container.net.rx.bytes  |       |container,container.image|byte|The number of received bytes.              |
|container.net.rx.drop   |       |container,container.image|byte|The number of received packages dropped.   |
|container.net.rx.errs   |       |container,container.image|byte|The number of received packages error.     |
|container.net.rx.packets|       |container,container.image|byte|The total number of received packages.     |
|container.net.tx.bytes  |       |container,container.image|byte|The number of transmitted bytes.           |
|container.net.tx.drop   |       |container,container.image|byte|The number of transmitted packages dropped.|
|container.net.tx.errs   |       |container,container.image|    |The number of transmitted packages error.  |
|container.net.tx.packets|       |container,container.image|    |The total number of transmitted packages.  |

== Installation ==

As Docker metrics are automatically collected by the Outlyer agent, just create the dashboard.

== Changelog ==

|Version|Release Date|Description                                         |
|-------|------------|----------------------------------------------------|
|1.0    |06-Jun-2018 |Initial version of our Docker monitoring integration|
