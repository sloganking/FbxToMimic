import numpy as np
import math
import json
import re
import os
from os import listdir
from os.path import isfile, join

def isnumber(x):
    return re.match("-?[0-9]+([.][0-9]+)?$", x) is not None

def depthOf(str):
    depth = 0
    for z in range(0,len(str)):
        if str[z] == "\t":
            depth += 1
        else:
            return depth
    return depth\

def getTabs(str):
    tabs = ""
    for i in range(0,depthOf(str)):
        tabs = tabs + "\t"
    return tabs + "\t"

# Remove all files in "./Utils/Temp/"
mypath = "./Utils/Temp/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for i in range(0,len(onlyfiles)):
    os.remove(f"{mypath}{onlyfiles[i]}")


lastDepth = 0    #initialize depth

from os import listdir
from os.path import isfile, join
mypath = "./InputFbx"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

print(f"Files to Convert: {onlyfiles}")

for j in range(0,len(onlyfiles)):
    print(f"Files Converted to JSON: {j}/{len(onlyfiles)}", end="\r")
    with open(f"./InputFbx/{onlyfiles[j]}") as input:
        with open(f"./Utils/Temp/{onlyfiles[j]}.json","w") as output:

            content = input.readlines()
            
            #Start JSON object
            print(f"{{", file=output)

            # Start of file conversion
            for x in range(0,len(content)):
                tokens = str.split(content[x])
                tabDepth = getTabs(content[x])
                strToPrint = ""
                curToken = 0
                stringLeft = ""

                if len(tokens) > 0:

                    # if first char of first token = ";"
                    if tokens[0][:1] == ";":
                        nonANumber = 1

                    # if last char of line is "{"
                    elif content[x][ len(content[x]) - 2] == "{":
                        stringLeft = ""
                        for i in range(curToken,len(tokens)):
                            if tokens[i] != "{":
                                stringLeft += tokens[i]
                        stringLeft = stringLeft.replace("\"", "")
                        strToPrint += f"\"{stringLeft}\": {{"

                    # if last char of line is "}"
                    elif content[x][ len(content[x]) - 2] == "}":
                        strToPrint += f"}}"

                        #add comma if next depth == curDepth && not already have comma
                        if x < len(content) - 1:
                            if depthOf(content[x]) == depthOf(content[x + 1]):
                                if strToPrint[len(strToPrint) - 1] != ",":
                                    strToPrint += ","
                    
                    #elif first token is property
                    elif tokens[0][ len(tokens[0]) - 1] == ':':

                        # Property is "Key"
                        if tokens[0][:-1] == "Key":
                            strToPrint = "\"Key\": ["

                        # Property is "Color"
                        elif tokens[0][:-1] == "Color":
                            print(f"{tabDepth}],", file=output)
                            strToPrint = "\"Color\": 0"
                        
                        # Property is "ReferenceTime"
                        elif tokens[0][:-1] == "ReferenceTime":
                            strToPrint = "\"ReferenceTime\": \"N/A\","

                        else:
                            #add property to front
                            strToPrint += f"\"{tokens[0][:-1]}\": "
                            curToken += 1
                            stringLeft = ""

                            # Combine rest of tokens into string
                            for i in range(curToken,len(tokens)):
                                stringLeft += tokens[i]
                            stringLeft = stringLeft.replace("\"","\\\"")
                            stringLeft = f"\"{stringLeft}\""
                            strToPrint += stringLeft

                            #add comma if next depth == curDepth && not already have comma
                            if x < len(content) - 1:
                                if depthOf(content[x]) == depthOf(content[x + 1]):
                                    if strToPrint[len(strToPrint) - 1] != ",":
                                        strToPrint += ","

                    # no property on line
                    else:
                        for i in range(curToken,len(tokens)):
                            stringLeft += tokens[i]
                        stringLeft = stringLeft.replace("\"","\\\"")
                        stringLeft = f"\"{stringLeft}\""
                        strToPrint += stringLeft

                        #add comma if next depth == curDepth && not already have comma
                        if x < len(content) - 1:
                            if depthOf(content[x]) == depthOf(content[x + 1]):
                                if strToPrint[len(strToPrint) - 1] != ",":
                                    strToPrint += ","

                #print(strToPrint)
                # If something to print
                if strToPrint != "":
                    strToPrint = f"{tabDepth}{strToPrint}"
                    print(f"{strToPrint}", file=output)

            #End JSON object
            print(f"}}", file=output)