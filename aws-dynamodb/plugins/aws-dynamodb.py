#!/usr/bin/env python3

import boto3
import sys
from datetime import datetime, timedelta

from outlyer_plugin import Plugin, Status

INSTANCE_METRICS = [
    {
        'id': 'dynamodb_provisionedwritecapacityunits_max',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ProvisionedWriteCapacityUnits',
        'stat': 'Maximum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'dynamodb_consumedwritecapacityunits_max',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ConsumedWriteCapacityUnits',
        'stat': 'Maximum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'dynamodb_provisionedreadcapacityunits_max',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ProvisionedReadCapacityUnits',
        'stat': 'Maximum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'dynamodb_consumedreadcapacityunits_max',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ConsumedReadCapacityUnits',
        'stat': 'Maximum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'dynamodb_getitem_throttledrequests_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ThrottledRequests',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'GetItem'
            }
        ]
    },
    {
        'id': 'dynamodb_scan_throttledrequests_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ThrottledRequests',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'Scan'
            }
        ]
    },
    {
        'id': 'dynamodb_query_throttledrequests_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ThrottledRequests',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'Query'
            }
        ]
    },
    {
        'id': 'dynamodb_batchgetitem_throttledrequests_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ThrottledRequests',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'BatchGetItem'
            }
        ]
    },
    {
        'id': 'dynamodb_putitem_throttledrequests_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ThrottledRequests',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'PutItem'
            }
        ]
    },
    {
        'id': 'dynamodb_updateitem_throttledrequests_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ThrottledRequests',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'UpdateItem'
            }
        ]
    },
    {
        'id': 'dynamodb_deleteitem_throttledrequests_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ThrottledRequests',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'DeleteItem'
            }
        ]
    },
    {
        'id': 'dynamodb_batchwriteitem_throttledrequests_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ThrottledRequests',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'BatchWriteItem'
            }
        ]
    },
    {
        'id': 'dynamodb_getitem_successfulrequestlatency_max',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ThrottledRequests',
        'stat': 'Maximum',
        'unit': 'Milliseconds',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'GetItem'
            }
        ]
    },
    {
        'id': 'dynamodb_putitem_successfulrequestlatency_max',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ThrottledRequests',
        'stat': 'Maximum',
        'unit': 'Milliseconds',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'PutItem'
            }
        ]
    },
    {
        'id': 'dynamodb_scan_successfulrequestlatency_max',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ThrottledRequests',
        'stat': 'Maximum',
        'unit': 'Milliseconds',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'Scan'
            }
        ]
    },
    {
        'id': 'dynamodb_query_successfulrequestlatency_max',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ThrottledRequests',
        'stat': 'Maximum',
        'unit': 'Milliseconds',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'Query'
            }
        ]
    },
    {
        'id': 'dynamodb_timetolivedeleteditemcount_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'TimeToLiveDeletedItemCount',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'dynamodb_getrecords_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'GetRecords',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            }
        ]
    },
    {
        'id': 'dynamodb_scan_returneditemcount_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ReturnedItemCount',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'Scan'
            }
        ]
    },
    {
        'id': 'dynamodb_query_returneditemcount_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'ReturnedItemCount',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'Query'
            }
        ]
    },
    {
        'id': 'dynamodb_getitem_systemerrors_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'SystemErrors',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'GetItem'
            }
        ]
    },
    {
        'id': 'dynamodb_scan_systemerrors_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'SystemErrors',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'Scan'
            }
        ]
    },
    {
        'id': 'dynamodb_query_systemerrors_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'SystemErrors',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'Query'
            }
        ]
    },
    {
        'id': 'dynamodb_batchgetitem_systemerrors_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'SystemErrors',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'BatchGetItem'
            }
        ]
    },
    {
        'id': 'dynamodb_putitem_systemerrors_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'SystemErrors',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'PutItem'
            }
        ]
    },
    {
        'id': 'dynamodb_updateitem_systemerrors_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'SystemErrors',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'UpdateItem'
            }
        ]
    },
    {
        'id': 'dynamodb_deleteitem_systemerrors_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'SystemErrors',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'DeleteItem'
            }
        ]
    },
    {
        'id': 'dynamodb_batchwriteitem_systemerrors_sum',
        'namespace': 'AWS/DynamoDB',
        'metric': 'SystemErrors',
        'stat': 'Sum',
        'unit': 'Count',
        'period': 300,
        'filter_dimension': 'TableName',
        'dimensions': [
            {
                'Name': 'TableName',
                'Value': ''
            },
            {
                'Name': 'Operation',
                'Value': 'BatchWriteItem'
            }
        ]
    },
]

class AWSDynamoDB(Plugin):

    def collect(self, _):
        try:
            aws_region = self.get('AWS_REGION', 'us-east-1')
            time_range = self.get('time_range', '10')

            # Get list of Lambda Functions in AWS Account Region
            instances = []
            awsclient = boto3.client('dynamodb', aws_region,
                                     aws_access_key_id = self.get('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key = self.get('AWS_SECRET_ACCESS_KEY'))
            paginator = awsclient.get_paginator('list_tables')
            for response in paginator.paginate():
                for instance in response['TableNames']:
                    instances.append(instance)

            self.logger.info(f"Found {len(instances)} DynamoDB tables in {aws_region} region.")

            # Get metrics for each function
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
                    'table': instance,
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
    sys.exit(AWSDynamoDB().run())