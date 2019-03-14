from elasticsearch import Elasticsearch
from elasticsearchHelper import elasticsearchHelper
import json

class elasticsearchSearch:

    def __init__(self):
        self.es = Elasticsearch()
        self.esHelper = elasticsearchHelper()
        self.index = self.esHelper.getIndex()

    def search(self, term):
        config = self.searchConfig()

        body = {
            '_source': {
                'excludes': config['searchFields']
            },
            'query': {
                'bool': {
                    'must': {
                        'multi_match': {
                            'query': term,
                            'fields': config['searchFields'],
                            'type': 'most_fields'
                        }

                    }
                }
            }
        }

        return self.es.search(index = self.esHelper.getIndex(), body = body)


    def searchConfig(self):
        searchFields = []
        fields = []

        for field in self.esHelper.getFields():
            searchFields.append('search_' + field)
            fields.append(field)

        config = {
            'searchFields': searchFields,
            'fields': fields
        }
        return config