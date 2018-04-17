"""
This file contains functionality for communicating
with other servers on WIFI network for controlling
Raspberry Pi remotely.
"""
import socket
import sys
import directions as car

# set port to listen on
port = 1128


def run_server(use_udp):
    # create socket object
    print("Creating socket...")
    sock = socket.socket()
    print("%s Socket created..." % protocol_string)

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

            if cmd == 'up' and last_cmd != 'up':
                car.forward()
            elif cmd == 'left' and last_cmd != 'left':
                car.left()
            elif cmd == 'right' and last_cmd != 'right':
                car.right()
            elif cmd == 'down' and last_cmd != 'down':
                car.reverse()
            elif cmd == 'space' and last_cmd != 'space' or cmd == 'stop':
                car.start()
            elif cmd == 'enter' and last_cmd != 'enter':
                car.forward()

            last_cmd = cmd

        # cleanup gpio pins
        car.cleanup()

        # close client connection
        client.close()


if __name__ == '__main__':
    udp = False
    if 'udp' in sys.argv:
        udp = True

    run_server(udp)

