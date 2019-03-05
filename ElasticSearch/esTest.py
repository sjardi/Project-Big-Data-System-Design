from initElasticsearch import elasticsearchIndexer

es = elasticsearchIndexer();

es.index('https://google.com', 'testtesttest')

es.search()

es.getAllDocuments()