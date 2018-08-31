#!/usr/bin/env python3

import boto3
import sys
import os
import json
import socket

socket.setdefaulttimeout = 1

class ELBDiscovery(object):

    def discover(self):
        try:
            instances = []

            aws_region = os.environ.get('AWS_REGION')
            if not aws_region:
                raise Exception("Please ensure AWS_REGION is set.")
            accound_id = self._get_aws_account_id()
            awsclient = boto3.client('elb',
                                     region_name=aws_region,
                                     aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

            paginator = awsclient.get_paginator('describe_load_balancers')
            for response in paginator.paginate():
                for instance in response['LoadBalancerDescriptions']:

                    host = {
                        'hostname': instance['DNSName'],
                        'ip': self.ip_from_hostname(instance['DNSName']),
                    }
                    labels = {
                        'instance.alias': instance['LoadBalancerName'],
                        'instance.type': 'device',
                        'cloud.provider': 'aws',
                        'cloud.service': 'aws.elb',
                        'cloud.account_id': accound_id,
                        'cloud.instance.region': aws_region,
                        'cloud.instance.id': instance['LoadBalancerName'],
                        'elb.scheme': instance['Scheme'],
                        'elb.connected_instances': str(len(instance['Instances']))
                    }

                    # Get tags for ELB instance
                    tags = awsclient.describe_tags(LoadBalancerNames=[instance['LoadBalancerName']])['TagDescriptions'][0]['Tags']
                    for tag in tags:
                        key = tag['Key']
                        value = tag['Value']
                        labels[key] = value

                    host['labels'] = labels
                    instances.append(host)

            # Output instance in JSON to Stdout
            print(json.dumps({"instances": instances, "version": "0.1.0"}))
            return 0

        except Exception as err:
            raise err

    def _get_aws_account_id(self) -> str:
        """
        Gets the AWS Account ID for the current API key user

        :return:    The AWS Account ID for the current API key user
        """
        return boto3.client('sts',
                     aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
                     aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')).get_caller_identity().get('Account')

    def ip_from_hostname(self, name):
        try:
            return socket.gethostbyname(name)
        except:
            return name

if __name__ == '__main__':
    sys.exit(ELBDiscovery().discover())