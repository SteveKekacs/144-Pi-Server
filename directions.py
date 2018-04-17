"""
This file contains functions for
driving the car.
"""
import RPi.GPIO as gpio
import time


def init():
    """
    Sets up GPIO pins
    for driving car.
    """
    gpio.setmode(gpio.BOARD)
    gpio.setup(7, gpio.OUT)
    gpio.setup(11, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(15, gpio.OUT)


def start():
    """
    Put car in indefinite forward
    direction, for use in autonomous driving.
    """
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, True)


def stop():
    """
    Stops car, for use in autonomous driving.
    """
    gpio.output(7, False)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, False)


def cleanup():
    gpio.cleanup()


def forward():
    """
    Drive car forward, for use in
    user controlled driving.
    """
    # put in forward direction
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, True)


def reverse():
    """
    Drive car in reverse, for use in
    user controlled driving.
    """
    # put in reverse direction
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, True)
    gpio.output(15, False)


def right():
    """
    Drive car right, for use in
    user controlled driving.
    """
    # put in right direction
    gpio.output(7, False)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, True)


def left():
    """
    Drive car left, for use in
    user controlled driving.
    """
    # put in left direction
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, False)


def pivot_left():
    """
    Pivot car left, for use in
    user controlled driving.
    """
    # put in left pivot
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, True)
    gpio.output(15, False)


def pivot_right():
    """
    Pivot car right, for use in
    user controlled driving.
    """
    # put in rightpivot
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, True)

