"""
This file contains functionality for communicating
with other servers on WIFI network for controlling
Raspberry Pi remotely.
"""
import socket
from directions import *

# set port to listen on
port = 1128

# set GPIO pin sleep time
sleep = .5


def run_server():
    # create socket object
    print("Creating socket...")
    sock = socket.socket()
    print("Socket created...")

    # bind to port
    print("Binding to port %d..." % port)
    # don't input IP so server can take requests
    # from any IP
    sock.bind(('', port))
    print("Socket binded to port %d..." % port)

    # put the socket into listening mode
    sock.listen(5)
    print("Socket is listening...")

    # continue accepting connections till interrupt
    while True:
        # establish connection with client
        client, (_, addr) = sock.accept()
        print("Established connection with %s..." % addr)

        data = ''
        started = False
        while data != 'esc':
            data = client.recv(1024).decode('utf-8')

            if data == 'up':
                started = False
                forward(sleep)
            elif data == 'left':
                started = False
                left(sleep)
            elif data == 'right':
                started = False
                right(sleep)
            elif data == 'down':
                started = False
                reverse(sleep)
            elif data == 'space' and not started:
                started = True
                start()
            else:
                started = False
                stop()

        # cleanup gpio pins
        stop()

        # close client connection
        client.close()


if __name__ == '__main__':
    run_server()

