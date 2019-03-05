from initElasticsearch import elasticsearchIndexer

es = elasticsearchIndexer();

es.index('google.com', 'testtesttest')

es.search()

es.getAllDocuments()