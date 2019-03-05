#!/usr/bin/env bash

#all servers are started in the background with &
#to make it possible to open multiple servers

#start ZooKeeper
echo "Starting ZooKeeper..."
kafka_2.11-2.1.0/bin/zookeeper-server-start.sh kafka_2.11-2.1.0/config/zookeeper.properties &
#start broker
echo "Starting Kafka Broker..."
kafka_2.11-2.1.0/bin/kafka-server-start.sh kafka_2.11-2.1.0/config/server.properties