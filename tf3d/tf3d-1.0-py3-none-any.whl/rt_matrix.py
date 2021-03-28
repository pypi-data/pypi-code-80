from tf3d.chaining import chain
from typing import List
from pyquaternion import Quaternion
import numpy as np


def Rt_from_quaternion(q: Quaternion, t: np.ndarray=None) -> np.ndarray:
    Rt = q.transformation_matrix
    if t is not None:
        Rt = chain(Rt, Rt_from_offset(t))
    return Rt


def Rt_from_axis_angle(axis: List[float], angle: float, t: np.ndarray=None) -> np.ndarray:
    return Rt_from_quaternion(Quaternion(axis=axis, angle=angle), t)


def Rt_from_offset(offset: np.ndarray) -> np.ndarray:
    matrix = np.identity(4, dtype=np.float32)
    matrix[:3, 3] = offset
    return matrix

def Rt_inverse(Rt: np.ndarray) -> np.ndarray:
    Rt = np.array(Rt)
    Rt[:3, :3] = R_from_Rt(Rt).T
    Rt[:3, 3] = -R_from_Rt(Rt).dot(t_from_Rt(Rt))
    return Rt


def R_from_Rt(Rt: np.ndarray) -> np.ndarray:
    return Rt[:3, :3]


def t_from_Rt(Rt: np.ndarray) -> np.ndarray:
    return Rt[:3, 3]


def transform(Rt: np.ndarray, point: np.ndarray) -> np.ndarray:
    if point.ndim == 1:
        return R_from_Rt(Rt).dot(point) + t_from_Rt(Rt)
    else:
        homogenized = np.insert(point.T, 3, 1, axis=0)
        return Rt.dot(homogenized)[:3].T
