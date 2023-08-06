#!/usr/bin/env python

import cv2
import numpy as np

import rospy
from cv_bridge import CvBridge

from sensor_msgs.msg import Image
from std_msgs.msg import Int32MultiArray ####

img_msg_update = False

def img_msg_callback(img_msg):
    global imagen
    global img_msg_update
    bridge = CvBridge()
    imagen = bridge.imgmsg_to_cv2(img_msg, desired_encoding="bgr8")
    img_msg_update = True

def build_model(is_cuda):
    #net = cv2.dnn.readNet("path/al/archivo/best.onnx")
    net = cv2.dnn.readNet("/home/puzzlebot/Luis/best.onnx")
    if is_cuda:
        print("Attempt using CUDA")
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
    else:
        print("Running on CPU")
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    return net

INPUT_WIDTH = 640
INPUT_HEIGHT = 640
SCORE_THRESHOLD = 0.2
NMS_THRESHOLD = 0.4
CONFIDENCE_THRESHOLD = 0.4

def detect(image, net):
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (INPUT_WIDTH, INPUT_HEIGHT), swapRB=True, crop=False)
    net.setInput(blob)
    preds = net.forward()
    return preds

# def load_capture():
#     cam_port = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=60/1 ! nvvidconv flip-method=2 ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink drop=true' #flip-method = 2, para voltear la imagen (sino aparece al reves)
#     #cam_port = 1
#     capture = cv2.VideoCapture(cam_port)
#     return capture

class_list = ['forward', 'giveway', 'greenlight', 'left', 'redlight', 'right', 'round', 'stop', 'working', 'yellowlight']
colors = [(255, 0, 0), (0, 0, 125), (0, 255, 0), (255, 125, 125),(0, 0, 255), (255, 200, 200), (238, 174, 245), (0, 0, 200),(0, 0, 125), (245, 227, 66)]

def wrap_detection(input_image, output_data):
    class_ids = []
    confidences = []
    boxes = []

    rows = output_data.shape[0]

    image_width, image_height, _ = input_image.shape

    x_factor = image_width / INPUT_WIDTH
    y_factor =  image_height / INPUT_HEIGHT

    for r in range(rows):
        row = output_data[r] #vector de 15 (0 es x izq, 1 es y top)
        confidence = row[4]
        if confidence >= 0.4:

            classes_scores = row[5:]
            _, _, _, max_indx = cv2.minMaxLoc(classes_scores)
            class_id = max_indx[1]
            if (classes_scores[class_id] > .25):

                confidences.append(confidence)

                class_ids.append(class_id)

                x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item()
                left = int((x - 0.5 * w) * x_factor)
                top = int((y - 0.5 * h) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                box = np.array([left, top, width, height])
                boxes.append(box)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.25, 0.45)

    result_class_ids = []
    result_confidences = []
    result_boxes = []

    for i in indexes:
        result_confidences.append(confidences[i])
        result_class_ids.append(class_ids[i])
        result_boxes.append(boxes[i])

    return result_class_ids, result_confidences, result_boxes

def format_yolov5(frame):
    result = cv2.resize(frame, [640,640], interpolation = cv2.INTER_AREA)
    return result


if __name__=='__main__': 
    rospy.init_node('deteccion')
    rate = rospy.Rate(10) ####

    camPub = rospy.Subscriber("/cam", Image, img_msg_callback)
    arrayPub = rospy.Publisher("/signals", Int32MultiArray, queue_size=10) #####

    array_msg = Int32MultiArray() ##
     ##
    net = build_model(1) #Define si opencv se corre con CUDA o con CPU 0 = CPU, 1 = CUDA

    while not rospy.is_shutdown(): ########

        while not img_msg_update:
            rospy.sleep(0.1)

        if imagen is None:
            print("End of stream")
            break

        inputImage = format_yolov5(imagen)
        outs = detect(inputImage, net)

        class_ids, confidences, boxes = wrap_detection(inputImage, outs[0])

	array_temp = []

        for (classid, confidence, box) in zip(class_ids, confidences, boxes):
            color = colors[int(classid) % len(colors)]
            cv2.rectangle(inputImage, box, color, 2)
            cv2.rectangle(inputImage, (box[0], box[1] - 20), (box[0] + box[2], box[1]), color, -1)
            cv2.putText(inputImage, class_list[classid], (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0))
            
            tam = box[2] * 2 + box[3] * 2##
	    if(classid == 3 or classid == 5 or classid == 0 or classid == 7):
		if(tam > 200):
		    array_temp.append(classid)
            elif(tam > 100): ##
                array_temp.append(classid) ##
                
            
        ## left, top, width, height
        
        array_msg.data = array_temp ##

        arrayPub.publish(array_msg) ##

	print(array_temp)

        #cv2.imshow("output", inputImage)
        
        if cv2.waitKey(1) > -1:
            print("finished by user")
            break
        
    rospy.spin()
