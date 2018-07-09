AWS SNS Integration
==================

== Description ==

This integration monitors your Amazon Simple Notification Service (SNS) topics via Cloudwatch. SNS is a flexible, fully 
managed pub/sub messaging and mobile notifications service for coordinating the delivery of messages to subscribing endpoints 
and clients.

Once enabled, this integration will collect metrics on every SNS Topic in your AWS region(s) and provide a dashboard to view 
the key metrics.

== Metrics Collected ==

A full list of available Cloudwatch metrics for SNS is available
<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/sns-metricscollected.html" target="_blank">here</a>.

|Metric Name                                           |Type   |Labels       |Unit |Description                                                                                                                                                                 |
|------------------------------------------------------|-------|-------------|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|aws.sns_messagespublished_sum                         |gauge  |topic, region|     |The number of messages published to your Amazon SNS topic.                                                                                                                  |
|aws.sns_notificationsdelivered_sum                    |gauge  |topic, region|     |The number of messages successfully delivered from your Amazon SNS topic to subscribing endpoints.                                                                          |
|aws.sns_notificationsfailed_sum                       |gauge  |topic, region|     |The number of messages that Amazon SNS failed to deliver.                                                                                                                   |
|aws.sns_notificationsfilteredout_sum                  |gauge  |topic, region|     |The number of messages that were rejected by subscription filter policies. A filter policy rejects a message when the message attributes do not match the policy attributes.|
|aws.sns_notificationsfilteredout_noattributes_sum     |gauge  |topic, region|     |The number of messages that were rejected by subscription filter policies because the messages have no attributes.                                                          |
|aws.sns_notificationsfilteredout_invalidattributes_sum|gauge  |topic, region|     |The number of messages that were rejected by subscription filter policies because the message's attributes are invalid.                                                     |
|aws.sns_publishsize_max                               |gauge  |topic, region|     |The size of messages published.                                                                                                                                             |
|aws.sns_monthtodatespendusd_max                       |gauge  |topic, region|     |The charges you have accrued since the start of the current calendar month for sending SMS messages across all topics                                                       |

== Installation ==

In order for this integration to run, you must create an IAM role and access keys for the plugin
to connect to your AWS SNS APIs and AWS Cloudwatch metrics:

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
|1.0    |24-Jun-2018 |Initial version of our AWS SNS integration.    |