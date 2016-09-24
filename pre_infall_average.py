"""
"""
import numpy as np


def pre_infall_average(data, infall_indices):
    """
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
    return np.sum(data*masking_matrix, axis=0)
