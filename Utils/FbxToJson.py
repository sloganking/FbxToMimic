import numpy as np
import math
import json

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

with open("13_29.fbx") as input:
    with open("FbxJson.json","w") as output:

        content = input.readlines()
        
        #Start JSON object
        print(f"{{", file=output)

        # for x in range(0,25):
        #     tabDepth = getTabs(content[x])
        #     tokens = str.split(content[x])
        #     #print(f"Line:{x + 1}    Depth: {depthOf(content[x])}")
        #     for i in range(0,len(tokens)):
        #         if tokens[0][:1] == ";":    # if first char of first token = ";"
        #             break
        #         elif tokens[i][ len(tokens[i]) - 1] == ':':     # if last char of any token = ":"
        #             print(f"{tabDepth}\"{tokens[i][:-1]}\":", file=output)
        #         elif tokens[i] == "{":
        #             print(f"{tabDepth}{{", file=output)
        #         elif tokens[i] == "}":
        #             if depthOf(content[x]) < lastDepth:
        #                 print(f"{tabDepth}}}", file=output)
        #             else:
        #                 print(f"{tabDepth}}},", file=output)
        #         else:
        #             print(f"{tabDepth}{tokens[i]}", file=output)

        #                 #if inProperty and next token is not a property, write a comma, 




        for x in range(0,25):
            tokens = str.split(content[x])
            tabDepth = getTabs(content[x])
            strToPrint = ""

            curToken = 0
            if len(tokens) > 0:
                print(tokens[0])
                if tokens[0][ len(tokens[0]) - 1] == ':':
                    strToPrint += f"\"{tokens[0][:-1]}\": "
                    curToken += 1
            
            for i in range(curToken,len(tokens)):
                if len(tokens) > 0:
                    if tokens[0][:1] == ";":    # if first char of first token = ";"
                        break
                    else:
                        strToPrint += tokens[i]

            # add comma if next depth == curDepth && not already have comma
            if depthOf(content[x]) == depthOf(content[x + 1]):
                if content[x][ len(content[x]) - 1] != ',':
                    strToPrint += ","
            
            if strToPrint != "":
                strToPrint = f"{tabDepth}{strToPrint}"
                print(f"{strToPrint}", file=output)


        #End JSON object
        print(f"}}", file=output)

        print("Conversion completed...")