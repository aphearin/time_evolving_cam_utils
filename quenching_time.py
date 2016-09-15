"""
"""
import numpy as np
from history_functions import ssfr_histories


fname="/Users/aphearin/Dropbox/UniverseMachine/data/histories/prelim_sfh_reduction/times.npy"
bolplanck_ages = np.load(fname)


def quenching_time(sfr_history, sm_history, cosmic_age_array=bolplanck_ages):
    """
    """
    assert np.shape(sfr_history) == np.shape(sm_history), "smh and sfh inputs must have the same shape"

    ssfr_matrix = ssfr_histories(sfr_history, sm_history)
    idx_quenching_time = quenching_indices(ssfr_matrix <= -11)
    return cosmic_age_array[idx_quenching_time]


def quenching_indices(is_quenched_matrix):
    """ Given a boolean-valued matrix of shape (m, n),
    for each row of the matrix find the largest column index storing a False value.
    Intended to use when calculating quenching timescales and
    the time-of-last-accretion.

    If given a matrix storing sSFR values in logarithmic units,
    where the matrix is of shape (num_gals, num_timesteps),
    with log10(sSFR) = -11 as a quenching cutoff,
    quenching_indices(ssfr_matrix <= -11) will give a length-num_gals array of indices
    at which each galaxy was last actively forming stars.
    Each returned index can be used with an array of cosmic ages
    (or, equivalently, an array of lookback-times)
    to identify the age of the universe at which the galaxy became quenched.

    Similarly, this function also works with an array storing ``upid`` values
    to identify the last snapshot that the satellite was still a central.

    Notes
    ------
    Edge case behavior is such that if all the values in a row are True,
    function returns 0 for that row.
    If all values in a row are False, function returns n-1.

    Parameters
    -----------
    is_quenched_matrix : array
        Boolean array of shape (m, n)

    Returns
    --------
    quenching_index : array
        Length-m array of integers, each between [0, n-1], inclusive.
    """
    assert len(np.shape(is_quenched_matrix)) == 2, "Input ``is_quenched_matrix`` must be a 2-d ndarray"
    assert is_quenched_matrix.dtype == bool, "Input ``is_quenched_matrix`` must have dtype boolean"

    idx_quenching_times = (is_quenched_matrix.shape[1] - 1) - np.argmin(is_quenched_matrix[:, ::-1], axis=1)

    # Now fix the edge case where the galaxy has always been quenched
    idx_quenching_times[np.all(is_quenched_matrix == True, axis=1)] = 0

    return idx_quenching_times
