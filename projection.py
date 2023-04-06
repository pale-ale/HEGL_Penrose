import numpy as np
from scipy import linalg


def project_point_line_2d(p:np.ndarray, s:np.ndarray, d:np.ndarray):
    assert linalg.norm(d) != 0
    p0, p1 = p
    s0, s1 = s
    d = d / linalg.norm(d)
    d0, d1 = d
    best_param = (d0 * (p0 - s0) + d1 * (p1 - s1)) / (d0**2 + d1**2)
    return s + best_param * d
