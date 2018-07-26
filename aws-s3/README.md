AWS S3 Integration
==================

== Description ==

This integration monitors Amazon's Simple Storage Service (S3). Amazon S3 is object storage 
built to store and retrieve any amount of data from anywhere – web sites and mobile apps, 
corporate applications, and data from IoT sensors or devices. It is designed to deliver 
99.999999999% durability, and stores data for millions of applications used by market leaders 
in every industry.

Once enabled, this integration will collect metrics on every S3 bucket in your AWS account
and provide a dashboard to view the key metrics.

== Metrics Collected ==

A full list of available Cloudwatch metrics for S3 is available
<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/s3-metricscollected.html" target="_blank">here</a>.

All S3 buckets will provide standard metrics, but request metrics need to be enabled on each bucket to view them 
and are counted as paid custom metrics. Hence by default request metrics will not be shown unless you enable
the additional monitoring on AWS.

## Standard Metrics

|Metric Name                   |Type   |Labels    |Unit |Description                                                                 |
|------------------------------|-------|----------|-----|----------------------------------------------------------------------------|
|aws.s3_bucketsizebytes_avg    |gauge  |s3.bucket |Bytes|The amount of data in bytes stored in a bucket in the Standard storage class|
|aws.s3_numberofobjects_avg    |gauge  |s3.bucket |Count|The total number of objects stored in a bucket for all storage classes      |

## Request Metrics

|Metric Name                   |Type   |Labels    |Unit        |Description                                                                                                                     |
|------------------------------|-------|----------|------------|--------------------------------------------------------------------------------------------------------------------------------|
|aws.s3_getrequests_sum        |gauge  |s3.bucket |Count       |The number of HTTP GET requests made for objects in an Amazon S3 bucket.                                                        |
|aws.s3_putrequests_sum        |gauge  |s3.bucket |Count       |The number of HTTP PUT requests made for objects in an Amazon S3 bucket.                                                        |
|aws.s3_deleterequests_sum     |gauge  |s3.bucket |Count       |The number of HTTP DELETE requests made to an Amazon S3 bucket.                                                                 |
|aws.s3_headrequests_sum       |gauge  |s3.bucket |Count       |The number of HTTP HEAD requests made to an Amazon S3 bucket.                                                                   |
|aws.s3_postrequests_sum       |gauge  |s3.bucket |Count       |The number of HTTP POST requests made to an Amazon S3 bucket.                                                                   |
|aws.s3_selectrequests_sum     |gauge  |s3.bucket |Count       |The number of Amazon S3 SELECT Object Content requests made for objects in an Amazon S3 bucket.                                 |
|aws.s3_listrequests_sum       |gauge  |s3.bucket |Count       |The number of HTTP requests that list the contents of a bucket.                                                                 |
|aws.s3_bytesdownloaded_sum    |gauge  |s3.bucket |Bytes       |The number bytes downloaded for requests made to an Amazon S3 bucket, where the response includes a body.                       |
|aws.s3_bytesuploaded_sum      |gauge  |s3.bucket |Bytes       |The number bytes uploaded that contain a request body, made to an Amazon S3 bucket.                                             |
|aws.s3_4xxerrors_sum          |gauge  |s3.bucket |Count       |The number of HTTP 4xx client error status code requests made to an Amazon S3 bucket with a value of either 0 or 1.             |
|aws.s3_5xxerrors_sum          |gauge  |s3.bucket |Count       |The number of HTTP 5xx server error status code requests made to an Amazon S3 bucket with a value of either 0 or 1.             |
|aws.s3_firstbytelatency_max   |gauge  |s3.bucket |Milliseconds|The per-request time from the complete request being received by an Amazon S3 bucket to when the response starts to be returned.|
|aws.s3_totalrequestlatency_max|gauge  |s3.bucket |Milliseconds|The elapsed per-request time from the first byte received to the last byte sent to an Amazon S3 bucket.                         |

== Installation ==

In order for this integration to run, you must create an IAM role and access keys for the plugin
to connect to your AWS S3 APIs and AWS Cloudwatch metrics:

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
* `AWS_REGION`: The AWS Region to list S3 buckets for

In addition the following variables can be set to override the default values:

* `time_range`: The time range in hours to query your metrics over. By default this is set to the last
48 hours as storatge usage is calculated once every day.

**It is recommended this plugin is run at most every 5 minutes to avoid high additional charges on your AWS acount**

== Changelog ==

|Version|Release Date|Description                                    |
|-------|------------|-----------------------------------------------|
|1.0    |24-Jun-2018 |Initial version of our AWS S3 integration.     |