import numpy as np
import cv2
import socket

UDP_IP = "65.112.8.3"
UDP_PORT = 1122

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()

    cv2.imshow('frame',frame)


    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    d = frame.flatten ()
    s = d.tostring ()



    for i in range(20):

        sock.sendto (s[i*1240:(i+1)*1240],(UDP_IP, UDP_PORT))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
