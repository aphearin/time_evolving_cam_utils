""" Functions used to collect the collection of binary files into a galaxy catalog.
"""
import numpy as np
from filename_utils import fname_generator
import os

default_root_dirname = ("/Users/aphearin/Dropbox/UniverseMachine/"
                        "data/binary_reductions/z0/binaries")


def assemble_catalog(scale_factor_string, **kwargs):
    # code goes here

    for propname in kwargs.keys():
        fname = propname_to_fname(propname)
        arr = np.load(fname)


def propname_to_fname(propname, dtype_string):
    dirname = propname
    basename = propname + '_data_' + str(np.dtype(dtype_string).type.__name__) + '.npy'
    return os.path.join(dirname, basename)

