#!/usr/bin/python3

# This script is for copying the files to the current directory from the system.
# The actual path of the original files should be stored in the "path/" subdirectory.
# The name of a file in the "path/" subdirectory matches the copyed file name.

# If run with "install" argument it will copy the files from local directory TO the system.

import os
import sys

# Set current directory
os.chdir(os.path.dirname(sys.argv[0]) )

# Go throu all the files in the path/ subdirectory. 
# Every file in path/ contains the actual path of the orignal file in the system.
for filename in os.listdir('path'):
   with open('path/'+filename, 'r') as fPath:
      filepath = fPath.readline().replace('\n', '').replace('\r', '')
   #print(filepath)
   command = ""
   if len(sys.argv)==1:
      command = "cp " + filepath + " " + filename
   if len(sys.argv)>1 and sys.argv[1] == "install":
      os.system("mkdir -p " + os.path.dirname(filepath))
      command = "cp " + filename + " " + filepath  
   if not command == "":
      print(command)
      try:
         os.system(command)
      except :
         print("error")
#print(sys.argv[0])

