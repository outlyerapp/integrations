import boto3
import json

TOPIC_ARN = 'arn:aws:sns:us-west-2:386261637651:topic-aws-worker'
AWS_REGION = 'us-west-2'

message = {"foo": "bar"}
client = boto3.client('sns', AWS_REGION)

i = 0
while i < 100:
    response = client.publish(
        TopicArn=TOPIC_ARN,
        Message=json.dumps({'default': json.dumps(message),
                            'sms': 'here a short version of the message',
                            'email': 'here a longer version of the message'}),
        Subject='a short subject for your message',
        MessageStructure='json'
    )
    print(f"{i}. {response['MessageId']}")
    i += 1
