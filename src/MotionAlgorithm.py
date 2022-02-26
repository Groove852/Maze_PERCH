#!/usr/bin/env python3

import rospy

from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import LaserScan
from PIDcontroller.PIDAutotune import PIDAutotune as autoPID
from PIDcontroller.PID import PID as mainPID

spdL = 0
spdR = 0


def PID(target, current):
    auto = autoPID(target, 10, 5, 60, 0, 265)
    auto.run(current)
    #mPID = mainPID(0.3, 0.3, 0.1, 0.3, 50, 265)
    mPID = mainPID(5, auto.get_pid_parameters()[0], auto.get_pid_parameters()[1], auto.get_pid_parameters()[2], 0, 265)
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
    global spdL
    global spdR
    middleLidarPlank_90_270 = (msg.intensities[90] + msg.intensities[270]) / 2
    spdR = PID(middleLidarPlank_90_270, msg.intensities[90])
    spdL = PID(middleLidarPlank_90_270, msg.intensities[270])


if __name__ == '__main__':
    rospy.init_node("test_node")
    rospy.loginfo("Test node has been started.")

    Publisher_XL430R = rospy.Publisher('/maze_v0.1.1/spdR', Vector3, queue_size=10)
    Publisher_XL430L = rospy.Publisher('/maze_v0.1.1/spdL', Vector3, queue_size=10)

    Subscriber_Scan = rospy.Subscriber("/scan", LaserScan, callback=scan_callback)

    rate = rospy.Rate(10)
    i = 0
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