AWS Lambda Integration
======================

== Description ==

This integration monitors the Relational Database Service (RDS) on AWS. Amazon RDS provides a managed relational
database service with a choice of six popular database engines: Amazon Aurora, PostgreSQL, MySQL, MariaDB, Oracle,
and Microsoft SQL Server.

This integration provides two plugins for monitoring your RDS instances:

* A discovery plugin that will list all of your RDS instances in Outlyer for monitoring
* A check that uses the Cloudwatch APIs to monitor each RDS instance in Outlyer

Once enabled you will see your RDS instances with all their metadata and labels in the host map in Outlyer, and a dashboard of all the key
metrics across your RDS instances in your AWS account.

== Metrics Collected ==

A full list of available Cloudwatch metrics for the RDS is available
<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/rds-metricscollected.html" target="_blank">here</a>.


| Metric Name                         |Type |Labels        |Unit        |Description                                                                                                                                                     |
|-------------------------------------|-----|--------------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
|aws.rds_burstbalance_max             |Gauge|region, engine|Percentage  |The percent of General Purpose SSD (gp2) burst-bucket I/O credits available.                                                                                    |
|aws.rds_swapusage_max                |Gauge|region, engine|Bytes       |The amount of swap space used on the DB instance.                                                                                                               |
|aws.rds_freestoragespace_max         |Gauge|region, engine|Bytes       |The amount of available storage space.                                                                                                                          |
|aws.rds_freeablememory_max           |Gauge|region, engine|Bytes       |The amount of available random access memory.                                                                                                                   |
|aws.rds_cpuutalization_max           |Gauge|region, engine|Percentage  |The percentage of CPU utilization.                                                                                                                              |
|aws.rds_networktransmitthroughput_max|Gauge|region, engine|Bytes/second|The outgoing (Transmit) network traffic on the DB instance, including both customer database traffic and Amazon RDS traffic used for monitoring and replication.|
|aws.rds_networkreceivethroughput_max |Gauge|region, engine|Bytes/second|The incoming (Receive) network traffic on the DB instance, including both customer database traffic and Amazon RDS traffic used for monitoring and replication. |
|aws.rds_writeops_max                 |Gauge|region, engine|Count/Second|The average number of disk write I/O operations per second.                                                                                                     |
|aws.rds_writelatency_max             |Gauge|region, engine|Seconds     |The average amount of time taken per disk I/O operation.                                                                                                        |
|aws.rds_writethroughput_max          |Gauge|region, engine|Bytes/second|The average number of bytes written to disk per second.                                                                                                         |
|aws.rds_readiops_max                 |Gauge|region, engine|Count/Second|The average number of disk read I/O operations per second.                                                                                                      |
|aws.rds_readthroughput_max           |Gauge|region, engine|Bytes/second|The average number of bytes read from disk per second.                                                                                                          |
|aws.rds_readlatency_max              |Gauge|region, engine|Seconds     |The average amount of time taken per disk I/O operation.                                                                                                        |
|aws.rds_diskqueuedepth_max           |Gauge|region, engine|Count       |The number of outstanding IOs (read/write requests) waiting to access the disk.                                                                                 |
|aws.rds_databaseconnections_max      |Gauge|region, engine|Count       |The number of database connections in use.                                                                                                                      |
|aws.rds_cpucreditusage_max           |Gauge|region, engine|Count       |The number of CPU credits spent by the instance for CPU utilization.                                                                                            |
|aws.rds_cpucreditbalance_max         |Gauge|region, engine|Count       |The number of earned CPU credits that an instance has accrued since it was launched or started.                                                                 |
|aws.rds_binlogdiskusage_max          |Gauge|region, engine|Bytes       |The amount of disk space occupied by binary logs on the master.                                                                                                 |

== Installation ==

In order for this integration to run, you must create an IAM role and access keys for the plugin
to connect to your AWS RDS APIs and AWS Cloudwatch metrics:

1. To get started, open the AWS Management Console
2. Click the IAM tab.
3. Click the Create a New Group of Users button.
4. Enter a Group Name called Outlyer.
5. Select the Read Only Access Policy Template then click Continue.
6. Click the Create New Users tab.
7. Enter a new User Name called Outlyer and click Continue and then Finish.
8. Click Show User Security Credentials.
9. Copy and paste your Access Key Id and the Secret Access Key somewhere safe.

# Plugins

There are two plugins:

* `rds-discovery.py` uses the Outlyer agent's instance discovery mechanism to automatically discover all the RDS instances in a specified region
* `aws-rds.py` is deployed as a standard check runs against each RDS instance discovered in the discovery plugin

The discovery plugin must be currently deployed manually to disk on an agent. The plugin must be put in the agent's `plugins` folder and
a discovery check YAML file must be configured in the agent's `conf.d` folder. An example of the YAML configuration file is shown below:

```yaml
discovers:
  rds-discovery:
    command: '/opt/outlyer/embedded/bin/python3 /etc/outlyer/plugins/rds-discovery.py'
    interval: 300
    disabled: false
    timeout: 120

    #labels:
    # environment: 'prod'

    #metric_labels:
    #  - 'environment'

    check_command: "/bin/bash -c 'echo ok'"
    check_interval: 30

    env:
      AWS_ACCESS_KEY_ID: <AWS_ACCESS_KEY_ID>
      AWS_SECRET_ACCESS_KEY: <AWS_SECRET_ACCESS_KEY>
      AWS_REGION: <AWS_REGION>
```

Once running you should see almost immediately all your RDS instances in the host view of the Outlyer UI. After that you can then deploy the
`aws-rds.py` monitoring check to monitor all of the instances via Cloudwatch. It is recommended that you use the check selector `cloud.service=aws.rds`
to ensure the check runs against all your RDS instances.

**It is recommended that both plugins run at 5 minute intervals to avoid significant charges on your AWS account bills**

Both plugins must set the following variables to run:

* `AWS_ACCESS_KEY_ID`: The AWS Access Key copied above
* `AWS_SECRET_ACCESS_KEY`: The AWS Secret Key copied above
* `AWS_REGION`: The AWS Region your RDS instnces are running in

In addition the following variables can be set to override the default values:

* `time_range`: The time range in minutes to query your metrics over. By default this is set to the last
10 minutes but if you run your functions rarely this can be set to longer for testing purposes.

== Changelog ==

|Version|Release Date|Description                                          |
|-------|------------|-----------------------------------------------------|
|1.0    |25-Jun-2018 |Initial version of our RDS monitoring integration.   |