"""
This file contains functionality for communicating
with other servers on WIFI network for controlling
Raspberry Pi remotely.
"""
import socket
from directions import *

# set port to listen on
port = 1128


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

        # initialize gpio pins
        init()
        print("Initialized GPIO pins...")

        cmd = ''
        last_cmd = ''
        while cmd != 'esc':
            try:
                cmd = client.recv(1024).decode('utf-8')
                cmd = cmd.split('.')[-1]
            except:
                pass
            print(cmd)

            if cmd == 'up' and last_cmd != 'up':
                forward()
            elif cmd == 'left' and last_cmd != 'left':
                left()
            elif cmd == 'right' and last_cmd != 'right':
                right()
            elif cmd == 'down' and last_cmd != 'down':
                reverse()
            elif cmd == 'space' and last_cmd != 'space' or cmd == 'stop':
                stop()
            elif cmd == 'enter':
                forward()

            last_cmd = cmd

        # cleanup gpio pins
        cleanup()

        # close client connection
        client.close()


if __name__ == '__main__':
    run_server()

