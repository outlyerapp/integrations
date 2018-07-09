import boto3

AWS_REGION = 'us-west-2'
QUEUE_URL = 'https://sqs.us-west-2.amazonaws.com/386261637651/aws-worker-queue1'

client = boto3.client('sqs', AWS_REGION)

# Put 100 records on queue
i = 0
while i < 100:
    response = client.send_message(
        QueueUrl=QUEUE_URL,
        DelaySeconds=10,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'The Whistler'
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'John Grisham'
            },
            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': '6'
            }
        },
        MessageBody=(
            'Information about current NY Times fiction bestseller for '
            'week of 12/11/2016.'
        )
    )
    print(f"{i}. Put message {response['MessageId']}")
    i += 1

# Read 100 records off queue
i = 0
while i < 100:
    response = client.receive_message(
        QueueUrl=QUEUE_URL,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    # Delete received message from queue
    client.delete_message(
        QueueUrl=QUEUE_URL,
        ReceiptHandle=receipt_handle
    )
    print(f"{i}. Read and deleted message {message['MessageId']}")
    i += 1