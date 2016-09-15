"""
"""
import os
import assemble_catalog


def test_assemble_catalog():
    snapshot_root_dirname = assemble_catalog.default_root_dirname
    num_subvols = assemble_catalog.default_num_subvols
    cat = assemble_catalog.assemble_catalog(snapshot_root_dirname, num_subvols, 'halo_id')


def test_subvol_dirname_from_snapshot_root_dirname():
    snapshot_root_dirname = assemble_catalog.default_root_dirname
    subvol_dirname = assemble_catalog.subvol_dirname_from_snapshot_root_dirname(
        snapshot_root_dirname)
    assert os.path.basename(subvol_dirname) == 'subvol_0'
