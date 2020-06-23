
from stanza.server import CoreNLPClient
import threading

CORE_NLP_FOLDER = "/Users/justin/Documents/codingprojects/stanford-corenlp-4.0.0/*"
annotators = ['tokenize','ssplit','pos','lemma','ner','depparse','sentiment']
SENTIMENT_MAP = {'Positive': 1, 'Neutral': 0, 'Negative': -1}

class HeadlineAnalyzer(object):
    def __init__(self, annotators=annotators, core_nlp_folder=CORE_NLP_FOLDER, memory='4G', timeout=30000):
        self.annotators = annotators
        self.core_nlp_folder = core_nlp_folder
        self.memory = memory
        self.timeout = timeout
        self.lock = threading.Lock()

    def highlight_text(self, original_text, mentions, nsubj_pass, aux_pass, nsubj):
        highlighted_text = original_text
        for mention in mentions:
            highlighted_text = highlighted_text.replace(mention[1], f"START_MENTION{mention[1]}END_MENTION")
        for np in nsubj_pass:
            highlighted_text = highlighted_text.replace(np[0], f"START_NSUBJ_PASS{np[0]}END_NSUBJ_PASS").replace(np[1], f"START_NSUBJ_PASS{np[1]}END_NSUBJ_PASS")
        for ap in aux_pass:
            highlighted_text = highlighted_text.replace(ap[0], f"START_AUX_PASS{ap[0]}END_AUX_PASS").replace(ap[1], f"START_AUX_PASS{ap[1]}END_AUX_PASS")
        for n in nsubj:
            highlighted_text = highlighted_text.replace(n[0], f"START_NSUBJ_ACT{n[0]}END_NSUBJ_ACT").replace(n[1], f"START_NSUBJ_ACT{n[1]}END_NSUBJ_ACT")
        print(highlighted_text)
        return highlighted_text

    def collect_data(self, annotated_headline):
        if(len(annotated_headline.sentence) > 1):
            return {'error_num': 1, 'error_text': 'more than 1 sentence'}
        
        nsubj_pass = [[annotated_headline.sentence[0].token[_edge.source - 1].value, annotated_headline.sentence[0].token[_edge.target - 1].value] for _edge in annotated_headline.sentence[0].basicDependencies.edge if _edge.dep == 'nsubj:pass']
        aux_pass = [[annotated_headline.sentence[0].token[_edge.source - 1].value, annotated_headline.sentence[0].token[_edge.target - 1].value] for _edge in annotated_headline.sentence[0].basicDependencies.edge if _edge.dep == 'aux:pass']
        nsubj = [[annotated_headline.sentence[0].token[_edge.source - 1].value, annotated_headline.sentence[0].token[_edge.target - 1].value] for _edge in annotated_headline.sentence[0].basicDependencies.edge if _edge.dep == 'nsubj']
        mentions = [[_mention.entityType, _mention.entityMentionText] for _mention in annotated_headline.mentions]

        return {
            'original_text': annotated_headline.text,
            'highlighted_text': self.highlight_text(annotated_headline.text, mentions, nsubj_pass, aux_pass, nsubj),
            'mentions': mentions,
            'sentiment': annotated_headline.sentence[0].sentiment,
            'nsentiment': SENTIMENT_MAP[annotated_headline.sentence[0].sentiment],
            'nsubj:pass': nsubj_pass,
            'nnsubj:pass': len(nsubj_pass),
            'aux:pass': aux_pass,
            'naux:pass': len(aux_pass),
            'nsubj': nsubj,
            'nnsubj': len(nsubj)
        }

    def process_one_headline(self, headline):
        with self.lock:
            with CoreNLPClient(annotators=self.annotators, timeout=self.timeout, memory=self.memory,classpath=self.core_nlp_folder) as client:
                return self.collect_data(client.annotate(headline))

    def process_multiple_headlines(self, headlines):
        data = []
        with self.lock:
            with CoreNLPClient(annotators=self.annotators, timeout=self.timeout, memory=self.memory,classpath=self.core_nlp_folder) as client:
                for headline in headlines:
                    data.append(self.collect_data(client.annotate(headline)))
            return data
