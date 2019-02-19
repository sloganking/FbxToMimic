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


#testArray = [0.0333320000,36.15644073486328,-47.417903900146484,85.23808288574219,0.3971598881909073,0.5099391074318974,0.480307113544098,-0.5929006717846446,0.9966937693208409,-0.009270758600407925,-0.08061328608623314,-0.004132957580995251,0.9762827643890308,-0.004823241112406072,0.21512515649144553,0.023871894491532812,0.8597030441519741,-0.02268270406528398,-0.5101677945166531,0.011179993297387319,,0.5423884150909892,-0.5203643724543552,-0.3936015867163114,-0.5292575157611576,0.6895779674684611,-0.59665797880739,-0.0641166349016439,0.40542636845231883,,0.8833189395857082,0.020719764882733457,-0.46808997756702864,-0.014495351450821741,,-0.5871534730758694,-0.45218121382303167,0.4915286921865896,-0.45736472719025345,0.6805606196020912,0.5905061544837423,-0.05552285114231231,-0.43018244683467627]

#print(f"Length of testArray:    {len(testArray)}")

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
        numFrames = numFrames - 20
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
                        keyFrame += f",{quat[0]},{quat[1]},{quat[2]},{quat[3]}"
                    elif dimensions[x] == 1:
                        if animated[x] == "Model:Model::rForeArm" or animated[x] == "Model:Model::lForeArm":
                            keyFrame += ","
                            keyFrame += str(math.radians(d["Takes:"]["Take:19_15"][animated[x]]["Channel:Transform"]["Channel:R"]["Channel:Z"]["Key"][i]))
                        elif animated[x] == "Model:Model::rShin" or animated[x] == "Model:Model::lShin":
                            keyFrame += ","
                            keyFrame += str(math.radians(d["Takes:"]["Take:19_15"][animated[x]]["Channel:Transform"]["Channel:R"]["Channel:Z"]["Key"][i]))

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