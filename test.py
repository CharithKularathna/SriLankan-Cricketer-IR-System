from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port':9200}])

mapping = es.indices.get_mapping(index="index-players")

print (mapping)