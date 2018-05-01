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
import _thread
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
VIDEO_PORT = 8022
COMMAND_PORT = 8023


def recv_stop_command(conn, clientsocket):
    """
    Waits to receive stop command from server,
    signals car to stop.
    """

    # wait for message to start car
    conn.recv(1024)
    print("Starting car...")
    car.start()

    # once message recieved again stop car
    conn.recv(1024)
    print("Stopping car...")
    car.stop()

    # cleanup pins
    car.cleanup()

    # close client socket
    clientsocket.close()


def send_video(protocol):
    """
    Sends video to server over given protocol,
    starts thread to receive stop command once
    stop sign is detected.
    """
    print("Initializing car...")
    car.init()

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
        while True:
            try:
                clientsocket.connect((HOST_IP, VIDEO_PORT))
                break
            except:
                time.sleep(1)
        print("Connected to %s:%d...\n\n" % (HOST_IP, VIDEO_PORT))

    # initialize the camera and grab a reference to the raw camera capture
    print("Initializing Camera...")
    camera = PiCamera()
    camera.resolution = (camera_width, camera_height)
    camera.framerate = 32
    camera.rotation = 180
    rawCapture = PiRGBArray(camera, size=(camera_width, camera_height))

    # allow the camera to warmup
    time.sleep(0.1)
    print("Camera ready...\n\n")

    # initialize comand socket
    time.sleep(1)

    print("Creating socket to receive car commands...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket for receiving car commands created...")

    # bind to host
    print("Binding to port %d..." % COMMAND_PORT)
    sock.bind(('', COMMAND_PORT))

    # listen and accept connection
    sock.listen(1)
    print("Socket for receiving car commands is listening...")

    conn, (_, addr) = sock.accept()
    print("Established connection with %s for receiving car commands\n\n" % addr)

    _thread.start_new_thread(recv_stop_command, (conn, clientsocket))

    time.sleep(3)

    print("Beginning video...\n\n")

    # continue to capture frames from camera and
    # send to remote server till interrupt
    for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        frame = image.array

        # convert to string
        data = frame.flatten().tostring()

        # send data len then data to client
        try:
            if protocol == 'TCP':
                clientsocket.sendall(data)
            else:
                # data = b'!' * 20 + data
                pckt_sz = 11520

                for i in range(20):
                    clientsocket.sendto(data[pckt_sz*i:pckt_sz*(i+1)], (HOST_IP, VIDEO_PORT))

        except:
            print("Connection closed...")
            break

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

    # close sockets
    sock.close()


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] in ['tcp', 'udp', 'rdp']:
        protocol = sys.argv[1].upper()
        send_video(protocol)
    else:
        print("Error: Invalid argument")
