# IAA_HACK_2017_TEAM_INTERNAT


# THE CHALLANGE
The challange is really simple. Create a system to communicate with the 


# USED HARDWARE
* PC/MAC with USB 3.0
* Kinect V2 with USB cable
* ESP8266
* 8x WS2813 Leds

We had acces to an Nvidia TX2 development board. This board is really small and it fits perfectly to our requirements.
The KinectV2 processing needs a bigger amount of cpu and gpu speed. We have build the libfreenect2 library with cuda support so we can use the advantages of tegra gpu.


# THE LIGHTBAR
For the user notification, we have decided to use some led warning lights.
The requirements for this light is, that the user can be notifiy in different colors and the left and right side should be controlled seperatly. The simplest solution are the WS2812 leds, so its possible control each led with a single dataline.
The controller in our case is the  ESP8266 board. The first idea is to control the lights over a udp/wifi connection.
But we had a time problem, so we used a simple serial connection nad the python-serial package.

# THE GESTURE DETECTION SYSTEM
For the detection system we are using the Kinect V2 camera. The advantage of this camera is, that we receive three video streams from it. A normal color, a nightvision/ir image and the depth image. The Ir image is very clear at night so the system can detect objects and the gestures very well. A depth stream is the second stream we are using to detect the gestures. With the depth image we can filter to near and to far objects from the ir/color image.
The image stream will directly feed into a neural network, which is trained to four gestures.
If a gesture is present in the right area of the image/car the lightbar will receieve a signal to light up.

# THE ADVANCED HUMAN DRIVER WARNING SYSTEM
So after a bit playing around with the KinectV2 image streams, we want to implement a system for the human driver too.


# IBM BLUEMIX WEBUI
In addition to the lightbar, we have build a simple webinterface with the ibm bluemix nodered grafical programming system.
With this system it is possible to show the detected gestures. So we can monitor the system while a test drive.



# USED SOFTWARE
* Python 2.7 
* libfreenect2 (kinect driver)
* pyserial (for the lightbar)
* tensorflow (deep learning framework)


# IMAGES

### DEPTH IMAGE

### HEAT MAP

### GESTURE DETECTION

### LIGHTBAR

