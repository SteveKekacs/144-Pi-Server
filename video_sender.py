"""
Sends PiCamera video from Rasperry Pi to Remote Server
for Object Detection Processing. On stop command,
stops car.
"""
import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

# to speed things up, lower the resolution of the camera
camera_width = 320
camera_height = 240
#scale_down = 6

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (camera_width, camera_height)
camera.framerate = 32
camera.rotation = 180
rawCapture = PiRGBArray(camera, size=(camera_width, camera_height))

# allow the camera to warmup
time.sleep(0.1)

# IP address of server to send video to
# HOST_IP = '127.0.0.1'
HOST_IP = '10.251.46.150'

# Port to send over
PORT = 8089


def send_video():
    # create socket
    print("Creating socket...")
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created...")

    print("Connecting to %s:%d..." % (HOST_IP, PORT))
    clientsocket.connect((HOST_IP, PORT))
    print("Connected to %s:%d..." % (HOST_IP, PORT))

    # capture video

    # continue to send video till interru
    # capture frames from the camera
    num = 1
    for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        print('got img %d' % num)
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        frame = image.array
        #frame = cv2.GaussianBlur(frame, (15,15), 0)

        # convert to string
        data = pickle.dumps(frame)
        print('got data (%d) %d' % (len(data), num))
        msg_size = struct.pack("<L", len(data))
        print('packed struct %d' % num)
        # send data len then data to client
        clientsocket.sendall(msg_size + data)
        print('sent data %d' % num)
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        print('cleared capture %d\n\n' % num)
        num += 1

if __name__ == '__main__':
    send_video()
