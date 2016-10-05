"""
"""
import numpy as np


def matching_infall_times(sats_infall_time, num_cens):
    """
        """
    idx_cens_ranselect = np.random.randint(0, len(sats_infall_time)-1, num_cens)
    return sats_infall_time[idx_cens_ranselect]
