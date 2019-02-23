#!/usr/bin/python3

import socket
from jinja2 import Template

def ProcessTemplate(FilePath):
    hostname = socket.gethostname()
    FileContents = ''
    with open(FilePath, 'r') as hFile:
        FileContents = hFile.read()
    template = Template(FileContents)
    return template.render(device=hostname)

print(ProcessTemplate('config.txt') )
