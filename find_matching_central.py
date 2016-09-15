"""
"""
import numpy as np


def matching_central_indices(central_histories, satellite_time_indices, vals_to_match):
    """
    """
    num_centrals = central_histories.shape[0]
    result = np.zeros_like(satellite_time_indices)

    for isat, time_idx in enumerate(satellite_time_indices):
        central_properties_at_time_idx = central_histories[np.arange(num_centrals), time_idx]
        absdiff = np.abs(central_properties_at_time_idx - vals_to_match[isat])
        result[isat] = np.argmin(np.abs(absdiff))

    return result

