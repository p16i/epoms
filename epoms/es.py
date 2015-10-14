from elasticsearch import Elasticsearch
from config import EPOMSConfig

class ES():
    def init(self):
        config   = EPOMSConfig()
        es_nodes = config.get('elasticsearch')['nodes']
        es = Elasticsearch( es_nodes )
        return es

