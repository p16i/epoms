# -*- coding: utf-8 -*-

from datetime import datetime
from os import listdir
from os.path import isfile, join
from concurrent import futures

import sys


import json


filename = sys.argv[1]
csv      = sys.argv[2]

lines = open( filename, 'r').readlines()

ranks = dict()
for l in open( csv, 'r').readlines():
    ( name, rank ) = l.strip().split(' ')
    ranks[name] = float(rank)


graph = dict()

for l in lines:
    ( src, dest ) = l.strip().split(' ')
    if( src in graph.keys() and dest not in graph[src] ):
        graph[src].append(dest)
    else:
        graph[src] = [ dest ]

def find_subtree( name, depth ):
    if( depth == 0 ):
        return []
    else:
        subtree = [ { "name": name, "nodes": graph[name] } ]
        for t in graph[name]:
            subtree = subtree + find_subtree( t, depth - 1 )

        return subtree

tree = find_subtree( 'Philips', 2 )

graph = {
    "nodes" : [],
    "links": []
}
edges = []
nodes = []

for n in tree:
    for d in n['nodes']:
        edges.append( ( n['name'], d ) )

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
    # TODO: Add pagerank here
    node = {
        'name': n,
        'rank': ranks[n]
    }


    if n == 'Philips' :
        node['group'] = 5

    graph['nodes'].append(node)

print json.dumps(graph)
