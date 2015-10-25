# -*- coding: utf-8 -*-

from datetime import datetime
from os import listdir
from os.path import isfile, join
from concurrent import futures

from epoms.db import *
from epoms.entity_extract import EntityExtract


INDEX_NAME  = 'epoms'
TIMEOUT     = 300
MAX_WORKER  = 1

config   = EPOMSConfig()
en = EntityExtract()

news = (News().select())

for n in news:
    print '>> Extracting Entity [%5d]' % ( n.id )
    try:
        names = en.extract_name( n.content )
        keys = names.keys()
        for i in keys:
            for j in range(names[i]):
                print i
    except Exception as exc:
        pass
