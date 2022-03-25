#!/usr/bin/env python3 
import rospy 

from geometry_msgs.msg import Vector3
from std_msgs.msg import Int32
from sensor_msgs.msg import LaserScan, Temperature, BatteryState

from Helpers.MotionAlgorithmD import Algorithm as algD
from Helpers.MotionAlgorithmS import Chanks as algS

#ты лох

chanksAlg = algS(2, 0, 0)
simpleAlg = algD()

def scan_callback(msg):
    simpleAlg.launch(msg.ranges)

    #chanksAlg.setScanArray(msg.ranges)
    #chanksAlg.calculate()

def temp_callback(msg):
    return

def battery_callback(msg):
    return

def main():
    rospy.init_node("MotionNode")

    Publisher_XL430R = rospy.Publisher('/maze_v0.1.1_spdR', Int32, queue_size=10)
    Publisher_XL430L = rospy.Publisher('/maze_v0.1.1_spdL', Int32, queue_size=10)

    #Subscriber_Battery = rospy.Subscriber("/OpenCR/battery", BatteryState, callback=battery_callback)
    #Subscriber_Temp = rospy.Subscriber("/OpenCR/temp", Temperature, callback=temp_callback)
    Subscriber_Scan = rospy.Subscriber("/scan", LaserScan, callback=scan_callback)
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        msg_XL430R = Int32
        msg_XL430L = Int32

        #msg_XL430L.y, msg_XL430R.y = 1, 2 # ID
        #msg_XL430L.x, msg_XL430R.x = chanksAlg.getSpeed() # Speed

        msg_XL430L, msg_XL430R = simpleAlg.getSpeed() 
        # msg_XL430L, msg_XL430R = chanksAlg.getSpeed() # Speed
        # msg_XL430L.z = IDK
        # msg_XL430L.z = IDK
        rospy.loginfo("left = " + str(msg_XL430L))
        rospy.loginfo("right = " + str(msg_XL430R))
        # msg_XL430L = 0
        # msg_XL430R = 0
        Publisher_XL430L.publish(msg_XL430L)
        Publisher_XL430R.publish(msg_XL430R)
        rate.sleep()
        


if __name__ == '__main__':
    main()

