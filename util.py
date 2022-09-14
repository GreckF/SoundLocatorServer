# -*- coding: UTF-8 -*-
import numpy as np

from quadratic import Quad



def zipWith(f, a, b):
    return map(lambda t: f(t[0], t[1]), zip(a, b))


class Config:
    p0 = None   # : Vec3 -- 主麦克风位置
    ps = None   # : Mat3 -- 第i行代表(x_{i+1}, y_{i+1}, z_{i+1}) 即三个
    drs = None  # : Vec3 -- (dr_1, dr_2, dr_3) 声源到p_i和p_0的距离差

    def __init__(self, p0, ps, drs):
        self.p0 = p0
        self.ps = ps
        self.drs = drs


# k(i) = (1/2) * ((x_0**2 + y_0**2 + z_0**2) - (x_i**2 + y_i**2 + z_i**2) + dr_i**2)
def k(cfg: Config, i: int) -> float:
    [x0, y0, z0] = cfg.p0
    [xi, yi, zi] = cfg.ps[i]
    dri = cfg.drs[i]
    return ((x0**2 + y0**2 + z0**2) - (xi**2 + yi**2 + zi**2) + dri**2) / 2


# relPosMat :: Num a => Config a -> Mat3 a
# relPosMat (Config p0' (Mat ps') _) = fmap negate (Mat $ fmap f ps') where
#   f p = (-) <$> p <*> p0'
# 相对位置矩阵A
def relPosMat(config: Config) -> np.ndarray:
    p0 = config.p0
    ps = list(config.ps)
    for i in range(len(ps)):
        ps[i] = ps[i] - p0
    return - np.array(ps)

# Config {
#   p0 = v[0.0, 0.0, 0.0],
#   ps = v[v[1.0, 0.0, 0.0],
#          v[0.0, 1.0, 0.0],
#          v[0.0, 0.0, 1.0]],
#   drs = v[-0.99724963423796, 5.681069222919177e-2, -4.759990889579058e-2]
# }
testConfig = Config\
    ( np.array([0, 0, 0])
    , np.array([ [1, 0, 0]
               , [0, 1, 0]
               , [0, 0, 1]])
    , np.array([-0.99724963423796, 5.681069222919177e-2, -4.759990889579058e-2])
    )

fmap = np.vectorize
inv = np.linalg.inv

# 将相对位置矩阵的逆转化成二次方程矩阵
def invRelPosQuadMat(config: Config) -> np.ndarray:
    return fmap (lambda x: Quad(c=x)) (inv(relPosMat(config)))

# fVec :: Fractional a => Config a -> Vec3 (Quadratic a)
# fVec c = fmap (\i -> Quadratic $ vec3 (0, v ! i, k c i)) $ fins (toSNat Proxy) where
#   v = fmap ($ genEq c) $ vec3 (_dr1, _dr2, _dr3)
# 向量 fVec : Mat 3 × 1
def fVec(config: Config) -> np.ndarray:
    drv = fmap (lambda x: Quad(b=x)) (config.drs)
    ks = fmap (lambda x: Quad(c=x)) (np.array(list(map(lambda i: k(config, i), range(3)))))
    return (drv + ks).transpose()



# genQuad :: (Ord a, Floating a) => Config a -> Quadratic a
# genQuad c = (runMat (transpose mV .*. mV) ! FZ ! FZ) - (Quadratic (vec3 (1, 0, 0)))
#   where
#     c' = genEq c
#     mV = mX - colMat (fmap (\f -> toQuad (f c')) $ vec3 (_x0, _y0, _z0))
#     mX = fmap toQuad (inv (relPosMat c)) .*. colMat (fVec c)
# 从Config生成方程
def genQuad(config: Config) -> Quad:
    X0 = fmap (lambda x: Quad(c=x)) (config.p0.transpose())
    A_ = invRelPosQuadMat(config)
    F  = fVec(config)
    M  = A_.dot(F) - X0
    N  = M.transpose().dot(M)
    return N - Quad(a=1)

def genQuadWithInvA(config: Config, A_: np.ndarray) -> Quad:
    X0 = fmap(lambda x: Quad(c=x))(config.p0.transpose())
    F = fVec(config)
    M = A_.dot(F) - X0
    N = M.transpose().dot(M)
    return N - Quad(a=1)

# getXYZ c@(Config _ _ dr) r0 = inv (relPosMat c) .@. f where
#   f = fmap (\i -> r0 * dr ! i + k c i) $ fins $ toSNat Proxy
def getXYZ(config: Config, invA: np.array, r0: float) -> np.array:
    return invA.dot(np.array([ r0 * config.drs[0] + k(config, 0)
                             , r0 * config.drs[1] + k(config, 1)
                             , r0 * config.drs[2] + k(config, 2)]))


def join(ls: list):
    r = []
    for e in ls:
        r = r + e
    return r

def do(x):
    return list(x)


analyzeSampleNum = 44100
samplePerSecond  = 44100
