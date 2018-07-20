#!/usr/bin/env python3

import boto3
import sys
from datetime import datetime, timedelta

from outlyer_plugin import Plugin, Status

INSTANCE_METRICS = [
    {
        'id': 'ec2_cpucreditusage_max',
        'namespace': 'AWS/EC2',
        'metric': 'CPUCreditUsage',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'InstanceId',
    },
    {
        'id': 'ec2_networkout_max',
        'namespace': 'AWS/EC2',
        'metric': 'NetworkOut',
        'stat': 'Maximum',
        'unit': 'Bytes',
        'filter_dimension': 'InstanceId',
    },
    {
        'id': 'ec2_networkpacketsout_max',
        'namespace': 'AWS/EC2',
        'metric': 'NetworkPacketsOut',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'InstanceId',
    },
    {
        'id': 'ec2_cpusurpluscreditbalance_max',
        'namespace': 'AWS/EC2',
        'metric': 'CPUSurplusCreditBalance',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'InstanceId',
    },
    {
        'id': 'ec2_cpuutilization_max',
        'namespace': 'AWS/EC2',
        'metric': 'CPUUtilization',
        'stat': 'Maximum',
        'unit': 'Percent',
        'filter_dimension': 'InstanceId',
    },
    {
        'id': 'ec2_diskwriteops_max',
        'namespace': 'AWS/EC2',
        'metric': 'DiskWriteOps',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'InstanceId',
    },
    {
        'id': 'ec2_cpucreditbalance_max',
        'namespace': 'AWS/EC2',
        'metric': 'CPUCreditBalance',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'InstanceId',
    },
    {
        'id': 'ec2_cpucreditscharged_max',
        'namespace': 'AWS/EC2',
        'metric': 'CPUSurplusCreditsCharged',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'InstanceId',
    },
    {
        'id': 'ec2_diskreadops_max',
        'namespace': 'AWS/EC2',
        'metric': 'DiskReadOps',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'InstanceId',
    },
    {
        'id': 'ec2_diskwritebytes_max',
        'namespace': 'AWS/EC2',
        'metric': 'DiskWriteBytes',
        'stat': 'Maximum',
        'unit': 'Bytes',
        'filter_dimension': 'InstanceId',
    },
    {
        'id': 'ec2_networkin_max',
        'namespace': 'AWS/EC2',
        'metric': 'NetworkIn',
        'stat': 'Maximum',
        'unit': 'Bytes',
        'filter_dimension': 'InstanceId',
    },
    {
        'id': 'ec2_networkpacketsin_max',
        'namespace': 'AWS/EC2',
        'metric': 'NetworkPacketsIn',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'InstanceId',
    },
    {
        'id': 'ec2_diskreadbytes_max',
        'namespace': 'AWS/EC2',
        'metric': 'DiskReadBytes',
        'stat': 'Maximum',
        'unit': 'Bytes',
        'filter_dimension': 'InstanceId',
    },
    {
        'id': 'ec2_statuscheckfailed_max',
        'namespace': 'AWS/EC2',
        'metric': 'StatusCheckFailed',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'InstanceId',
    },
    {
        'id': 'ec2_statuscheckfailed_system_max',
        'namespace': 'AWS/EC2',
        'metric': 'StatusCheckFailed_System',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'InstanceId',
    },
    {
        'id': 'ec2_statuscheckfailed_instance_max',
        'namespace': 'AWS/EC2',
        'metric': 'StatusCheckFailed_Instance',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'InstanceId',
    },
]

class AWSEC2(Plugin):

    def collect(self, _):
        try:
            aws_region = self.get('AWS_REGION')
            if not aws_region:
                raise Exception("Please set AWS_REGION")
            time_range = self.get('time_range', '10')
            instance = self.get('cloud.instance.id')

            # Get metrics for the EC2 Instance
            cloudwatch = boto3.client('cloudwatch', aws_region,
                                      aws_access_key_id=self.get('AWS_ACCESS_KEY_ID'),
                                      aws_secret_access_key=self.get('AWS_SECRET_ACCESS_KEY'))
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=int(time_range))
            response = cloudwatch.get_metric_data(
                MetricDataQueries=self.build_instance_query(instance),
                StartTime=start_time,
                EndTime=end_time,
                ScanBy='TimestampAscending')

            metric_labels = {
                'cloud.service': 'aws.ec2',
                'cloud.instance.type': self.get('cloud.instance.type'),
                'cloud.instance.region': aws_region,
                'cloud.instance.az': self.get('cloud.instance.az')
            }

            instance_tags = self.get('INSTANCE_LABELS', '').split(',')
            for tag in instance_tags:
                if self.get(tag.strip()):
                    metric_labels[tag] = self.get(tag.strip())

            # Get last value for each metric, if no values set metric to 0
            for metric in response['MetricDataResults']:
                metric_name = "aws." + metric['Id']
                if len(metric['Values']) > 0:
                    value = metric['Values'][-1]
                    ts = int(metric['Timestamps'][-1].utcnow().timestamp() * 1000)
                    if metric['Id'] == 'ec2_cpuutilization_max':
                    	self.gauge('sys.cpu.pct', metric_labels).set(value, ts=ts)
                    else:
                        self.gauge(metric_name, metric_labels).set(value, ts=ts)
                else:
                    if metric['Id'] == 'ec2_cpuutilization_max':
                    	self.gauge('sys.cpu.pct', metric_labels).set(0)
                    else:
                        self.gauge(metric_name, metric_labels).set(0)

            return Status.OK
        except Exception as err:
            raise err

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
                    'Period': 300,
                    'Stat': instance_metric['stat'],
                    'Unit': instance_metric['unit'],
                }
            }
            query.append(metric)
            id += 1

        return query


if __name__ == '__main__':
    sys.exit(AWSEC2().run())