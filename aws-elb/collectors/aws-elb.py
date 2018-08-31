#!/usr/bin/env python3

import boto3
import sys
from datetime import datetime, timedelta

from outlyer_plugin import Plugin, Status

INSTANCE_METRICS = [
    {
        'id': 'elb_latency_max',
        'namespace': 'AWS/ELB',
        'metric': 'Latency',
        'stat': 'Maximum',
        'unit': 'Seconds',
        'filter_dimension': 'LoadBalancerName',
    },
    {
        'id': 'elb_backendconnectionerrors_max',
        'namespace': 'AWS/ELB',
        'metric': 'BackendConnectionErrors',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'LoadBalancerName',
    },
    {
        'id': 'elb_estimatedprocessedbytes_max',
        'namespace': 'AWS/ELB',
        'metric': 'EstimatedProcessedBytes',
        'stat': 'Maximum',
        'unit': 'Bytes',
        'filter_dimension': 'LoadBalancerName',
    },
    {
        'id': 'elb_requestcount_max',
        'namespace': 'AWS/ELB',
        'metric': 'RequestCount',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'LoadBalancerName',
    },
    {
        'id': 'elb_surgequeuelength_max',
        'namespace': 'AWS/ELB',
        'metric': 'SurgeQueueLength',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'LoadBalancerName',
    },
    {
        'id': 'elb_healthyhostcount_max',
        'namespace': 'AWS/ELB',
        'metric': 'HealthyHostCount',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'LoadBalancerName',
    },
    {
        'id': 'elb_unhealthyhostcount_max',
        'namespace': 'AWS/ELB',
        'metric': 'UnHealthyHostCount',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'LoadBalancerName',
    },
    {
        'id': 'elb_estimatedalbactiveconnectioncount_max',
        'namespace': 'AWS/ELB',
        'metric': 'EstimatedALBActiveConnectionCount',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'LoadBalancerName',
    },
    {
        'id': 'elb_estimatedalbnewconnectioncount_max',
        'namespace': 'AWS/ELB',
        'metric': 'EstimatedALBNewConnectionCount',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'LoadBalancerName',
    },
    {
        'id': 'elb_estimatedalbconsumedlcus_max',
        'namespace': 'AWS/ELB',
        'metric': 'EstimatedALBConsumedLCUs',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'LoadBalancerName',
    },
    {
        'id': 'elb_elb2xx_max',
        'namespace': 'AWS/ELB',
        'metric': 'HTTPCode_ELB_2XX',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'LoadBalancerName',
    },
    {
        'id': 'elb_http2xx_max',
        'namespace': 'AWS/ELB',
        'metric': 'HTTPCode_Backend_2XX',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'LoadBalancerName',
    },
    {
        'id': 'elb_elb4xx_max',
        'namespace': 'AWS/ELB',
        'metric': 'HTTPCode_ELB_4XX',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'LoadBalancerName',
    },
    {
        'id': 'elb_http4xx_max',
        'namespace': 'AWS/ELB',
        'metric': 'HTTPCode_Backend_4XX',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'LoadBalancerName',
    },
    {
        'id': 'elb_elb5xx_max',
        'namespace': 'AWS/ELB',
        'metric': 'HTTPCode_ELB_5XX',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'LoadBalancerName',
    },
    {
        'id': 'elb_http5xx_max',
        'namespace': 'AWS/ELB',
        'metric': 'HTTPCode_Backend_5XX',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'LoadBalancerName',
    },
    {
        'id': 'elb_spillovercount_max',
        'namespace': 'AWS/ELB',
        'metric': 'SpilloverCount',
        'stat': 'Maximum',
        'unit': 'Count',
        'filter_dimension': 'LoadBalancerName',
    },
]

class AWSELB(Plugin):

    def collect(self, _):
        try:
            aws_region = self.get('cloud.instance.region')
            if not aws_region:
                raise Exception("Please set AWS_REGION")
            time_range = self.get('time_range', '10')
            instance = self.get('cloud.instance.id')

            # Get metrics for the ELB Instance
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
                'region': aws_region
            }

            # Get last value for each metric, if no values set metric to 0
            for metric in response['MetricDataResults']:
                metric_name = "aws." + metric['Id']
                if len(metric['Values']) > 0:
                    value = metric['Values'][-1]
                    ts = int(metric['Timestamps'][-1].utcnow().timestamp() * 1000)
                    self.gauge(metric_name, metric_labels).set(value, ts=ts)
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
                    'Period': 60,
                    'Stat': instance_metric['stat'],
                    'Unit': instance_metric['unit'],
                }
            }
            query.append(metric)
            id += 1

        return query


if __name__ == '__main__':
    sys.exit(AWSELB().run())