from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearchHelper import elasticsearchHelper
import json

class elasticsearchIndexer:

    def __init__(self):
        self.es = Elasticsearch()
        self.esHelper = elasticsearchHelper()

    def createIndex(self):
        index = self.esHelper.getIndex()

        if self.es.indices.exists(index):
            self.es.indices.delete(index=index)

        config = {
            'settings': self.getSettings(),
            'mappings': self.getMappings()
        }

        print(config)
        self.es.indices.create(index=index, ignore=400, body=config)

    def getSettings(self):
        settings = {
            "settings": {
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
                            'tokenizer': 'whitespace',
                            'filter': [
                                'lowercase',
                                'unique',
                                'autocomplete_edge_ngram',
                                'word_delimiter_optimized',
                            ]
                        },
                        'search_optimization': {
                            'tokenizer': 'whitespace',
                            'filter': [
                                'lowercase',
                                'unique',
                            ]
                        },
                    }
                },
                "number_of_shards": 1
            }
        }
        return settings

    def getMappings(self):
        mappings = {
            "mappings": {
                "_doc": {
                    "properties": {
                    }
                }
            }
        }

        for item in self.esHelper.getIndex():
            mappings['mappings']['_doc']['properties'] = {
                'search_' + item : {
                    'type': 'text',
                    'analyzer': 'indexer_optimization',
                    'search_analyzer': 'search_optimization',
                }
            }
        #mappings = json.dumps(mappings)
        return mappings


es = elasticsearchIndexer()
es.createIndex()