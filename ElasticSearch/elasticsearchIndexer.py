from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearchHelper import elasticsearchHelper
from elasticsearchSearch import elasticsearchSearch
import json

class elasticsearchIndexer:

    def __init__(self):
        self.es = Elasticsearch()
        self.esHelper = elasticsearchHelper()
        self.index = self.esHelper.getIndex()

    def createIndex(self):

        if self.es.indices.exists(self.index):
            self.es.indices.delete(index=self.index)

        settings = self.getSettings()
        mappings = self.getMappings()

        print(self.es.indices.create(index=self.index, ignore=400))
        print(self.es.indices.close(index=self.index, ignore=400))
        print(self.es.indices.put_settings(index=self.index, body=settings))
        print(self.es.indices.put_mapping(index=self.index, body=mappings, doc_type='_doc'))
        print(self.es.indices.open(index=self.index, ignore=400))

    def indexDoc(self, content):
        doc = {}
        for field in self.esHelper.getFields():
            doc[field] = content[field]
            doc['search_' + field] = content[field]

        self.es.index(index = self.index, doc_type = '_doc', body = doc)

    def getSettings(self):
        settings = {
            'settings': {
                'analysis': {
                    'filter': {
                        'autocomplete_edge_ngram': {
                            'type': 'edge_ngram',
                            'min_gram': 2,
                            'max_gram': 20,
                        },
                        'word_delimiter_optimized': {
                            'type': 'word_delimiter',
                            'preserve_original': True,
                        }
                    },
                    'analyzer': {
                        'indexer_optimization': {
                            'type': 'custom',
                            'tokenizer': 'whitespace',
                            'filter': [
                                'lowercase',
                                'unique',
                                'autocomplete_edge_ngram',
                                'word_delimiter_optimized',
                            ]
                        },
                        'search_optimization': {
                            'type': 'custom',
                            'tokenizer': 'whitespace',
                            'filter': [
                                'lowercase',
                                'unique',
                            ]
                        },
                    }
                },
            }
        }
        return settings

    def getMappings(self):
        mappings = {
            "_doc": {
                "properties": {
                }
            }
        }

        for field in self.esHelper.getFields():
            mappings['_doc']['properties']['search_' + field] = {
                    'type': 'text',
                    'analyzer': 'indexer_optimization',
                    'search_analyzer': 'search_optimization',
                }
        return mappings