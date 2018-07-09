import boto3

AWS_REGION = 'us-west-2'
STREAM_NAME = 'kinesis-aws-worker'

client = boto3.client('kinesis', AWS_REGION)

# Put 200 records on stream
i = 0
while i < 200:
    client.put_record(StreamName=STREAM_NAME,
                      Data="{'test': 'record'}",
                      PartitionKey='test')

    print(f"Added record-{i}")
    i += 1

# Read 200 records off stream
response = client.describe_stream(StreamName=STREAM_NAME)
shard_id = response['StreamDescription']['Shards'][1]['ShardId']
shard_iterator = client.get_shard_iterator(StreamName=STREAM_NAME,
                                           ShardId=shard_id,
                                           ShardIteratorType='TRIM_HORIZON')
shard_iterator = shard_iterator['ShardIterator']
record_response = client.get_records(ShardIterator=shard_iterator,
                                     Limit=10)
print(record_response['Records'])

while 'NextShardIterator' in record_response:
    record_response = client.get_records(ShardIterator=record_response['NextShardIterator'],
                                         Limit=10)
    print(record_response['Records'])


