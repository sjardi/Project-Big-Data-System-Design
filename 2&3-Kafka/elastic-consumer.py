from time import sleep
from datetime import datetime
from kafka import KafkaConsumer
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch

if __name__ == '__main__':
    parsed_topic_name = 'pages'
    
    es = Elasticsearch()

    consumer = KafkaConsumer(parsed_topic_name, auto_offset_reset='earliest',
                             bootstrap_servers=['localhost:9092'], api_version=(0, 10), consumer_timeout_ms=1000)
    
    while True:
        for msg in consumer:
            raw_data = msg.value.decode("utf-8") 
            firstLine = raw_data.index("\n")
            secondLine = raw_data.index("\n", firstLine+1)

            url = raw_data[:firstLine]
            party = raw_data[firstLine+1:secondLine]
            raw_html = raw_data[secondLine+1:]
            soup = BeautifulSoup(raw_html, 'html.parser')
            title = soup.head.title.string
            content = "\n".join(soup.stripped_strings)

            print(url)
            print(party)
            print(title)
            print("\n---Content---\n")
            print(content)
            print("\n\n")

            doc = {
                'title': title,
                'party': party,
                'url': url,
                'content': content,
                'timestamp': datetime.now(),
                'keyword': "test",
            }

            res = es.index(index="scraped-content", doc_type='page', body=doc)
            es.indices.refresh(index="scraped-content")

    if consumer is not None:
        consumer.close()