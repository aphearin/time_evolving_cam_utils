""" Utility functions for reading in star formation histories
in the ASCII format provided by Peter Behroozi
"""
import numpy as np
import os
from lookback_time import lookback_time

fname="/Users/aphearin/Dropbox/UniverseMachine/data/histories/small_sfh_catalog_1.002310.txt"


def get_num_total_lines(fname):
    """
    """
    with open(fname) as f:
        for num_lines_tot, raw_line in enumerate(f):
            pass
    return num_lines_tot


def get_num_header_lines(fname):
    """
    """
    num_header_lines = 0
    with open(fname) as f:
        for i, raw_line in enumerate(f):
            if raw_line[0] == '#':
                num_header_lines += 1
            else:
                break
    return num_header_lines


def get_header(fname):
    header = []
    with open(fname) as f:
        for i, raw_line in enumerate(f):
            if raw_line[0] == '#':
                header.append(raw_line)
            else:
                break
    return header


def get_scales(fname):
    """
    """
    with open(fname) as f:
        __ = f.readline()
        __ = f.readline()
        __ = f.readline()
        scale_list = [float(a) for a in f.readline().strip()[13:].split(' ')]
    return np.array(scale_list)


def get_num_scales(fname):
    """
    """
    header_length = get_num_header_lines(fname)
    header = []
    with open(fname) as f:
        for __ in range(header_length):
            header.append(next(f).strip().replace('#', ''))
    num_scales = int(header[2][12:])

    return num_scales


def filename_string_generator(num_files, prefix='', suffix=''):
    num_files = int(num_files)
    str_num_files = str(num_files)
    formatter = "{:0" + str(len(str_num_files)) + "d}"
    for i in range(num_files):
        yield prefix + "_" + formatter.format(i) + suffix


def get_colnames(fname):
    """
    """
    with open(fname) as f:
        colnames = [s.lower() for s in f.readline().strip().split(' ')]
        __ = f.readline()
        __ = f.readline()
        __ = np.array([float(s) for s in f.readline()[13:].strip().split(' ')])
    colnames[0] = 'id'
    colnames[4] = 'vmax_mpeak'
    colnames[8] = 'rank_rank_dvmax_zscore'
    colnames[9] = 'random_rank_zscore'
    colnames = colnames[:-2]

    num_scales = get_num_scales(fname)
    sfh_colnames_list = list(filename_string_generator(num_scales, prefix='sfh', suffix=''))
    colnames.extend(sfh_colnames_list)
    iclh_colnames_list = list(filename_string_generator(num_scales, prefix='iclh', suffix=''))
    colnames.extend(iclh_colnames_list)

    return colnames


def get_dt_list(fname):
    """
    """
    colnames = get_colnames(fname)
    f = ['i8', 'i8'] + list('f4' for i in range(len(colnames)-2))
    return [(a, b) for a, b in zip(colnames, f)]


def get_history_indices(colnames, num_scales, history='sfh'):
    """
    """
    if history=='sfh':
        first_sfh_index = colnames.index('sfh_000')
        last_sfh_index = first_sfh_index + num_scales
        indices = list(range(first_sfh_index, last_sfh_index))
        history_colnames = colnames[first_sfh_index:last_sfh_index]
        return indices, history_colnames
    elif history=='iclh':
        first_iclh_index = colnames.index('iclh_000')
        last_iclh_index = first_iclh_index + num_scales
        indices = list(range(first_iclh_index, last_iclh_index))
        history_colnames = colnames[first_iclh_index:last_iclh_index]
        return indices, history_colnames
    else:
        raise ValueError("Input ``history`` should be either ``sfh`` or ``iclh``")


def reduced_history_generator(fname, stellar_mass_cut,
            additional_colnames_to_keep=['id', 'sm', 'sfr'], history='sfh'):
    """
    """
    num_header_lines = get_num_header_lines(fname)
    num_total_lines = get_num_total_lines(fname)
    num_scales = get_num_scales(fname)
    colnames = get_colnames(fname)

    column_indices_to_yield = [colnames.index(s) for s in additional_colnames_to_keep]
    history_indices, history_colnames = get_history_indices(colnames, num_scales, history=history)
    column_indices_to_yield.extend(history_indices)

    colnames_to_keep = additional_colnames_to_keep
    colnames_to_keep.extend(history_colnames)

    stellar_mass_index = colnames.index('sm')

    with open(fname) as f:

        for i in range(num_header_lines):
            raw_line = f.readline()
            if i == 0:
                alternate_first_line = '#' + ' '.join(colnames_to_keep) + '\n'
                yield alternate_first_line
            else:
                yield raw_line

        for i in range(num_total_lines - num_header_lines):
            raw_line = f.readline()
            if raw_line[0] == '#':
                pass
            else:
                line = raw_line.strip().split(' ')
                sm = float(line[stellar_mass_index])
                if sm > stellar_mass_cut:
                    yield ' '.join(line[c] for c in column_indices_to_yield) + '\n'


def write_reduced_history(fname, stellar_mass_cut, output_fname, **kwargs):
    """
    """
    generator = reduced_history_generator(fname, stellar_mass_cut, **kwargs)

    with open(output_fname, 'wb') as fout:

        for line in generator:
            fout.write(line)


def get_reduced_filename(fname, stellar_mass_cut, **kwargs):
    """
    """
    history = kwargs.get('history', 'sfh')
    dirname = kwargs.get('output_dirname', os.path.dirname(fname))

    basename = os.path.basename(fname)
    sm_string = "smcut_{0:.2f}".format(np.log10(stellar_mass_cut))
    new_basename = basename[:-4] + '_' + sm_string + '_' + history + '.txt'

    output_fname = os.path.join(dirname, new_basename)
    return output_fname

scale_factor_array = get_scales(fname)
times = lookback_time(scale_factor_array)
