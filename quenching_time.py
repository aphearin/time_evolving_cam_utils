"""
"""
import numpy as np


def quenching_indices(matrix):
    """ Given a boolean-valued matrix of shape (m, n), for each row of the matrix
    find the largest index storing a True value.

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
    return (matrix.shape[1] - 1) - np.argmin(matrix[:, ::-1], axis=1)
