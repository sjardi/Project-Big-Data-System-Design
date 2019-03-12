import glob
import errno
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))

path = '../1-Spider/Html_Output/*.html.txt'
files = glob.glob(path)
for name in files:
    try:
        with open(name) as f:
            topic_name = "pages"
            key = name
            value = f.read()
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(value, encoding='utf-8')
            producer.send(topic_name, key=key_bytes, value=value_bytes)
            producer.flush()
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise

if producer is not None:
    producer.close()