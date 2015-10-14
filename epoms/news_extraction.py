from unidecode import unidecode
from entity_extract import EntityExtract
from BeautifulSoup import BeautifulSoup
import xmltodict
import eatiht.v2 as v2
import dateutil.parser

class NewsExtraction():
    def extract_news( self, filename ):
        f = open(filename)

        content = v2.extract(f)

        ee = EntityExtract()
        names = ee.extract_name( content )

        doc = {
            "content": content,
            "entities": names
        }

        f.seek(0)

        meta_data = {
            "url" : "og:url",
            "sitename": "og:site_name",
            "published_time": "article:published_time"
        }

        soup = BeautifulSoup(f)

        doc['title'] = soup.title.string

        for k in meta_data.keys():
            try:
                value = soup.find(property= meta_data[k] )['content']
                doc[k] = value
            except Exception as exc:
                pass

        if( 'published_time' in doc.keys() ):
            doc['published_time'] = self._make_datetime( doc.pop('published_time') )


        return doc
    def _make_datetime( self, text ):
        d = dateutil.parser.parse(text)
        return d.strftime('%Y-%m-%d %H:%M:%S')
