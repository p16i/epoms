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
    filename  = TextField()

    def as_dict( self ):
        entities = json.loads(self.entities)
        return {
            "id"    : self.id,
            "title" : self.title,
            "url"   : self.url,
            "sitename": self.sitename,
            "content": self.content,
            "entities": entities.keys(),
            "relevant": self.relevant,
            "published_time": self.published_time
        }

class Tweet(BaseModel):
    pass
    id             = PrimaryKeyField()
    username       = TextField()
    body           = TextField()
    _body          = TextField()
    polarity       = BooleanField()
    is_ad          = BooleanField()
    published_time = DateTimeField()
    indexed_time   = DateTimeField()
    query          = TextField()

    def as_dict( self ):
        return {
            "id"    : self.id,
            "username" : self.username,
            "body"   : self.body,
            "polarity" : self.polarity,
            "is_ad"   : self.is_ad,
            "published_time": self.published_time
        }

class Name(BaseModel):
    id        = PrimaryKeyField()
    name      = TextField()
    pagerank  = FloatField()


class Name_Graph(BaseModel):
    id        = PrimaryKeyField()
    doc_id    = ForeignKeyField( News, to_field="id", db_column="doc_id", related_name='name_graph')
    name1     = ForeignKeyField( Name, to_field="name", db_column="name1", related_name='outbound')
    name2     = ForeignKeyField( Name, to_field="name", db_column="name2", related_name='inbound')
