""" Functions used to transform the ascii data output of the
reduce_sfh_ascii.py script into an hdf5 binary with
columns that have multi-dimensional arrays of formation history information.
"""
import numpy as np
from astropy.table import Table
from read_sfh import get_history_indices, get_num_scales


def history_ascii_to_hdf5(ascii_fname, output_fname, history='sfh'):
    """
    """
    t = Table.read(ascii_fname, format='ascii.commented_header')

    sfh_keylist = list(key for key in t.keys() if key[0:3]==history)
    remaining_keylist = list(key for key in t.keys() if key[0:3]!=history)

    m = np.zeros((len(t), len(sfh_keylist)))
    for i in range(len(sfh_keylist)):
        m[:, i] = np.copy(t[sfh_keylist[i]].data)

    result = Table()
    for key in remaining_keylist:
        result[key] = t[key]
    result[history] = m

    result.write(output_fname, path='data')




