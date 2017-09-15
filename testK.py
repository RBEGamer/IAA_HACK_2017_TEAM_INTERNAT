
import numpy as np
import cv2
import sys
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel





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
    depth = frames["depth"]
    di = depth.asarray() / 4500.  # float 0-1

    #print(pos_xa)



    listener.release(frames)



device.stop()
device.close()

sys.exit(0)
