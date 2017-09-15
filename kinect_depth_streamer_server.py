
# coding: utf-8

# In[68]:

import cv2
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
#import glob
#from mpl_toolkits.mplot3d import Axes3D
#from skimage.feature import hog
#from sklearn.preprocessing import StandardScaler
#from sklearn.svm import LinearSVC
#get_ipython().magic('matplotlib inline')
from random import shuffle

import pickle
import struct ## new
import socket
import sys

# In[69]:

# Define a Matrix

matrix = np.random.random((424, 512))


# In[106]:

#Size of the resulting matrix
x_size = 50
y_size = 40

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


'''
def draw_boxes(img, bboxes, color=(0, 255, 255), thick=6, random_color=False):
    #Make a copy of the image
    imcopy = np.copy(img)
    #Iterate through the bounding boxes
    for bbox in bboxes:
        #Use different colors so we can appreciate overlap
        if random_color == True:
            color = (np.random.randint(0, 255), np.random.randint(0,255), np.random.randint(0,255))
        #Draw a rectangle given bbox coordinates
        cv2.rectangle(imcopy, bbox[0], bbox[1], color, thick)

    return imcopy


test_image = mpimg.imread('test_images/test4.jpg')

windows = slide_window(test_image, x_start_stop=[None, None],
                       y_start_stop=[400, 656], xy_window= (64, 64),
                      xy_overlap=(0.5, 0.5))

windows_img = draw_boxes(test_image, windows, random_color=True)
plt.imshow(windows_img)
#matplotlib.rc('xtick', labelsize=15)
#matplotlib.rc('ytick', labelsize=15)
plt.title('Sliding Windows Technique:', fontsize=15);
plt.savefig('output_image/sliding_windows.png', bbox_inches="tight")
'''





# SERVER SETUP
HOST=''
PORT=8089
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print 'Socket created'
s.bind((HOST,PORT))
print 'Socket bind complete'
s.listen(10)
print 'Socket now listening'
conn,addr=s.accept()



### new
data = ""
payload_size = struct.calcsize("L")
print(payload_size)

# In[107]:




# In[109]:

#Iterate over the windows list

#For every square



while True:
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame_raw_depth=pickle.loads(frame_data)
    frame_normalizes_depth = frame_raw_depth / 4500.




    windows_list = slide_window(matrix)

    x_coord = 0
    y_coord = 0
    y_size = 10
    x_size = 10

    min_matrix = np.zeros((y_size, x_size))
    max_matrix = np.zeros((y_size, x_size))
    mean_matrix = np.zeros((y_size, x_size))




# In[108]:
    print(len(windows_list))
    print(windows_list[0][0])

    for x in windows_list:

    #extract =  matrix[x[0][0]:x[1][0], x[0][1]:x[1][1]]
        extract = frame_raw_depth[x[0][1]:x[1][1], x[0][0]:x[1][0]]
        print(extract)
    #print(extract.shape)
        min_matrix[x_coord, y_coord] = np.amin(extract)
        max_matrix[x_coord, y_coord] = np.amax(extract)
        mean_matrix[x_coord, y_coord] = np.mean(extract)

        if y_coord < (y_size-1):
            y_coord = y_coord + 1
            print("Coordinate y is: ", y_coord)
        else:
            y_coord = 0
            x_coord = x_coord + 1
            print("Coordinate x is: ", x_coord)

            print(min_matrix.shape)
#print(min_matrix)
    print(min_matrix)

    cv2.imshow('frame',cv2.resize(min_matrix,(1000,1000)))
# add this
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# In[ ]:
