import numpy as np
import math
import json

with open("13_29.fbx") as input:
    with open("FbxJson.json","w") as output:

        content = input.readlines()
        
        #Start JSON object
        print(f"{{", file=output)

        for x in range(0,25):
            tokens = str.split(content[x])
            if content[x][0] == "\t":
                print(f"Tab found on line: {x + 1}")
            for i in range(0,len(tokens)):
                if tokens[0][:1] == ";":    # if first char of first token = ";"
                    break
                elif tokens[i][ len(tokens[i]) - 1] == ':':     # if last char of any token = ":"
                    print(f"\"{tokens[i][:-1]}\":", file=output)
                elif tokens[i] == "{":
                    print(f"{{", file=output)
                elif tokens[i] == "}":
                    print(f"}}", file=output)


                        #if inProperty and next token is not a property, write a comma, 
        

        #End JSON object
        print(f"}}", file=output)

        print("Conversion completed...")