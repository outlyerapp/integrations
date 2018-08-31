#!/usr/bin/env python3

import boto3
import sys
import os
import json

class RDSDiscovery(object):

    def discover(self):
        try:
            instances = []

            aws_region = os.environ.get('AWS_REGION')
            if not aws_region:
                raise Exception("Please ensure AWS_REGION is set.")
            account_id = self._get_aws_account_id()
            awsclient = boto3.client('rds',
                                     region_name=aws_region,
                                     aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

            paginator = awsclient.get_paginator('describe_db_instances')
            for response in paginator.paginate():
                for instance in response['DBInstances']:

                    if instance['DBInstanceStatus'] == 'available':

                        host = {
                            'hostname': instance['Endpoint']['Address'],
                            'ip': instance['Endpoint']['Address'],
                        }
                        labels = {
                            'instance.type': 'host',
                            'cloud.provider': 'aws',
                            'cloud.service': 'aws.rds',
                            'cloud.account_id': account_id,
                            'cloud.instance.region': aws_region,
                            'cloud.instance.az': instance['AvailabilityZone'],
                            'cloud.instance.id': instance['DBInstanceIdentifier'],
                            'cloud.instance.type': instance['DBInstanceClass'],
                            'cloud.instance.image_id': instance['Engine'] + "-" + instance['EngineVersion'],
                            # Get RDS Specific metadata
                            'rds.auto-minor-version-upgrade': str(instance['AutoMinorVersionUpgrade']),
                            'rds.backup-retention-period': str(instance['BackupRetentionPeriod']),
                            'rds.engine': instance['Engine'],
                            'rds.engine-version': instance['EngineVersion'],
                            'rds.license-model': instance['LicenseModel'],
                            'rds.multi-az': str(instance['MultiAZ']),
                            'rds.publicly-accessible': str(instance['PubliclyAccessible']),
                            'rds.storage-encrypted': str(instance['StorageEncrypted']),
                            'rds.storage-type': instance['StorageType']
                        }

                        # Get tags for RDS instance
                        tags = awsclient.list_tags_for_resource(ResourceName=instance['DBInstanceArn'])['TagList']
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

if __name__ == '__main__':
    sys.exit(RDSDiscovery().discover())