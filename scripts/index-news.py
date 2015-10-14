# -*- coding: utf-8 -*-

from datetime import datetime
from os import listdir
from os.path import isfile, join
from concurrent import futures

from epoms.config import EPOMSConfig
from epoms.news_extraction import NewsExtraction
from epoms.es import *
from epoms.db import *


INDEX_NAME  = 'epoms'
TIMEOUT     = 300
MAX_WORKER  = 1

config   = EPOMSConfig()
es_nodes = config.get('elasticsearch')['nodes']
es = ES().init()

news = (News()
    .select()
    .where( News.indexed_time >> None )
    )

def xstr(s):
    if s is None:
        return ''
    return str(s.encode('utf-8'))

print 'Connecting %s' % ( es_nodes );
print 'Indexing %d news' % ( news.count() )
for n in news:
    print 'Indexing [%5d] %s' % ( n.id, xstr(n.title) )
    res = ""
    try:
        res = es.index(index="epoms", doc_type='news', body=n.as_dict())
    except Exception as exc:
        print '--> Error %s' % n.as_dict()
        print(exc)

print 'DONE!'
