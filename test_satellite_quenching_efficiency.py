"""
"""
import numpy as np
from satellite_quenching_efficiency import build_matching_central_lookup_table
from satellite_quenching_efficiency import satellite_lookup_table_indices
from satellite_quenching_efficiency import satellite_quenching_efficiency
from time import time


def test_build_matching_central_lookup_table():
    num_centrals, num_time_steps = 10000, 178
    logsm_min, logsm_max = 8, 11
    sm = np.logspace(logsm_min, logsm_max, num_time_steps)
    central_sm_histories = np.tile(sm, num_centrals).reshape((num_centrals, num_time_steps))
    central_is_quenched = np.ones(num_centrals, dtype=bool)
    logsm_bins = np.linspace(logsm_min, logsm_max, 50)

    start = time()
    table, lookup_table_counts = build_matching_central_lookup_table(
        central_sm_histories, central_is_quenched, logsm_bins)
    end = time()
    runtime = end-start
    assert runtime < 10

    assert np.all(table[~np.isnan(table)] == 1)
    assert np.sum(lookup_table_counts) >= num_centrals


def test_satellite_lookup_table_indices():
    num_centrals, num_time_steps = 1000, 18
    logsm_min, logsm_max, num_sm_bins = 8, 11, 50
    logsm_bins = np.linspace(logsm_min, logsm_max, num_sm_bins)

    central_sm_histories = np.random.uniform(10**logsm_min, 10**logsm_max, num_centrals*num_time_steps)
    central_sm_histories = np.reshape(central_sm_histories, (num_centrals, num_time_steps))
    central_is_quenched = np.random.randint(0, 2, num_centrals).astype(bool)
    lookup_table, lookup_table_counts = build_matching_central_lookup_table(
        central_sm_histories, central_is_quenched, logsm_bins)

    num_satellites = 500
    satellite_sm_histories = np.random.uniform(10**logsm_min, 10**logsm_max, num_satellites*num_time_steps)
    satellite_sm_histories = np.reshape(satellite_sm_histories, (num_satellites, num_time_steps))
    satellite_time_indices = np.random.randint(0, num_time_steps, num_satellites)

    satellite_idx = satellite_lookup_table_indices(
        satellite_sm_histories, satellite_time_indices, logsm_bins)

    matching_vals = lookup_table[satellite_idx]
    assert matching_vals.shape == (num_satellites, )


def test_satellite_quenching_efficiency():
    num_centrals, num_time_steps = 5000, 8
    logsm_min, logsm_max, num_sm_bins = 8, 11, 5
    logsm_bins = np.linspace(logsm_min, logsm_max, num_sm_bins)
    num_satellites = 5000

    central_sm_histories = np.random.uniform(10**logsm_min, 10**logsm_max, num_centrals*num_time_steps)
    central_sm_histories = np.reshape(central_sm_histories, (num_centrals, num_time_steps))
    central_is_quenched = np.random.randint(0, 2, num_centrals).astype(bool)

    satellite_sm_histories = np.random.uniform(10**logsm_min, 10**logsm_max, num_satellites*num_time_steps)
    satellite_sm_histories = np.reshape(satellite_sm_histories, (num_satellites, num_time_steps))
    satellite_time_indices = np.random.randint(0, num_time_steps, num_satellites)
    satellite_is_quenched = np.random.randint(0, 2, num_satellites).astype(bool)
    satellite_sm = np.random.uniform(10**logsm_min, 10**logsm_max, num_satellites)

    cen_lookup_table, lookup_table_counts = build_matching_central_lookup_table(
        central_sm_histories, central_is_quenched, logsm_bins)

    fq_sat, fq_matching_cen = satellite_quenching_efficiency(
        satellite_sm_histories, satellite_sm, satellite_time_indices,
        satellite_is_quenched, cen_lookup_table, lookup_table_counts, logsm_bins)
    assert np.all(fq_sat >= 0)
    assert np.all(fq_sat <= 1)
    assert np.all(fq_matching_cen >= 0)
    assert np.all(fq_matching_cen <= 1)






