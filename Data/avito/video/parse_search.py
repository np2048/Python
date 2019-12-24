#!/usr/bin/python3

from bs4 import BeautifulSoup

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

#def writeCsv(items, append=false):
 #   return ( csv.writeCsv(items, FILE_NAME, append) )
