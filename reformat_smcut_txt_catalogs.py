""" Functions used to transform the ascii data output of the
reduce_sfh_ascii.py script into an hdf5 binary with
columns that have multi-dimensional arrays of formation history information.
"""
import os
import numpy as np
from astropy.table import Table
from read_sfh import get_history_indices, get_num_scales


def history_ascii_to_hdf5(ascii_fname, output_fname, history='sfh'):
    """
    """
    t = Table.read(ascii_fname, format='ascii.commented_header')

    sfh_keylist = list(key for key in t.keys() if history in key)
    remaining_keylist = list(key for key in t.keys() if history not in key)

    m = np.zeros((len(t), len(sfh_keylist)))
    for i in range(len(sfh_keylist)):
        m[:, i] = np.copy(t[sfh_keylist[i]].data)

    result = Table()
    for key in remaining_keylist:
        result[key] = t[key]
    result[history] = m

    result.sort('id')
    result.write(output_fname, path='data')


def produce_collated_history_hdf5(sfh_ascii_fname, iclh_ascii_fname, output_fname):
    """
    """
    history_ascii_to_hdf5(sfh_ascii_fname, 'tmp.sfh.hdf5', history='sfh')
    history_ascii_to_hdf5(iclh_ascii_fname, 'tmp.iclh.hdf5', history='iclh')
    t1 = Table.read('tmp.sfh.hdf5', path='data')
    t2 = Table.read('tmp.iclh.hdf5', path='data')
    t1['iclh'] = t2['iclh']
    t1.write(output_fname, path='data')
    os.remove('tmp.sfh.hdf5')
    os.remove('tmp.iclh.hdf5')



