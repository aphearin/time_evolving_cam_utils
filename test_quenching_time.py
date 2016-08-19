"""
"""
import numpy as np
from quenching_time import quenching_indices


def test_quenching_time1():
    """
    """
    m = np.array(((-10, -10, -12, -12), (-10, -12, -12, -12)))
    bm = m < -11
    qtimes = quenching_indices(bm)
    assert np.all(qtimes == (1, 0)), qtimes


def test_quenching_time2():
    """
    """
    m = np.array((
        (-10, -10.5, -11.5, -11.25, -10, -12, -12),
        (-11.25, -10.5, -11.25, -11.5, -10.9, -12, -12),
        (-10, -10.5, -11.5, -11.25, -10, -12, -12)
    ))

    bm = m < -11
    qtimes = quenching_indices(bm)

    assert np.all(qtimes == (4, 4, 4)), qtimes


def test_quenching_time3():
    """
    """
    m = np.array((
        (-12, -12, -12, -12, -12, -12, -12),
        (-10, -10, -10, -10, -10, -10, -10),
        (-11, -11, -11, -11, -11, -11, -11),
    ))

    bm = m <= -11
    qtimes = quenching_indices(bm)

    assert np.all(qtimes == (0, 6, 0)), qtimes


def test_quenching_time4():
    """
    """
    m, n = 1000, 8
    seedlist = np.arange(10).astype(int)
    for seed in seedlist:
        np.random.seed(seed)
        matrix = np.random.uniform(-12, -10, n*m).reshape((m, n))
        is_quenched_matrix = matrix <= -11
        idx_quenching_time = quenching_indices(is_quenched_matrix)





