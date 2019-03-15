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
                'excludes': config['excludeFields']
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
            },
            'explain': 'true'
        }

        return self.es.search(index = self.esHelper.getIndex(), body = body)


    def searchConfig(self):
        excludeFields = []
        fields = []

        for field in self.esHelper.getFields():
            excludeFields.append('search_' + field)
            if field == 'title' or field == 'party':
                fields.append('search_' + field + '^5')
            elif field == 'url':
                fields.append('search_' + field + '^2')
            else:
                fields.append('search_' + field + '^1')


        config = {
            'excludeFields': excludeFields,
            'searchFields': fields
        }
        return config