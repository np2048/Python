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
            '.', ' ').replace(
            '/', ' ')
    return (re.sub('\s\s+', ' ', caption).lower())

def listFilter(lst, index=0):
    result = []
    for item in lst:
        item[index] = strFilter(item[index])
        result.append((item))
    return(result)

def strSplit(caption):
    return (re.findall('[a-z]+', caption) + re.findall('\d+', caption))

def listSplit(lst, index=0):
    result = []
    for item in lst:
        item.insert(1, strSplit(item[index]))
        result.append((item))
    return(result)

def lstIntersection(list1, list2):
    res = []
    for item in list1:
        if item in list2: res += item
    return(res)
#print(lstIntersection([[1],[ 2],[ 3]], [[2], [3], [5]]))

def listIn(lst, item):
    for lst1 in lst:
        for i in lst1:
            if i == item:
                return(True)
    return(False)
print(listIn([[1, 2], [3, 4]], 1))

def listMerge(lst):
    result = []
    for i in range(0, len(lst) - 1):
        resultI = []
        itemList = lst[i]
        for item in itemList:
            if listIn(lst[i+1:], item):
                resultI += item
        if len(resultI) > 0 : result += [resultI]
    return(result)
print(listMerge([[[1, 1], [2, 2], [3, 3]], [[2, 2], [3, 3], [4, 4]]]))
#exit()

def findGpu(caption, listGpu):
    listCaption = strSplit(caption)
    #print(listCaption)
    listResult = []
    for word in listCaption:
        if len(word) < 2 : continue
        listResWord = []
        for gpu in listGpu:
            (gpuName, gpuNameWords, gpuPerf, gpuLink) = gpu
            if word in gpuNameWords :
                listResWord.append([gpu])
        if (len(listResWord) == 0): continue
        listResult.append(listResWord)
        listResult = listMerge(listResult)
    return (listResult)

# start timer and go
timeStart = time.time()

# load gpu list
listOrigin = parse_search.readCsv('gpulist.csv')
listOrigin = listFilter(listOrigin)
listOrigin = listSplit(listOrigin)
#print(listOrigin)

# load search results 
listSearch = parse_search.readCsv('search.csv')
listSearch = listFilter(listSearch)
#print(listSearch)

# find gpu by name
listRecognized = []
listUnknown = []
for item in listSearch:
    (name, price, link) = item
    listGpu = findGpu(name, listOrigin)
    listUnknown.append(listGpu)
print(listUnknown[-1])
for lst in listUnknown[-1]:
    for lst1 in lst:
        for lst2 in lst1:
            print(lst2[0])
    #print('{0} : {1}'.format(name, listGpu))
    #if len(listAds): print(listAds)

# save merged list

# save unrecognized list

timeDuration = - timeStart + time.time()
print('Duration: {0} seconds'.format(int(ceil(timeDuration))) )
