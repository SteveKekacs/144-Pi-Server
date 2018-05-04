# 144-Pi-Server
This is the code that runs on the Raspberry Pi 3 that is hardwired to our mobile RC car, and its function is to capture video from the camera module attached to the Pi and send it over the network (either through a TCP or UDP socket) to an external server and wait for commands for the mobile car (start and stop). 

There are two main files that perform this functionality:
1. `directions.py`: This contains functionality for interacting with the Raspberry Pi GPIO pins that are wired to the motor of the RC car. It contains functions to initialize and cleanup the pins, then steer the car forward, backwards, left, right, pivot left, pivot right, and to stop the car.
2. `autonomous_sender.py`: This file contains functionality for setting up the appropriate socket (UDP or TCP based on passed command line paramater) for sending video the an external server, then another TCP socket for receiving commands for the car. It uses the picamera library to access footage that is captured by the camera module that is attached to the Raspberry Pi, and then transmit that video over the established socket to an external server for object detection. It then waits for a `start` command that is sent after 10 frames have been sent successfully, then a `stop` command that is sent once a stop sign has been detected.

There is also one irrelevant file (for fun) `server.py`, that allows you to manually drive the mobile RC car from an external server.
