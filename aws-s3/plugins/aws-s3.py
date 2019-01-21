#!/usr/bin/env python3

import boto3
import sys
from datetime import datetime, timedelta

from outlyer_plugin import Plugin, Status

INSTANCE_METRICS = [
    {
        'id': 's3_bucketsizebytes_avg',
        'namespace': 'AWS/S3',
        'metric': 'BucketSizeBytes',
        'stat': 'Average',
        'unit': 'Bytes',
        'period': 86400,
        'filter_dimension': 'BucketName',
        'dimensions': [
            {
                'Name': 'BucketName',
                'Value': ''
            },
            {
                'Name': 'StorageType',
                'Value': 'StandardStorage'
            }
        ]
    },
    {
        'id': 's3_numberofobjects_avg',
        'namespace': 'AWS/S3',
        'metric': 'NumberOfObjects',
        'stat': 'Average',
        'unit': 'Count',
        'period': 86400,
        'filter_dimension': 'BucketName',
        'dimensions': [
            {
                'Name': 'BucketName',
                'Value': ''
            },
            {
                'Name': 'StorageType',
                'Value': 'AllStorageTypes'
            }
        ]
    },
    # Paid Cloudwatch Metrics
    {
        'id': 's3_getrequests_sum',
        'namespace': 'AWS/S3',
        'metric': 'GetRequests',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'BucketName',
        'dimensions': [
            {
                'Name': 'BucketName',
                'Value': ''
            },
            {
                'Name': 'FilterId',
                'Value': 'EntireBucket'
            }
        ]
    },
    {
        'id': 's3_putrequests_sum',
        'namespace': 'AWS/S3',
        'metric': 'PutRequests',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'BucketName',
        'dimensions': [
            {
                'Name': 'BucketName',
                'Value': ''
            },
            {
                'Name': 'FilterId',
                'Value': 'EntireBucket'
            }
        ]
    },
    {
        'id': 's3_deleterequests_sum',
        'namespace': 'AWS/S3',
        'metric': 'DeleteRequests',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'BucketName',
        'dimensions': [
            {
                'Name': 'BucketName',
                'Value': ''
            },
            {
                'Name': 'FilterId',
                'Value': 'EntireBucket'
            }
        ]
    },
    {
        'id': 's3_headrequests_sum',
        'namespace': 'AWS/S3',
        'metric': 'HeadRequests',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'BucketName',
        'dimensions': [
            {
                'Name': 'BucketName',
                'Value': ''
            },
            {
                'Name': 'FilterId',
                'Value': 'EntireBucket'
            }
        ]
    },
    {
        'id': 's3_postrequests_sum',
        'namespace': 'AWS/S3',
        'metric': 'PostRequests',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'BucketName',
        'dimensions': [
            {
                'Name': 'BucketName',
                'Value': ''
            },
            {
                'Name': 'FilterId',
                'Value': 'EntireBucket'
            }
        ]
    },
    {
        'id': 's3_selectrequests_sum',
        'namespace': 'AWS/S3',
        'metric': 'SelectRequests',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'BucketName',
        'dimensions': [
            {
                'Name': 'BucketName',
                'Value': ''
            },
            {
                'Name': 'FilterId',
                'Value': 'EntireBucket'
            }
        ]
    },
    {
        'id': 's3_listrequests_sum',
        'namespace': 'AWS/S3',
        'metric': 'ListRequests',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'BucketName',
        'dimensions': [
            {
                'Name': 'BucketName',
                'Value': ''
            },
            {
                'Name': 'FilterId',
                'Value': 'EntireBucket'
            }
        ]
    },
    {
        'id': 's3_bytesdownloaded_sum',
        'namespace': 'AWS/S3',
        'metric': 'BytesDownloaded',
        'stat': 'Sum',
        'unit': 'Bytes',
        'period': 300,
        'filter_dimension': 'BucketName',
        'dimensions': [
            {
                'Name': 'BucketName',
                'Value': ''
            },
            {
                'Name': 'FilterId',
                'Value': 'EntireBucket'
            }
        ]
    },
    {
        'id': 's3_bytesuploaded_sum',
        'namespace': 'AWS/S3',
        'metric': 'BytesUploaded',
        'stat': 'Sum',
        'unit': 'Bytes',
        'period': 300,
        'filter_dimension': 'BucketName',
        'dimensions': [
            {
                'Name': 'BucketName',
                'Value': ''
            },
            {
                'Name': 'FilterId',
                'Value': 'EntireBucket'
            }
        ]
    },
    {
        'id': 's3_4xxerrors_sum',
        'namespace': 'AWS/S3',
        'metric': '4xxErrors',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'BucketName',
        'dimensions': [
            {
                'Name': 'BucketName',
                'Value': ''
            },
            {
                'Name': 'FilterId',
                'Value': 'EntireBucket'
            }
        ]
    },
    {
        'id': 's3_5xxerrors_sum',
        'namespace': 'AWS/S3',
        'metric': '5xxErrors',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'BucketName',
        'dimensions': [
            {
                'Name': 'BucketName',
                'Value': ''
            },
            {
                'Name': 'FilterId',
                'Value': 'EntireBucket'
            }
        ]
    },
    {
        'id': 's3_firstbytelatency_max',
        'namespace': 'AWS/S3',
        'metric': 'FirstByteLatency',
        'stat': 'Maximum',
        'unit': 'Milliseconds',
        'period': 300,
        'filter_dimension': 'BucketName',
        'dimensions': [
            {
                'Name': 'BucketName',
                'Value': ''
            },
            {
                'Name': 'FilterId',
                'Value': 'EntireBucket'
            }
        ]
    },
    {
        'id': 's3_totalrequestlatency_max',
        'namespace': 'AWS/S3',
        'metric': 'TotalRequestLatency',
        'stat': 'Maximum',
        'unit': 'Milliseconds',
        'period': 300,
        'filter_dimension': 'BucketName',
        'dimensions': [
            {
                'Name': 'BucketName',
                'Value': ''
            },
            {
                'Name': 'FilterId',
                'Value': 'EntireBucket'
            }
        ]
    },
]

class AWSS3(Plugin):

    def collect(self, _):
        try:
            aws_region = self.get('AWS_REGION')
            if not aws_region:
                raise Exception("Please set AWS_REGION")
            time_range = self.get('time_range', '2')

            # Get list of all S3 buckets in AWS Account
            awsclient = boto3.client('s3', aws_region,
                                     aws_access_key_id=self.get('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key=self.get('AWS_SECRET_ACCESS_KEY'))
            buckets = awsclient.list_buckets()['Buckets']
            self.logger.info(f"Successfully found {len(buckets)} buckets")

            # Get metrics for each bucket
            cloudwatch = boto3.client('cloudwatch', aws_region,
                                      aws_access_key_id=self.get('AWS_ACCESS_KEY_ID'),
                                      aws_secret_access_key=self.get('AWS_SECRET_ACCESS_KEY'))
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=int(time_range))
            for instance in buckets:
                response = cloudwatch.get_metric_data(
                    MetricDataQueries=self.build_instance_query(instance['Name']),
                    StartTime=start_time,
                    EndTime=end_time,
                    ScanBy='TimestampAscending')

                metric_labels = {
                    's3.bucket': instance['Name'],
                }

                # Get last value for each metric, if no values skip
                for metric in response['MetricDataResults']:
                    metric_name = "aws." + metric['Id']
                    if len(metric['Values']) > 0:
                        value = metric['Values'][-1]
                        self.gauge(metric_name, metric_labels).set(value)

            return Status.OK
        except Exception as err:
            raise err
            return Status.UNKNOWN

    def build_instance_query(self, instance: str):
        query = []
        id = 0
        for instance_metric in INSTANCE_METRICS:
            dimensions = instance_metric['dimensions']
            for dimension in dimensions:
                if dimension['Name'] == instance_metric['filter_dimension']:
                    dimension['Value'] = instance
            metric = {
                'Id': instance_metric['id'],
                'MetricStat': {
                    'Metric': {
                        'Namespace': instance_metric['namespace'],
                        'MetricName': instance_metric['metric'],
                        'Dimensions': dimensions,
                     },
                    'Period': instance_metric['period'],
                    'Stat': instance_metric['stat'],
                    'Unit': instance_metric['unit'],
                }
            }
            query.append(metric)
            id += 1

        return query


if __name__ == '__main__':
    sys.exit(AWSS3().run())