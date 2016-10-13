"""
"""


def calculate_null_hypothesis(backsplash_fraction, backsplash_mean,
        true_central_fraction, true_central_mean,
        satellite_fraction, satellite_mean):
    result = (backsplash_mean*backsplash_fraction +
                satellite_mean*satellite_fraction +
                true_central_mean*true_central_fraction)
    return result
