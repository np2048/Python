#!/usr/bin/python3

def writeCsv(items, fileName, append=False):
    fileOpenMode = 'w' 
    if append : fileOpenMode = 'a' 
    file = open(fileName, fileOpenMode)
    for item in items:
        file.write(';'.join(item).replace('\n', '') + '\n')
    file.close()

def readCsv(fileName):
    data = []
    file = open(fileName, "r")
    lines = file.readlines()
    file.close()
    for line in lines:
        data.append(line.split(';'))
    return(data)
