 
from stanza.server import CoreNLPClient

CORE_NLP_FOLDER = "/Users/justin/Documents/codingprojects/stanford-corenlp-4.0.0/*"
annotators = ['tokenize','ssplit','openie','depparse']
with CoreNLPClient(annotators=annotators, timeout=30000, memory='2G',classpath=CORE_NLP_FOLDER) as client:
    input("Press enter to stop server")