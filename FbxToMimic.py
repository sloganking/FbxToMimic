import numpy as np
import math
import json

# Function declarations
def euler_to_quaternion(roll, pitch, yaw):

    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)

    return [qw, qx, qy, qz]

def quaternion_to_euler(x, y, z, w):

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    X = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    Y = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    Z = math.atan2(t3, t4)

    return X, Y, Z

# Initilize variables
Docs = [
"duration of frame in seconds (1D)",
"root position (3D)",
"root rotation (4D)",
"chest rotation (4D)",
"neck rotation (4D)",
"right hip rotation (4D)",
"right knee rotation (1D)",
"right ankle rotation (4D)",
"right shoulder rotation (4D)",
"right elbow rotation (1D)",
"left hip rotation (4D)",
"left knee rotation (1D)",
"left ankle rotation (4D)",
"left shoulder rotation (4D)",
"left elbow rotation (1D)"
]
animated = ["Seconds", "Model:Model::hip", "Model:Model::hip", "Model:Model::chest","Model:Model::neck","Model:Model::rThigh","Model:Model::rShin","Model:Model::rFoot","Model:Model::rShldr","Model:Model::rForeArm","Model:Model::lThigh","Model:Model::lShin","Model:Model::lFoot","Model:Model::lShldr","Model:Model::lForeArm"]
dimensions = [1,3,4,4,4,4,1,4,4,1,4,1,4,4,1]

# Open files, Start of main program
with open('./FbxJson.json') as json_data:
    with open("Output.txt","w") as output:
        d = json.load(json_data)

        #File Header
        print(f"{{", file=output)
        print(f"\"Loop\": \"none\",", file=output)
        print(f"\"Frames\":", file=output)
        print(f"[", file=output)

        #Start of Keyframes
        numFrames = d["Takes:"]["Take:19_15"]["Model:Model::hip"]["Channel:Transform"]["Channel:T"]["Channel:X"]["KeyCount"]
        print(f"Numframes: {numFrames}")
        for i in range(0,numFrames):
            keyFrame = "["
            for x in range(0,len(Docs)):
                if x == 0:
                    keyFrame += "0.0333320000"
                elif x == 1:
                    keyFrame += ","
                    keyFrame += str(d["Takes:"]["Take:19_15"]["Model:Model::hip"]["Channel:Transform"]["Channel:T"]["Channel:X"]["Key"][i]) 
                    keyFrame += ","
                    keyFrame += str(d["Takes:"]["Take:19_15"]["Model:Model::hip"]["Channel:Transform"]["Channel:T"]["Channel:Y"]["Key"][i]) 
                    keyFrame += ","
                    keyFrame += str(d["Takes:"]["Take:19_15"]["Model:Model::hip"]["Channel:Transform"]["Channel:T"]["Channel:Z"]["Key"][i]) 
                else:
                    if dimensions[x] == 4:
                        Z = d["Takes:"]["Take:19_15"][animated[x]]["Channel:Transform"]["Channel:R"]["Channel:Z"]["Key"][i]
                        Y = d["Takes:"]["Take:19_15"][animated[x]]["Channel:Transform"]["Channel:R"]["Channel:Y"]["Key"][i]
                        X = d["Takes:"]["Take:19_15"][animated[x]]["Channel:Transform"]["Channel:R"]["Channel:X"]["Key"][i]
                        quat = euler_to_quaternion(math.radians(-Z), math.radians(-Y), math.radians(-X))
                        keyFrame += f"{quat[0]},{quat[1]},{quat[2]},{quat[3]}"
                    
            #closing keyframe
            keyFrame += "]"
            if i < (numFrames - 1):     # put comma at end of all arrays except last one (JSON format)
                keyFrame += ","
            else:
                keyFrame += ""

            # Write keyFrame to file
            print(f"{keyFrame}", file=output)

        #Closing up file
        print(f"]", file=output)
        print(f"}}", file=output)

       

        # for i in range(0,len(Docs)):
        #     print(f"DocWants: {Docs[i]}     dimensions: {dimensions[i]}     JSON: {animated[i]}")