"""
"""
import numpy as np


def pre_infall_average(data, infall_indices):
    """
    The input data of shape (num_gals, num_time_steps) contains the evolutionary history
    of some galaxy property. At each time step, that is, for each column of data,
    the `pre_infall_average` function calculates averages over rows of input data,
    masking over rows as determined by the input ``infall_indices`` array.

    For the i^th row of data,
    Suppose the i^th element of the input infall_indices is j.
    Then columns j, j + 1, ..., num_time_steps-1 will not include row i in the
    row-wise averages for these columns.
    This function can be exploited to calcuate, for example,
    for some sample of satellite galaxies, the average SFR of the satellites
    prior to the time of infall.

    Parameters
    ----------
    data : ndarray
        matrix of shape (nrows, ncols)

    infall_indices : ndarray
        array of shape (nrows, ) indicating the index at which the
        object became a satellite

    Returns
    -------
    result : ndarray
        array of shape (ncols, ) storing the average value over rows of data,
        excluding data after infall.
    """
    column_index_matrix = np.tile(np.arange(data.shape[1]), data.shape[0]).reshape(data.shape)
    infall_indices_matrix = np.repeat(infall_indices, data.shape[1]).reshape(data.shape)
    masking_matrix = column_index_matrix < infall_indices_matrix
    tot = np.sum(data*masking_matrix, axis=0).astype(float)
    counts = np.sum(masking_matrix, axis=0).astype(float)

    result = np.zeros(data.shape[1]).astype(float) + np.nan
    nonzero_mask = counts > 0
    result[nonzero_mask] = tot[nonzero_mask]/counts[nonzero_mask]
    return result


def post_infall_average(data, infall_indices):
    """
    The input data of shape (num_gals, num_time_steps) contains the evolutionary history
    of some galaxy property. At each time step, that is, for each column of data,
    the `pre_infall_average` function calculates averages over rows of input data,
    masking over rows as determined by the input ``infall_indices`` array.

    For the i^th row of data,
    Suppose the i^th element of the input infall_indices is j.
    Then columns 1, 2, ..., j-1 will not include row i in the
    row-wise averages for these columns.
    This function can be exploited to calcuate, for example,
    for some sample of satellite galaxies, the average SFR of the satellites
    after the time of infall.

    Parameters
    ----------
    data : ndarray
        matrix of shape (nrows, ncols)

    infall_indices : ndarray
        array of shape (nrows, ) indicating the index at which the
        object became a satellite

    Returns
    -------
    result : ndarray
        array of shape (ncols, ) storing the average value over rows of data,
        excluding data prior to infall. Returns nan for columns where every
        row was excluded from the average.

    """
    column_index_matrix = np.tile(np.arange(data.shape[1]), data.shape[0]).reshape(data.shape)
    infall_indices_matrix = np.repeat(infall_indices, data.shape[1]).reshape(data.shape)
    masking_matrix = column_index_matrix >= infall_indices_matrix
    tot = np.sum(data*masking_matrix, axis=0).astype(float)
    counts = np.sum(masking_matrix, axis=0).astype(float)

    result = np.zeros(data.shape[1]).astype(float) + np.nan
    nonzero_mask = counts > 0
    result[nonzero_mask] = tot[nonzero_mask]/counts[nonzero_mask]
    return result
