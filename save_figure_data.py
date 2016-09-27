""" This module stores functions used to output data points used in publication plots
"""
import os
import numpy as np


def save_figure_data(root_dirname, figname, curve_data, curve_name):
    save_figure_npy_binary(root_dirname, figname, curve_data, curve_name)
    save_figure_ascii(root_dirname, figname, curve_data, curve_name)


def save_figure_npy_binary(root_dirname, figname, curve_data, curve_name):
    try:
        os.makedirs(os.path.join(root_dirname, figname))
    except OSError:
        pass
    output_fname = os.path.join(root_dirname, figname, curve_name)
    np.save(output_fname, curve_data)
    return output_fname + '.npy'


def save_figure_ascii(root_dirname, figname, curve_data, curve_name):
    pass
