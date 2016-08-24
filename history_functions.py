""" This module collects together functions that accept matrices of SFR histories
as input and return derived histories such as stellar mass growth, and
also summary statistics like quenching times.
"""
import numpy as np

fname="/Users/aphearin/Dropbox/UniverseMachine/data/histories/prelim_sfh_reduction/times.npy"
bolplanck_ages = np.load(fname)


def remaining_mass_fraction(t, t_form):
    """
    Fraction of mass lost during time interval dt due to passive evolution.

    Parameters
    ----------
    t : float
        Age of universe at the time for which the remaining mass fraction
        is to be calculated, in units of Gyr.

    t_form : array_like
        Length N array of times at which the stars were formed, in units of Gyr.
        All values of t_form should be less than t.

    Returns
    --------
    mass_fraction : array
        Length N array of the fraction of remaining mass.
    """
    return 1 - 0.05*np.log(1 + 1000.*(t - t_form)/1.4)


def stellar_mass_t_now(sfr_history, t_now, cosmic_age_array=bolplanck_ages):
    """
    """
    assert t_now > cosmic_age_array[0], "This function does not work for t_now < t_init"
    assert t_now < cosmic_age_array[-1], "This function does not work for t_now > today"

    idx_t_now = np.searchsorted(cosmic_age_array, t_now)
    sfh_matrix = np.insert(sfr_history[:, :idx_t_now+1], 0, sfr_history[:, 0], axis=1)
    t = np.append(np.insert(cosmic_age_array[:idx_t_now], 0, 0), t_now)

    sfh_midpoints_matrix = 0.5*(sfh_matrix[:, 1:] + sfh_matrix[:, :-1])
    dt = np.diff(t)
    frac_remaining = np.append(remaining_mass_fraction(t_now, t[1:-1]), 1.)
    return np.sum(sfh_midpoints_matrix * dt * frac_remaining, axis=1) * 1e9


def stellar_mass_histories(sfr_history):
    """
    """
    times = np.copy(bolplanck_ages)
    times[0] += 0.001
    times[-1] -= 0.001
    result = np.zeros_like(sfr_history)
    for idx, time in enumerate(times):
        result[:, idx] = stellar_mass_t_now(sfr_history, time)
    return result


def ssfr_histories(sfr_history, sm_history):
    """
    """
    ssfr_history = np.zeros_like(sfr_history)

    zero_mask = (sfr_history == 0) | (sm_history == 0)
    nzeros = len(sfr_history[zero_mask])
    ssfr_history[zero_mask] = np.random.normal(loc=-12, scale=0.3, size=nzeros)
    ssfr_history[~zero_mask] = np.log10(sfr_history[~zero_mask] / sm_history[~zero_mask])
    return ssfr_history


def ssfr_at_infall(sfr_history, sm_history, infall_times, cosmic_age_array=bolplanck_ages):
    """
    """
    ssfr_matrix = ssfr_histories(sfr_history, sm_history)
    idx_infall = np.searchsorted(cosmic_age_array, infall_times)
    return ssfr_matrix[np.arange(len(idx_infall)), idx_infall]



