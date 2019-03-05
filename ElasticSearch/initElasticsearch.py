from datetime import datetime
from elasticsearch import Elasticsearch
import json

class elasticsearchIndexer:

    def __init__(self):
        self.es = Elasticsearch()

    def index(self, websiteUrl, content):
        doc = {
            'url': websiteUrl,
            'content': content,
            'timestamp': datetime.now(),
        }

        res = self.es.index(index="scraped-content", doc_type='page', body=doc)
        print(res['result'])

        # res = self.es.get(index="scraped-content", doc_type='page')
        # print(res['_source'])

        self.es.indices.refresh(index="scraped-content")

    def search(self):
        res = self.es.search(index="scraped-content", body={"query": {"match_all": {}}})
        print("Got %d Hits:" % res['hits']['total'])
        for hit in res['hits']['hits']:
            print("%(timestamp)s %(url)s: %(content)s" % hit["_source"])


    def getAllDocuments(self):
        res = self.es.search(index="scraped-content", body={"query": {"match_all": {}}})
        print(type(json.dumps(res)))
        return json.dumps(res)
