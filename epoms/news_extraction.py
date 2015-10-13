from unidecode import unidecode
from entity_extract import EntityExtract
from BeautifulSoup import BeautifulSoup
import xmltodict
import eatiht.v2 as v2

class NewsExtraction():
    def extract_news( self, filename ):
        f = open(filename)

        content = v2.extract(f)

        ee = EntityExtract()
        names = ee.extract_name( content )

        doc = {
            "content": content,
            "extract_name": names
        }

        f.seek(0)

        try:
            meta_data = {
                "url" : "og:url",
                "sitename": "og:site_name",
                "published_time": "article:published_time",
                "title": "og:title"
            }

            soup = BeautifulSoup(f)

            for k in meta_data.keys():
                value = soup.find(property= meta_data[k] )['content']
                doc[k] = value
        except Exception as exc:
            pass


        return doc
