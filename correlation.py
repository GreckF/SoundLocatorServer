# -*- coding: UTF-8 -*-
from typing import *
import numpy as np

def max_index(ls):
    i = 0
    m = ls[0]
    max_ind = 0
    for x in ls:
        if x > m:
            m = x
            max_ind = i
        i += 1
    return max_ind


def getMaxPoint(y1: List, y2: List):
    # n = min(len(y1), len(y2))

    # # f i = (sum . map (\t -> y1 t * y2 (i + t)) $ [ t | t <- [0 .. n - 1] , 0 <= i + t && i + t < n ])
    # #       / length [ t | t <- [0 .. n - 1] , 0 <= i + t && i + t < n ]
    # # i ∈ (-n, n)
    # def f(i: int):
    #     ls = list(filter(lambda t: 0 <= i + t < n, range(n)))
    #     lenLs = n - abs(i)
    #     assert lenLs == len(ls)
    #     return sum(map(lambda t: y1[t] * y2[i + t], ls)) / lenLs

    # return max_index(list(map(f, range(-n + 1, n)))) - n + 1
    return gcc_phat(np.array(y2), np.array(y1))[0]


def gcc_phat(sig, refsig, fs=1, max_tau=None, interp=1):
    '''
    This function computes the offset between the signal sig and the reference signal refsig
    using the Generalized Cross Correlation - Phase Transform (GCC-PHAT)method.
    '''

    # make sure the length for the FFT is larger or equal than len(sig) + len(refsig)
    n = sig.shape[0] + refsig.shape[0]

    # Generalized Cross Correlation Phase Transform
    SIG = np.fft.rfft(sig, n=n)
    REFSIG = np.fft.rfft(refsig, n=n)
    R = SIG * np.conj(REFSIG)

    if all(np.abs(R)) == True:
        cc = np.fft.irfft(R / np.abs(R), n=(interp * n))
    else:
        cc = np.fft.irfft(R, n=(interp * n))

    max_shift = int(interp * n / 2)
    if max_tau:
        max_shift = np.minimum(int(interp * fs * max_tau), max_shift)

    cc = np.concatenate((cc[-max_shift:], cc[:max_shift + 1]))

    # find max cross correlation index
    shift = np.argmax(np.abs(cc)) - max_shift

    tau = shift / float(interp * fs)

    return tau, cc

