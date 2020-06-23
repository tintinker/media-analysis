from flask import Flask, request
from app.HeadlineAnalyzer import HeadlineAnalyzer
from app.NewsParser import NewsParser
import pandas as pd
from flask_cors import CORS, cross_origin
from pycorenlp import StanfordCoreNLP
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

analyzer = HeadlineAnalyzer()
parser = NewsParser()

@app.route("/extension/headline")
@cross_origin()
def extension_headline():
    headline = request.args.get('q')
    nlp = StanfordCoreNLP('http://localhost:9000')
    output = nlp.annotate(headline, properties={
        'annotators': 'tokenize,openie,depparse',
        'outputFormat': 'json'
    })
    return output

@app.route("/extension/headline/simple")
@cross_origin()
def extension_headline_simple():
    headline = request.args.get('q')
    nlp = StanfordCoreNLP('http://localhost:9000')
    output = nlp.annotate(headline, properties={
        'annotators': 'tokenize,openie,depparse',
        'outputFormat': 'json'
    })

    result = {"voice": [], "relationships": []}

    for dep in output["sentences"][0]["basicDependencies"]:
        if dep["dep"] == "nsubj":
            result["voice"].append("Active Voice: "+dep["dependentGloss"]+" -> "+dep["governorGloss"])
        if dep["dep"] == "nsubj:pass":
            result["voice"].append("Passive Voice: "+dep["dependentGloss"]+" -> "+dep["governorGloss"])

    for openie in output["sentences"][0]["openie"]:
        result["relationships"].append(f"Object: "+openie["object"]+", Relation: "+openie["relation"]+", Subject: "+openie["subject"])
    
    return json.dumps(result)

@app.route('/analyze/headline')
@cross_origin()
def analyze_headline():
    headline = request.args.get('q')
    if not headline:
        return "format: ?q=HEADLINE+TEXT+GOES+HERE"
    return json.dumps(analyzer.process_one_headline(headline))

@app.route('/headlines')
@cross_origin()
def headlines():
    search_term = request.args.get('q')
    if not search_term:
        return "format: ?q=SEARCH+TERM"
    return json.dumps(parser.get_headlines(search_term))

@app.route('/analyze/search')
@cross_origin()
def analyze_search():
    search_term = request.args.get('q')
    if not search_term:
        return "format: ?q=SEARCH+TERM"
    
    headlines = parser.get_headlines(search_term)
    data = analyzer.process_multiple_headlines(headlines)

    df = pd.DataFrame(data)

    report = {'stats': df.describe().to_dict(), 'data': data}

    return json.dumps(report)
