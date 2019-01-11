MongoDB Integration
===================

== Description ==

MongoDB is a free and open source cross-platform document-oriented NoSQL database.

This integration will monitor your MongoDB cluster by collecting metrics from MongoDB [dbStats](https://docs.mongodb.com/manual/reference/command/dbStats/) and [serverStatus](https://docs.mongodb.com/manual/reference/command/serverStatus/) commands.

Once enabled you will get a default MongoDB dashboard to help you get started monitoring your key MongoDB metrics.

== Metrics Collected ==

|Metric Name                  |Type   |Labels  |Unit            |Description                                                                                                 |
|-----------------------------|-------|--------|----------------|------------------------------------------------------------------------------------------------------------|
|mongodb.collections          |Gauge  |database|                |Number of collections in the database.                                                                      |
|mongodb.objects              |Gauge  |database|                |number of objects (i.e. documents) in the database across all collections.                                  |
|mongodb.avg_obj_size         |Gauge  |database|byte            |Average size of each document in bytes. This is the dataSize divided by the number of documents.            |
|mongodb.data_size            |Gauge  |database|byte            |Total size of the uncompressed data held in this database. The dataSize decreases when you remove documents.|
|mongodb.storage_size         |Gauge  |database|byte            |Total amount of space allocated to collections in this database for document storage.                       |
|mongodb.indexes              |Gauge  |database|                |Total number of indexes across all collections in the database.                                             |
|mongodb.index_size           |Gauge  |database|byte            |Total size of all indexes created on this database.                                                         |
|mongodb.fs_used_size         |Gauge  |database|byte            |Total size of all disk space in use on the filesystem where MongoDB stores data.                            |
|mongodb.fs_total_size        |Gauge  |database|byte            |Total size of all disk capacity on the filesystem where MongoDB stores data.                                |
|mongodb.network.bytes_in     |Counter|        |byte/second     |Rate of bytes that reflects the amount of network traffic received.                                         |
|mongodb.network.bytes_out    |Counter|        |byte/second     |Rate of bytes that reflects the amount of network traffic sent.                                             |
|mongodb.network.num_requests |Counter|        |request/second  |Rate of of distinct requests that the server has received.                                                  |
|mongodb.opcounters.delete    |Counter|        |operation/second|Rate of delete operations since the mongod instance last started.                                           |
|mongodb.opcounters.getmore   |Counter|        |operation/second|Rate of “getmore” operations since the mongod instance last started.                                        |
|mongodb.opcounters.insert    |Counter|        |operation/second|Rate of insert operations received since the mongod instance last started.                                  |
|mongodb.opcounters.query     |Counter|        |operation/second|Rate of queries received since the mongod instance last started.                                            |
|mongodb.opcounters.update    |Counter|        |operation/second|Rate of update operations received since the mongod instance last started.                                  |
|mongodb.connections.available|Gauge  |        |                |Number of unused incoming connections available.                                                            |
|mongodb.connections.current  |Gauge  |        |                |Number of incoming connections from clients to the database server.                                         |
|mongodb.uptime               |Gauge  |        |second          |Number of seconds that the current MongoDB process has been active.                                         |

== Installation ==

Just run the MongoDB plugin against your MongoDB instances and it will start collecting metrics.

### Plugin Environment Variables

The MongoDB plugin can be customized via environment variables.

|Variable       |Default  |Description                                                                |
|---------------|---------|---------------------------------------------------------------------------|
|port           |27017    |MongoDB port.                                                              |
|username       |         |MongoDB username when MongoDB Auth is enabled.                             |
|password       |         |MongoDB password when MongoDB Auth is enabled.                             |
|auth_source    |         |The name of the database that has the collection with the user credentials.|
|connect_timeout|5000     |The number of milliseconds to wait before timing out a connection attempt. |
|socket_timeout |5000     |The maximum number of milliseconds to wait for responses from the server.  |

== Changelog ==

|Version|Release Date|Description                                           |
|-------|------------|------------------------------------------------------|
|1.1    |11-Jan-2019 |`serverSelectionTimeoutMS` for server connection timeout | 
|1.0    |21-Jun-2018 |Initial version of our MongoDB monitoring integration.|
