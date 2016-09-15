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


def satellite_lookup_table_indices(satellite_sm_histories, satellite_time_indices, logsm_bins):
    """
    """
    num_satellites, num_time_steps = satellite_sm_histories.shape
    msg = "satellite_sm_histories and satellite_time_indices and have inconsistent shapes"
    assert num_satellites == len(satellite_time_indices), msg

    satellite_sm = satellite_sm_histories[np.arange(num_satellites), satellite_time_indices]
    satellite_sm_idx = np.digitize(satellite_sm, logsm_bins)

    satellite_sm_idx[satellite_sm_idx >= len(logsm_bins)-1] = len(logsm_bins)-2

    return np.array((satellite_sm_idx, satellite_time_indices))


def satellite_quenching_efficiency(satellite_sm_histories, satellite_sm, satellite_time_indices,
        satellite_is_quenched, central_sm_histories, central_is_quenched, logsm_bins):

        cen_lookup_table = build_matching_central_lookup_table(
            central_sm_histories, central_is_quenched, logsm_bins)
        sat_table_idx = satellite_lookup_table_indices(
            satellite_sm_histories, satellite_time_indices, logsm_bins)
        sat_sm_idx = np.digitize(satellite_sm, 10**logsm_bins)
        sat_sm_idx[sat_sm_idx>=len(logsm_bins)-1] = len(logsm_bins)-2
        assert 4 == 5, "Unfinished function"





