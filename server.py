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

        cmd = ''
        last_cmd = ''
        while cmd != 'esc':
            cmd = client.recv(1024).decode('utf-8')

            if cmd == 'up' and last_cmd != 'up':
                forward()
                last_cmd = cmd
            elif cmd == 'left' and last_cmd != 'left':
                left()
                last_cmd = cmd
            elif cmd == 'right' and last_cmd != 'right':
                right()
                last_cmd = cmd
            elif cmd == 'down' and last_cmd != 'down':
                reverse()
                last_cmd = cmd
            elif cmd == 'space' and last_cmd != 'space':
                start()
                last_cmd = cmd
            elif cmd == 'stop' or cmd == 'space':
                last_cmd = ''
                stop()

        # cleanup gpio pins
        stop()

        # close client connection
        client.close()


if __name__ == '__main__':
    run_server()

