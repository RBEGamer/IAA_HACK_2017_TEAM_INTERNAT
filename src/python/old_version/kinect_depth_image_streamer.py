import cv2
import numpy as np
#import cv2
import sys
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel

import csv

import socket
import sys
import pickle

import struct ## new

import struct ### new code
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('192.168.100.98',8089))

import signal
import sys
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        device.stop()
        device.close()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)






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
# Register listeners
device.setColorFrameListener(listener)
device.setIrAndDepthFrameListener(listener)
device.start()
# NOTE: must be called after device.start()
registration = Registration(device.getIrCameraParams(),device.getColorCameraParams())
undistorted = Frame(512, 424, 4)
registered = Frame(512, 424, 4)



nmax = 10000



while True:
    frames = listener.waitForNewFrame()

    color = frames["color"]
    #ir = frames["ir"]
    depth = frames["depth"]

    #registration.apply(color, depth, undistorted, registered)

    #cv2.imshow("ir", ir.asarray() / 65535.)
    cv2.imshow("depth", depth.asarray() / 4500.)
    #cv2.imshow("undistorted", undistorted.asarray(np.float32) / 4500.)
    #if enable_rgb:
    #    cv2.imshow("color", cv2.resize(color.asarray(),
                                       #(int(1920 / 3), int(1080 / 3))))
#    if enable_rgb and enable_depth:
#        cv2.imshow("registered", registered.asarray(np.uint8))
    ret = 0
    data = pickle.dumps(depth.asarray()) ### new code
    clientsocket.sendall(struct.pack("L", len(data))+data) ### new code
    listener.release(frames)

    key = cv2.waitKey(delay=1)
    if key == ord('q'):
        break


cv2.destroyAllWindows()
device.stop()
device.close()

sys.exit(0)
