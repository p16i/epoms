# -*- coding: utf-8 -*-

from datetime import datetime
from os import listdir
from os.path import isfile, join
from concurrent import futures
import operator

import sys


import json


graph_filename = sys.argv[1]
rank_filename  = sys.argv[2]

lines = open( graph_filename, 'r').readlines()

ranks = dict()
for l in open( rank_filename, 'r').readlines():
    ( name, rank ) = l.strip().split(' ')
    ranks[name] = float(rank)


graph = dict()

for l in lines:
    ( src, dest ) = l.strip().split(' ')
    if( src in graph.keys() and dest not in graph[src] ):
        graph[src].append(dest)
    else:
        graph[src] = [ dest ]

names = []

def find_subtree( name, depth ):
    if( depth == 0 ):
        return { "name": name }
    else:
        flare_graph = {
            "name" : name,
            "rank" : ranks[name],
            "children": []
        }
        names.append(name)

        candidates = []
        for t in graph[name]:
            if( t not in names ):
                # print t
                candidates.append({
                    "name": t,
                    "rank": ranks[t]
                })
                names.append(t)

        sorted_candiates = sorted( candidates, key=lambda x: x['rank'], reverse=True )
        sorted_candiates = sorted_candiates[:10]

        for c in sorted_candiates:
            flare_graph['children'].append( find_subtree( c['name'], depth - 1 ) )

        return flare_graph


flare_graph = find_subtree( 'Philips', 3 )

flare_graph['min_rank'] = min( ranks.values() )
flare_graph['max_rank'] = max( ranks.values() )



print json.dumps(flare_graph)
