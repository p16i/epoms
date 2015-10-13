from datetime import datetime
from elasticsearch import Elasticsearch
from os import listdir
from os.path import isfile, join
from concurrent import futures

from epoms.config import EPOMSConfig
from epoms.news_extraction import NewsExtraction


INDEX_NAME  = 'epoms'
TIMEOUT     = 300
MAX_WORKER  = 1

es = Elasticsearch()
config = EPOMSConfig()
nn = NewsExtraction()

datasource = config.get('datasource')['news']

files = []
for f in listdir(datasource):
    absolute_path = join(datasource, f )
    if( isfile( absolute_path ) ):
        files.append( absolute_path )

# Sample document
# doc = {
#     'sitename': 'Jojo.com',
#     'title': 'Elasticsearch: cool. bonsai cool.',
#     'published_time': datetime.now(),
#     'content': 'Slow life by indexeeeer',
#     'entities': ['Elasticsearch', 'Solar', 'Apache Spark' ]
# }

# res = es.index(index="epoms", doc_type='news', body=doc)
# print(res['created'])

print 'Indexing %d files' % len(files)

def index_news( filename ):
    print 'Indexing %s' % filename
    res = ""
    try:
        doc = nn.extract_news( filename )
        res = es.index(index="epoms", doc_type='news', body=doc)
    except Exception as exc:
        print '--> Error %s' % filename
        print(exc)

    return

for f in files:
    index_news( f )


print 'DONE!'
