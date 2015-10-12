import nltk
import re
import time

class EntityExtract():

    def extract_name( self, text ):
        # TODO: Normalise text

        tokenized = nltk.word_tokenize(text)

        tagged = nltk.pos_tag(tokenized)

        entities = nltk.ne_chunk(tagged, binary=True )
        nodes = self.getNodes( entities, 'NE' )

        freq = dict();
        for n in nodes :
            if n in freq :
                freq[n] = freq[n] + 1
            else:
                freq[n] = 1

        return freq

    def getNodes( self, node, node_type ):
        res = []

        if( hasattr( node, 'label' ) and node.label ):
            if node.label() == node_type:
                res.append(' '.join([child[0] for child in node]))
            else:
                for child in node:
                    res.extend( self.getNodes( child, node_type ) )
        return res