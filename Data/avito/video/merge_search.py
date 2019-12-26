#!/usr/bin/python3

import os
import time
from math import ceil
from parse_search import *
import csv

# start timer and go
timeStart = time.time()

# load gpu list
listOrigin = csv.readCsv('gpulist.csv')
listOrigin = listFilter(listOrigin)
listOrigin = listSplit(listOrigin)
#print(listOrigin[-1])

# load search results 
listSearch = csv.readCsv('search.csv')
listSearch = listFilter(listSearch)
#print(listSearch)

# load exceptions list
# exceptions are the advertisments than doesn't count
# file may contain additional information
# but only first column is valid for identification
listExceptions = csv.readCsv('exceptions.csv')
lst = []
for item in listExceptions :
    lst.append(item[0])
listExceptions = lst
#print(listExceptions)

# find gpu by name
listRecognized = []
listUnknown = []
for item in listSearch:
    (name, price, link) = item
    link = link.replace('\n', '')
    if link in listExceptions : continue
    listGpu = findItem(name, listOrigin)
    #print(listGpu) 
    #exit()
    if len(listGpu) > 1 :
        choose = chooseItem(item, listGpu)
        if len(choose) > 0 : listGpu = choose
    if len(listGpu) > 1 :
        choose = chooseItemPairs(item, listGpu)
        if len(choose) > 0 : listGpu = choose
    if len(listGpu) == 1 :
        (gpuName, gpuNameList, gpuPerf, gpuLink) = listGpu[0] 
        listRecognized.append([
                name, gpuName, price, gpuPerf, link, gpuLink
                ])
    else :
        print(link)
        unknown = []
        for gpu in listGpu:
            (gpuName, gpuNameList, gpuPerf, gpuLink) = gpu 
            unknown += [gpuName, gpuPerf]
        listUnknown.append([link, name, price] + unknown)
print('Recognized: {0}\nUnknown: {1}'.format(
    len(listRecognized), 
    len(listUnknown)
    ))
#print(listRecognized)

# save merged list
csv.writeCsv(listRecognized, 'recognized.csv')

# save unrecognized list
csv.writeCsv(listUnknown, 'undefined.csv')
#print(listUnknown[-1])
#print(listSearch[-1])

timeDuration = - timeStart + time.time()
print('Duration: {0} seconds'.format(int(ceil(timeDuration))) )
