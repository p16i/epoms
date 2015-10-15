import unicodedata
import sys
import re

from nltk.tokenize import RegexpTokenizer
from Levenshtein import *

NON_DECOMPOSABLE_CHARACTERS = {
        u'\N{Latin capital letter AE}': 'AE',
        u'\N{Latin small letter ae}': 'ae',
        u'\N{Latin capital letter Eth}': 'D', #
        u'\N{Latin small letter eth}': 'd', #
        u'\N{Latin capital letter O with stroke}': 'O', #
        u'\N{Latin small letter o with stroke}': 'o',  #
        u'\N{Latin capital letter Thorn}': 'Th',
        u'\N{Latin small letter thorn}': 'th',
        u'\N{Latin small letter sharp s}': 's',#
        u'\N{Latin capital letter D with stroke}': 'D',#
        u'\N{Latin small letter d with stroke}': 'd',#
        u'\N{Latin capital letter H with stroke}': 'H',
        u'\N{Latin small letter h with stroke}': 'h',
        u'\N{Latin small letter dotless i}': 'i',
        u'\N{Latin small letter kra}': 'k',#

        u'\N{Latin small letter l with stroke}': 'l',
        u'\N{Latin capital letter Eng}': 'N', #
        u'\N{Latin small letter eng}': 'n', #
        u'\N{Latin capital ligature OE}': 'Oe',
        u'\N{Latin small ligature oe}': 'oe',
        u'\N{Latin capital letter T with stroke}': 'T', #
        u'\N{Latin small letter t with stroke}': 't',#
}

class LinguisticUtility():
    def remove_diacritics( self, text ):
        if not text:
            return text
        uni = None
        if isinstance(text, unicode):
            uni = text
        else :
            encoding=sys.getfilesystemencoding()
            uni =unicode(text, encoding, 'ignore')
        s = unicodedata.normalize('NFKD', uni)
        b=[]
        for ch in s:
            if  unicodedata.category(ch)!= 'Mn':
                if NON_DECOMPOSABLE_CHARACTERS.has_key(ch):
                    b.append(NON_DECOMPOSABLE_CHARACTERS[ch])
                elif ord(ch)<128:
                    b.append(ch)
                else:
                    b.append(' ')
        return ''.join(b)

    def clean_up_space( self, text ):

        text = re.sub(r'\s{2,}', ' ', text )
        text = text.strip()

        return text

    def clean_up_tweet( self, text ):
        tokens = text.split(' ');
        res = []
        for t in tokens:
            if( re.match(r'RT', t) ):
                res.append('[RT]')
            elif ( re.match(r'https?://.+', t) ):
                res.append('[URL]')
            elif ( re.match(r'@.+', t)):
                res.append('[MENTION]')
            else:
                res.append(t)

        return ' '.join(res)

    def tokenizer( self, text ):

        tokenizer = RegexpTokenizer(r'\w+')
        tokenized = tokenizer.tokenize(text)

        return tokenized

    def choose_furthest_term( self, ref, t1, t2 ):
        ref = unicode(ref)
        t1  = unicode(t1)
        t2  = unicode(t2)

        d_t1 = distance( ref, t1 )
        d_t2 = distance( ref, t2 )

        if( d_t1 > d_t2 ):
            return t1

        return t2

