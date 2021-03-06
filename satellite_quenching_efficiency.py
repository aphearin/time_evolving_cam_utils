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
    counts = np.zeros((num_sm_bins, num_time_steps))

    for ism, logsm_low, logsm_high in zip(range(num_sm_bins), logsm_bins[:-1], logsm_bins[1:]):
        for idx_time in range(num_time_steps):
            ism_values = central_sm_histories[:, idx_time]
            ism_mask = (ism_values >= 10**logsm_low) & (ism_values < 10**logsm_high)
            lookup_table[ism, idx_time] = central_is_quenched[ism_mask].mean()
            counts[ism, idx_time] = len(central_is_quenched[ism_mask])

    return lookup_table, counts


def satellite_lookup_table_indices(satellite_sm_histories, satellite_time_indices, logsm_bins):
    """
    """
    num_satellites, num_time_steps = satellite_sm_histories.shape
    msg = "satellite_sm_histories and satellite_time_indices and have inconsistent shapes"
    assert num_satellites == len(satellite_time_indices), msg

    satellite_sm = satellite_sm_histories[np.arange(num_satellites), satellite_time_indices]
    satellite_sm_idx = np.digitize(satellite_sm, logsm_bins)

    satellite_sm_idx[satellite_sm_idx >= len(logsm_bins)-1] = len(logsm_bins)-2

    return satellite_sm_idx, satellite_time_indices


def satellite_quenching_efficiency(satellite_sm_histories, satellite_sm, satellite_time_indices,
        satellite_is_quenched, cen_lookup_table, lookup_table_counts, logsm_bins):

    satellite_sm_at_infall = satellite_sm_histories[np.arange(len(satellite_sm)), satellite_time_indices]
    sat_table_idx = satellite_lookup_table_indices(
        satellite_sm_histories, satellite_time_indices, logsm_bins)
    sat_sm_idx = np.digitize(satellite_sm, 10**logsm_bins)
    sat_sm_idx[sat_sm_idx>=len(logsm_bins)-1] = len(logsm_bins)-2

    fq_sat = np.zeros(len(logsm_bins)-1)
    fq_matching_cen = np.zeros(len(logsm_bins)-1)
    for ism, logsm_low, logsm_high in zip(range(len(logsm_bins)-1), logsm_bins[:-1], logsm_bins[1:]):
        ism_mask = (satellite_sm >= 10**logsm_low) & (satellite_sm < 10**logsm_high)
        fq_sat[ism] = satellite_is_quenched[ism_mask].mean()

        ism_infall_mask = (satellite_sm_at_infall >= 10**logsm_low) & (satellite_sm_at_infall < 10**logsm_high)
        cen_fq_ism = cen_lookup_table[sat_table_idx[0][ism_infall_mask], sat_table_idx[1][ism_infall_mask]]
        cen_counts_ism = lookup_table_counts[sat_table_idx[0][ism_infall_mask], sat_table_idx[1][ism_infall_mask]]
        cen_fq_ism_mask = ~np.isnan(cen_fq_ism)
        fq_matching_cen[ism] = np.sum(cen_fq_ism[cen_fq_ism_mask]*cen_counts_ism[cen_fq_ism_mask])
        fq_matching_cen[ism] /= np.sum(cen_counts_ism[cen_fq_ism_mask])

    return fq_sat, fq_matching_cen




