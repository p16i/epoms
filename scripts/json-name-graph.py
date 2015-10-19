# -*- coding: utf-8 -*-

from datetime import datetime
from os import listdir
from os.path import isfile, join
from concurrent import futures

from epoms.db import *
from epoms.entity_extract import EntityExtract

import json

en = EntityExtract()
news = (News().select().limit(10))


graph = {
    "nodes" : [],
    "links": []
}

edges = []
nodes = []

for n in news:
    names = en.extract_name( n.content )
    keys = names.keys()

    for i in range(len(keys)):
        for j in range(len(keys)):
            if( i != j ):
                edges.append( ( keys[i], keys[j] ) )

for e in edges:
    l = [0,0]
    for i in range(2):
        if( e[i] not in nodes ):
            nodes.append(e[i])

        l[i] = nodes.index(e[i])
    graph['links'].append({
        'source': l[0],
        'target': l[1]
    })

for n in nodes:
    node = {
        'name': n
    }


    if n == 'Philips' :
        node['group'] = 5

    graph['nodes'].append(node)

print json.dumps(graph)
