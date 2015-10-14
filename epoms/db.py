from config import EPOMSConfig
from peewee import *

import MySQLdb
import json

c = EPOMSConfig();
db_config = c.get('db')

database = MySQLDatabase( db_config.pop('db'), **db_config )

class BaseModel(Model):
    class Meta:
        database = database

class News(BaseModel):
    id = PrimaryKeyField()
    title = CharField()
    url = CharField()
    sitename = CharField()
    content = TextField()
    entities = TextField()
    relevant = BooleanField()
    published_time = DateTimeField()
    indexed_time = DateTimeField()

    def as_dict( self ):
        entities = json.loads(self.entities)
        return {
            "title" : self.title,
            "url"   : self.url,
            "sitename": self.content,
            "entities": entities.keys(),
            "relevant": self.relevant,
            "published_time": self.published_time
        }

class Tweet(BaseModel):
    pass
    # id
    # username
    # body
    # tweeted_time
    # indexed_time
    # polarity
