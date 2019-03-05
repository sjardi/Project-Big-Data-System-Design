#!/usr/bin/env bash

#start ZooKeeper
kafka_2.11-2.1.0/bin/zookeeper-server-start.sh kafka_2.11-2.1.0/config/zookeeper.properties
#start broker
kafka_2.11-2.1.0/bin/kafka-server-start.sh kafka_2.11-2.1.0/config/server.properties