"""
"""
import os
import argparse
import halocat_binary_reduction

parser = argparse.ArgumentParser()

parser.add_argument("halocat_fname", type=str,
    help="Absolute path to the hlist file storing the halo catalog ascii data")

parser.add_argument("output_dirname", type=str,
    help="Absolute path to the directory where the binaries will be stored")

parser.add_argument("colnames", nargs='*',
    help="Name(s) of the columns to reduce to binaries. "
    "Each entry must appear in the corresponding column_info.dat file. "
    "One of the column names must be ``halo_id``.")

args = parser.parse_args()

assert os.path.isfile(args.halocat_fname), "Input ``halocat_fname`` does not exist"

halocat_dirname = os.path.dirname(args.halocat_fname)
column_info_basename = 'column_info.dat'
column_info_fname = os.path.join(halocat_dirname, column_info_basename)
column_info_array = halocat_binary_reduction.read_column_info_array(column_info_fname)

arr = halocat_binary_reduction.read_structured_array_from_ascii(
    args.halocat_fname, column_info_array, *args.colnames)
print("Number of galaxies = {0}".format(len(arr)))

snapshot_root_dirname = halocat_binary_reduction.create_output_dir(
    args.halocat_fname, output_base_dirname=args.output_dirname)

halocat_binary_reduction.save_structured_array_columns(
    arr, column_info_array, snapshot_root_dirname, *args.colnames)
print("\n\a\aLocation of halo catalog binaries = {0}\n".format(snapshot_root_dirname))

