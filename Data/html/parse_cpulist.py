#!/usr/bin/python3

from bs4 import BeautifulSoup
import numpy as np

fCpu = open("cpulist.html")
bsObj = BeautifulSoup(fCpu.read(), 'html.parser')
trList = bsObj.find("table", id="cputable").findAll("tr", role="row")
cpuName = []
cpuPerf = []
for tr in trList :
    tdList = tr.findAll("td")
    if not tdList : continue
    cpuName.append(tdList[0].text)
    cpuPerf.append(tdList[1].text)
    #print(tdList[0].text + " " + tdList[1].text)
#print(cpuName)
np.savetxt("cpulist.csv", [p for p in zip(cpuName, cpuPerf)], fmt="%s", delimiter=';')
