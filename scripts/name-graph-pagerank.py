# -*- coding: utf-8 -*-

from datetime import datetime
from os import listdir
from os.path import isfile, join
from concurrent import futures

from epoms.db import *
from epoms.entity_extract import EntityExtract


INDEX_NAME  = 'epoms'
TIMEOUT     = 300
MAX_WORKER  = 1

config   = EPOMSConfig()
en = EntityExtract()

news = (News().select().limit(100))

for n in news:
    print '>> Extracting Entity [%5d]' % ( n.id )
    res = ""
    try:
        names = en.extract_name( n.content )
        keys = names.keys()
        for i in range(len(keys)):
            orig = keys[i].replace(' ','_')
            for j in range(len(keys)):
                if( i != j ):
                    dest = keys[j].replace( ' ', '_' )
                    print orig, dest
    except Exception as exc:
        pass
        # print '--> Error %s' % n.as_dict()
        # print(exc)

# print 'DONE!'
