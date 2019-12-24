#!/usr/bin/python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
from math import ceil
import os
import time
from download_video import SearchDownload
import parse_search
import csv

# start timer and go
timeStart = time.time()
search = SearchDownload()

# download first search result page
html = search.getData() 

# count pages of search results
bsSearch = BeautifulSoup(html, "html.parser")
pagesCount = parse_search.pagesCount(bsSearch)

# get items from search results
itemList = parse_search.itemList(bsSearch)
#print(itemList)
parse_search.writeCsv(itemList)

# download all pages of search results
for page in range(2, pagesCount+1):
    time.sleep(1)
    html =  search.getData(page) 
    bsSearch = BeautifulSoup(html, "html.parser")
    itemList = parse_search.itemList(bsSearch)
    parse_search.writeCsv(itemList, append=True)

timeDuration = - timeStart + time.time()
print('Duration: {0} seconds'.format(int(ceil(timeDuration))) )
