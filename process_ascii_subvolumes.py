"""
"""
import gzip
import os
import numpy as np


def _compression_safe_opener(fname):
    """ Determine whether to use *open* or *gzip.open* to read
    the input file, depending on whether or not the file is compressed.
    """
    f = gzip.open(fname, 'r')
    try:
        f.read(1)
        opener = gzip.open
    except IOError:
        opener = open
    finally:
        f.close()
    return opener


def show_header(fname):
    opener = _compression_safe_opener(fname)
    with opener(fname, 'r') as f:
        raw_line = next(f)
        print(raw_line)


def sm_cut_raw_data_generator(fname, stellar_mass_index=10, logsm_cut=9.5):
    sm_cut = 10**logsm_cut
    opener = _compression_safe_opener(fname)
    with opener(fname, 'r') as f:
        while True:
            try:
                raw_line = next(f)
                if raw_line[0] != '#':
                    line = raw_line.strip().split()
                    if float(line[10]) >= sm_cut:
                        yield line
            except StopIteration:
                break


def infer_num_scales(fname, num_single_props=16, num_histories=6):

    opener = _compression_safe_opener(fname)
    with opener(fname, 'r') as f:
        while True:
            raw_line = next(f)
            if raw_line[0] != '#':
                line = raw_line.strip().split()
                num_cols_total = len(line)
                break
        return (num_cols_total - num_single_props) / num_histories


def history_array(raw_data_array, ihist, num_scales, num_single_props=16, num_histories=6):
    first_idx = num_single_props + ihist*num_scales
    last_idx = first_idx + num_scales
    return np.array(raw_data_array[:, first_idx:last_idx], dtype='f4')

