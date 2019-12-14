
from urllib.request import urlopen

html = urlopen("http://ya.ru")
print(html.read())