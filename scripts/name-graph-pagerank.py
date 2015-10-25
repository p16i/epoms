# -*- coding: utf-8 -*-

from datetime import datetime
from os import listdir
from os.path import isfile, join
from concurrent import futures

from epoms.db import *
from epoms.entity_extract import EntityExtract

from nltk.tokenize import sent_tokenize

import sys
import re

INDEX_NAME  = 'epoms'
TIMEOUT     = 300
MAX_WORKER  = 1

config   = EPOMSConfig()
en = EntityExtract()


mode = sys.argv[1]
# 1 = extract name from one sentence
# all = whole text

news = (News().select())

def merge_sentence( sentences, mode ):
    start = 0
    length = len(sentences)

    if( mode == 'all' ):
        mode = length
    else:
        mode = int(mode)

    res = []

    for i in range( int(length/mode) ):

        new_start = start + mode

        t =  ' '.join( sentences[start:new_start])
        res.append(t)

        start = new_start

    return res

for n in news:
    try:

        content = n.content
        sentences = sent_tokenize(content)

        sentences = merge_sentence( sentences, mode )

        print "Getting %d groups of text from document %d" % ( len(sentences), n.id )
        for s in sentences:
            names = en.extract_name(s)
            keys = names.keys()
            for i in range(len(keys)):
                name1, created = Name().get_or_create( name=keys[i] )
                orig = keys[i].replace(' ','_')
                for j in range(len(keys)):
                    if( i != j ):
                        # Save graph to db
                        name2, created = Name().get_or_create( name=keys[j] )
                        Name_Graph.create( name1=name1, name2=name2,  doc_id=n.id )

                        dest = keys[j].replace( ' ', '_' )
                        print '### ',orig,dest
    except Exception as exc:
        pass
        # print '--> Error %s' % n.as_dict()
        # print(exc)

# print 'DONE!'

