#!/usr/bin/python2

# import
import re

# settings
Settings = {
        "decimal_separator" : "\.",
        "exp_separator" : "[eE]",
        "":"" }

while (True) :
    input_string = raw_input("> ")
    #reNum = re.compile("[-+]?\d+" + Settings["decimal_separator"]+"?" + "\d*" + 
    #        Settings["exp_separator"]+"?"+ "[-+]?\d*") 
    num = None
    #if (reNum.match(input_string)):
    try:
        num = float(input_string)
    except:
        num = ""
    if (num) : print(num)

