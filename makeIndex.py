from elasticsearch import Elasticsearch, helpers
import json

es = Elasticsearch([{'host': 'localhost', 'port':9200}])


def data_upload(dataArray):
    print (dataArray)
    helpers.bulk(es, data, index='index-players', doc_type='players')


data = []
for i in range(1,203):
    file = "data/sin/" + str(i) + "-e.json"
    with open(file) as f:
        data.append(json.loads(f.read()))

json_object = json.dumps(data)
file_name = "players.json"

with open(file_name, "w") as outfile:
    outfile.write(json_object)

data_upload(data)

