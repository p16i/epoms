from sys import argv
import re
import csv
import datetime

from epoms.config import EPOMSConfig
from epoms.db import *
from epoms.linguistic_utility import LinguisticUtility

from pymoji import PyMoji

script, filename = argv
moji = PyMoji()
ling = LinguisticUtility()

query = filename.split('.')[1]

def ts_2_datetime( ts ):
    return datetime.datetime.fromtimestamp(float(ts)).strftime('%Y-%m-%d %H:%M:%S')


with open( filename, 'rU') as csvfile:
        tweets = csv.reader(csvfile)
        count = 1
        for row in tweets:
            try:
                print '[%5d] Extracting %s' % ( count, row[1] )
                t = {
                    # we dont' want @ at the front
                    'username': row[0][1:],
                    'body':     moji.encode(row[1]),
                    'published_time': ts_2_datetime( row[2] )
                }

                t['_body'] = ling.clean_up_tweet( t['body'] )
                t['query'] = query
                Tweet.create( **t )
            except Exception as exc:
                print '--> Error %s' % ( exc )
                pass

            count = count + 1
