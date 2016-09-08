"""
"""
import numpy as np
from astropy.utils.misc import NumpyRNGContext


def noisy_percentile(percentile, sigma, seed=None):
    """
    """
    percentile = np.atleast_1d(percentile)
    if sigma < 0:
        msg = "Input ``sigma`` must be non-negative"
        raise ValueError(msg)
    elif sigma == 0:
        return percentile
    else:
        pass

    # Add Gaussian noise to the percentiles
    N = len(np.atleast_1d(percentile))
    with NumpyRNGContext(seed):
        noise = np.random.normal(0, sigma, N)
    noisy_percentile = percentile + noise

    to_the_right = (noisy_percentile >= 1)
    to_the_left = (noisy_percentile < 0)

    while np.any(to_the_right | to_the_left):
        noisy_percentile[to_the_left] = np.fabs(noisy_percentile[to_the_left])
        noisy_percentile[to_the_right] = 1 - (noisy_percentile[to_the_right] - 1)
        to_the_right = (noisy_percentile >= 1)
        to_the_left = (noisy_percentile < 0)

    return noisy_percentile
