# -*- coding: utf-8 -*-

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

tweets = (Tweet()
    .select()
    .where( Tweet.indexed_time >> None )
    )


print 'Connecting %s' % ( es_nodes );
print 'Indexing %d news' % ( tweets.count() )
for t in tweets:
    print 'Indexing [%5d] %s' % ( t.id, t.body )
    res = ""
    try:
        res = es.index(index="epoms", doc_type='tweet', body=t.as_dict())
    except Exception as exc:
        print '--> Error %s' % n.as_dict()
        print(exc)

print 'DONE!'
