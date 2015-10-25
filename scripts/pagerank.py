#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
This is an example implementation of PageRank. For more conventional use,
Please refer to PageRank implementation provided by graphx
"""
from __future__ import print_function

import re
import sys
from operator import add

from pyspark import SparkContext


damping = 0.15

def computeContribs(urls, rank):
    """Calculates URL contributions to the rank of other URLs."""
    num_urls = len(urls)
    for url in urls:
        yield (url, rank / num_urls)


def parseNeighbors(urls):
    """Parses a urls pair string into urls pair."""
    parts = re.split(r'\s+', urls)
    return parts[0], parts[1]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: pagerank <file> <lambda>", file=sys.stderr)
        exit(-1)

    damping = float(sys.argv[2])

    print("""WARN: This is a naive implementation of PageRank and is
          given as an example! Please refer to PageRank implementation provided by graphx""",
          file=sys.stderr)

    # Initialize the spark context.
    sc = SparkContext(appName="PythonPageRank")

    # Loads in input file. It should be in format of:
    #     URL         neighbor URL
    #     URL         neighbor URL
    #     URL         neighbor URL
    #     ...
    lines = sc.textFile(sys.argv[1], 1)

    # Loads all URLs from input file and initialize their neighbors.
    # URL 1
    #       - URL2
    #       - URL3
    links = lines.map(lambda urls: parseNeighbors(urls)).distinct().groupByKey().cache()

    # Loads all URLs with other URL(s) link to from input file and initialize ranks of them to one.
    ranks = links.map(lambda url_neighbors: (url_neighbors[0], 1.0))

    total_links = ranks.count()
    ranks = ranks.map(lambda r: (r[0], r[1]/total_links))

    print( '>> Total  Link' + str(total_links) )

    # Calculates and updates URL ranks continuously using PageRank algorithm.
    prev_max = 0
    iteration = 1
    while (1):

        print(">> Iteration : "+str(iteration))
        # Calculates URL contributions to the rank of other URLs.
        contribs = links.join(ranks).flatMap(
            lambda url_urls_rank: computeContribs(url_urls_rank[1][0], url_urls_rank[1][1]))

        # Re-calculates URL ranks based on neighbor contributions.
        ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * ( 1 - damping ) + damping/total_links )



        count = ranks.map( lambda r: ( 1, r[1] ) ) \
            .reduceByKey( lambda a, b: a if (a > b) else b )

        cur_max = count.collect()[0][1]

        print (">> Diff "+ str(abs( cur_max-prev_max )) )

        if( abs( cur_max - prev_max ) < 0.000001 ):
            break
        else:
            prev_max = cur_max

        iteration = iteration + 1


    ranks = ranks.sortBy( lambda r: -r[1] )
    ranks.map(lambda r: " ".join([ r[0], str(r[1]) ])).coalesce(1).saveAsTextFile('output-pagerank')

    sc.stop()
