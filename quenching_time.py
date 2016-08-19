"""
"""
import numpy as np


def quenching_indices(matrix):
    """ Given a boolean-valued matrix of shape (m, n),
    for each row of the matrix find the largest column index storing a False value.
    Intended to use when calculating quenching timescales and
    the time-of-last-accretion.

    If given a matrix storing sSFR values in logarithmic units,
    where the matrix is of shape (num_gals, num_timesteps),
    with log10(sSFR) = -11 as a quenching cutoff,
    quenching_indices(matrix <= -11) will give a length-num_gals array of indices
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
    matrix : array
        Boolean array of shape (m, n)

    Returns
    --------
    quenching_index : array
        Length-m array of integers, each between [0, n-1], inclusive.
    """
    assert len(np.shape(matrix)) == 2, "Input ``matrix`` must be a 2-d ndarray"

    idx_quenching_times = (matrix.shape[1] - 1) - np.argmin(matrix[:, ::-1], axis=1)

    # Now fix the edge case where the galaxy has always been quenched
    idx_quenching_times[np.all(matrix == True, axis=1)] = 0

    return idx_quenching_times

