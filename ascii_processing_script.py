""" Python script processing ascii history data into binaries
"""
from time import time
from process_ascii_subvolumes import process_snapshot_into_binaries

start = time()
print("\n\nBeginning to process z = 0 data into binaries\n")
scale_factor_string = "1.002310"
input_dirname = "../orig_ascii_data/a_"+scale_factor_string
output_dirname = "../binaries/a_"+scale_factor_string
process_snapshot_into_binaries(input_dirname, scale_factor_string, output_dirname)
end = time()
runtime = (end - start)*60.
print("Total runtime to a = {0} ascii to binares = {1:.1f} minutes".format(scale_factor_string, runtime))
