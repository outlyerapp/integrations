#!/usr/bin/env python3

import boto3
import sys
from datetime import datetime, timedelta

from outlyer_plugin import Plugin, Target, Status

INSTANCE_METRICS = [
    {
        'id': 'lambda_invocations_count',
        'namespace': 'AWS/Lambda',
        'metric': 'Invocations',
        'stat': 'Sum',
        'unit': 'Count',
        'filter_dimension': 'FunctionName',
    },
    {
        'id': 'lambda_duration_max',
        'namespace': 'AWS/Lambda',
        'metric': 'Duration',
        'stat': 'Maximum',
        'unit': 'Milliseconds',
        'filter_dimension': 'FunctionName',
    },
    {
        'id': 'lambda_duration_avg',
        'namespace': 'AWS/Lambda',
        'metric': 'Duration',
        'stat': 'Average',
        'unit': 'Milliseconds',
        'filter_dimension': 'FunctionName',
    },
    {
        'id': 'lambda_errors',
        'namespace': 'AWS/Lambda',
        'metric': 'Errors',
        'stat': 'Sum',
        'unit': 'Count',
        'filter_dimension': 'FunctionName',
    },
    {
        'id': 'lambda_throttles',
        'namespace': 'AWS/Lambda',
        'metric': 'Throttles',
        'stat': 'Sum',
        'unit': 'Count',
        'filter_dimension': 'FunctionName',
    }
]


class AWSLambda(Plugin):

    def collect(self, _):
        try:
            aws_region = self.get('AWS_REGION', 'us-east-1')
            time_range = self.get('time_range', '10')

            # Get list of Lambda Functions in AWS Account Region
            instances = []
            awsclient = boto3.client('lambda', aws_region)
            paginator = awsclient.get_paginator('list_functions')
            for response in paginator.paginate():
                for instance in response['Functions']:
                    instances.append(instance['FunctionName'])

            # Get metrics for each function
            cloudwatch = boto3.client('cloudwatch', aws_region)
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=int(time_range))
            for instance in instances:
                response = cloudwatch.get_metric_data(
                    MetricDataQueries=self.build_instance_query(instance),
                    StartTime=start_time,
                    EndTime=end_time,
                    ScanBy='TimestampAscending')

                metric_labels = {
                    'function': instance,
                    'region': aws_region
                }

                # Get last value for each metric, if no values set metric to 0
                for metric in response['MetricDataResults']:
                    value = 0
                    if len(metric['Values']) > 0:
                        value = metric['Values'][-1]
                    metric_name = "aws." + metric['Id']
                    self.gauge(metric_name, metric_labels).set(value)

            return Status.OK
        except Exception as err:
            raise err
            return Status.UNKNOWN

    def build_instance_query(self, instance: str):
        query = []
        id = 0
        for instance_metric in INSTANCE_METRICS:
            metric = {
                'Id': instance_metric['id'],
                'MetricStat': {
                    'Metric': {
                        'Namespace': instance_metric['namespace'],
                        'MetricName': instance_metric['metric'],
                        'Dimensions': [{
                            'Name': instance_metric['filter_dimension'],
                            'Value': instance
                        }]
                    },
                    'Period': 60,
                    'Stat': instance_metric['stat'],
                    'Unit': instance_metric['unit'],
                }
            }
            query.append(metric)
            id += 1

        return query


if __name__ == '__main__':
    sys.exit(AWSLambda().run())