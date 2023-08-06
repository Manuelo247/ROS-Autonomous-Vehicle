#!/usr/bin/env python

import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2

img_msg_update = False

def img_msg_callback(img_msg):
    global imagen
    global img_msg_update
    bridge = CvBridge()
    imagen = bridge.imgmsg_to_cv2(img_msg, desired_encoding="bgr8")
    img_msg_update = True


if __name__ == '__main__':
    rospy.init_node('visualizador')
    rospy.Subscriber("/cam", Image, img_msg_callback)

    while not img_msg_update:
        rospy.sleep(0.1)

    while not rospy.is_shutdown():
        cv2.imshow("Imagen recibida", imagen)
        cv2.waitKey(1)

    rospy.spin()
