from time import sleep
from kafka import KafkaConsumer

if __name__ == '__main__':
    parsed_topic_name = 'pages'

    consumer = KafkaConsumer(parsed_topic_name, auto_offset_reset='earliest',
                             bootstrap_servers=['localhost:9092'], api_version=(0, 10), consumer_timeout_ms=1000)
    
    while True:
        for msg in consumer:
            print(msg.value)

    if consumer is not None:
        consumer.close()