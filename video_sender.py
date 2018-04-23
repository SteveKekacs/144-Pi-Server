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
import thread
import directions as car
from picamera.array import PiRGBArray
from picamera import PiCamera

# to speed things up, lower the resolution of the camera
camera_width = 320
camera_height = 240

# IP address of server to send video to
# HOST_IP = '127.0.0.1'
HOST_IP = '10.251.46.150'

# Ports to send over
VIDEO_PORT = 8089
COMMAND_PORT = 8989


def recv_stop_command():
    """
    Waits to receive stop command from server,
    signals car to stop.

    """
    print("Creating socket to receive stop command...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket for receiving stop command created...")

    # bind to host
    print("Binding to port %d..." % PORT)
    sock.bind(('', PORT))

    # listen and accept connection
    sock.listen(10)
    print("Socket for receiving stop command is listening...")

    conn, (_, addr) = sock.accept()
    print("Established connection with %s for receiving stop command" % addr)

    # once message recieved stop car
    conn.recv(1024)
    car.stop() 


def send_video(protocol):
    """
    Sends video to server over given protocol,
    starts thread to receive stop command once 
    stop sign is detected.
    """

    # create socket
    # get socket type based on protocol
    socket_type = socket.SOCK_STREAM
    if protocol == 'UDP':
        socket_type = socket.SOCK_DGRAM

    print("Creating %s socket..." % protocol)
    clientsocket = socket.socket(socket.AF_INET, socket_type)
    print("%s Socket created..." % protocol)

    if protocol == 'TCP':
        print("Connecting to %s:%d..." % (HOST_IP, VIDEO_PORT))
        clientsocket.connect((HOST_IP, VIDEO_PORT))
        print("Connected to %s:%d..." % (HOST_IP, VIDEO_PORT))

    # initialize the camera and grab a reference to the raw camera capture
    print("Initializing Camera...")
    camera = PiCamera()
    camera.resolution = (camera_width, camera_height)
    camera.framerate = 32
    camera.rotation = 180
    rawCapture = PiRGBArray(camera, size=(camera_width, camera_height))

    # allow the camera to warmup
    time.sleep(0.1)
    print("Camera ready...")

    # start a thread to receive stop command
    thread.start_new_thread(recv_stop_command, ())

    # continue to capture frames from camera and
    # send to remote server till interrupt
    for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        frame = image.array

        # convert to string
        data = pickle.dumps(frame)

        # pack message size into struct
        msg_size = struct.pack("<L", len(data))

        # send data len then data to client
        if protocol == 'TCP':
            clientsocket.sendall(msg_size + data)
        else:
            clientsocket.sendto(msg_size + data, (HOST_IP, VIDEO_PORT))

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)


if __name__ == '__main__':
    protcol = 'TCP'
    if sys.argv and sys.argv[0] in ['tcp', 'udp', 'rdp']:
        protocol = sys.argv[0].upper()
    else:
        print("Error: Invalid argument")
        return 

    send_video(protocol)
