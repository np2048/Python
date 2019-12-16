#!/usr/bin/python3

from urllib.request import urlopen
import os
import time
from download import CacheDownload

class SearchDownload(CacheDownload):
    URL = "https://www.avito.ru/krasnodar/tovary_dlya_kompyutera/komplektuyuschie/videokarty?cd=1" 
    DIR_PREFIX = "search_"
    def __init__(this, priceMin=1000, priceMax=6000):
        this.pMax = priceMax
        this.pMin = priceMin
        this.verbose = this.VERBOSE
    def getUrl(this, page=1):
        searchUrl = this.URL + "&pmax={0}&pmin={1}".format(
            this.pMax, this.pMin)
        if page > 1 : searchUrl += "&p={0}".format(page)
        return ( searchUrl )
    def getDirName(this):
        return ( "{0}{1}".format(this.DIR_PREFIX, this.pMax) )

