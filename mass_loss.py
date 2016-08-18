"""
"""
import numpy as np


def mass_loss_fraction(x):
    """
    """
    return 0.05*np.log(1 + x/1.4)


def remaining_mass(t_now, sfh, t):
    """
    """
    x = t_now - t
    frac_loss = mass_loss_fraction(x)
    integrand = sfh * (1. - frac_loss)
