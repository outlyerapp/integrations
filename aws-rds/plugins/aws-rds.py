#!/usr/bin/env python3

import boto3
import sys
from datetime import datetime, timedelta

from outlyer_plugin import Plugin, Status

INSTANCE_METRICS = [
    {
        'id': 'rds_burstbalance_max',
        'namespace': 'AWS/RDS',
        'metric': 'BurstBalance',
        'stat': 'Maximum',
        'unit': 'Percent',
        'filter_dimension': 'DBInstanceIdentifier',
    },
    {
        'id': 'rds_swapusage_max',
        'namespace': 'AWS/RDS',
        'metric': 'SwapUsage',
        'stat': 'Maximum',
        'unit': 'Bytes',
        'filter_dimension': 'DBInstanceIdentifier',
    },
    {
        'id': 'rds_freestoragespace_max',
        'namespace': 'AWS/RDS',
        'metric': 'FreeStorageSpace',
        'stat': 'Maximum',
        'unit': 'Bytes',
        'filter_dimension': 'DBInstanceIdentifier',
    },
    {
        'id': 'rds_freeablememory_max',
        'namespace': 'AWS/RDS',
        'metric': 'FreeableMemory',
        'stat': 'Maximum',
        'unit': 'Bytes',
        'filter_dimension': 'DBInstanceIdentifier',
    },
    {
        'id': 'rds_cpuutalization_max',
        'namespace': 'AWS/RDS',
        'metric': 'CPUUtilization',
        'stat': 'Maximum',
        'unit': 'Percent',
        'filter_dimension': 'DBInstanceIdentifier',
    },
    {
        'id': 'rds_networktransmitthroughput_max',
        'namespace': 'AWS/RDS',
        'metric': 'NetworkTransmitThroughput',
        'stat': 'Maximum',
        'unit': 'Bytes/Second',
        'filter_dimension': 'DBInstanceIdentifier',
    },
    {
        'id': 'rds_networkreceivethroughput_max',
        'namespace': 'AWS/RDS',
        'metric': 'NetworkReceiveThroughput',
        'stat': 'Maximum',
        'unit': 'Bytes/Second',
        'filter_dimension': 'DBInstanceIdentifier',
    },
    {
        'id': 'rds_writeops_max',
        'namespace': 'AWS/RDS',
        'metric': 'WriteIOPS',
        'stat': 'Maximum',
        'unit': 'Count/Second',
        'filter_dimension': 'DBInstanceIdentifier',
    },
    {
        'id': 'rds_writelatency_max',
        'namespace': 'AWS/RDS',
        'metric': 'WriteLatency',
        'stat': 'Maximum',
        'unit': 'Seconds',
        'filter_dimension': 'DBInstanceIdentifier',
    },
    {
        'id': 'rds_writethroughput_max',
        'namespace': 'AWS/RDS',
        'metric': 'WriteThroughput',
        'stat': 'Maximum',
        'unit': 'Bytes/Second',
        'filter_dimension': 'DBInstanceIdentifier',
    },
    {
        'id': 'rds_readiops_max',
        'namespace': 'AWS/RDS',
        'metric': 'ReadIOPS',
        'stat': 'Maximum',
        'unit': 'Count/Second',
        'filter_dimension': 'DBInstanceIdentifier',
    },
    {
        'id': 'rds_readthroughput_max',
        'namespace': 'AWS/RDS',
        'metric': 'ReadThroughput',
        'stat': 'Maximum',
        'unit': 'Bytes/Second',
        'filter_dimension': 'DBInstanceIdentifier',
    },
    {
        'id': 'rds_readlatency_max',
        'namespace': 'AWS/RDS',
        'metric': 'ReadLatency',
        'stat': 'Maximum',
        'unit': 'Seconds',
        'filter_dimension': 'DBInstanceIdentifier',
    },
    {
        'id': 'rds_diskqueuedepth_max',
        'namespace': 'AWS/RDS',
        'metric': 'DiskQueueDepth',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'DBInstanceIdentifier',
    },
    {
        'id': 'rds_databaseconnections_max',
        'namespace': 'AWS/RDS',
        'metric': 'DatabaseConnections',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'DBInstanceIdentifier',
    },
    {
        'id': 'rds_cpucreditusage_max',
        'namespace': 'AWS/RDS',
        'metric': 'CPUCreditUsage',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'DBInstanceIdentifier',
    },
    {
        'id': 'rds_cpucreditbalance_max',
        'namespace': 'AWS/RDS',
        'metric': 'CPUCreditBalance',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'DBInstanceIdentifier',
    },
    {
        'id': 'rds_binlogdiskusage_max',
        'namespace': 'AWS/RDS',
        'metric': 'BinLogDiskUsage',
        'stat': 'Maximum',
        'unit': 'Bytes',
        'filter_dimension': 'DBInstanceIdentifier',
    },
]

class AWSRDS(Plugin):

    def collect(self, _):
        try:
            aws_region = self.get('AWS_REGION')
            if not aws_region:
                raise Exception("Please set AWS_REGION")
            time_range = self.get('time_range', '10')
            instance = self.get('cloud.instance.id')

            # Get metrics for the RDS Instance
            cloudwatch = boto3.client('cloudwatch', aws_region)
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=int(time_range))
            response = cloudwatch.get_metric_data(
                MetricDataQueries=self.build_instance_query(instance),
                StartTime=start_time,
                EndTime=end_time,
                ScanBy='TimestampAscending')

            metric_labels = {
                'engine': self.get('rds.engine'),
                'region': aws_region
            }

            # Get last value for each metric, if no values set metric to 0
            for metric in response['MetricDataResults']:
                metric_name = "aws." + metric['Id']
                if len(metric['Values']) > 0:
                    value = metric['Values'][-1]
                    ts = int(metric['Timestamps'][-1].utcnow().timestamp() * 1000)
                    self.gauge(metric_name, metric_labels).set(value, ts=ts)
                    if metric['Id'] == 'rds_cpuutalization_max':
                    	self.gauge('sys.cpu.pct', metric_labels).set(value, ts=ts)
                else:
                    self.gauge(metric_name, metric_labels).set(0)
                    if metric['Id'] == 'rds_cpuutalization_max':
                    	self.gauge('sys.cpu.pct', metric_labels).set(value, ts=ts)

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
                    'Period': 60,
                    'Stat': instance_metric['stat'],
                    'Unit': instance_metric['unit'],
                }
            }
            query.append(metric)
            id += 1

        return query


if __name__ == '__main__':
    sys.exit(AWSRDS().run())