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

# IP address of server to send video to
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
    print("Capturing video...")
    cap=cv2.VideoCapture(0)

    print(struct.calcsize("L"))
    # continue to send video till interrupt
    while True:
        # read frame
        ret, frame = cap.read()

        # convert to string
        data = pickle.dumps(frame)

        # send data len then data to client
        print("SENDING FRAME")
        print(struct.pack("L", len(data)))
        clientsocket.sendall(struct.pack("L", len(data)) + data)
        print(hi)

if __name__ == '__main__':
    send_video()
