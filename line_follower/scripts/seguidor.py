#!/usr/bin/env python
############ Librerias ###########
import cv2
import numpy as np

import rospy
from cv_bridge import CvBridge

from std_msgs.msg import Float32
from sensor_msgs.msg import Image
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import Twist

signal_msg_update = False
img_msg_update = False
esperari = False
esperard = False
esperarf = False

def signals_callback(signal_msg):
    global signals
    global signal_msg_update

    signals = signal_msg.data
    signal_msg_update = True

def img_msg_callback(img_msg):
    global imagen
    global img_msg_update
    bridge = CvBridge()
    imagen = bridge.imgmsg_to_cv2(img_msg, desired_encoding="bgr8")
    img_msg_update = True


##################################
#//////////////////////////////////////////////#
############################### Ajustar imagen ##############################
def ajustar_imagen(imagen):
    height, width = imagen.shape[:2]
    cut_height = height // 1.6
    cut_width = width * 0.25
    imagen = imagen[int(cut_height):, int(cut_width):int(width-cut_width)]
    return imagen
#############################################################################
#//////////////////////////Medir error trayectoria/////////////////////////////#
###################################################################################
def medir_error_trayectoria(imagen):
    suma = 0
    cantidad = 0

    imagen_suavizada = cv2.blur(imagen, (5, 5))
    imagen_gris = cv2.cvtColor(imagen_suavizada, cv2.COLOR_BGR2GRAY)
    _, imagen_binaria = cv2.threshold(imagen_gris, 127, 255, cv2.THRESH_BINARY)
    # cv2.imshow('Imagen binaria', imagen_binaria)

    for y in range(imagen.shape[1]):
        if imagen_binaria[int(imagen.shape[0]*0.5), y] == 0:
            cantidad += 1
            suma += y

    if cantidad > 0:
        error = suma / cantidad
        return error - imagen.shape[1]*0.5

    return 0
###########################################################################################
#///////////////////////////////////Marcar imagen///////////////////////////////////////###
###########################################################################################
def marcar_imagen(imagen, error_medido):
    centro_error = (int(imagen.shape[1]*0.5) + int(error_medido), int(imagen.shape[0]*0.5))
    centro = (int(imagen.shape[1]*0.5), int(imagen.shape[0]*0.5))
    
    imagen_con_punto = np.copy(imagen)
    cv2.circle(imagen_con_punto, centro_error, 5, (0, 0, 255), -1)
    cv2.circle(imagen_con_punto, centro, 5, (0, 0, 255), -1)
    
    return imagen_con_punto


if __name__=='__main__':   
    rospy.init_node('linefollower')
    rate = rospy.Rate(25)

    tiempo_inicial = rospy.get_time()

    signaldetector = rospy.Subscriber("/signals", Int32MultiArray, signals_callback)
    camPub = rospy.Subscriber("/cam", Image, img_msg_callback)

    velPub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    print("DEBUG")
    while not rospy.is_shutdown():
        while not img_msg_update:
            rospy.sleep(0.1)

        imagen_ajustada = ajustar_imagen(imagen)
        error_medido = medir_error_trayectoria(imagen_ajustada)
        imagen_ajustada = marcar_imagen(imagen_ajustada, error_medido)

	while not signal_msg_update:
	    rospy.sleep(0.1)

	pV = Twist()

        vM = 0.08

        krvM = vM / 1.4
        kvaM = 0.3
        errorM = 300.0
        rv = (krvM * abs(error_medido)) / errorM
        va = (kvaM * error_medido) / errorM

        vl = vM - rv

	tiempo_actual = rospy.get_time() - tiempo_inicial
	if esperarf == True:
	    print("forward")

            print(tiempo_actual, tiempo_inicio)
            if  tiempo_actual >= tiempo_inicio:
                esperarf = False
		rospy.sleep(0.1)
	
	if esperari == True:
	    print("Izquierda")
	    if  tiempo_actual >= tiempo_inicio:
		esperari = False
                pV.linear.x = 0.018
                pV.angular.z = 0.16

                velPub.publish(pV)

                va = 0

                rospy.sleep(10)
                
	if esperard == True:
	    print("Derecha")
            if  tiempo_actual >= tiempo_inicio:
                esperard = False
                pV.linear.x = 0.02
                pV.angular.z = -0.15

                velPub.publish(pV)

                va = 0

                rospy.sleep(10)
                
	if esperard == False and esperari == False and esperarf == False:
	    for signal in signals:
                if signal == 0:
		    tiempo_inicio = tiempo_actual + 10
                    vl *= 1
		    esperarf = True

                elif signal == 1:
                    vl *= 0.5

                elif signal == 2:
                    vl *= 1
            
	        elif signal == 3:
		    tiempo_inicio = tiempo_actual + 5
		    esperari = True

	        elif signal == 4:
		    vl *= 0

	        elif signal == 5:
		    tiempo_inicio = tiempo_actual + 5
		    esperard = True
                elif signal == 6:
                    vl *= 0.5

                elif signal == 7:
                    vl *= 0

                elif signal == 8:
                    vl *= 0.5
	    
	        elif signal == 9:
                    vl *= 0.5

        pV.linear.x = vl
        pV.angular.z = -va


	velPub.publish(pV)

        #cv2.imshow('Imagen con error', imagen_ajustada)
        #cv2.waitKey(1)
        #print("Error medido:", error_medido)
    ###################################################
    rospy.spin()

