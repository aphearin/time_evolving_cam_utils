""" Functions used to collect the collection of binary files into a galaxy catalog.
"""
import numpy as np
from filename_utils import fname_generator, subdir_generator
import os


default_root_dirname = "/Users/aphearin/work/UniverseMachine_data/0930_binaries/a_1.002310"
default_num_subvols = 144


def assemble_catalog(snapshot_root_dirname, num_subvols, *propnames):
    """
    Parameters
    -----------
    snapshot_root_dirname : string

    num_subvols : int

    propnames : sequence
    """
    propnames = add_haloid_to_propnames(*propnames)

    dt, num_gals = build_composite_dtype(snapshot_root_dirname, *propnames)

    arr = np.empty(num_gals, dtype=dt)
    for propname in propnames:
        dtype_string = infer_dtype_string_from_propname(snapshot_root_dirname, propname)
        arr[propname] = assemble_single_property_array(snapshot_root_dirname,
            propname, dtype_string, num_subvols)

    return arr


def build_composite_dtype(snapshot_root_dirname, *propnames):

    dtype_list = []
    ngals = 0
    for iprop, propname in enumerate(propnames):
        dtype_string = infer_dtype_string_from_propname(snapshot_root_dirname, propname)
        gen = subvol_fname_generator(snapshot_root_dirname, propname, dtype_string, default_num_subvols)
        for isubvol, subvol_fname in enumerate(gen):
            arr = np.load(subvol_fname)
            if isubvol == 0:
                dtype_list.append(
                    (propname, str(arr.dtype.type.__name__), arr.shape[1:])
                    )
            if iprop == 0:
                ngals += arr.shape[0]

    return np.dtype(dtype_list), ngals


def subvol_dirname_from_snapshot_root_dirname(snapshot_root_dirname, subvol_string=None):
    if subvol_string is not None:
        return os.path.join(snapshot_root_dirname, subvol_string)
    else:
        for subdirname in subdir_generator(snapshot_root_dirname, 'subvol_*'):
            break
        try:
            return subdirname
        except:
            raise NameError("sub-directory ``{0}`` does not exist".format(
                snapshot_root_dirname+'/subvol_*'))


def infer_dtype_string_from_propname(snapshot_root_dirname, propname):
    """
    """
    subvol_dirname = subvol_dirname_from_snapshot_root_dirname(snapshot_root_dirname)
    subdirname = os.path.join(subvol_dirname, propname)
    filepat = propname + '_data_*.npy'

    for fname in fname_generator(subdirname, filepat):
        first_idx = len(propname + '_data_')
        last_idx = -len('.npy')
        basename = os.path.basename(fname)
        dtype_string = basename[first_idx:last_idx]
        break

    try:
        return dtype_string
    except UnboundLocalError:
        raise ValueError("There are no directories detected that match \n"
            "subvol_dirname = {0}\npropname={1}".format(subvol_dirname, propname))


def assemble_single_property_array(snapshot_root_dirname, propname, dtype_string, num_subvols):

    for i, fname in enumerate(subvol_fname_generator(
            snapshot_root_dirname, propname, dtype_string, num_subvols)):

        new_subvol = np.load(fname)

        try:
            subvol_array = np.vstack([subvol_array, new_subvol])
        except NameError:
            subvol_array = np.load(fname)
        except ValueError:
            subvol_array = np.append(subvol_array, new_subvol)
    return subvol_array


def propname_to_basename(propname, dtype_string):
    basename = propname + '_data_' + str(np.dtype(dtype_string).type.__name__) + '.npy'
    return basename


def subvol_fname_generator(snapshot_root_dirname, propname, dtype_string, num_subvols):
    for isubvol in range(num_subvols):
        dirname = 'subvol_'+str(isubvol)
        basename = propname_to_basename(propname, dtype_string)
        yield os.path.join(snapshot_root_dirname, dirname, propname, basename)


def add_haloid_to_propnames(*propnames):
    propnames = list(propnames)
    propnames.insert(0, 'halo_id')
    propnames = list(set(propnames))
    propnames.insert(0, propnames.pop(propnames.index('halo_id')))
    return propnames
