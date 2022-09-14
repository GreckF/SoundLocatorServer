# -*- coding: UTF-8 -*-
#import smbus
#import time
#import RPi.GPIO as GPIO
#
#bus = smbus.SMBus(1)
#
#def setup():
#    GPIO.setmode(GPIO.BCM)
#    global address
#    address = 0x48
#
#def read(chn): #channel
#  if chn == 0:
#    bus.write_byte(address,0x40)
#  elif chn == 1:
#    bus.write_byte(address,0x41)
#  elif chn == 2:
#    bus.write_byte(address,0x42)
#  elif chn == 3:
#    bus.write_byte(address,0x43)
#
#  bus.read_byte(address)
#  return bus.read_byte(address)

from math import sin, cos, tan, sqrt
from time import time

import numpy as np

def f(t):
    return 1000*sin(t / 10000)

def read(chn) -> float:
    srcPos = np.array([102, 222, 123])
    p0 = np.array([0,0,0])
    poss = np.array([ [1, 0, 0]
                    , [0, 1, 0]
                    , [0, 0, 1]])
    t0 = np.linalg.norm(srcPos - p0) / 340
    t1 = np.linalg.norm(srcPos - poss[0]) / 340
    t2 = np.linalg.norm(srcPos - poss[1]) / 340
    t3 = np.linalg.norm(srcPos - poss[2]) / 340
    if chn == 0:
        return f(time() - t0)
    if chn == 1:
        return f(time() - t1)
    if chn == 2:
        return f(time() - t2)
    if chn == 3:
        return f(time() - t3)

def setup(): pass

def readAll():
    s0 = read(0)
    s1 = read(1)
    s2 = read(2)
    s3 = read(3)
    return (s0, s1, s2, s3)
