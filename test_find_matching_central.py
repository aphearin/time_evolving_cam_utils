"""
"""
import numpy as np
from find_matching_central import matching_central_indices


def test_find_matching_central():
    central_histories = np.array(((0, 1, 2), (3, 4, 5), (7, 8, 9)))
    satellite_time_indices = np.array((0, 1, 0))
    vals_to_match = np.array((0, 4, 7))
    matching_idx = matching_central_indices(
        central_histories, satellite_time_indices, vals_to_match)
    assert np.all(matching_idx == (0, 1, 2))
