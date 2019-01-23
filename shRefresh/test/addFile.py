#!/usr/bin/python3
import os
import sys

# create a test file for shRefresh script.
# Usage:
#  ./addFile.py fileName fileContents


# Goto main script directory
os.chdir( os.path.dirname(os.path.dirname( os.path.abspath( sys.argv[0] ))) )

# Overwrite test file contents if exists or create new file else
fileName = sys.argv[1]
fileContent = sys.argv[2]
with open(fileName, "w") as f:
   f.write(fileContent)

# Create path directory if not exists
if not os.path.exists("path/"):
   os.mkdir("path")

# Create path file
with open("path/" + fileName, "w") as f:
   f.write("target/" + fileName)
