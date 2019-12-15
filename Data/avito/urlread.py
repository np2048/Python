#!/usr/bin/python3

from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://webasyst.ru")
bsObj = BeautifulSoup(html.read(), 'html.parser')
print(bsObj.h1)
