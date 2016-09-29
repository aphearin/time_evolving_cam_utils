"""
"""
import gzip
import os
import numpy as np
import filename_utils
from time import time


#ID UPID Mpeak Mnow V@Mpeak Vnow Rvir Tidal_Tdyn Rank_DVmax(Z-score)
#Random_Rank(Z-score) SM ICL SFR Obs_SM Obs_SFR Obs_UV
#SFH(1..num_scales) ICLH(1..num_scales) SM_main_progenitor(1..num_scales)
#ICL_main_progenitor(1..num_scales) M_main_progenitor(1..num_scales) SFR_main_progenitor(1..num_scales)


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


def sm_cut_raw_data_generator(fname, stellar_mass_index=10, logsm_cut=9.):
    sm_cut = 10**logsm_cut
    opener = _compression_safe_opener(fname)
    with opener(fname, 'r') as f:
        while True:
            try:
                raw_line = next(f)
                if raw_line[0] != '#':
                    line = raw_line.strip().split()
                    if float(line[stellar_mass_index]) >= sm_cut:
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


def save_singleprop_binary(raw_data_array, output_subvol_dirname, idx, colname, dtype):
    """
    """
    dt = np.dtype(dtype)
    arr = np.array(raw_data_array[:, idx], dtype=dt)

    output_dirname = os.path.join(output_subvol_dirname, colname)
    try:
        os.makedirs(output_dirname)
    except OSError:
        pass
    output_basename = colname+'_data_'+str(arr.dtype.type.__name__)
    output_fname = os.path.join(output_dirname, output_basename)
    np.save(output_fname, arr)


def process_snapshot_into_binaries(input_dirname, scale_factor_string, output_dirname):
    """
    """
    start = time()
    filepat = filename_utils.fname_prefix + scale_factor_string + '*'
    for fname in filename_utils.fname_generator(input_dirname, filepat):
        print("Reducing {0} to a collection of Numpy binaries".format(os.path.basename(fname)))
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

        save_singleprop_binary(raw_data_array, output_subvol_dirname, 0, 'halo_id', 'i8')
        save_singleprop_binary(raw_data_array, output_subvol_dirname, 1, 'halo_upid', 'i8')
        save_singleprop_binary(raw_data_array, output_subvol_dirname, 2, 'halo_mpeak', 'f4')
        save_singleprop_binary(raw_data_array, output_subvol_dirname, 3, 'halo_mvir', 'f4')
        save_singleprop_binary(raw_data_array, output_subvol_dirname, 4, 'halo_vmax_at_mpeak', 'f4')
        save_singleprop_binary(raw_data_array, output_subvol_dirname, 5, 'halo_vmax', 'f4')
        save_singleprop_binary(raw_data_array, output_subvol_dirname, 7, 'halo_tidal_force', 'f4')
        save_singleprop_binary(raw_data_array, output_subvol_dirname, 10, 'stellar_mass', 'f4')
        save_singleprop_binary(raw_data_array, output_subvol_dirname, 12, 'sfr', 'f4')
        save_singleprop_binary(raw_data_array, output_subvol_dirname, 13, 'obs_stellar_mass', 'f4')
        save_singleprop_binary(raw_data_array, output_subvol_dirname, 14, 'obs_sfr', 'f4')

    end = time()
    print("Total runtime to reduce ascii to binares = {0:.1f} minutes".format(60.*(end-start)))
#ID UPID Mpeak Mnow V@Mpeak Vnow Rvir Tidal_Tdyn Rank_DVmax(Z-score)
#Random_Rank(Z-score) SM ICL SFR Obs_SM Obs_SFR Obs_UV




