import numpy as np
import math
import rospy as tf

def euler_to_quaternion(roll, pitch, yaw):  # X Y Z
    quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)

    qx = quaternion[0]
    qy = quaternion[1]
    qz = quaternion[2]
    qw = quaternion[0]

    return [qw,qx,qy,qz]




 
X = 57
Y = 57
Z = 57

print("X: ", X)
print("Y: ", Y)
print("Z: ", Z)

X = math.radians(X)
Y = math.radians(Y)
Z = math.radians(Z)

quat = euler_to_quaternion(X,Y,Z)
print("Qw:", quat[0], "Qx: ", quat[1], "Qy: ", quat[2], "Qz: ", quat[3],)
