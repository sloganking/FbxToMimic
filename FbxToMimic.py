import numpy as np
import math
import json

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

with open('./rThigh.json') as json_data:
    d = json.load(json_data)

    with open("Output.txt","w") as output:

        #File Header
        print(f"{{", file=output)
        print(f"\"Loop\": \"none\",", file=output)
        print(f"\"Frames\":", file=output)
        print(f"[", file=output)

        #Start of Keyframes
        numFrames = 900
        for i in range(0,numFrames):
            if i < (numFrames - 1):     # put comma at end of all arrays except last one (JSON format)
                ending = ","
            else:
                ending = ""
            quat = euler_to_quaternion(math.radians(-d["Z"][(2*i)+1]), math.radians(-d["Y"][(2*i)+1]), math.radians(-d["X"][(2*i)+1]))
            print(f"[0.0333320000,0.0000000000,0.8475320000,0.0000000000,0.9986780000,0.0141040000,-0.0006980000,-0.0494230000,0.9988130000,0.0094850000,-0.0475600000,-0.0044750000,1.0000000000,0.0000000000,0.0000000000,0.0000000000,{quat[0]},{quat[1]},{quat[2]},{quat[3]},-0.2491160000,0.9993660000,0.0099520000,0.0326540000,0.0100980000,0.9854980000,-0.0644070000,0.0932430000,-0.1262970000,0.1705710000,0.9927550000,-0.0209010000,0.0888240000,-0.0781780000,-0.3915320000,0.9828790000,0.1013910000,-0.0551600000,0.1436190000,0.9659420000,0.1884590000,-0.1422460000,0.1058540000,0.5813480000]{ending}", file=output)

        #Closing up file
        print(f"]", file=output)
        print(f"}}", file=output)

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

        animated = ["Seconds", "Model:Model::hip", "Model:Model::hip", "Model:Model::chest","Model:Model::neck","Model:Model::rThigh","Model:Model::rShin","Model:Model::rFoot","Model:Model::rShldr","Model:Model::rForeArm","Model:Model::lThigh","Model:Model::lShin","Model:Model::lFoot","Model:Model::lShldr,Limb","Model:Model::lForeArm,Limb"]

        dimensions = [1,3,4,4,4,4,1,4,4,1,4,1,4,4,1]

        for i in range(0,len(Docs)):
            print(f"DocWants: {Docs[i]}     dimensions: {dimensions[i]}     JSON: {animated[i]}")