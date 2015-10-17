import nltk
import re
import time

from linguistic_utility import LinguisticUtility

class EntityExtract():

    def __init__( self ):
        self.ling = LinguisticUtility()

    def extract_name( self, text ):

        text = self.ling.remove_diacritics( text )
        tokenized = self.ling.tokenizer( text )

        tagged = nltk.pos_tag(tokenized)

        entities = nltk.ne_chunk(tagged, binary=True )
        nodes = self.getNodes( entities, 'NE' )


        freq = dict();
        for n in nodes :
            if n in freq :
                freq[n] = freq[n] + 1
            else:
                freq[n] = 1

        freq = self.merge_name( freq )

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

    def merge_name( self, names_dic ):
        res = dict()
        uniq_name = dict()

        for k in names_dic.keys():
            n_k = self.ling.remove_diacritics(k.lower())

            if( n_k in uniq_name.keys() ):

                old_key = uniq_name[n_k]
                new_key = self.ling.choose_furthest_term( n_k, old_key , k )
                if( new_key == k ):
                    old_freq = res.pop( uniq_name[n_k] )
                    res[new_key] = names_dic[k] + old_freq
                    uniq_name[n_k] = new_key
                else:
                    res[old_key] = res[old_key] + names_dic[k]

            else:
                res[k] = names_dic[k]
                uniq_name[n_k] = k

        return res



