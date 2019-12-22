#!/usr/bin/python3

import os
import time
from math import ceil
import parse_search
import re

def strFilter(caption):
    caption = caption.replace(
            '-', ' ').replace(
            '+', ' ').replace(
            '/', ' ')
    return (caption.replace('  ', ' '))

def strSplit(caption):
    return re.findall('(\w+|\d+)', caption)

def findItem(captionWords, listNames):
    for word in captionWords:


# start timer and go
timeStart = time.time()

# load gpu list
listOrigin = parse_search.readCsv('gpulist.csv')
#print(listOrigin)

# load search results 
listSearch = parse_search.readCsv('search.csv')
#print(listSearch)

# find gpu by name
listRecognized = []
listUnknown = []
for item in listSearch:
    (caption, price, link) = item
    caption = strFilter(caption)
    captionWords = strSplit(caption)
    #print(captionWords)
    listResult = findItem(captionWords, listOrigin)

# save merged list

# save unrecognized list

timeDuration = - timeStart + time.time()
print('Duration: {0} seconds'.format(int(ceil(timeDuration))) )
