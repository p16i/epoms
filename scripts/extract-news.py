from os import listdir
from os.path import isfile, join

from epoms.news_extraction import NewsExtraction
from epoms.db import *
import json
import sys

config = EPOMSConfig()
datasource = sys.argv[1]
print datasource
nn = NewsExtraction()

files = []
for f in listdir(datasource):
    absolute_path = join(datasource, f )
    if( isfile( absolute_path ) ):
        files.append( absolute_path )

count = 1
for f in files:
    print '[%5d] Extracting %s' % ( count, f )
    res = ""
    try:
        doc = nn.extract_news( f )
        doc['entities'] = json.dumps(doc['entities'])
        doc['filename'] = f

        n = News.create( **doc )
    except Exception as exc:
        print '--> Error %s' % ( exc )

    count += 1
