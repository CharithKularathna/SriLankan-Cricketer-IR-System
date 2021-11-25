from elasticsearch import Elasticsearch, helpers
import json

es = Elasticsearch([{'host': 'localhost', 'port':9200}])

def data_upload():
    with open('players.json') as f:
        data = json.loads(f.read())
    print (data)
    helpers.bulk(es, data, index='index-players2', doc_type='players')


if __name__ == "__main__":
    data_upload()