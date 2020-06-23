#!/bin/sh

echo "Starting Headlines Server in the background"
cd ~/headlines && authbind --deep python3 headlines_server.py &

echo "Starting Core NLP server in the background"
cd ~/stanford-corenlp && java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators depparse,openie -port 9000 -timeout 15000 &


echo "To stop, run netstat -tulpn to find the PIDs and run kill -9 [PID]"

