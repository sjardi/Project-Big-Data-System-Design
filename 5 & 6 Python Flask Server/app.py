from flask import Flask, send_from_directory
from elasticsearch import Elasticsearch
import json

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/search/<keyword>')
def search(keyword):
    return getAllDocuments()

def getAllDocuments():
    es = Elasticsearch()
    res = es.search(index="scraped-content", body={"query": {"match_all": {}}})
    return json.dumps(res)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')