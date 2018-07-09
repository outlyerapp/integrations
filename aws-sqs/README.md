AWS SQS Integration
==================

== Description ==

Once enabled, this integration will collect metrics on every SQS Queue in your AWS account
for a particular region(s) and provide a dashboard to view the key metrics. Amazon Simple Queue Service (SQS) is a fully managed 
message queuing service that enables you to decouple and scale microservices, distributed systems, and serverless applications. 

== Metrics Collected ==

A full list of available Cloudwatch metrics for S3 is available
<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/sqs-metricscollected.html" target="_blank">here</a>.

|Metric Name                   |Type   |Labels       |Unit   |Description                                                                                                                                                                                                |
|------------------------------|-------|-------------|-------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|aws.sqs_oldestmessage_max     |gauge  |queue, region|Seconds|The approximate age of the oldest non-deleted message in the queue.                                                                                                                                        |
|aws.sqs_messagesdelayed_sum   |gauge  |queue, region|Count  |The number of messages in the queue that are delayed and not available for reading immediately.                                                                                                            |
|aws.sqs_messagesnotvisible_sum|gauge  |queue, region|Count  |The number of messages that are "in flight." Messages are considered in flight if they have been sent to a client but have not yet been deleted or have not yet reached the end of their visibility window.|
|aws.sqs_messagesvisible_sum   |gauge  |queue, region|Count  |The number of messages available for retrieval from the queue.                                                                                                                                             |
|aws.sqs_emptyreceives_sum     |gauge  |queue, region|Count  |The number of ReceiveMessage API calls that did not return a message.                                                                                                                                      |
|aws.sqs_messagesdeleted_sum   |gauge  |queue, region|Count  |The number of messages deleted from the queue.                                                                                                                                                             |
|aws.sqs_messagesreceived_sum  |gauge  |queue, region|Count  |The number of messages returned by calls to the ReceiveMessage action.                                                                                                                                     |
|aws.sqs_messagessent_sum      |gauge  |queue, region|Count  |The number of messages added to a queue.                                                                                                                                                                   |
|aws.sqs_sentmessagesize_avg   |gauge  |queue, region|Bytes  |The size of messages added to a queue.                                                                                                                                                                     |

== Installation ==

In order for this integration to run, you must create an IAM role and access keys for the plugin
to connect to your AWS SQS APIs and AWS Cloudwatch metrics:

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
|1.0    |24-Jun-2018 |Initial version of our AWS SQS integration.    |