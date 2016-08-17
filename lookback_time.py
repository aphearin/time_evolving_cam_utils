"""
"""
from astropy.cosmology import Planck13

__all__ = ('lookback_time', )


def lookback_time(scales):
    """
    """
    z = (1./scales)-1.
    return Planck13.lookback_time(z)
