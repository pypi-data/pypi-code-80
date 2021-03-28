import numpy as np


def _solve_quadratic_equation(a: np.ndarray, b: np.ndarray, c: np.ndarray):
    solution_1 = (-b - np.sqrt(b * b - 4 * a * c)) / (2 * a)
    solution_2 = (-b + np.sqrt(b * b - 4 * a * c)) / (2 * a)
    return solution_1, solution_2


def pinhole_matrix(fx: float, fy: float, cx: float, cy: float, tx: float = 0, ty: float = 0, tz: float = 0) -> np.ndarray:
    return np.array([
        [fx, 0, cx, tx],
        [0, fy, cy, ty],
        [0, 0, 1, tz],
    ])


def pinhole_project(pinhole_projection: np.ndarray, xyz: np.ndarray) -> np.ndarray:    
    if xyz.ndim != 1:
        xyz = xyz.T
    homogenized = np.insert(xyz, 3, 1, axis=0)
    uvw = pinhole_projection.dot(homogenized)
    depth = np.sqrt((xyz**2).sum(axis=0))
    depth = np.where(uvw[2] < 0, -depth, depth)
    uvw /= uvw[2]
    uvw[2] = depth
    if xyz.ndim != 1:
        return uvw.T
    else:
        return uvw


def pinhole_reproject(pinhole_projection: np.ndarray, uvd: np.ndarray) -> np.ndarray:
    if uvd.ndim != 1:
        uvd = uvd.T
    u, v, d = uvd
    m00 = float(pinhole_projection[0][0])
    m11 = float(pinhole_projection[1][1])
    m02 = float(pinhole_projection[0][2])
    m12 = float(pinhole_projection[1][2])
    m22 = float(pinhole_projection[2][2])
    t_1 = float(pinhole_projection[0][3])
    t_2 = float(pinhole_projection[1][3])
    t_3 = float(pinhole_projection[2][3])

    alpha_1 = (u * m22 - m02) / m00
    alpha_2 = (v * m22 - m12) / m11
    beta_1 = (u * t_3 - t_1) / m00
    beta_2 = (v * t_3 - t_2) / m11

    a = 1 + alpha_1 * alpha_1 + alpha_2 * alpha_2
    b = 2 * (alpha_1 * beta_1 + alpha_2 * beta_2)
    c = beta_1 * beta_1 + beta_2 * beta_2 - d * d

    solution_1, solution_2 = _solve_quadratic_equation(a, b, c)

    z = np.where(solution_1 > solution_2, solution_1, solution_2)
    z = np.where(d < 0, -z, z)
    x = alpha_1 * z + beta_1
    y = alpha_2 * z + beta_2
    return np.stack([x, y, z], axis=-1)
