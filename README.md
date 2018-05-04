# 144-Pi-Server
This is the code that runs on the Raspberry Pi 3 that is hardwired to our mobile RC car, and its function is to capture video from the camera module attached to the Pi and send it over the network (either through a TCP or UDP socket) to an external server and wait for commands for the mobile car (start and stop). 

There is one main file that performs this functionality: 