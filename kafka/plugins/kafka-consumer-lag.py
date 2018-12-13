#!/usr/bin/env python3

import logging
import re
import sys

from outlyer_plugin import Status, Plugin

import pykafka
from pykafka.cli import kafka_tools
from pykafka.utils.compat import iteritems

class MemberLag(object):
    def __init__(self, topic, group, member, partition, latest_offset, current_offset):
        self.topic = topic.decode('UTF-8')
        self.group = group.decode('UTF-8')
        self.member = member.decode('UTF-8')
        self.partition = str(partition)
        self.latest_offset = latest_offset
        self.current_offset = current_offset

    def lag(self):
        return self.latest_offset - self.current_offset

class KafkaConsumerLagPlugin(Plugin):
    def collect(self, _):
        try:
            # Disable verbose logging for Kafka client lib 
            logger = logging.getLogger("pykafka")
            logger.setLevel(logging.ERROR)

            host = self.get('ip', 'localhost')
            port = self.get('port', 9092)
            consumer_group_regex = re.compile(self.get('consumer_group_regex', '.*'))
            consumer_group_names = self.get('consumer_groups', '')

            server = f'{host}:{port}'
            client = pykafka.KafkaClient(hosts=server)

            consumer_groups = set(map(lambda g: g.encode('UTF-8'), filter(lambda g: len(g) > 0, consumer_group_names.split(','))))

            brokers = client.brokers

            group_topics = {}
            member_assignment = {}
            for _, broker in iteritems(brokers):
                broker_groups = broker.list_groups().groups.keys()
                if consumer_groups:
                    groups = list(filter(lambda g: g in consumer_groups, broker_groups))
                else:
                    groups = list(filter(lambda g: consumer_group_regex.match(g.decode('UTF-8')), broker_groups))

                groups_metadata = broker.describe_groups(group_ids=groups).groups
                for group_id, describe_group_response in iteritems(groups_metadata):
                    members = describe_group_response.members
                    topics = set([])
                    for member_id, member in iteritems(members):
                        for topic, assignments in member.member_assignment.partition_assignment:
                            topics.add(topic)
                            for assignment in assignments:
                                member_assignment[(topic, group_id, assignment)] = member_id
                    group_topics[group_id] = topics

            lags = []
            for group_id, topics in iteritems(group_topics):
                for topic_name in topics:
                    topic = client.topics[topic_name]
                    lag = kafka_tools.fetch_consumer_lag(client, topic, group_id)
                    for partition, offsets in iteritems(lag):
                        member = member_assignment[(topic_name, group_id, partition)]
                        lags.append(MemberLag(topic_name, group_id, member, partition, offsets[0], offsets[1]))

            for lag in lags:
                labels = {
                    'topic': lag.topic,
                    'consumer_group': lag.group,
                    'consumer_client_id': lag.member,
                    'topic_partition': lag.partition
                }
                self.gauge('kafka_consumer_lag', labels).set(lag.lag())

            return Status.OK
        except Exception:
            self.logger.error('Unable to scrape metrics from Kafka')
            return Status.CRITICAL


if __name__ == '__main__':
    sys.exit(KafkaConsumerLagPlugin().run())
