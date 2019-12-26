#!/usr/bin/python3

#
# Generic class for cached pages download
#

from urllib.request import urlopen
import os
import time

class CacheDownload:
    DIR_NAME = "cache"
    CACHE_VALID_TIME = 3600 * 24 * 1
    VERBOSE = True
    DELAY_RETRY = 1 # wait time in seconds to retry download on error
    def __init__(this):
        this.verbose = this.VERBOSE
    def getData(this, id=1):
        html = ""
        fileName = this.getFileName(id) 
        if this.isCacheFileValid(fileName) :
           html = this.getFromCache(fileName)
        else :
           html = this.getFromInternet(this.getUrl(id) )
           this.saveCacheById(id, html)
        return ( html )
    def saveCacheById(this, id, data):
        dir = this.getDirName()
        if not os.path.exists(dir) : os.makedirs(dir)
        this.saveCacheFile(this.getFileName(id), data)
    def saveCacheFile(this, fileName, data):
        if this.verbose : print('Saving cache file ' + fileName)
        with open(fileName, 'w') as file:
            file.write(data.decode('utf-8'))
            file.close()
    def getFromInternet(this, url):
        retryCount = 0
        while True:     # try to download the page until it's not blank
            if retryCount : print("Retry {0}: ".format(retryCount), end='')
            if this.verbose : print(url)
            html = None
            try:
                html = urlopen(url, timeout=30).read() 
            except: 
                continue
            if html : break
            retryCount += 1
            time.sleep(DELAY_RETRY)
        return (html)
    def getFromCache(this, fileName):
        if not os.path.exists(fileName): return( "" )
        data = ""
        with open(fileName, "r") as file : 
            data = file.read()
            file.close()
        if this.verbose : print(fileName)
        return (data.encode('utf-8'))
    def isCacheFileValid(this, fileName):
        if not os.path.exists(fileName): return ( False )
        modifiedTime = os.path.getmtime(fileName)
        currentTime = time.time()
        return ( (currentTime - modifiedTime ) < this.CACHE_VALID_TIME )
    def getFileName(this, id=1):
            dirName = this.getDirName()
            return ( "{0}{1}{2}.html".format(dirName, os.sep, id) )
    def getDirName(this):
        return (this.DIR_NAME)

