#!/usr/bin/python3
import os
import sys
import shutil

# define colors for output
CRED = '\033[91m'
CGREEN = '\033[92m'
CEND = '\033[0m'
#print(CRED + "Error, does not compute!" + CEND)

# try to install 1 test file

# Goto main script directory
#os.chdir( os.path.dirname(os.path.dirname( os.path.abspath( sys.argv[0] ))) )

# remove target directory if exists
target = "target"
if os.path.exists("../" + target + "/"):
   shutil.rmtree("../" + target + "/")

# create test file
fileName = "test1"
fileContent = "test1content"
os.system("./addFile.py " + fileName + " " + fileContent)

# run INSTALL
os.system("../refresh.py install")

# return error if target directory not created
if not os.path.exists("../" + target + "/"):
   print(CRED + "No target directory" + CEND)
   exit()

# return error if no file1 int the target directory
if not os.path.exists("../" + target + "/" + fileName):
   print(CRED + "File not installed" + CEND)
   exit()

# return error if targer file content doesn't match
targetFileContent=""
with open("../" + target + "/" + fileName, "r") as f :
   targetFileContent = f.read()
if not targetFileContent == fileContent :
   print(CRED + "File content doesn't match the target" + CEND)
   exit()

print(CGREEN + sys.argv[0] + " OK" + CEND)
