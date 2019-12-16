#!/usr/bin/python3

from urllib.request import urlopen
from bs4 import BeautifulSoup
from math import ceil
import os
import time
from download_video import SearchDownload


def parsePageCount(bsSearch):
    bsPages = bsSearch.findAll("span", class_="pagination-item-1WyVp")
    maxPage = 0
    for bsPage in bsPages :
        #print (bsPage.text)
        if not bsPage.text.isdigit() : continue
        page = int(bsPage.text)
        if page  > maxPage : maxPage = page
    print('Total page count: {0}'.format(maxPage))
    return (maxPage)

# start timer and go
timeStart = time.time()
search = SearchDownload()

# download first search result page
html = search.getData() 

# count pages of search results
bsSearch = BeautifulSoup(html, "html.parser")
pagesCount = parsePageCount(bsSearch)

# download all pages of search results
for page in range(2, pagesCount+1):
    time.sleep(1)
    search.getData(page)

timeDuration = - timeStart + time.time()
print('Duration: {0} seconds'.format(int(ceil(timeDuration))) )
