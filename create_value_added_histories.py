""" This module starts from the formatted_histories hdf5 file,
adds a M* history column called 'smh',
cross-matches against the halotools halocat
to add a few useful columns like upid, host mass and cosmic time of accretion,
throws away all model galaxies without matches in the halo catalog,
and writes the value-added catalog to disk.

"""
import numpy as np
from astropy.cosmology import Planck13
import os
from astropy.table import Table
from halotools.sim_manager import CachedHaloCatalog
from history_functions import stellar_mass_histories
from halotools.utils import crossmatch


def retrieve_formatted_histories_hdf5():
    print("Loading formatted histories into memory")
    dirname = "/Users/aphearin/Dropbox/UniverseMachine/data/histories/prelim_sfh_reduction"
    history_fname = "sfh_catalog_1.002310_smcut_9.50_formatted_histories.hdf5"
    histories = Table.read(os.path.join(dirname, history_fname), path='data')
    return histories


def cross_match_against_halocat(histories, halocat):
    """
    """
    print("cross-matching against the halo catalog")
    histories['upid'] = 0L
    histories['tidal_force_tdyn'] = 0.
    histories['mvir_host_halo'] = 0.
    histories['dmvir_dt_tdyn'] = 0.

    idxA, idxB = crossmatch(histories['id'], halocat.halo_table['halo_id'])
    histories['upid'][idxA] = halocat.halo_table['halo_upid'][idxB]
    histories['tidal_force_tdyn'][idxA] = halocat.halo_table['halo_tidal_force_tdyn'][idxB]
    histories['mvir_host_halo'][idxA] = halocat.halo_table['halo_mvir_host_halo'][idxB]
    histories['dmvir_dt_tdyn'][idxA] = halocat.halo_table['halo_dmvir_dt_tdyn'][idxB]


def add_accretion_times(histories, halocat):
    print("Calculating accretion times using shockingly slow Astropy cosmology.ages function")

    idxA, idxB = crossmatch(histories['id'], halocat.halo_table['halo_id'])

    histories['time_first_acc'] = 0.
    histories['time_last_acc'] = 0.

    z_last_acc = 1./halocat.halo_table['halo_scale_factor_lastacc'][idxB] - 1.
    z_last_acc[z_last_acc<0] = 0.

    age_last_acc = np.zeros_like(z_last_acc)
    age_last_acc[z_last_acc==0] = Planck13.age(0)
    age_last_acc[z_last_acc!=0] = Planck13.age(z_last_acc[z_last_acc!=0])

    histories['time_last_acc'][idxA] = age_last_acc

    z_first_acc = 1./halocat.halo_table['halo_scale_factor_firstacc'][idxB] - 1.
    z_first_acc[z_first_acc<0] = 0.

    age_first_acc = np.zeros_like(z_first_acc)
    age_first_acc[z_first_acc==0] = Planck13.age(0)
    age_first_acc[z_first_acc!=0] = Planck13.age(z_first_acc[z_first_acc!=0])

    histories['time_first_acc'][idxA] = age_first_acc


histories = retrieve_formatted_histories_hdf5()

print("Calculating stellar mass histories")
histories['smh'] = stellar_mass_histories(histories['sfh'])

halocat = CachedHaloCatalog(simname='bolplanck')
cross_match_against_halocat(histories, halocat)

add_accretion_times(histories, halocat)

histories = histories[histories['upid']!=0]

dirname = "/Users/aphearin/Dropbox/UniverseMachine/data/histories/prelim_sfh_reduction"
basename = "sfh_catalog_1.002310_smcut_9.50_value_added_histories.hdf5"
histories.write(os.path.join(dirname, basename), path='data')
