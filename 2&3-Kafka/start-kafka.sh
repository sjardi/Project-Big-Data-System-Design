#!/usr/bin/env bash

#all servers are started in the background with &
#to make it possible to open multiple servers

read -p "Remove /tmp/kafka-logs/ (useful if you get errors)? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    rm -r /tmp/kafka-logs
fi

#start ZooKeeper
echo "Starting ZooKeeper..."
kafka_2.11-2.1.0/bin/zookeeper-server-start.sh kafka_2.11-2.1.0/config/zookeeper.properties &
#start broker
echo "Starting Kafka Broker..."
kafka_2.11-2.1.0/bin/kafka-server-start.sh kafka_2.11-2.1.0/config/server.properties &
#creating topic
echo "Creating Kafka Topic..."
kafka_2.11-2.1.0/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic pages &

sleep 30

#starting consumer
echo "Starting Kafka Consumer"
python3 elastic-consumer.py &

#starting producer
echo "Starting Kafka Producer"
tail -n +1 -- ../1-Spider/output/* | kafka_2.11-2.1.0/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic pages &