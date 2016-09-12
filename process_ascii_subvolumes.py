"""
"""
import gzip
import os
import numpy as np
import filename_utils


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


def save_history_binary(raw_data_array, idx, colname, output_subvol_dirname, num_scales):
    """
    """
    arr = history_array(raw_data_array, idx, num_scales)
    output_dirname = os.path.join(output_subvol_dirname, colname)
    try:
        os.makedirs(output_dirname)
    except OSError:
        pass
    output_basename = colname+'_data_float32'
    output_fname = os.path.join(output_dirname, output_basename)
    np.save(output_fname, arr)


def process_snapshot_into_binaries(input_dirname, scale_factor_string, output_dirname):
    """
    """
    filepat = filename_utils.fname_prefix + scale_factor_string + '*'
    for fname in filename_utils.fname_generator(input_dirname, filepat):
        num_scales = infer_num_scales(fname)
        raw_data_array = np.array(list(sm_cut_raw_data_generator(fname)))

        scale_factor, filenum = filename_utils.parse_fname(fname)
        output_subvol_dirname = os.path.join(output_dirname, 'subvol_'+str(filenum))

        save_history_binary(raw_data_array, 0, 'sfh', output_subvol_dirname, num_scales)
        save_history_binary(raw_data_array, 1, 'iclh', output_subvol_dirname, num_scales)
        save_history_binary(raw_data_array, 2, 'sm_mp', output_subvol_dirname, num_scales)
        save_history_binary(raw_data_array, 3, 'icl_mp', output_subvol_dirname, num_scales)
        save_history_binary(raw_data_array, 4, 'mpeak_mp', output_subvol_dirname, num_scales)
        save_history_binary(raw_data_array, 5, 'sfr_mp', output_subvol_dirname, num_scales)
