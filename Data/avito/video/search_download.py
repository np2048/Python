#!/usr/bin/python3

from urllib.request import urlopen
from bs4 import BeautifulSoup

searchUrl = "https://www.avito.ru/krasnodar/tovary_dlya_kompyutera/komplektuyuschie/videokarty?cd=1&pmax=6000&pmin=1000"
html = urlopen(searchUrl)
bsSearch = BeautifulSoup(html.read(), "html.parser")
bsPages = bsSearch.findAll("span", class_="pagination-item-1WyVp")
for bsPage in bsPages :
    print (bsPage.text)
