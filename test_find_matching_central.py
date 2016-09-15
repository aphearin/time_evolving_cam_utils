"""
"""
import numpy as np
from time import time
from find_matching_central import matching_central_indices
from astropy.utils.misc import NumpyRNGContext


def test_find_matching_central1():
    central_histories = np.array(((0, 1, 2), (3, 4, 5), (7, 8, 9)))
    satellite_time_indices = np.array((0, 1, 0))
    vals_to_match = np.array((0, 4, 7))
    matching_idx = matching_central_indices(
        central_histories, satellite_time_indices, vals_to_match)
    assert np.all(matching_idx == (0, 1, 2))


def test_find_matching_central2():
    num_centrals = int(1e4)
    num_satellites = int(5e3)
    num_time_steps = 178

    with NumpyRNGContext(43):
        central_histories = np.random.random((num_centrals, num_time_steps))
        satellite_time_indices = np.random.randint(0, num_time_steps, num_satellites)
        vals_to_match = np.random.random(num_satellites)

    start = time()
    matching_idx = matching_central_indices(
        central_histories, satellite_time_indices, vals_to_match)
    end = time()
    runtime = end-start
    assert runtime < 5

    assert np.all(matching_idx < num_centrals)
    assert np.all(matching_idx >= 0)
    matching_cen_vals = central_histories[matching_idx, satellite_time_indices]
    assert np.all(np.abs(matching_cen_vals - vals_to_match) < 0.05)





