#!/usr/bin/env python3

import boto3
import sys
import uuid
from datetime import datetime, timedelta

from outlyer_plugin import Plugin, Status


class AWSBilling(Plugin):

    def collect(self, _):
        try:
            time_range = self.get('time_range', '24')

            # Create CloudWatch client for us-east-1 region
            # All billing metrics are stored in this region
            cloudwatch = boto3.client('cloudwatch', 'us-east-1')

            # List all metrics through the pagination interface
            metrics = {}
            paginator = cloudwatch.get_paginator('list_metrics')
            for response in paginator.paginate(Namespace='AWS/Billing'):
                for metric in response['Metrics']:
                    # Add a uuid so we can link metric values to original metric
                    id = 'a_' + uuid.uuid4().hex
                    metrics[id] = metric

            if len(metrics) < 1:
                raise Exception('No metrics found. Did you enable Billing Alerts under your AWS billing preferences?')

            # Build metric query to get metric values
            query = []
            for key, value in metrics.items():
                query.append({
                    'Id': key,
                    'MetricStat': {
                        'Metric': {
                            'Namespace': value['Namespace'],
                            'MetricName': value['MetricName'],
                            'Dimensions': value['Dimensions']
                        },
                        'Period': 300,
                        'Stat': 'Maximum',
                    }
                })

            # Get metric values
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=int(time_range))
            values = cloudwatch.get_metric_data(
                MetricDataQueries=query,
                StartTime=start_time,
                EndTime=end_time,
                ScanBy='TimestampAscending')

            for value in values['MetricDataResults']:
                metric = metrics[value['Id']]
                metric_labels = self.convertDimensionToDict(metric['Dimensions'])
                metric_value = 0
                if len(value['Values']) > 0:
                    metric_value = value['Values'][-1]
                self.gauge('aws.billing_estimated_charges', metric_labels).set(metric_value)

            return Status.OK

        except Exception as err:
            raise err
            return Status.UNKNOWN

    def convertDimensionToDict(self, dimensions):
        labels = {}
        for label in dimensions:
            labels[label['Name']] = label['Value']
        return labels


if __name__ == '__main__':
    sys.exit(AWSBilling().run())