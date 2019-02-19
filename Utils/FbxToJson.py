import numpy as np
import math
import json
import re

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

lastDepth = 0    #initialize depth

#with open("13_29.fbx") as input:
with open("19_15.fbx") as input:
    with open("FbxJson.json","w") as output:

        content = input.readlines()
        
        #Start JSON object
        print(f"{{", file=output)

        print(f"Content length: {len(content)}")
        # Start of file conversion
        for x in range(0,len(content)):
            tokens = str.split(content[x])
            tabDepth = getTabs(content[x])
            strToPrint = ""
            curToken = 0
            stringLeft = ""

            if len(tokens) > 0:
                if tokens[0][:1] == ";":    # if first char of first token = ";"
                    nonANumber = 1

                elif content[x][ len(content[x]) - 2] == "{":   # if last char of line is "{"
                    stringLeft = ""
                    for i in range(curToken,len(tokens)):
                        if tokens[i] != "{":
                            stringLeft += tokens[i]
                    stringLeft = stringLeft.replace("\"", "")
                    strToPrint += f"\"{stringLeft}\": {{"
                
                elif tokens[0][ len(tokens[0]) - 1] == ':':     #elif first token is property
                    
                    # if len(tokens) < 2:
                    #     strToPrint = "\"BadProperty\": \"none\""

                    if tokens[0][:-1] == "CameraIndexName":
                        strToPrint = "\"CameraIndexName\": \"bad property\""
                    elif tokens[0][:-1] == "Shading":
                        strToPrint = ""
                    elif tokens[0][:-1] == "ReferenceTime":
                        strToPrint = "\"ReferenceTime\": 590797937750,"
                    elif tokens[0][:-1] == "Month":
                        strToPrint = "\"Month\": \"bad property\""
                        #add comma if next depth == curDepth && not already have comma
                        if x < len(content) - 1:
                            if depthOf(content[x]) == depthOf(content[x + 1]):
                                if strToPrint[len(strToPrint) - 1] != ",":
                                    strToPrint += ","

                    elif tokens[0][:-1] == "Key":
                        strToPrint = "\"Key\": ["
                    elif tokens[0][:-1] == "Color":
                        print(f"{tabDepth}],", file=output)
                        strToPrint = "\"Color\": 0"
                    else:
                        #add property to front
                        strToPrint += f"\"{tokens[0][:-1]}\": "
                        curToken += 1
                        stringLeft = ""
                        for i in range(curToken,len(tokens)):       #
                            stringLeft += tokens[i]
                        if len(stringLeft.split(",")) > 1:
                            strToPrint += stringLeft.split(",")[1]
                        else:
                            strToPrint += stringLeft.split(",")[0]

                        #add comma if next depth == curDepth && not already have comma
                        if x < len(content) - 1:
                            if depthOf(content[x]) == depthOf(content[x + 1]):
                                if strToPrint[len(strToPrint) - 1] != ",":
                                    strToPrint += ","

                else:
                    for i in range(curToken,len(tokens)):
                        stringLeft += tokens[i]
                    if len(stringLeft.split(",")) > 1:
                        strToPrint += stringLeft.split(",")[1]
                    else:
                        strToPrint += stringLeft.split(",")[0]

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

        print("Conversion completed...")

#===============================================================================


#if ;, print no line
#elif the last char is "{"
    #concatenate the entire line and make it a property name, 
    # add "{ to the end of the line
#elif first token is property
    # create property name
    # assign value (preference of second commad value)
    # add comma if needed