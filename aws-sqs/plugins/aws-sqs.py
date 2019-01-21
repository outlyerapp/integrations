#!/usr/bin/env python3

import boto3
import sys
from datetime import datetime, timedelta

from outlyer_plugin import Plugin, Status

INSTANCE_METRICS = [
    {
        'id': 'sqs_oldestmessage_max',
        'namespace': 'AWS/SQS',
        'metric': 'ApproximateAgeOfOldestMessage',
        'stat': 'Maximum',
        'unit': 'Seconds',
        'period': 300,
        'filter_dimension': 'QueueName',
        'dimensions': [
            {
                'Name': 'QueueName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'sqs_messagesdelayed_sum',
        'namespace': 'AWS/SQS',
        'metric': 'ApproximateNumberOfMessagesDelayed',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'QueueName',
        'dimensions': [
            {
                'Name': 'QueueName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'sqs_messagesnotvisible_sum',
        'namespace': 'AWS/SQS',
        'metric': 'ApproximateNumberOfMessagesNotVisible',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'QueueName',
        'dimensions': [
            {
                'Name': 'QueueName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'sqs_messagesvisible_sum',
        'namespace': 'AWS/SQS',
        'metric': 'ApproximateNumberOfMessagesVisible',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'QueueName',
        'dimensions': [
            {
                'Name': 'QueueName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'sqs_emptyreceives_sum',
        'namespace': 'AWS/SQS',
        'metric': 'NumberOfEmptyReceives',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'QueueName',
        'dimensions': [
            {
                'Name': 'QueueName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'sqs_messagesdeleted_sum',
        'namespace': 'AWS/SQS',
        'metric': 'NumberOfMessagesDeleted',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'QueueName',
        'dimensions': [
            {
                'Name': 'QueueName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'sqs_messagesreceived_sum',
        'namespace': 'AWS/SQS',
        'metric': 'NumberOfMessagesReceived',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'QueueName',
        'dimensions': [
            {
                'Name': 'QueueName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'sqs_messagessent_sum',
        'namespace': 'AWS/SQS',
        'metric': 'NumberOfMessagesSent',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'QueueName',
        'dimensions': [
            {
                'Name': 'QueueName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'sqs_sentmessagesize_avg',
        'namespace': 'AWS/SQS',
        'metric': 'SentMessageSize',
        'stat': 'Average',
        'unit': 'Bytes',
        'period': 300,
        'filter_dimension': 'QueueName',
        'dimensions': [
            {
                'Name': 'QueueName',
                'Value': ''
            }
        ]
    },
]

class AWSSQS(Plugin):

    def collect(self, _):
        try:
            aws_region = self.get('AWS_REGION', 'us-east-1')
            time_range = self.get('time_range', '10')

            # Get list of SQS Queues in AWS Account Region
            instances = []
            sqs = boto3.resource('sqs', region_name=aws_region,
                                     aws_access_key_id = self.get('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key = self.get('AWS_SECRET_ACCESS_KEY'))
            for queue in sqs.queues.all():
                queue_name = queue.url.split('/')[-1]
                instances.append(queue_name)

            self.logger.info(f"Found {len(instances)} SQS Queues in {aws_region} region.")

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
                    'queue': instance,
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
    sys.exit(AWSSQS().run())