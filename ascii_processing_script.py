""" Python script invoking the processing of raw ascii into binaries
for all three snapshots, z=0, z=1, z=2.
"""
from process_ascii_subvolumes import process_snapshot_into_binaries

print("\n\nBeginning to process z = 0 data into binaries\n")
scale_factor_string = "1.002310"
input_dirname = "/Volumes/NbodyDisk1/UniverseMachine/0909_ascii_catalogs/z0/orig_ascii_data"
output_dirname = "/Volumes/NbodyDisk1/UniverseMachine/0922_binaries/z0/binaries"
process_snapshot_into_binaries(input_dirname, scale_factor_string, output_dirname)

print("\n\nBeginning to process z = 1 data into binaries\n")
scale_factor_string = "0.501122"
input_dirname = "/Volumes/NbodyDisk1/UniverseMachine/0909_ascii_catalogs/z1/orig_ascii_data"
output_dirname = "/Volumes/NbodyDisk1/UniverseMachine/0922_binaries/z1/binaries"
process_snapshot_into_binaries(input_dirname, scale_factor_string, output_dirname)

print("\n\nBeginning to process z = 2 data into binaries\n")
scale_factor_string = "0.334060"
input_dirname = "/Volumes/NbodyDisk1/UniverseMachine/0909_ascii_catalogs/z2/orig_ascii_data"
output_dirname = "/Volumes/NbodyDisk1/UniverseMachine/0922_binaries/z2/binaries"
process_snapshot_into_binaries(input_dirname, scale_factor_string, output_dirname)

print("\n\n\a\a\a\a\a")
