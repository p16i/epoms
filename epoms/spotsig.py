import re
from nltk.tokenize import RegexpTokenizer

class SpotSig():
    STOPWORDS_FILE =  "./share/stopwords.txt"
    STOPWORDS   = dict()

    DISTANCE    = 1
    CHAINLENGTH = 2
    ANTECEDENT  = r"^(a|an|the|is)$"
    TERM_SEPARATOR = ":"

    def __init__(self):

        self.tokenizer = RegexpTokenizer(r'\w+')

        for l in open( self.STOPWORDS_FILE, 'r'):
            self.STOPWORDS[l.strip()] = 1

    def signature( self, doc ):

        tokens = self.tokenizer.tokenize(doc.lower())

        signatures = dict();

        sig = dict()
        for i in range( len(tokens) ):
            t = tokens[i]
            if( self.is_antecedent(t) ):
                sig[i] = { "terms": [t] }
            elif(   not self.is_stopword(t)
                    and not self.is_antecedent(t)
                 ):

                for s in sig.keys():
                    if( (i-s) % self.DISTANCE == 0 ):
                        sig[s]['terms'].append(t)

                        if( len(sig[s]['terms']) == self.CHAINLENGTH + 1 ):
                            signature = self.spot_signature(sig[s]['terms'])
                            signatures[signature] = 1
                            del sig[s]

        return signatures

    def is_stopword( self, term ):
        return term in self.STOPWORDS

    def is_antecedent( self, term ):
        return re.search( self.ANTECEDENT, term )

    def spot_signature( self, terms ):
        return self.TERM_SEPARATOR.join(terms)

