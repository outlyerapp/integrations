#!/usr/bin/env python3

import boto3
import sys
import os
import json

class EC2Discovery(object):

    def discover(self):
        try:
            instances = []

            aws_region = os.environ.get('AWS_REGION')
            if not aws_region:
                raise Exception("Please ensure AWS_REGION is set.")
            accound_id = self._get_aws_account_id()
            awsclient = boto3.client('ec2',
                                     region_name=aws_region,
                                     aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

            paginator = awsclient.get_paginator('describe_instances')
            for response in paginator.paginate():
                for reservation in response['Reservations']:
                    for instance in reservation['Instances']:

                        if instance['State']['Name'] == 'running':
                            host = {
                                'hostname': instance['PrivateDnsName'],
                                'ip': instance['PrivateIpAddress'],
                            }
                            labels = {
                                'instance.type': 'host',
                                'cloud.provider': 'aws',
                                'cloud.service': 'aws.ec2',
                                'cloud.account_id': accound_id,
                                'cloud.instance.region': aws_region,
                                'cloud.instance.az': instance['Placement']['AvailabilityZone'],
                                'cloud.instance.id': instance['InstanceId'],
                                'cloud.instance.type': instance['InstanceType'],
                                'cloud.instance.image_id': instance['ImageId']
                            }

                            if 'Tags' in instance:
                                for tag in instance['Tags']:
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
            return 3

    def _get_aws_account_id(self) -> str:
        """
        Gets the AWS Account ID for the current API key user

        :return:    The AWS Account ID for the current API key user
        """
        return boto3.client('sts',
                     aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
                     aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')).get_caller_identity().get('Account')

if __name__ == '__main__':
    sys.exit(EC2Discovery().discover())