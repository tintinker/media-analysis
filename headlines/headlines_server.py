from flask import Flask, request
from flask_cors import CORS, cross_origin
from pycorenlp import StanfordCoreNLP
import json

#init flask
app = Flask(__name__)

#enable cross origin
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def annotate(headline):
    
    #requires CoreNLP to already be running on port 9000
    #this should be started by setup.sh but may take a while to warm up
    #TODO: add error checking here (return status 500 if nlp not running)
    nlp = StanfordCoreNLP('http://localhost:9000')
    
    return = nlp.annotate(headline, properties={
        #these annoators must be a subset of the ones used when starting the core nlp server in setup.sh
        #TODO: move this list of annoators to a config file to ensure the same ones are used here and in setup.sh
        'annotators': 'tokenize,openie,depparse',
        'outputFormat': 'json'
    })


@app.route("/")
@cross_origin()
def welcome():
    return "Welcome! The server is live! \n Usage: \n /analyze/headline/simple?q=barack+obama+is+from+hawaii \n note that the first request after the ec2 instance is started will be slow"
#returns full result of openie, token, and depparse nlp annotation
#request syntax fetch("localhost:5000/analyze/headline?q=barack+obama+is+from+hawaii")
@app.route("/analyze/headline")
@cross_origin()
def extension_headline():
    headline = request.args.get('q')
    return annotate(headline)
    

#repackages openie and depparse annotations into simplified json object
#request syntax fetch("localhost:5000/analyze/headline/simple?q=barack+obama+is+from+hawaii")
@app.route("/analyze/headline/simple")
@cross_origin()
def extension_headline_simple():
    headline = request.args.get('q')
    output = annotate(headline)

    #reformat nlp output
    result = {"voice": [], "relationships": []}

    #assumes headlines are only one sentence (fragments). This should generally be true
    #TODO: (optional) analyze subsequent sentences or add error status for requests with more than one sentence
    for dep in output["sentences"][0]["basicDependencies"]:
        if dep["dep"] == "nsubj":
            result["voice"].append("Active Voice: "+dep["dependentGloss"]+" -> "+dep["governorGloss"])
        if dep["dep"] == "nsubj:pass":
            result["voice"].append("Passive Voice: "+dep["dependentGloss"]+" -> "+dep["governorGloss"])

    for openie in output["sentences"][0]["openie"]:
        result["relationships"].append(f"Object: "+openie["object"]+", Relation: "+openie["relation"]+", Subject: "+openie["subject"])
    
    return json.dumps(result)

