from elasticsearchSearch import elasticsearchSearch
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearchHelper import elasticsearchHelper
from elasticsearchIndexer import elasticsearchIndexer

import json
import time



#esIndexer = elasticsearchIndexer()
#esIndexer.createIndex()
#content = esIndexer.esHelper.getDummyDoc()
#esIndexer.indexDoc(content)

search = elasticsearchSearch()
#time.sleep(2)
print(search.search('utrecht'))