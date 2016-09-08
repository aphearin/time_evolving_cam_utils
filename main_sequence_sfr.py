"""
"""
import numpy as np
from scipy.stats.distributions import norm


def gaussian_random_from_uniform_random(unif, mean, sigma):
    """ Transform a length-*npts* array storing uniform random variables
    into an array storing values distributed as a gaussian.
    """
    return norm(loc=mean, scale=sigma).ppf(unif)


def get_fiducial_params():
    v_0, v_a, v_lna, v_z = 2.099, -0.652, -0.11, 0.899
    e_0, e_a, e_lna, e_z = 0.497, -2.895, -0.359, 3.681
    alpha_0, alpha_a, alpha_lna, alpha_z = -7.954, 5.622, 0.475, -2.899
    beta_0, beta_a, beta_z = 1.011, -11.374, 1.973
    gamma_0, gamma_a, gamma_z = -0.504, 3.038, -0.476
    delta_0 = 0.083
    return (v_0, v_a, v_lna, v_z, e_0, e_a, e_lna, e_z,
        alpha_0, alpha_a, alpha_lna, alpha_z,
        beta_0, beta_a, beta_z, gamma_0, gamma_a, gamma_z, delta_0)


def mean_sfr(vmax_at_mpeak, *params, **kwargs):
    try:
        redshift = kwargs['redshift']
    except KeyError:
        redshift = 0.

    if len(params) == 0:
        params = get_fiducial_params()
    v_0, v_a, v_lna, v_z, e_0, e_a, e_lna, e_z, alpha_0, alpha_a, alpha_lna, alpha_z, \
    beta_0, beta_a, beta_z, gamma_0, gamma_a, gamma_z, delta_0 = params

    vmax_characteristic = 10**_log10_vmax_characteristic(redshift, v_0, v_a, v_lna, v_z)
    # print("vmax_characteristic = {0}".format(vmax_characteristic))
    epsilon = 10**_log10_epsilon(redshift, e_0, e_a, e_lna, e_z)
    alpha = _alpha(redshift, alpha_0, alpha_a, alpha_lna, alpha_z)
    beta = _beta(redshift, beta_0, beta_a, beta_z)
    gamma = _gamma(redshift, gamma_0, gamma_a, gamma_z)
    delta = _delta(redshift, delta_0)

    nu = vmax_at_mpeak/vmax_characteristic
    # print("nu = {0}".format(nu))

    term1 = 1./(nu**alpha + nu**beta)
    # print("term1 = {0}".format(term1))

    exp_arg_numerator = np.log10(nu)**2
    exp_arg_denominator = 2*delta*delta
    # print("exp_arg_numerator = {0}".format(exp_arg_numerator))
    # print("exp_arg_denominator = {0}".format(exp_arg_denominator))
    term2 = gamma*np.exp(-exp_arg_numerator/exp_arg_denominator)
    # print("term2 = {0}".format(term2))

    return epsilon*(term1 + term2)


def _log10_vmax_characteristic(redshift, v_0, v_a, v_lna, v_z):
    a = 1 / (1+redshift)
    return v_0 +v_a*(a-1) - v_lna*np.log(a) + v_z*redshift


def _log10_epsilon(redshift, e_0, e_a, e_lna, e_z):
    a = 1 / (1+redshift)
    return e_0 +e_a*(a-1) - e_lna*np.log(a) + e_z*redshift


def _alpha(redshift, alpha_0, alpha_a, alpha_lna, alpha_z):
    a = 1 / (1+redshift)
    return alpha_0 +alpha_a*(a-1) - alpha_lna*np.log(a) + alpha_z*redshift


def _beta(redshift, beta_0, beta_a, beta_z):
    a = 1 / (1+redshift)
    return beta_0 +beta_a*(a-1) + beta_z*redshift


def _gamma(redshift, gamma_0, gamma_a, gamma_z):
    a = 1 / (1+redshift)
    result = gamma_0 +gamma_a*(a-1) + gamma_z*redshift
    return max(result, 0)


def _delta(redshift, delta_0):
    return delta_0

