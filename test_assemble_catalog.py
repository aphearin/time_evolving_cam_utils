"""
"""
import os
import numpy as np
import assemble_catalog

snapshot_root_dirname = assemble_catalog.default_root_dirname


def test_assemble_catalog():
    num_subvols = assemble_catalog.default_num_subvols
    cat = assemble_catalog.assemble_catalog(snapshot_root_dirname, num_subvols, 'halo_id')
    assert 'halo_id' in cat.dtype.names
    assert len(cat) > 1e5


def test_subvol_dirname_from_snapshot_root_dirname():
    subvol_dirname = assemble_catalog.subvol_dirname_from_snapshot_root_dirname(
        snapshot_root_dirname)
    assert os.path.basename(subvol_dirname) == 'subvol_0'


def test_infer_dtype_string_from_propname():
    propname = 'halo_mpeak'
    dtype_string = assemble_catalog.infer_dtype_string_from_propname(snapshot_root_dirname, propname)
    assert dtype_string == 'float32'


def test_build_composite_dtype():
    dt, num_gals = assemble_catalog.build_composite_dtype(snapshot_root_dirname, 'halo_id')
    assert dt == np.dtype([('halo_id', 'i8')])
    assert num_gals > 1e5
