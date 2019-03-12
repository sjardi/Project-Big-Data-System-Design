from time import sleep
from datetime import datetime
from kafka import KafkaConsumer
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from bs4.element import Comment

#from https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(soup):
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return " ".join(t.strip() for t in visible_texts)

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
            content = text_from_html(soup)

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