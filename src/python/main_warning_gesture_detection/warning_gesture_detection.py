
# coding: utf-8
import sys
import serial
import signal
import thread
import time

import cv2
import numpy as np
import tensorflow as tf

from random import shuffle

from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel

import urllib2


### WORKING VARS
matrix = np.random.random((424, 512))
x_size = 50 #set heatmap size here the default values are very fine
y_size = 40
lastsum = -1

#SERIAL SETUP
ser = serial.Serial(
    port='/dev/cu.SLAB_USBtoUART',  #SETUP YOUR DEVICE FILE HERE
    baudrate=115200,                #SETUP BAUD RATE
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.open()
if not ser.isOpen():
    print("cant open serial terminal")
    sys.exit(0)

#REG SINGAL HANDLER
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        ws.close()
        device.stop()
        device.close()
        ser.close()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#########  TF SETUP AND LOAD MODEL #########
labels = [line.rstrip() for line in tf.gfile.GFile("./retrained_labels.txt")]
with tf.gfile.FastGFile("./retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')
_session = tf.Session()

######## SETUP KINECT #########
try:
    from pylibfreenect2 import OpenGLPacketPipeline
    pipeline = OpenGLPacketPipeline()
except:
    from pylibfreenect2 import CpuPacketPipeline
    pipeline = CpuPacketPipeline()
print("Packet pipeline:", type(pipeline).__name__)
# Create and set logger
logger = createConsoleLogger(LoggerLevel.Error)
setGlobalLogger(logger)
fn = Freenect2()
num_devices = fn.enumerateDevices()
if num_devices == 0:
    print("No device connected!")
    sys.exit(1)
serial = fn.getDeviceSerialNumber(0)
device = fn.openDevice(serial, pipeline=pipeline)
listener = SyncMultiFrameListener(FrameType.Color | FrameType.Ir | FrameType.Depth)
device.setColorFrameListener(listener)
device.setIrAndDepthFrameListener(listener)
device.start()
registration = Registration(device.getIrCameraParams(),device.getColorCameraParams())
undistorted = Frame(512, 424, 4)
registered = Frame(512, 424, 4)

##################### DEPTH HEATMAP ALGORYTHM #########################################
def slide_window(img, x_start_stop=[None, None], y_start_stop=[None, None], xy_window=(x_size, y_size), xy_overlap=(0, 0)):
    if x_start_stop[0] == None:
        x_start_stop[0] = 0
    if x_start_stop[1] == None:
        x_start_stop[1] = img.shape[1]
    if y_start_stop[0] == None:
        y_start_stop[0] = 0
    if y_start_stop[1] == None:
        y_start_stop[1] = img.shape[0]
    #Compute the span of the region to be searched
    xspan = x_start_stop[1] - x_start_stop[0]
    yspan = y_start_stop[1] - y_start_stop[0]
    # Compute the number of pixels per step in x/y
    nx_pix_per_step = np.int(xy_window[0]*(1 - xy_overlap[0]))
    ny_pix_per_step = np.int(xy_window[1]*(1 - xy_overlap[1]))
    #Compute the number of pixels per step in x/y
    nx_buffer = np.int(xy_window[0]*(xy_overlap[0]))
    ny_buffer = np.int(xy_window[1]*(xy_overlap[1]))
    nx_windows = np.int((xspan-nx_buffer)/nx_pix_per_step)
    ny_windows = np.int((yspan-ny_buffer)/ny_pix_per_step)
    # Initialize a list to append window positions to
    window_list = []
    # Loop through finding x and y window positions
    # Note: you could vectorize this step, but in practice
    # you'll be considering windows one by one with your
    # classifier, so looping makes sense
    for ys in range(ny_windows):
        for xs in range(nx_windows):
            # Calculate window position
            startx = xs*nx_pix_per_step + x_start_stop[0]
            endx = startx + xy_window[0]
            starty = ys*ny_pix_per_step + y_start_stop[0]
            endy = starty + xy_window[1]
            # Append window position to list
            window_list.append(((startx, starty), (endx, endy)))
    # Return the list of windows
    return window_list
##################### DEPTH HEATMAP ALGORYTHM END #########################################



while True:
######## GET FRAME FROM KINECT #############################
    frames = listener.waitForNewFrame()
    color = frames["color"]
    depth = frames["depth"]
    cv2.imshow("depth", depth.asarray() / 4500.)
    registration.apply(color, depth, undistorted, registered)
############# MAKE PREDICTION ############
    predicted_data_image = cv2.imdecode( color.asarray(), cv2.IMREAD_COLOR)
    softmax_tensor = _session.graph.get_tensor_by_name('final_result:0')
    predictions = _session.run(softmax_tensor,{'DecodeJpeg/contents:0': image_data})
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

    fontFace = cv2.FONT_HERSHEY_DUPLEX
    fontScale = 0.6
    thickness = 1
    old = 0

    for node_id in top_k:
        human_string = self.labels[node_id]
        score = predictions[0][node_id]
        answer = '%s (p = %.4f)' % (human_string, score)
        textSize = cv2.getTextSize(answer, fontFace, fontScale, thickness)
        img_height, img_width = cv_image.shape[:2]
        old += textSize[0][1] + 4
        textOrg = ((img_width - textSize[0][0]), old)
        predicted_data_image = cv2.putText(cv_image, answer, textOrg, fontFace, fontScale, (0,0,0), thickness, 8)

###### SPLIT DEPTH IMAGE INTO A 10by10 HEATMAP ###############
    windows_list = slide_window(matrix)
    x_coord = 0
    y_coord = 0
    y_size = 10
    x_size = 10
    min_matrix = np.zeros((y_size, x_size))
    max_matrix = np.zeros((y_size, x_size))
    mean_matrix = np.zeros((y_size, x_size))
    for x in windows_list:
        extract = depth.asarray()[x[0][1]:x[1][1], x[0][0]:x[1][0]]
        min_matrix[x_coord, y_coord] = np.amin(extract)
        max_matrix[x_coord, y_coord] = np.amax(extract)
        mean_matrix[x_coord, y_coord] = np.mean(extract)
        if y_coord < (y_size-1):
            y_coord = y_coord + 1
        else:
            y_coord = 0
            x_coord = x_coord + 1

###### GET HEAT VALUES SUM UP REGIONS ###############
    left_flag = 0
    middle_flag = 0
    right_flag = 0
    for x in range(3):
        for y in range(y_size):
            if min_matrix[y][x]>100:
                if min_matrix[y][x]<800:
                    left_flag = left_flag +1
    for x in range(3,7):
        for y in range(y_size):
            if min_matrix[y][x]>100:
                if min_matrix[y][x]<800:
                    middle_flag = middle_flag +1
    for x in range(7, 10):
        for y in range(y_size):
            if min_matrix[y][x]>100:
                if min_matrix[y][x]<800:
                    right_flag = right_flag +1

##### UPDATE THE LIGHTBAR COLOR TO NOTIFIY THE DRIVER ##################
    v1 = 0 #blue 1= green 2= yellow 3 = red
    v2 = 0
    if left_flag > 8:
        v1 = 3
        left_flag = 0
    elif left_flag >5:
        #print("There is something in the left")
        v1 = 2 #yellow 3 red 1 green
        left_flag=0
    if middle_flag > 9:
        v1 = 3
        v2 = 3
    elif middle_flag >6:
        #print("There is something in the middle")
        v1 = 2
        v2 = 2
        middle_flag=0
    if right_flag >8:
        v2 = 3
        right_flag=0
    elif right_flag >5:
        #print("There is something in the right")
        v2 = 2
        right_flag=0
    _sum = v1+v2
    # send only a update if changed
    if not _sum == lastsum:
        lastsum = _sum
        #SEND SERIAL COLOR DATA
        ser.write(str(v2) + "_" +str(v1) + "_\n")
        # UPDATE BLUEMIX REDNODE APP
        response = urllib2.urlopen("http://iaahakers.mybluemix.net/main?query="+str(np.mean(min_matrix)))


    # SHOW RESULTS
    heatmap_depth_combined = 0.1 * cv2.resize(min_matrix / 100,(512,424)) + 0.8* cv2.resize(depth.asarray(np.uint8),(512,424))
    cv2.imshow('HEATMAP_IMAGE',cv2.resize(heatmap_depth_combined,(1024,1024)))
    cv2.imshow('PREDICITON_IMAGE',cv2.resize(predicted_data_image,(1024,1024)))


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #FREE FRAMES
    listener.release(frames)
