#!/usr/bin/env python
import rospy

from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32MultiArray

signal_msg_update = False

def vel_callback(vel_msg):
    global vel
    vel = Twist()
    vel = vel_msg

def signals_callback(signal_msg):
    global signals
    global signal_msg_update

    signals = Int32MultiArray()

    signals.data = signal_msg.data
    signal_msg_update = True

if __name__=='__main__':
    #Initialise and Setup node
    rospy.init_node("controller")
    rate = rospy.Rate(25)

    #Setup Publishers and subscribers here
    signaldetector = rospy.Subscriber("/signals", Int32MultiArray, signals_callback)
    controller = rospy.Subscriber("/cmd_vel", Twist, vel_callback)

    pV = Twist()

    while not rospy.is_shutdown():

        while not signal_msg_update:
            rospy.sleep(0.1)
	
	vl = vel.linear.x
        """
        vsenial = 0
        for signal in signals.data:
            
            if signal == "forward":
                vsenial += 0

            elif signal == "giveway":
                vsenial += vl * 0.3

            elif signal == "greenlight":
                vsenial += 0

            elif signal == "left":
                pV.linear.x = 0.02
                pV.angular.z = 0.08
                controller.publish(pV)

                vsenial = 0
                va = 0

                rospy.sleep(5)
                break

            elif signal == "redlight":
                vsenial += vl * 1
                
            elif signal == "right":
                pV.linear.x = 0.02
                pV.angular.z = -0.08
                controller.publish(pV)

                vsenial = 0
                va = 0

                rospy.sleep(5)
                break

            elif signal == "round":
                vsenial = vl * 0.2

            elif signal == "stop":
                vsenial += vl * 1

            elif signal == "working":
                vsenial += vl * 0.3

            elif signal == "yellowlight":
                vsenial += vl * 0.5

        if(vsenial > vl): vsenial = vl

        vl -= vsenial
	"""
        pV.linear.x = vl
        pV.angular.z = -va
        
        controller.publish(pV)

    rospy.spin()
