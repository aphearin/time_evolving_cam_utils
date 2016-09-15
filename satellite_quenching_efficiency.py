"""
"""
import numpy as np


def build_matching_central_lookup_table(central_sm_histories, central_is_quenched, logsm_bins):
    """
    """
    num_centrals, num_time_steps = central_sm_histories.shape
    msg = "central_sm_histories and central_is_quenched and have inconsistent shapes"
    assert num_centrals == len(central_is_quenched), msg

    num_sm_bins = len(logsm_bins)-1
    lookup_table = np.zeros((num_sm_bins, num_time_steps))

    for ism, logsm_low, logsm_high in zip(range(num_sm_bins), logsm_bins[:-1], logsm_bins[1:]):
        for idx_time in range(num_time_steps):
            ism_values = central_sm_histories[:, idx_time]
            ism_mask = (ism_values >= 10**logsm_low) & (ism_values < 10**logsm_high)
            lookup_table[ism, idx_time] = central_is_quenched[ism_mask].mean()

    return lookup_table


