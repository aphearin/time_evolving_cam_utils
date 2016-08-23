""" This module collects together functions that accept matrices of SFR histories
as input and return derived histories such as stellar mass growth, and
also summary statistics like quenching times.
"""
import numpy as np

fname="/Users/aphearin/Dropbox/UniverseMachine/data/histories/prelim_sfh_reduction/times.npy"
bolplanck_ages = np.load(fname)


def mass_loss_fraction(dt):
    """
    Fraction of mass lost during time interval dt due to passive evolution.

    Parameters
    ----------
    dt : array
        Length N array of time intervals in units of Gyr

    Returns
    --------
    frac_loss : array
        Length N array of fractional mass loss.
    """
    return 0.05*np.log(1 + 1000.*dt/1.4)


def stellar_mass_history(sfr_history, cosmic_age_array=bolplanck_ages):
    """
    Calculate stellar mass histories from star formation histories.

    Parameters
    ----------
    sfr_history : array
        Array of shape (num_gals, num_time_steps) storing the value of SFR
        in units of Msun/yr for each galaxy as a function of cosmic time.

    cosmic_age_array : array
        Array of shape (num_time_steps, ) storing the values of the age of the
        universe at which galaxy SFR has been tabulated, in units of Gyr.
        Sign and normalization convention are such that galaxies have
        zero stellar mass at cosmic_age_array[0], with the present-day
        cosmic epoch being stored in cosmic_age_array[-1]

    Returns
    --------
    sm_history : array
        Array of shape (num_gals, num_time_steps) storing the value of M*
        in units of Msun for each galaxy as a function of cosmic time.
        Algorithm is an implementation of Eq. 17 in Behroozi+17,
        assumes that all galaxies begin with zero stellar mass
        and that mass loss is calculated according to the Behroozi+13 fitting function.
    """
    dt_in_gyr = np.diff(cosmic_age_array)
    frac_loss = mass_loss_fraction(dt_in_gyr)
    integrand = sfr_history[:, :-1]*dt_in_gyr*(1.-frac_loss)
    return np.insert(np.cumsum(integrand, axis=1), 0, 0, axis=1)*1e9







