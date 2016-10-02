""" This module contains a convenience function for assembling together history data
and snapshot data into a unified astropy table.
"""
import os
import numpy as np
from astropy.table import Table
from halotools.utils import crossmatch

from assemble_catalog import assemble_catalog as assemble_history_data
from assemble_catalog import add_haloid_to_propnames
from halocat_binary_reduction import assemble_halocat, read_column_info_array


root_dropbox_dirname = "/Users/aphearin/Dropbox/UniverseMachine/data"


def collate_catalog(a_string, history_colnames=[], halocat_propnames=[],
        num_subvols=144, verbose=False, backsplash_cutoff=0.99):
    assert a_string in ('a_1.002310', )

    print("... Assembling history data")
    history_data_dirname = os.path.join(root_dropbox_dirname, 'binary_reductions',
        '0930', a_string)
    history_colnames = add_haloid_to_propnames(*history_colnames)
    history_data = Table(assemble_history_data(history_data_dirname, num_subvols, *history_colnames))

    print("... Assembling halo catalog data")
    halocat_scale_factor_string = get_halocat_scale_factor_string(a_string)
    halocat_binary_dirname = os.path.join(root_dropbox_dirname, 'halocat_snapshot',
        halocat_scale_factor_string)
    column_info_fname = os.path.join(os.path.dirname(halocat_binary_dirname), 'column_info.dat')
    column_info_array = read_column_info_array(column_info_fname)
    halocat_propnames = add_haloid_to_propnames(*halocat_propnames)
    halocat_data = assemble_halocat(halocat_binary_dirname, column_info_array, *halocat_propnames)

    if verbose:
        print("... Cross-matching on halo_id")
    idxA, idxB = crossmatch(history_data['halo_id'], halocat_data['halo_id'])
    if verbose:
        print("\nNumber of objects in history catalog = {0}".format(len(history_data)))
        print("Number of objects in halo catalog = {0}".format(len(halocat_data)))
        print("Number of matching objects = {0}".format(len(history_data['halo_id'][idxA])))
        matching_fraction = len(history_data['halo_id'][idxA])/float(len(history_data['halo_id']))
        print("Fraction of objects appearing in both catalogs = {0:.3f}".format(matching_fraction))
        msg = 'Less than 80% matches - probably indicating a bookkeeping inconsistency'
        assert matching_fraction > 0.8, msg

    new_colnames = list(set(halocat_propnames) - set(history_colnames))
    print("New colnames to add from halo catalog = {0}".format(new_colnames))
    for new_colname in new_colnames:
        new_dtype = halocat_data[new_colname].dtype
        history_data[new_colname] = np.zeros(len(history_data), dtype=new_dtype)
        history_data[new_colname][idxA] = halocat_data[new_colname][idxB]

    history_data['gal_type'] = np.empty(len(history_data), dtype='S10')

    is_orphan_mask = np.ones(len(history_data), dtype=bool)
    is_orphan_mask[idxA] = False
    is_central_mask = (history_data['halo_upid'] == -1)*(~is_orphan_mask)
    is_satellite_mask = (history_data['halo_upid'] != -1)*(~is_orphan_mask)
    history_data['gal_type'][is_orphan_mask] = 'orphan'
    history_data['gal_type'][is_central_mask] = 'central'
    history_data['gal_type'][is_satellite_mask] = 'satellite'
    if 'a_first_infall' in history_data.keys():
        scale_factor = get_scale_factor_value(a_string)
        is_backsplash_mask = is_central_mask*(history_data['a_first_infall'] < backsplash_cutoff*scale_factor)
        history_data['gal_type'][is_backsplash_mask] = 'backsplash'

    if verbose:
        print("\a")
    return history_data


def get_halocat_scale_factor_string(a_string):
    if a_string == 'a_1.002310':
        return 'a_1.00231'
    else:
        raise ValueError("Scale factor string ``{0}`` not recognized".format(a_string))


def get_scale_factor_value(a_string):
    return float(a_string[2:])



