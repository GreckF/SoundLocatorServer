import socket
from queue import *

from util import samplePerSecond, do


def toIntArray(data):
    ls = []
    for i in range(0, len(data), 2):
        x = int.from_bytes([data[i], data[i+1]], byteorder="big")
        ls.append(x if -32768 <= x < 32768 else x - 65536)
    return ls

isRun = False





def listen(client, addr, queue):
    print(f"id(queue) !! = { id(queue) }")
    client.send("I\n".encode("utf-8"))
    while not isRun: pass
    client.send("START\n".encode("utf-8"))
    samplePerPack = int(client.recv(64).decode("utf-8"))
    i = 0
    while True:
        d = client.recv(64)
        t = int(d.decode("utf-8"))
        data = toIntArray(client.recv(samplePerPack * 2))

        if len(d) == 0 and not isRun:
            break
        for i in range(samplePerPack):
            queue.put((t + i / samplePerSecond, data[i]))

        if i == 0:
            print(f"t0 = {t}")
            i += 1


    client.close()
    print(f"{addr} 已断开")
    print("关闭全部线程")