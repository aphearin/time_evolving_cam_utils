"""
"""
import numpy as np
from read_sfh import times as universe_age_array

universe_dt_array = np.diff(np.insert(universe_age_array, 0, 0))


def mass_loss_fraction(x):
    """
    """
    return 0.05*np.log(1 + 1000.*x/1.4)


def redshift_zero_stellar_mass(sfr_histories):
    """
    """
    shape_err_msg = "Input ``sfr_histories`` must have shape (num_gals, num_time_steps)"
    assert len(np.shape(sfr_histories)) == 2, shape_err_msg

    frac_loss = mass_loss_fraction(universe_age_array[-1] - universe_age_array)
    integrand = sfr_histories * (1. - frac_loss)
    z0_stellar_mass = np.sum(integrand*universe_dt_array, axis=1)*1e9

    return z0_stellar_mass
