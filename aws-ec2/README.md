AWS EC2 Integration
===================

== Description ==

This integration monitors the Amazon Elastic Compute Cloud Service (EC2) on AWS. Amazon EC2 is a web service that provides secure, 
resizable compute capacity in the cloud. It is designed to make web-scale cloud computing easier for developers.

This integration provides two plugins for monitoring your EC2 instances:

* A discovery plugin that will list all of your EC2 instances in Outlyer for monitoring
* A check that uses the Cloudwatch APIs to monitor each EC2 instance in Outlyer

Once enabled you will see your EC2 instances with all their metadata and labels in the host map in Outlyer, and a dashboard of all the key
metrics across your EC2 instances in your AWS account.

== Metrics Collected ==

A full list of available Cloudwatch metrics for the RDS is available
<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ec2-metricscollected.html" target="_blank">here</a>.

|Metric Name                           |Type   |Labels                                                                      |Unit   |Description                                                                                                           |
|--------------------------------------|-------|----------------------------------------------------------------------------|-------|----------------------------------------------------------------------------------------------------------------------|
|aws.ec2_cpucreditusage_max            |gauge  |cloud.service, cloud.instance.type, cloud.instance.region, cloud.instance.az|Count  |The number of CPU credits spent by the instance for CPU utilization.                                                  |
|aws.ec2_networkout_max                |gauge  |cloud.service, cloud.instance.type, cloud.instance.region, cloud.instance.az|Bytes  |The number of bytes sent out on all network interfaces by the instance.                                               |
|aws.ec2_networkpacketsout_max         |gauge  |cloud.service, cloud.instance.type, cloud.instance.region, cloud.instance.az|Count  |The number of packets sent out on all network interfaces by the instance.                                             |
|aws.ec2_cpusurpluscreditbalance_max   |gauge  |cloud.service, cloud.instance.type, cloud.instance.region, cloud.instance.az|Count  |The number of surplus credits that have been spent by a T2 Unlimited instance when its CPUCreditBalance is zero.      |
|sys.cpu.pct                           |gauge  |cloud.service, cloud.instance.type, cloud.instance.region, cloud.instance.az|Percent|The percentage of allocated EC2 compute units that are currently in use on the instance.                              |
|aws.ec2_diskwriteops_max              |gauge  |cloud.service, cloud.instance.type, cloud.instance.region, cloud.instance.az|Count  |Completed write operations to all instance store volumes available to the instance in a specified period of time.     |
|aws.ec2_cpucreditbalance_max          |gauge  |cloud.service, cloud.instance.type, cloud.instance.region, cloud.instance.az|Count  |The number of earned CPU credits that an instance has accrued since it was launched or started.                       |
|aws.ec2_cpucreditscharged_max         |gauge  |cloud.service, cloud.instance.type, cloud.instance.region, cloud.instance.az|Count  |The number of spent surplus credits that are not paid down by earned CPU credits, and thus incur an additional charge.|
|aws.ec2_diskreadops_max               |gauge  |cloud.service, cloud.instance.type, cloud.instance.region, cloud.instance.az|Count  |Completed read operations from all instance store volumes available to the instance in a specified period of time.    |
|aws.ec2_diskwritebytes_max            |gauge  |cloud.service, cloud.instance.type, cloud.instance.region, cloud.instance.az|Bytes  |Bytes written to all instance store volumes available to the instance.                                                |
|aws.ec2_networkin_max                 |gauge  |cloud.service, cloud.instance.type, cloud.instance.region, cloud.instance.az|Bytes  |The number of bytes received on all network interfaces by the instance.                                               |
|aws.ec2_networkpacketsin_max          |gauge  |cloud.service, cloud.instance.type, cloud.instance.region, cloud.instance.az|Count  |The number of packets received on all network interfaces by the instance.                                             |
|aws.ec2_diskreadbytes_max             |gauge  |cloud.service, cloud.instance.type, cloud.instance.region, cloud.instance.az|Bytes  |Bytes read from all instance store volumes available to the instance.                                                 |
|aws.ec2_statuscheckfailed_max         |gauge  |cloud.service, cloud.instance.type, cloud.instance.region, cloud.instance.az|Count  |Reports whether the instance has passed both the instance status check and the system status check in the last minute.|
|aws.ec2_statuscheckfailed_system_max  |gauge  |cloud.service, cloud.instance.type, cloud.instance.region, cloud.instance.az|Count  |Reports whether the instance has passed the system status check in the last minute.                                   |
|aws.ec2_statuscheckfailed_instance_max|gauge  |cloud.service, cloud.instance.type, cloud.instance.region, cloud.instance.az|Count  |Reports whether the instance has passed the instance status check in the last minute.                                 |

Additional labels can be applied to all the metrics from this plugin via the `INSTANCE_LABELS` plugin variable.

== Installation ==

In order for this integration to run, you must create an IAM role and access keys for the plugin
to connect to your AWS EC2 APIs and AWS Cloudwatch metrics:

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

* `ec2-discovery.py` uses the Outlyer agent's instance discovery mechanism to automatically discover all the EC2 instances in a specified region
* `aws-ec2.py` is deployed as a standard check runs against each EC2 instance discovered in the discovery plugin

The discovery plugin must be currently deployed manually to disk on an agent. The plugin must be put in the agent's `plugins` folder and
a discovery check YAML file must be configured in the agent's `conf.d` folder. An example of the YAML configuration file is shown below:

```yaml
discovers:
  ec2-discovery:
    command: '/opt/outlyer/embedded/bin/python3 /etc/outlyer/plugins/ec2-discovery.py'
    interval: 300
    disabled: false
    timeout: 120

    #labels:
    # environment: 'prod'

    #metric_labels:
    #  - 'environment'

    #check_command: 
    check_interval: 30

    env:
      AWS_ACCESS_KEY_ID: <AWS_ACCESS_KEY_ID>
      AWS_SECRET_ACCESS_KEY: <AWS_SECRET_ACCESS_KEY>
      AWS_REGION: <AWS_REGION>
```

Once running you should see almost immediately all your EC2 instances in the host view of the Outlyer UI. After that you can then deploy the
`aws-ec2.py` monitoring check to monitor all of the instances via Cloudwatch. It is recommended that you use the check selector `cloud.service=aws.ec2`
to ensure the check runs against all your EC2 instances.

**It is recommended that both plugins run at 5 minute intervals to avoid significant charges on your AWS account bills**

Both plugins must set the following variables to run:

* `AWS_ACCESS_KEY_ID`: The AWS Access Key copied above
* `AWS_SECRET_ACCESS_KEY`: The AWS Secret Key copied above
* `AWS_REGION`: The AWS Region your RDS instnces are running in

In addition the following variables can be set to override the default values:

* `INSTANCE_LABELS`: A comma seperated list of any labels applied to the EC2 instance from the discovery script to add to all the metrics from the aws-ec2.py plugin.
* `time_range`: The time range in minutes to query your metrics over. By default this is set to the last
10 minutes but if you run your functions rarely this can be set to longer for testing purposes.

== Changelog ==

|Version|Release Date|Description                                           |
|-------|------------|------------------------------------------------------|
|1.1    |19-Jul-2018 |Added INSTANCE_LABELS variable and fixed several bugs.|
|1.0    |25-Jun-2018 |Initial version of our EC2 monitoring integration.    |