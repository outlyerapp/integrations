AWS DynamoDB Integration
========================

== Description ==

Amazon DynamoDB is a fast and flexible nonrelational database service for all applications that need consistent, 
single-digit millisecond latency at any scale. It is a fully managed cloud database and supports both document and 
key-value store models. Its flexible data model, reliable performance, and automatic scaling of throughput capacity 
make it a great fit for mobile, web, gaming, ad tech, IoT, and many other applications.

This integration captures all the key DynamoDB metrics from Amazon Cloudwatch and provides a dashboard so you can easily
see the status and performance of all your DynamoDB tables in one place.

== Metrics Collected ==

A full list of available Cloudwatch metrics for DynamoDB is available
<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/dynamo-metricscollected.html" target="_blank">here</a>.

|Metric Name                                      |Type   |Labels       |Unit        |Description                                                                                                                                  |
|-------------------------------------------------|-------|-------------|------------|---------------------------------------------------------------------------------------------------------------------------------------------|
|aws.dynamodb_provisionedwritecapacityunits_max   |gauge  |table, region|Count       |The number of provisioned write capacity units for a table                                                                                   |
|aws.dynamodb_consumedwritecapacityunits_max      |gauge  |table, region|Count       |The number of write capacity units consumed over the specified time period, so you can track how much of your provisioned throughput is used.|
|aws.dynamodb_provisionedreadcapacityunits_max    |gauge  |table, region|Count       |The number of provisioned read capacity units for a table or a global secondary index.                                                       |
|aws.dynamodb_consumedreadcapacityunits_max       |gauge  |table, region|Count       |The number of read capacity units consumed over the specified time period, so you can track how much of your provisioned throughput is used. |
|aws.dynamodb_getitem_throttledrequests_sum       |gauge  |table, region|Count       |GetItem requests to DynamoDB that exceed the provisioned throughput limits on a table.                                                       |
|aws.dynamodb_scan_throttledrequests_sum          |gauge  |table, region|Count       |Scan requests to DynamoDB that exceed the provisioned throughput limits on a table.                                                          |
|aws.dynamodb_query_throttledrequests_sum         |gauge  |table, region|Count       |Query requests to DynamoDB that exceed the provisioned throughput limits on a table.                                                         |
|aws.dynamodb_batchgetitem_throttledrequests_sum  |gauge  |table, region|Count       |BatchGetItem requests to DynamoDB that exceed the provisioned throughput limits on a table.                                                  |
|aws.dynamodb_putitem_throttledrequests_sum       |gauge  |table, region|Count       |PutItem requests to DynamoDB that exceed the provisioned throughput limits on a table.                                                       |
|aws.dynamodb_updateitem_throttledrequests_sum    |gauge  |table, region|Count       |UpdateItem requests to DynamoDB that exceed the provisioned throughput limits on a table.                                                    |
|aws.dynamodb_deleteitem_throttledrequests_sum    |gauge  |table, region|Count       |DeleteItem requests to DynamoDB that exceed the provisioned throughput limits on a table.                                                    |
|aws.dynamodb_batchwriteitem_throttledrequests_sum|gauge  |table, region|Count       |BatchWriteItem requests to DynamoDB that exceed the provisioned throughput limits on a table.                                                |
|aws.dynamodb_getitem_successfulrequestlatency_max|gauge  |table, region|Milliseconds|The maximum elapsed time for successful GetItem requests to DynamoDB or Amazon DynamoDB Streams during the specified time period.            |
|aws.dynamodb_putitem_successfulrequestlatency_max|gauge  |table, region|Milliseconds|The maximum elapsed time for successful PutItem requests to DynamoDB or Amazon DynamoDB Streams during the specified time period.            |
|aws.dynamodb_scan_successfulrequestlatency_max   |gauge  |table, region|Milliseconds|The maximum elapsed time for successful Scan requests to DynamoDB or Amazon DynamoDB Streams during the specified time period.               |
|aws.dynamodb_query_successfulrequestlatency_max  |gauge  |table, region|Milliseconds|The maximum elapsed time for successful Query requests to DynamoDB or Amazon DynamoDB Streams during the specified time period.              |
|aws.dynamodb_timetolivedeleteditemcount_sum      |gauge  |table, region|Count       |The number of items deleted by Time To Live (TTL) during the specified time period.                                                          |
|aws.dynamodb_getrecords_sum                      |gauge  |table, region|Count       |Get records represents the number of stream records retrieved.                                                                               |
|aws.dynamodb_scan_returneditemcount_sum          |gauge  |table, region|Count       |The number of items returned by Scan operations during the specified time period.                                                            |
|aws.dynamodb_query_returneditemcount_sum         |gauge  |table, region|Count       |The number of items returned by Query operations during the specified time period.                                                           |
|aws.dynamodb_getitem_systemerrors_sum            |gauge  |table, region|Count       |GetItem Requests to DynamoDB or Amazon DynamoDB Streams that generate an HTTP 500 status code during the specified time period.              |
|aws.dynamodb_scan_systemerrors_sum               |gauge  |table, region|Count       |Scan Requests to DynamoDB or Amazon DynamoDB Streams that generate an HTTP 500 status code during the specified time period.                 |
|aws.dynamodb_query_systemerrors_sum              |gauge  |table, region|Count       |Query Requests to DynamoDB or Amazon DynamoDB Streams that generate an HTTP 500 status code during the specified time period.                |
|aws.dynamodb_batchgetitem_systemerrors_sum       |gauge  |table, region|Count       |BatchGetItem Requests to DynamoDB or Amazon DynamoDB Streams that generate an HTTP 500 status code during the specified time period.         |
|aws.dynamodb_putitem_systemerrors_sum            |gauge  |table, region|Count       |PutItem Requests to DynamoDB or Amazon DynamoDB Streams that generate an HTTP 500 status code during the specified time period.              |
|aws.dynamodb_updateitem_systemerrors_sum         |gauge  |table, region|Count       |UpdateItem Requests to DynamoDB or Amazon DynamoDB Streams that generate an HTTP 500 status code during the specified time period.           |
|aws.dynamodb_deleteitem_systemerrors_sum         |gauge  |table, region|Count       |DeleteItem Requests to DynamoDB or Amazon DynamoDB Streams that generate an HTTP 500 status code during the specified time period.           |
|aws.dynamodb_batchwriteitem_systemerrors_sum     |gauge  |table, region|Count       |BatchWriteItem Requests to DynamoDB or Amazon DynamoDB Streams that generate an HTTP 500 status code during the specified time period.       |

== Installation ==

In order for this integration to run, you must create an IAM role and access keys for the plugin
to connect to your AWS DynamoDB APIs and AWS Cloudwatch metrics:

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

|Version|Release Date|Description                                     |
|-------|------------|------------------------------------------------|
|1.0    |24-Jun-2018 |Initial version of our AWS DynamoDB integration.|