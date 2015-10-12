import eatiht.v2 as v2
from sys import argv
from epoms.entity_extract import EntityExtract
import xmltodict

from BeautifulSoup import BeautifulSoup


script, filename = argv
f = open(filename)

content = v2.extract(f)
ee = EntityExtract()
names = ee.extract_name( content )

f.seek(0)
soup = BeautifulSoup(f)

meta_data = {
    "url" : "og:url",
    "sitename": "og:site_name",
    "published_time": "article:published_time",
    "title": "og:title"
}

doc = {
    "content": content,
    "extract_name": names
}

for k in meta_data.keys():
    value = soup.find(property= meta_data[k] )['content']
    doc[k] = value

print '------------ Document -----------'
print 'Filename : %s' % filename
print 'Attributes : '

for k in doc.keys():
    print ' --> %s : %s' % (k, doc[k])
