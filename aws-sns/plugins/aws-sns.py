#!/usr/bin/env python3

import boto3
import sys
from datetime import datetime, timedelta

from outlyer_plugin import Plugin, Status

INSTANCE_METRICS = [
    {
        'id': 'sns_messagespublished_sum',
        'namespace': 'AWS/SNS',
        'metric': 'NumberOfMessagesPublished',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TopicName',
        'dimensions': [
            {
                'Name': 'TopicName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'sns_notificationsdelivered_sum',
        'namespace': 'AWS/SNS',
        'metric': 'NumberOfNotificationsDelivered',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TopicName',
        'dimensions': [
            {
                'Name': 'TopicName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'sns_notificationsfailed_sum',
        'namespace': 'AWS/SNS',
        'metric': 'NumberOfNotificationsFailed',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TopicName',
        'dimensions': [
            {
                'Name': 'TopicName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'sns_notificationsfilteredout_sum',
        'namespace': 'AWS/SNS',
        'metric': 'NumberOfNotificationsFilteredOut',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TopicName',
        'dimensions': [
            {
                'Name': 'TopicName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'sns_notificationsfilteredout_noattributes_sum',
        'namespace': 'AWS/SNS',
        'metric': 'NumberOfNotificationsFilteredOut-NoMessageAttributes',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TopicName',
        'dimensions': [
            {
                'Name': 'TopicName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'sns_notificationsfilteredout_invalidattributes_sum',
        'namespace': 'AWS/SNS',
        'metric': 'NumberOfNotificationsFilteredOut-InvalidAttributes',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TopicName',
        'dimensions': [
            {
                'Name': 'TopicName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'sns_publishsize_max',
        'namespace': 'AWS/SNS',
        'metric': 'PublishSize',
        'stat': 'Maximum',
        'unit': 'Bytes',
        'period': 300,
        'filter_dimension': 'TopicName',
        'dimensions': [
            {
                'Name': 'TopicName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'sns_monthtodatespendusd_max',
        'namespace': 'AWS/SNS',
        'metric': 'SMSMonthToDateSpentUSD',
        'stat': 'Maximum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TopicName',
        'dimensions': [ ]
    },
]

class AWSSQS(Plugin):

    def collect(self, _):
        try:
            aws_region = self.get('AWS_REGION', 'us-east-1')
            time_range = self.get('time_range', '10')

            # Get list of SNS Topics in AWS Account Region
            instances = []
            awsclient = boto3.client('sns', region_name=aws_region,
                                     aws_access_key_id = self.get('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key = self.get('AWS_SECRET_ACCESS_KEY'))
            paginator = awsclient.get_paginator('list_topics')
            for response in paginator.paginate():
                for instance in response['Topics']:
                    topic_name = instance['TopicArn'].split(':')[-1]
                    instances.append(topic_name)

            self.logger.info(f"Found {len(instances)} SNS Topics in {aws_region} region.")

            # Get metrics for each topic
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
                    'topic': instance,
                    'region': aws_region
                }

                # Get last value for each metric, if no values set metric to 0
                for metric in response['MetricDataResults']:
                    metric_name = "aws." + metric['Id']
                    if len(metric['Values']) > 0:
                        value = metric['Values'][-1]
                        ts = int(metric['Timestamps'][-1].utcnow().timestamp() * 1000)
                        self.gauge(metric_name, metric_labels).set(value,ts=ts)
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
    sys.exit(AWSSQS().run())