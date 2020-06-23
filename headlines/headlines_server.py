from flask import Flask, request
from flask_cors import CORS, cross_origin
from pycorenlp import StanfordCoreNLP
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("analyze/headline")
@cross_origin()
def extension_headline():
    headline = request.args.get('q')
    nlp = StanfordCoreNLP('http://localhost:9000')
    output = nlp.annotate(headline, properties={
        'annotators': 'tokenize,openie,depparse',
        'outputFormat': 'json'
    })
    return output

@app.route("analyze/headline/simple")
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

