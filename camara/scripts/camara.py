#!/usr/bin/env python
import cv2

import rospy
from cv_bridge import CvBridge

from sensor_msgs.msg import Image

if __name__=='__main__':   
    rospy.init_node('camara')
    rate = rospy.Rate(30)

    cam_port = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=60/1 ! nvvidconv flip-method=2 ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink drop=true' #flip-method = 2, para voltear la imagen (sino aparece al reves)

    # cap = cv2.VideoCapture("/home/manuelo247/catkin_ws/src/line_follower/test/ruta1.mp4")
    cap = cv2.VideoCapture(cam_port)     

    if not cap.isOpened():
        print("No se pudo abrir la webcam")
        exit()

    camPub = rospy.Publisher("/cam", Image, queue_size=10)

    bridge = CvBridge()

    while not rospy.is_shutdown():
        ret, imagen = cap.read()

        if ret:
            img_msg = bridge.cv2_to_imgmsg(imagen, encoding="bgr8")
            camPub.publish(img_msg)

        else:
            break

    cap.release()

