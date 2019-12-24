#!/usr/bin/python3

import os
import time
from math import ceil
import parse_search
import re
import csv

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

def listIn(item, lst) :
    for lst1 in lst:
        for i in lst1:
            if i == item:
                return(True)
    return(False)
#print(listIn([3, 4], [[[1, 2], [3, 4], [5, 6]]]))

def listMerge(lst):
    result = []
    for i in range(0, len(lst) - 1):
        resultI = []
        itemList = lst[i]
        for item in itemList:
            if listIn(item, lst[i+1:]):
                resultI += [item]
                itemList.remove(item)
        if len(resultI) > 0 : result += [resultI]
    return(result)
#print(listMerge([[[1, 1], [3, 3], [2, 2]], [[2, 2], [3, 3], [4, 4]]]))
#exit()

def listMakeFlat(lst):
    result = []
    for lst1 in lst:
        for item in lst1:
            result += [item]
    return (result)

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
                listResWord.append(gpu)
        if (len(listResWord) == 0): continue
        listResult.append(listResWord)
        #print(listResult)
    count = 10
    while len(listResult) > 1  and count > 0:
        merge = listMerge(listResult)
        if len(merge) > 0: listResult = merge
        count -= 1
    listResult = listMakeFlat(listResult)
    #print(listResult)
    return (listResult)

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

# find gpu by name
listRecognized = []
listUnknown = []
for item in listSearch:
    (name, price, link) = item
    listGpu = findGpu(name, listOrigin)
    #print(listGpu) 
    #exit()
    if len(listGpu) == 1 :
        (gpuName, gpuNameList, gpuPerf, gpuLink) = listGpu[0] 
        listRecognized.append([
                name, price, link, 
                gpuName, gpuPerf, gpuLink
                ])
    else :
        unknown = []
        for gpu in listGpu:
            (gpuName, gpuNameList, gpuPerf, gpuLink) = gpu 
            unknown += [gpuName, gpuPerf]
        listUnknown.append([name] + unknown)
print('Recognized: {0}\nUnknown: {1}'.format(
    len(listRecognized), 
    len(listUnknown)
    ))
#print(listRecognized)
#csv.writeCsv(listRecognized, 'recognized.csv')
csv.writeCsv(listUnknown, 'undefined.csv')
print(listUnknown[-1])
#print(listSearch[-1])
#for lst in listUnknown[-1]:
 #   for lst1 in lst:
  #      print(lst1[0])
   #     print(lst1[2])
    #print('{0} : {1}'.format(name, listGpu))
    #if len(listAds): print(listAds)

# save merged list

# save unrecognized list

timeDuration = - timeStart + time.time()
print('Duration: {0} seconds'.format(int(ceil(timeDuration))) )
