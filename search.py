from elasticsearch import Elasticsearch
import json
#from googletrans import Translator
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

es = Elasticsearch([{'host': 'localhost', 'port':9200}])

'''
def englishTranslator(value):
	translator = Translator()
	englishQuery = translator.translate(value, dest='en')
	return englishQuery.text
'''

def getAllResults(results):
    nameList = []
    for i in range(len(results['hits']['hits'])):
        nameList.append(results['hits']['hits'][i]['_source'])
        #print("")
    #aggregations = results['aggregations']
    names = nameList
    #bio = aggregations['bio_']['buckets']
    #years = aggregations['years_']['buckets']
    
    #print ("TEST")
    #print (names)
    return names

# "fields" : ["name", "bio", "years","matches","runs_scored", "highest_score", "bat_avg","wickets","runs_conceded", "best_figures","ball_avg", "catches_taken"],
def searchText(term):
    #print (term)
    try:
        results = es.search(index='index-players2',doc_type = 'players', body={
            "size" : 500,
            "query" :{
                "multi_match": {
                    "query" : term,
                    "type" : "best_fields",
                    "fields" : ["name", "bio", "years"],
                }
            },
            

        })
        
    except:
        token = term.split()[-1]
        results = es.search(index='index-players2',doc_type = 'players', body={
            "size" : 500,
            "query" :{
                "bool": {
                    "must" : {
                        "term" : { "bio" : token }
                    },
                }
            },
        })
        
    name = getAllResults(results)
    return name


def topRanker(term):
    query = []
    size = 100
    with open('players_meta.json') as f:
        meta_data = json.loads(f.read())

    players = meta_data["name"]
    bio = meta_data["bio"]
    years = meta_data["years"]

    playerDocs = [term]
    playerDocs.extend(players)
    bioDocs = [term]
    bioDocs.extend(bio)
    yearsDocs = [term]
    yearsDocs.extend(years)
    
    typeSelect = False
    
    allTerms = term.split()
    print(allTerms)
    for i in allTerms:
        if i.isnumeric():
            size = int(i)

    tfidfVectorizor = TfidfVectorizer(analyzer="char", token_pattern=u'(?u)\\b\w+\\b')
    matrixTfIdf = tfidfVectorizor.fit_transform(playerDocs)

    cs = cosine_similarity(matrixTfIdf[0:1],matrixTfIdf)

    similarity_list = cs[0][1:]
    
    if typeSelect != True :
        query.append({"match_all" : {}})

    print(query)
    results = es.search(index='index-players',doc_type = 'players',body={
        "size" : size,
        "query" :{
            "bool": {
                "must": query
            }
        },
        "sort" :{
            "views": {"order": "desc"}
        },
        "aggs": {
            "name_": {
                "terms": {
                    "field": "name.keyword",
                    "size" : 15    
                }        
            },
            "bio_": {
                "terms": {
                    "field":"bio.keyword",
                    "size" : 15
                }             
            },
            "years_": {
                "terms": {
                    "field":"years.keyword",
                    "size" : 15
                }             
            },
           

        }
    })
    names = getAllResults(results)
    return names

def searchQuery(query):
    name = searchText(query)
    return name







    
