"""
"""
import numpy as np
from scipy.special import erf
from noisy_percentile import noisy_percentile


def main_sequence_designation(vmax_at_mpeak, subhalo_percentile, *params, **kwargs):
    """
    """
    try:
        seed = kwargs['seed']
    except KeyError:
        seed = None
    try:
        ms_designation_scatter = kwargs['ms_designation_scatter']
    except KeyError:
        ms_designation_scatter = 0.
    noisy_subhalo_percentile = noisy_percentile(subhalo_percentile,
        ms_designation_scatter, seed=seed)

    if len(params) == 0:
        params = get_fiducial_params()

    fq = quiescent_fraction(vmax_at_mpeak, *params, **kwargs)
    galaxy_is_on_main_sequence = np.where(fq > noisy_subhalo_percentile, 1, 0)

    return galaxy_is_on_main_sequence


def quiescent_fraction(vmax_at_mpeak, *params, **kwargs):
    """
    """
    if len(params) == 0:
        params = get_fiducial_params()
    qmin_0, qmin_a, vq_0, vq_a, vq_z, sigma_q_0, sigma_q_a, sigma_q_z = params

    try:
        redshift = kwargs['redshift']
    except KeyError:
        redshift = 0.

    vmax_characteristic = 10**_log10_vmax_characteristic(redshift, vq_0, vq_a, vq_z)
    sigma_quiescent = _sigma_quiescent(redshift, sigma_q_0, sigma_q_a, sigma_q_z)
    qmin = _qmin(redshift, qmin_0, qmin_a)

    numerator = np.log10(vmax_at_mpeak / vmax_characteristic)
    denominator = np.sqrt(2*sigma_quiescent)
    erf_term = 0.5 + 0.5*erf(numerator/denominator)
    result = np.atleast_1d(qmin + (1 - qmin)*erf_term)
    result = np.where(result < 0, 0, result)
    result = np.where(result > 1, 1, result)
    return result


def _qmin(redshift, qmin_0, qmin_a):
    """
    """
    a = 1 / (1+redshift)
    return qmin_0 + qmin_a*(a-1)


def _log10_vmax_characteristic(redshift, vq_0, vq_a, vq_z):
    """
    """
    a = 1 / (1+redshift)
    return vq_0 + vq_a*(a-1) + vq_z*redshift


def _sigma_quiescent(redshift, sigma_q_0, sigma_q_a, sigma_q_z):
    """
    """
    a = 1 / (1+redshift)
    return sigma_q_0 + sigma_q_a*(a-1) + sigma_q_z*redshift


def get_fiducial_params():
    qmin_0, qmin_a = -0.128, -0.015
    vq_0, vq_a, vq_z = 2.185, 0.272, 0.05
    sigma_q_0, sigma_q_a, sigma_q_z = 0.432, -0.89, 0.201
    return (qmin_0, qmin_a, vq_0, vq_a, vq_z, sigma_q_0, sigma_q_a, sigma_q_z)

