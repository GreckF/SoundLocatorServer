# -*- coding: UTF-8 -*-
import numpy as np
from typing import *
from math import sqrt

class Quad:
    vec = []

    def __init__(self, a=0, b=0, c=0):
        self.vec = [a, b, c]

    def __str__(self):
        return str(self.vec)

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        return Quad(  self.vec[0] + other.vec[0]
                    , self.vec[1] + other.vec[1]
                    , self.vec[2] + other.vec[2])

    def __sub__(self, other):
        return Quad(  self.vec[0] - other.vec[0]
                    , self.vec[1] - other.vec[1]
                    , self.vec[2] - other.vec[2])

    def __mul__(self, other):
        [a1, b1, c1] = self.vec
        [a2, b2, c2] = other.vec
        x = a1 * a2                         # 新4次项
        y = a1 * b2 + a2 * b1               # 新3次项
        a = a1 * c2 + a2 * c1 + b1 * b2     # 新2次项
        b = b1 * c2 + b2 * c1               # 新1次项
        c = c1 * c2                         # 新0次项
        if isZero(x) and isZero(y):
            return Quad(a, b, c)
        else:
            print("higher than expect")

    def solve(self) -> Optional[Tuple[float, float]]:
        [a, b, c] = self.vec
        delta = b * b - 4 * a * c
        if delta < 0: return None
        return (- b + sqrt(delta)) / (2 * a), (- b - sqrt(delta)) / (2 * a)

# 选取合适的解
def pickSolves(q: Quad) -> Optional[float]:
    s = q.solve()
    if s is None:
        return None
    (a, b) = s
    if a < 0:   return b
    if b < 0:   return a
    if a < b:   return b
    else:       return a

def isZero(x):
    return abs(x) < 1e-7


def toQuad(vec):
    return Quad(vec[0], vec[1], vec[2])



