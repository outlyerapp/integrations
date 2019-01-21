#!/usr/bin/env python3

import boto3
import sys
from datetime import datetime, timedelta

from outlyer_plugin import Plugin, Status

INSTANCE_METRICS = [
    {
        'id': 'kinesis_getrecords_bytes_sum',
        'namespace': 'AWS/Kinesis',
        'metric': 'GetRecords.Bytes',
        'stat': 'Sum',
        'unit': 'Bytes',
        'period': 300,
        'filter_dimension': 'StreamName',
        'dimensions': [
            {
                'Name': 'StreamName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'kinesis_getrecords_iteratoragemilliseconds_max',
        'namespace': 'AWS/Kinesis',
        'metric': 'GetRecords.IteratorAgeMilliseconds',
        'stat': 'Maximum',
        'unit': 'Milliseconds',
        'period': 300,
        'filter_dimension': 'StreamName',
        'dimensions': [
            {
                'Name': 'StreamName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'kinesis_getrecords_latency_max',
        'namespace': 'AWS/Kinesis',
        'metric': 'GetRecords.Latency',
        'stat': 'Maximum',
        'unit': 'Milliseconds',
        'period': 300,
        'filter_dimension': 'StreamName',
        'dimensions': [
            {
                'Name': 'StreamName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'kinesis_getrecords_records_sum',
        'namespace': 'AWS/Kinesis',
        'metric': 'GetRecords.Records',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'StreamName',
        'dimensions': [
            {
                'Name': 'StreamName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'kinesis_getrecords_success_sum',
        'namespace': 'AWS/Kinesis',
        'metric': 'GetRecords.Success',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'StreamName',
        'dimensions': [
            {
                'Name': 'StreamName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'kinesis_incomingbytes_sum',
        'namespace': 'AWS/Kinesis',
        'metric': 'IncomingBytes',
        'stat': 'Sum',
        'unit': 'Bytes',
        'period': 300,
        'filter_dimension': 'StreamName',
        'dimensions': [
            {
                'Name': 'StreamName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'kinesis_incomingrecords_sum',
        'namespace': 'AWS/Kinesis',
        'metric': 'IncomingRecords',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'StreamName',
        'dimensions': [
            {
                'Name': 'StreamName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'kinesis_putrecord_bytes_sum',
        'namespace': 'AWS/Kinesis',
        'metric': 'PutRecord.Bytes',
        'stat': 'Sum',
        'unit': 'Bytes',
        'period': 300,
        'filter_dimension': 'StreamName',
        'dimensions': [
            {
                'Name': 'StreamName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'kinesis_putrecord_latency_max',
        'namespace': 'AWS/Kinesis',
        'metric': 'PutRecord.Latency',
        'stat': 'Maximum',
        'unit': 'Milliseconds',
        'period': 300,
        'filter_dimension': 'StreamName',
        'dimensions': [
            {
                'Name': 'StreamName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'kinesis_putrecord_success_sum',
        'namespace': 'AWS/Kinesis',
        'metric': 'PutRecord.Success',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'StreamName',
        'dimensions': [
            {
                'Name': 'StreamName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'kinesis_putrecords_bytes_sum',
        'namespace': 'AWS/Kinesis',
        'metric': 'PutRecords.Bytes',
        'stat': 'Sum',
        'unit': 'Bytes',
        'period': 300,
        'filter_dimension': 'StreamName',
        'dimensions': [
            {
                'Name': 'StreamName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'kinesis_putrecords_latency_max',
        'namespace': 'AWS/Kinesis',
        'metric': 'PutRecords.Latency',
        'stat': 'Maximum',
        'unit': 'Milliseconds',
        'period': 300,
        'filter_dimension': 'StreamName',
        'dimensions': [
            {
                'Name': 'StreamName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'kinesis_putrecords_success_sum',
        'namespace': 'AWS/Kinesis',
        'metric': 'PutRecords.Success',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'StreamName',
        'dimensions': [
            {
                'Name': 'StreamName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'kinesis_putrecords_records_sum',
        'namespace': 'AWS/Kinesis',
        'metric': 'PutRecords.Records',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'StreamName',
        'dimensions': [
            {
                'Name': 'StreamName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'kinesis_readprovisionedthroughputexceeded_avg',
        'namespace': 'AWS/Kinesis',
        'metric': 'ReadProvisionedThroughputExceeded',
        'stat': 'Average',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'StreamName',
        'dimensions': [
            {
                'Name': 'StreamName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'kinesis_writeprovisionedthroughputexceeded_avg',
        'namespace': 'AWS/Kinesis',
        'metric': 'WriteProvisionedThroughputExceeded',
        'stat': 'Average',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'StreamName',
        'dimensions': [
            {
                'Name': 'StreamName',
                'Value': ''
            }
        ]
    },
]

class AWSKinesis(Plugin):

    def collect(self, _):
        try:
            aws_region = self.get('AWS_REGION', 'us-east-1')
            time_range = self.get('time_range', '10')

            # Get list of Kinesis Streams in AWS Account Region
            instances = []
            awsclient = boto3.client('kinesis', aws_region,
                                     aws_access_key_id = self.get('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key = self.get('AWS_SECRET_ACCESS_KEY'))
            paginator = awsclient.get_paginator('list_streams')
            for response in paginator.paginate():
                for instance in response['StreamNames']:
                    instances.append(instance)

            self.logger.info(f"Found {len(instances)} Kinesis Streams in {aws_region} region.")

            # Get metrics for each stream
            cloudwatch = boto3.client('cloudwatch', aws_region,
                                     aws_access_key_id = self.get('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key = self.get('AWS_SECRET_ACCESS_KEY'))
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=int(time_range))
            for instance in instances:
                response = cloudwatch.get_metric_data(
                    MetricDataQueries=self.build_instance_query(instance),
                    StartTime=start_time,
                    EndTime=end_time,
                    ScanBy='TimestampAscending')

                metric_labels = {
                    'stream': instance,
                    'region': aws_region
                }

                # Get last value for each metric, if no values set metric to 0
                for metric in response['MetricDataResults']:
                    metric_name = "aws." + metric['Id']
                    if len(metric['Values']) > 0:
                        value = metric['Values'][-1]
                        self.gauge(metric_name, metric_labels).set(value)
                    else:
                      	self.gauge(metric_name, metric_labels).set(0)

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
    sys.exit(AWSKinesis().run())