"""
"""
import os
import numpy as np
from astropy.table import Table
from process_ascii_subvolumes import _compression_safe_opener


default_halocat_dirname = "/Users/aphearin/work/sims/bolplanck/halo_catalogs/halotools_v0p4"
default_halocat_basename = "hlist_0.08037.list.gz"
default_halocat_fname = os.path.join(default_halocat_dirname, default_halocat_basename)

default_column_info_fname = os.path.join(default_halocat_dirname, "column_info.dat")


def create_output_dir(halocat_fname=default_halocat_fname, output_base_dirname=None):
    if output_base_dirname is None:
        output_base_dirname = os.path.dirname(halocat_fname)

    halocat_basename = os.path.basename(halocat_fname)
    try:
        # sanity check on string formatting
        first_idx, last_idx = len('hlist_'), -len('.list.gz')
        a = float(halocat_basename[first_idx:last_idx])
        assert a > 0.
    except:
        raise ValueError("halocat_fname basename {0} not formatted as expected".format(halocat_basename))

    a_substring = 'a' + halocat_basename[first_idx-1: last_idx]
    output_binaries_dirname = os.path.join(output_base_dirname, a_substring)
    try:
        os.makedirs(output_binaries_dirname)
    except OSError:
        pass

    return output_binaries_dirname


def read_column_info_array(column_info_fname=default_column_info_fname):
    column_info_array = Table.read(column_info_fname, format='ascii.commented_header')
    return column_info_array.as_array()


def get_column_info(colname, column_info_array):
    idx = np.where(column_info_array['colname'] == colname)[0]
    try:
        dt = column_info_array['coltype'][idx][0]
        assert len(idx) == 1
    except AssertionError:
        raise AssertionError("detected multiple columns names ``{0}``".format(colname))
    except IndexError:
        raise IndexError("column name ``{0}`` not available".format(colname))
    return idx[0], dt


def build_composite_dt(column_info_array, *colnames):
    assert 'halo_id' in column_info_array['colname'], "``halo_id`` is a required column name"

    colnames = add_haloid_to_propnames(*colnames)

    try:
        assert len(colnames) == len(set(colnames))
    except AssertionError:
        raise AssertionError("Input ``colnames`` sequence contains repeated elements")
    dt_list = []
    idx_list = []
    for colname in colnames:
        idx, dt = get_column_info(colname, column_info_array)
        dt_list.append((colname, dt))
        idx_list.append(idx)

    idx_sorted = np.argsort(idx_list)
    dt_list = [tuple(x) for x in np.array(dt_list)[idx_sorted]]
    return np.dtype(dt_list)


def get_index_list(dt, column_info_array):
    idx_list = []
    for colname in dt.names:
        idx, dt = get_column_info(colname, column_info_array)
        idx_list.append(idx)
    return idx_list


def row_generator(fname, column_info_array, *colnames):
    idx_list = get_index_list(build_composite_dt(column_info_array, *colnames), column_info_array)
    opener = _compression_safe_opener(fname)
    with opener(fname, 'r') as f:
        for raw_line in f:
            if raw_line[0] != '#':
                yield tuple(s for i, s in enumerate(raw_line.strip().split()) if i in idx_list)


def read_structured_array_from_ascii(fname, column_info_array, *colnames):
    dt = build_composite_dt(column_info_array, *colnames)
    return np.array(list(row_generator(fname, column_info_array, *colnames)), dtype=dt)


def get_dtype_string(dt):
    return str(dt.type.__name__)


def get_binary_basename_from_colname(colname, column_info_array):
    dt = column_info_array['coltype'][column_info_array['colname']==colname][0]

    dtype_string = get_dtype_string(np.dtype(dt))
    return colname+'_data_' + dtype_string


def save_structured_array_columns(arr, column_info_array, output_root_dirname, *colnames):
    for colname in colnames:
        output_dirname = os.path.join(output_root_dirname, colname)
        try:
            os.makedirs(output_dirname)
        except OSError:
            pass
        output_basename = get_binary_basename_from_colname(colname, column_info_array)
        output_fname = os.path.join(output_dirname, output_basename)
        np.save(output_fname, arr[colname])


def add_haloid_to_propnames(*propnames):
    propnames = list(propnames)
    propnames.insert(0, 'halo_id')
    propnames = list(set(propnames))
    propnames.insert(0, propnames.pop(propnames.index('halo_id')))
    return propnames


def assemble_halocat(snapshot_root_dirname, column_info_array, *propnames):
    binary_basename = get_binary_basename_from_colname('halo_id', column_info_array)
    halo_id_fname = os.path.join(snapshot_root_dirname, 'halo_id', binary_basename)
    num_gals = len(np.load(halo_id_fname+'.npy'))
    propnames = add_haloid_to_propnames(*propnames)
    dt = build_composite_dt(column_info_array, *propnames)

    arr = np.empty(num_gals, dtype=dt)
    for propname in propnames:
        basename = get_binary_basename_from_colname(propname, column_info_array)
        fname = os.path.join(snapshot_root_dirname, propname, basename+'.npy')
        arr[propname] = np.load(fname)

    return arr
