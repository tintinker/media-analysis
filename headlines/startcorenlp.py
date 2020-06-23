 
from stanza.server import CoreNLPClient

CORE_NLP_FOLDER = "/home/ubuntu/stanford-corenlp/*"
ANNOTATORS = ['tokenize','ssplit','openie','depparse']

#will need to raise this if you implement more annotators (i.e. sentiment) 
#the EC2 instance is set up with 4G memory, but you can prob get away with 2 if you keep just these annotators
MEMORY = '2G' 
TIMEOUT = 15000 #milliseconds

with CoreNLPClient(annotators=ANNOTATORS, timeout=TIMEOUT, memory=MEMORY,classpath=CORE_NLP_FOLDER) as client:
    #just to keep server running
    #TODO: replace with Keyboard Interrupt or a more standard solution
    input("Press enter to stop server")