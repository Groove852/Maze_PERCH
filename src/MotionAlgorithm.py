#!/usr/bin/env python3
import matplotlib
import rospy
import matplotlib.pyplot as plt 
import matplotlib.pyplot as plt1 
import numpy as np

from geometry_msgs.msg import Vector3
from sensor_msgs.msg import LaserScan
from PIDcontroller.PIDAutotune import PIDAutotune as autoPID
from PIDcontroller.PID import PID as mainPID

spdL = 0
spdR = 0


def PID(target, current):
    #auto = autoPID(target, 10, 5, 60, 50, 265)
    #auto.run(current) #0.3 0.1 0.3
    mPID = mainPID(5, 2, 1, 1, 50, 265)
    #mPID = mainPID(5, auto.getKp(), auto.getKi(), auto.getKd(), 50, 265)
    return mPID.calc(current, target)

def scan_callback(msg):
    """rospy.loginfo("90 - " + str(msg.intensities[90])
                    + "(intensities), "
                    + str(msg.ranges[90])
                    + "(ranges).")
    rospy.loginfo("270 - " + str(msg.intensities[270])
                + "(intensities), "
                + str(msg.ranges[270])
                + "(ranges).")"""
    f_max = False
    f_min = False
    middle = 0
    aC = 0 #array counter
    mass=[[-1]*3]*30
    mas=[-1]*30
    #rospy.loginfo(mas) 
    '''
    mass[i][0] - max or min value (1 or 0)
    mass[i][1] - degree of point (gradus)
    mass[i][2] - value of point (range)
'''    '''
    
    #filter
    for i in range(0,360):
        middle += msg.ranges[i]
    middle = middle / 360  
    
    #sorting
    if msg.ranges[359]<msg.ranges[0] or f_max:
        f_max=True
        if msg.ranges[359]>msg.ranges[0]:
            #mass[aC][0]=1 
            #mass[aC][1]=0
            #mass[aC][2]=msg.ranges[359]
            mas[aC]=msg.ranges[359]
            aC+=1
            f_max=False
    
    if msg.ranges[359]>msg.ranges[0] or f_min:
        f_min=True
        if msg.ranges[359]<msg.ranges[0]:
            #mass[aC][0]=0
            #mass[aC][1]=0
            #mass[aC][2]=msg.ranges[359]
            mas[aC]=msg.ranges[359]
            aC+=1
            f_min=False  

    for i in range (0,359):
        if msg.ranges[i-1]<msg.ranges[i] or f_max:
            f_max=True
            if msg.ranges[i-1]>msg.ranges[i]:
                #mass[aC][0]=1 
                #mass[aC][1]=i
                #mass[aC][2]=msg.ranges[i-1]
                mas[aC]=msg.ranges[i-1]
                aC+=1
                f_max=False
        if msg.ranges[i-1]>msg.ranges[0] or f_min:
            f_min=True
            if msg.ranges[i-1]<msg.ranges[0]:
                #mass[aC][0]=0
                #mass[aC][1]=i
                #mass[aC][2]=msg.ranges[i-1]
                mas[aC]=msg.ranges[i-1]
                aC+=1
                f_min=False
    max(mass[1])
'''

    global spdL 
    global spdR
    middleLidarPlank_90_270 = (msg.intensities[90] + msg.intensities[270]) / 2
    spdR = PID(middleLidarPlank_90_270, msg.intensities[90]) 
    spdL = PID(middleLidarPlank_90_270, msg.intensities[270])
    #plt.plot(mas)
    #plt.pause(0.01)
    #plt.show()
    #plt.clf()
    #rospy.logerr(mas)


if __name__ == '__main__':
    rospy.init_node("Motion node")
    #rospy.loginfo("Test node has been started.")

    Publisher_XL430R = rospy.Publisher('/maze_v0.1.1/spdR', Vector3, queue_size=10)
    Publisher_XL430L = rospy.Publisher('/maze_v0.1.1/spdL', Vector3, queue_size=10)

    Subscriber_Scan = rospy.Subscriber("/scan", LaserScan, callback=scan_callback)

    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        
        msg_XL430R = Vector3()
        msg_XL430L = Vector3()
        
        msg_XL430L.y = 1 #ID
        msg_XL430R.y = 2 #ID

        msg_XL430L.x = spdL #spd
        msg_XL430R.x = spdR #spd

        #msg_XL430L.z = IDK
        #msg_XL430L.z = IDK

        rospy.loginfo("left = " + str(msg_XL430L.x))
        rospy.loginfo("right = " + str(msg_XL430R.x))

        Publisher_XL430L.publish(msg_XL430L)
        Publisher_XL430R.publish(msg_XL430R)

        rate.sleep()