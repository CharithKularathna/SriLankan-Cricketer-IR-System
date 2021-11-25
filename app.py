from elasticsearch import Elasticsearch
from flask import Flask
from flask import flash, render_template, request, redirect, jsonify
from search import searchQuery

es = Elasticsearch([{'host': 'localhost', 'port':9200}])
app = Flask(__name__)


gSearch = "kkkkk"

@app.route('/', methods=['GET', 'POST'])
def index():
    global gSearch
    
    if request.method == 'POST':
        if 'form' in request.form:
            if request.form['query']:
                search = request.form['query']
                gSearch = search
            else :
                search = gSearch
            names = searchQuery(search)
            nameSet = set()
            newNames = []
            for obj in names:
                if obj['name'] not in nameSet:
                    newNames.append(obj)
                    nameSet.add(obj['name'])
            

        return render_template('index.html',  names = newNames)
    return render_template('index.html',  names = '')

if __name__ == "__main__":
    app.run(debug=True)
