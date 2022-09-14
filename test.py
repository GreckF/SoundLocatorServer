# -*- coding: UTF-8 -*-
import socket
from queue import *

from correlation import *
from quadratic import *
from util import *
from hardware import *
from time import time
from numpy import array
# 声速
c = 340

sig0 = sig1 = sig2 = sig3 = []
pos0 = array([0, 0, 0])
poss = array([ [1, 0, 0]
             , [0, 1, 0]
             , [0, 0, 1] ])

A_ = None
def getInvQuadA(config: Config):
    global A_
    if A_ is None:
        A_ = invRelPosQuadMat(config)
    return A_

A = None
def getInvA(config: Config):
    global A
    if A is None:
        A = inv(relPosMat(config))
    return A

def waitUtil(t):
    while time() < t: pass

def sampleLoop(freq: float, numOfSamples: int):
    global sig0, sig1, sig2, sig3
    sig0 = sig1 = sig2 = sig3 = []
    dT = 1 / freq
    startT = time()
    for i in range(numOfSamples):
        (s0, s1, s2, s3) = readAll()
        sig0.append(s0)
        sig1.append(s1)
        sig2.append(s2)
        sig3.append(s3)
        waitUtil(startT + (i + 1) * dT)
    print("T:", time() - startT)

def getPos(freq: float):
    # t0 = 0
    t1 = getMaxPoint(sig0, sig1) / freq
    t2 = getMaxPoint(sig0, sig2) / freq
    t3 = getMaxPoint(sig0, sig3) / freq
    cfg = Config(pos0, poss, array([t1 * c, t2 * c, t3 *c]))
    r0 = pickSolves(genQuadWithInvA(cfg, getInvQuadA(cfg)))
    return tuple(getXYZ(cfg, getInvA(cfg), r0))

def mainLoop(freq: float, numOfSamples: int):
    global sig0, sig1, sig2, sig3
    while True:
        sampleLoop(freq, numOfSamples)
        pos = getPos(freq)
        print(pos)

# setup()
# print("---------------------------------")
# mainLoop(10, 200)


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()



msg_queue = Queue()

import struct
def bytesToFloat(ls):
    h1,h2,h3,h4=ls
    ba = bytearray()
    ba.append(h1)
    ba.append(h2)
    ba.append(h3)
    ba.append(h4)
    return struct.unpack("!f",ba)[0]


def toIntArray(data):
    ls = []
    for i in range(0, len(data), 2):
        x = int.from_bytes([data[i], data[i+1]], byteorder="big")
        ls.append(x if -32768 <= x < 32768 else x - 65536)
    return ls

print(socket.gethostbyname_ex(host))
port = 8888
serversocket.bind(("127.0.0.1", port))
serversocket.listen(5)

while True:
    # 建立客户端连接
    clientsocket, addr = serversocket.accept()

    print("连接地址: %s" % str(addr))

    i = 0
    while True:
        print(i)
        i += 1
        msg = clientsocket.recv(64)
        data = clientsocket.recv(402)
        print(msg)
        print("recv")
        print(int(msg.decode("utf-8")))
        print(toIntArray(data))

    clientsocket.close()
