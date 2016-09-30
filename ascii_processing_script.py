""" Python script processing ascii history data into binaries
"""
from time import time
from process_ascii_subvolumes import process_snapshot_into_binaries

start = time()
print("\n\nBeginning to process z = 2 data into binaries\n")
scale_factor_string = "0.334060"
input_dirname = "../orig_ascii_data/a_"+scale_factor_string
output_dirname = "../binaries/a_"+scale_factor_string
process_snapshot_into_binaries(input_dirname, scale_factor_string, output_dirname)
end = time()
runtime4 = (end - start)*60.
print("Total runtime to a = {0} ascii to binares = {1:.1f} minutes".format(scale_factor_string, runtime4))

start = time()
print("\n\nBeginning to process z = 0 data into binaries\n")
scale_factor_string = "1.002310"
input_dirname = "../orig_ascii_data/a_"+scale_factor_string
output_dirname = "../binaries/a_"+scale_factor_string
process_snapshot_into_binaries(input_dirname, scale_factor_string, output_dirname)
end = time()
runtime1 = (end - start)*60.
print("Total runtime to a = {0} ascii to binares = {1:.1f} minutes".format(scale_factor_string, runtime1))

start = time()
print("\n\nBeginning to process z = 0.1 data into binaries\n")
scale_factor_string = "0.911185"
input_dirname = "../orig_ascii_data/a_"+scale_factor_string
output_dirname = "../binaries/a_"+scale_factor_string
process_snapshot_into_binaries(input_dirname, scale_factor_string, output_dirname)
end = time()
runtime2 = (end - start)*60.
print("Total runtime to a = {0} ascii to binares = {1:.1f} minutes".format(scale_factor_string, runtime2))

start = time()
print("\n\nBeginning to process z = 1 data into binaries\n")
scale_factor_string = "0.501122"
input_dirname = "../orig_ascii_data/a_"+scale_factor_string
output_dirname = "../binaries/a_"+scale_factor_string
process_snapshot_into_binaries(input_dirname, scale_factor_string, output_dirname)
end = time()
runtime3 = (end - start)*60.
print("Total runtime to a = {0} ascii to binares = {1:.1f} minutes".format(scale_factor_string, runtime3))








