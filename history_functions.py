""" This module collects together functions that accept matrices of SFR histories
as input and return derived histories such as stellar mass growth, and
also summary statistics like quenching times.
"""
import numpy as np


def stellar_mass_history(sfr_history, cosmic_age):
    """
    Parameters
    ----------
    sfr_history : array
        Array of shape (num_gals, num_time_steps) storing the value of SFR
        in units of Msun/yr for each galaxy as a function of cosmic time.

    cosmic_age : array
        Array of shape (num_time_steps, ) storing the values of the age of the
        universe at which galaxy SFR has been tabulated. Sign and normalization
        convention should be such that cosmic_age[0] = 0 corresponds to the
        big bang, with units in Gyr.

    Returns
    --------
    sm_history : array
        Array of shape (num_gals, num_time_steps) storing the value of M*
        in units of Msun for each galaxy as a function of cosmic time.
        Algorithm assumes that all galaxies begin with zero stellar mass
        and that mass loss is calculated according to the Behroozi+13 fitting function.
    """
    pass

