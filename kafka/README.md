# Kafka Integration

This pack requires that JMX be enabled on the Kafka server. If you have
not already enabled JMX, set the `JMX_PORT` environment variable before
starting Kafka, for example:

```
JMX_PORT=55555 \
nohup ~/kafka/bin/kafka-server-start.sh ~/kafka/config/server.properties \
> ~/kafka/kafka.log 2>&1 &
```

If you have already setup JMX for Kafka, make sure you supply the
correct port number in the configuration.
