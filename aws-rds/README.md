AWS Lambda Integration
======================

== Description ==

== Metrics Collected ==

| Metric Name                |Type |Labels          |Unit |Description                                      |
|----------------------------|-----|----------------|-----|-------------------------------------------------|
|aws.lambda_invocations_count|Gauge|function, region|Count|Number of times function was run in period.      |

== Installation ==

In order for this integration to run, you must create an IAM role and access keys for the plugin
to connect to your AWS Cloudwatch metrics:

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

* `AWS_REGION`: The AWS Region your Lambda functions are running in (Default `us-east-1`)
* `time_range`: The time range in minutes to query your metrics over. By default this is set to the last
10 minutes but if you run your functions rarely this can be set to longer for testing purposes.

== Changelog ==

|Version|Release Date|Description                                          |
|-------|------------|-----------------------------------------------------|
|1.0    |25-Jun-2018 |Initial version of our RDS monitoring integration.   |