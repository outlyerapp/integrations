AWS Kineis Integration
======================

== Description ==

This integration will collect metrics on every Kinesis Stream in a specified AWS region via Cloudwatch
so you can easily monitor your Kinesis Streams in Outlyer.

AWS Kinesis provides high throughput message queues (streams) as a managed service so producers can put messages on
the streams for consumers to process.

The following diagram illustrates the high-level architecture of Kinesis Data Streams. 
The producers continually push data to Kinesis Data Streams and the consumers process the data in real time. 
Consumers (such as a custom application running on Amazon EC2, or an Amazon Kinesis Data Firehose delivery stream) 
can store their results using an AWS service such as Amazon DynamoDB, Amazon Redshift, or Amazon S3.

![Kinesis Diagram](https://docs.aws.amazon.com/streams/latest/dev/images/architecture.png)

== Metrics Collected ==

A full list of available Cloudwatch metrics for Amazon Kinesis is available
<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ak-metricscollected.html" target="_blank">here</a>.

|Metric Name                                       |Type   |Labels        |Unit        |Description                                                                                    |
|--------------------------------------------------|-------|--------------|------------|-----------------------------------------------------------------------------------------------|
|aws.kinesis_getrecords_bytes_sum                  |gauge  |stream, region|Bytes       |The number of bytes retrieved from the Kinesis stream.                                         |
|aws.kinesis_getrecords_iteratoragemilliseconds_max|gauge  |stream, region|Milliseconds|The age of the last record in all GetRecords calls made against an Kinesis stream.             |
|aws.kinesis_getrecords_latency_max                |gauge  |stream, region|Count       |The maximum time taken per GetRecords operation.                                               |
|aws.kinesis_getrecords_records_sum                |gauge  |stream, region|Count       |The number of records retrieved from the shard.                                                |
|aws.kinesis_getrecords_success_sum                |gauge  |stream, region|Count       |The number of successful GetRecords operations per stream.                                     |
|aws.kinesis_incomingbytes_sum                     |gauge  |stream, region|Bytes       |The number of bytes successfully put to the Kinesis stream.                                    |
|aws.kinesis_incomingrecords_sum                   |gauge  |stream, region|Count       |The number of records successfully put to the Kinesis stream.                                  |
|aws.kinesis_putrecord_bytes_sum                   |gauge  |stream, region|Bytes       |The number of bytes put to the Kinesis stream using the PutRecord operation.                   |
|aws.kinesis_putrecord_latency_max                 |gauge  |stream, region|Milliseconds|The maximum time taken per PutRecord operation.                                                |
|aws.kinesis_putrecord_success_sum                 |gauge  |stream, region|Count       |The number of successful PutRecord operations per Kinesis stream.                              |
|aws.kinesis_putrecords_bytes_sum                  |gauge  |stream, region|Bytes       |The number of bytes put to the Kinesis stream using the PutRecords operation.                  |
|aws.kinesis_putrecords_latency_max                |gauge  |stream, region|Milliseconds|The maximum time taken per PutRecords operation.                                               |
|aws.kinesis_putrecords_records_sum                |gauge  |stream, region|Count       |The number of successful records in a PutRecords operation per Kinesis stream.                 |
|aws.kinesis_putrecords_success_sum                |gauge  |stream, region|Count       |The number of PutRecords operations where at least one record succeeded, per Kinesis stream.   |
|aws.kinesis_readprovisionedthroughputexceeded_avg |gauge  |stream, region|Count       |The number of GetRecords calls throttled for the stream over the specified time period.        |
|aws.kinesis_writeprovisionedthroughputexceeded_avg|gauge  |stream, region|Count       |The number of records rejected due to throttling for the stream over the specified time period.|

== Installation ==

In order for this integration to run, you must create an IAM role and access keys for the plugin
to connect to your AWS Kinesis APIs and AWS Cloudwatch metrics:

1. To get started, open the AWS Management Console
2. Click the IAM tab.
3. Click the Create a New Group of Users button.
4. Enter a Group Name called Outlyer.
5. Select the Read Only Access Policy Template then click Continue.
6. Click the Create New Users tab.
7. Enter a new User Name called Outlyer and click Continue and then Finish.
8. Click Show User Security Credentials.
9. Copy and paste your Access Key Id and the Secret Access Key somewhere safe.

The plugin must set the following variables to run:

* `AWS_ACCESS_KEY_ID`: The AWS Access Key copied above
* `AWS_SECRET_ACCESS_KEY`: The AWS Secret Key copied above

In addition the following variables can be set to override the default values:

* `time_range`: The time range in minutes to query your metrics over. By default this is set to the last 10 minutes.

**It is recommended this plugin is run at most every 5 minutes to avoid high additional charges on your AWS acount**

== Changelog ==

|Version|Release Date|Description                                    |
|-------|------------|-----------------------------------------------|
|1.0    |24-Jun-2018 |Initial version of our AWS Kinesis integration.|
