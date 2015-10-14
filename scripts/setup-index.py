from datetime import datetime
from epoms.config import EPOMSConfig
from epoms.es import *

INDEX_NAME = 'epoms'
TIMEOUT = 300

config = EPOMSConfig()
es = ES().init()

# TODO:
# - Accept parameter and delete only index that specified.

es.indices.delete( index=INDEX_NAME, ignore=[400, 404] )

# doc = {
#     'author': 'kimchy',
#     'text': 'Elasticsearch: cool. bonsai cool.',
#     'timestamp': datetime.now(),
# }

# res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
# print(res['created'])

body = {
    "mappings": config.get('index_schema')
}

res = es.indices.create( index=INDEX_NAME, body=body )

print res
