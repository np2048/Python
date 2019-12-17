#!/usr/bin/python3

from bs4 import BeautifulSoup
import numpy as np

itemName = []
itemPerf = []
itemLink = []
rowCount = 0
for gpuListNum in range(1, 4+1):
    htmlFileName = "gpu{0}.html".format(gpuListNum)
    print(htmlFileName)
    fCpu = open(htmlFileName)
    bsObj = BeautifulSoup(fCpu.read(), 'html.parser')
    rowList = bsObj.find("ul", class_="chartlist").findAll("a")
    for tr in rowList :
        rowCount += 1
        name = tr.find("span", class_='prdname')
        if not name : continue
        itemName.append(name.text)
        itemPerf.append(tr.find("span", class_='count').text.replace(',', ''))
        itemLink.append(tr.get('href'))
print("Total rows processed: {0}".format(rowCount))
np.savetxt("gpulist.csv", [p for p in zip(itemName, itemPerf, itemLink)], fmt="%s", delimiter=';')
