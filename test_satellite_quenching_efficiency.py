"""
"""
import numpy as np
from satellite_quenching_efficiency import build_matching_central_lookup_table
from time import time


def test_build_matching_central_lookup_table():
    num_centrals, num_time_steps = 10000, 178
    logsm_min, logsm_max = 8, 11
    sm = np.logspace(logsm_min, logsm_max, num_time_steps)
    central_sm_histories = np.tile(sm, num_centrals).reshape((num_centrals, num_time_steps))
    central_is_quenched = np.ones(num_centrals, dtype=bool)
    logsm_bins = np.linspace(logsm_min, logsm_max, 50)

    start = time()
    table = build_matching_central_lookup_table(central_sm_histories, central_is_quenched, logsm_bins)
    end = time()
    runtime = end-start
    assert runtime < 10

    assert np.all(table[~np.isnan(table)] == 1)

