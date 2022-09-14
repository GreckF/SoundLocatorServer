# -*- coding: UTF-8 -*-
import socket
import threading
from queue import *
from typing import *
from numpy.compat import long

import listener
from listener import *
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

ips = socket.gethostbyname_ex(host)[2]
print(ips)
print("Choose One:")
i = 0
for ip in ips:
    print(f"{i}: {ip}")
    i += 1



port = 8888
serversocket.bind((ips[int(input())], port))
serversocket.listen(5)
print("listening")
msg_queue = Queue()

import struct
def bytesToFloat(ls):
    h1, h2, h3, h4=ls
    ba = bytearray()
    ba.append(h1)
    ba.append(h2)
    ba.append(h3)
    ba.append(h4)
    return struct.unpack("!f", ba)[0]



queueList = [Queue(), Queue(), Queue(), Queue()]

micNum = 2
for i in range(micNum):
    client_socket, addr = serversocket.accept()

    thread = threading.Thread(target=listen, args=(client_socket, addr, queueList[i]), name=f"Lis {i}")
    thread.start()
    print(f"{addr} 已连接")


input("wait enter to start...")

listener.isRun = True

f = open('log.txt', 'w')


print("run1")
while listener.isRun:
    i = 0
    s = [[], [], [], []] [:micNum]
    print("run2")
    while i < analyzeSampleNum:
        if all(map(lambda e: not e.empty(), queueList[:micNum])) :
            i += 1
            heads = do(map(lambda e: e.get(), queueList[:micNum]))
            for j in range(micNum):
                (s[j]).append(heads[j])


        else:
            pass  # print("表空")



    # analyze
    print(f"开始分析时差:")


#     for queue in queueList:
#         print(f"idqueue: { id(queue) }")
#         for i in range(1000):
#             print(queue.get())
#         print("-" * 40)
    # print("s: ")
    # do(map(print, s))
    ts      = do(map(do, do(map(lambda t: map(lambda e: e[0], t) , s))))
    samples = do(map(do, do(map(lambda t: map(lambda e: e[1], t) , s))))
    print("ts: ")
    do(map(print, ts))
#
    print("samples: ")
    do(map(print, samples))

    dS = getMaxPoint(samples[0], samples[1])
    print("-" * 40)
    print(f"ΔSample = { dS }, ΔT = { dS / samplePerSecond } s")
    print(f"{ dS / samplePerSecond }", file=f)
    print("-" * 40)

exit()