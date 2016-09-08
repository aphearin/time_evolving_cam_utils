"""
"""
import numpy as np


def mean_sfr(stellar_mass, log10_median_ssfr=-11.8):
    return stellar_mass*10**log10_median_ssfr

