#!/usr/bin/python3

from bs4 import BeautifulSoup

import re
import csv

FILE_NAME = 'search.csv'
URL_PREFIX = 'https://www.avito.ru'

def pagesCount(bsSearch):
    bsPages = bsSearch.findAll('span', class_='pagination-item-1WyVp')
    maxPage = 0
    for bsPage in bsPages :
        #print (bsPage.text)
        if not bsPage.text.isdigit() : continue
        page = int(bsPage.text)
        if page  > maxPage : maxPage = page
    print('Total page count: {0}'.format(maxPage))
    return (maxPage)

# parse html to get the list of items
def itemList(bsSearch):
    bsItems = bsSearch.findAll('div', 
            class_='description item_table-description')
    list = []
    for bsItem in bsItems:
        href = bsItem.find('a', class_='snippet-link').get('href')
        title = bsItem.find('div', class_='snippet-title-row').text
        title = title.strip('\n ')
        price = bsItem.find('span', class_='price').text
        price = ''.join( filter(lambda i: i in '0123456789', price) )
        list.append((title, price, URL_PREFIX + href))
    return(list)

def strFilter(caption):
    caption = caption.replace(
            '-', ' ').replace(
            '.', ' ').replace(
            'х', 'x').replace(
            '/', ' ')
    return (re.sub('\s\s+', ' ', caption).lower())

def listFilter(lst, index=0):
    result = []
    for item in lst:
        item[index] = strFilter(item[index])
        result.append((item))
    return(result)

def strSplit(caption):
    return (re.findall('\d+', caption) + re.findall('[a-z]+', caption))

def listSplit(lst, index=0):
    result = []
    for item in lst:
        item.insert(1, strSplit(item[index]))
        result.append((item))
    return(result)

def listIntersect(list1, list2):
    res = []
    for item in list1:
        if item in list2: res.append(item)
    return(res)

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

def findItemText(caption, listItems):
    listResult = []
    for item in listItems:
        (name, nameWords, perf, link) = item
        if caption.replace(' ', '').find(name.replace(' ', '')) >= 0 :
            listResult.append(item)
    return(listResult)

def findItemNums(caption, listItems):
    listResult = []
    for item in listItems:
        (name, nameWords, perf, link) = item
        itemNums = re.findall('\d+', name)
        for num in itemNums :
            if len(num) <= 1 : continue
            if caption.replace(' ', '').find(num) >= 0 :
                if not item in listResult : listResult.append(item)
    return(listResult)

def findItem(caption, listItems):
    listCaption = strSplit(caption)
    #print(listCaption)
    listText = findItemText(caption, listItems)
    if len(listText) == 0 :
        listText = findItemNums(caption, listItems)
    if len(listText) == 1:
        return(listText)
    listResult = []
    for word in listCaption:
        if len(word) < 2 : continue
        listResWord = []
        for gpu in listItems:
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
    if len(listResult) > 1 and len(listText) > 0 :
        listInt = listIntersect(listResult, listText)
        if len(listInt) > 0 : 
            listResult = listInt
        else :
            listResult = listText
    return (listResult)

def chooseItemPairs(adv, listItem):
    (caption, price, link) = adv
    caption = caption.replace(' ', '')
    result = []
    match = []
    for i in range(0, len(listItem)):
        item = listItem[i]
        match.append(0)
        itemWords = item[0].split(' ')
        for w in range(0, len(itemWords) - 1) :
            word = itemWords[w] + itemWords[w + 1]
            if caption.find(word) >= 0:
                match[i] += 1
    maxMatch = max(match)
    for i in range(0, len(match)):
        if match[i] == maxMatch:
            result.append(listItem[i])
    return(result)

def chooseItem(adv, listItem):
    (caption, price, link) = adv
    result = []
    match = []
    for i in range(0, len(listItem)):
        item = listItem[i]
        match.append(0.0)
        itemWords = item[0].split(' ')
        for word in itemWords :
            if caption.find(word) >= 0:
                match[i] += 1.0 / len(itemWords)
    maxMatch = max(match)
    for i in range(0, len(match)):
        if match[i] == maxMatch:
            result.append(listItem[i])
    return(result)

