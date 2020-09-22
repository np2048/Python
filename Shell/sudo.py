#!/usr/bin/python3

import os

path = '~/.zshrc'
path = '/etc/sudoers'
command = 'cat ' + path

if not os.access(path, os.W_OK) :
    command = 'sudo ' + command
print(command)
os.system(command)

command = 'cat ' + path
if not os.access(path, os.W_OK) :
    command = 'sudo ' + command
print(command)
os.system(command)
