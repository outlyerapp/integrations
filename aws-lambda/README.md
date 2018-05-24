AWS Lambda Integration
======================

== Description ==

AWS Lambda lets you run code without provisioning or managing servers. If provides 'functions' as
a service. You pay only for the compute time you consume - there is no charge when your code is not running.

This integration pulls your key lambda metrics from AWS Cloudwatch for each of your functions for a specific
region in your AWS account.

== Metrics Collected ==

| Metric Name                |Type |Labels          |Unit |Description                                     |
|----------------------------|-----|----------------|-----|------------------------------------------------|
|aws.lambda_invocations_count|Gauge|function, region|Count|Number of times function was run in period      |
|aws.lambda_duration_max     |Gauge|function, region|Count|Max run duration of function in period          |
|aws.lambda_duration_avg     |Gauge|function, region|Count|Average run duration of function in period      |
|aws.lambda_errors           |Gauge|function, region|Count|Number of times function errored in period      |
|aws.lambda_throttles        |Gauge|function, region|Count|Number of times function was throttled in period|

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

|Version|Release Date|Description                                         |
|-------|------------|----------------------------------------------------|
|1.0    |22-May-2018 |Initial version of our lambda monitoring integration|