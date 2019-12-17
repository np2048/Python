#!/usr/bin/python3

from bs4 import BeautifulSoup

FILE_NAME = 'search.csv'
URL_PREFIX = 'http://avito.ru'

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

def writeCsv(items, append=False):
    fileOpenMode = 'w'
    if append : fileOpenMode = 'a'
    file = open(FILE_NAME, fileOpenMode)
    for item in items:
        file.write(';'.join(item) + '\n')
    file.close()

def readCsv(fileName):
    data = []
    file = open(fileName, "r")
    lines = file.readlines()
    file.close()
    for line in lines:
        data.append(line.split(';'))
    return(data)
