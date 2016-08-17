""" Command line script to write reduced versions of sfh ascii data
"""
import os
import read_sfh
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("fname", type=str,
    help="Filename storing the entire sfh file")

parser.add_argument("log10_sm_cut", type=float,
    help="stellar mass cut in log10 units")

parser.add_argument("-output_dirname",
    help="Disk location to store the reduced catalog. Default is same directory as input file.",
    default=None, type=str)

parser.add_argument("-history",
    help="star-formation vs. ICL history. Default is sfh.",
    choices=['sfh', 'iclh'], default='sfh', type=str)


args = parser.parse_args()
stellar_mass_cut = 10**args.log10_sm_cut
if args.output_dirname is None:
    output_dirname = os.path.dirname(args.fname)
else:
    output_dirname = args.output_dirname
history = args.history
input_fname = args.fname

output_fname = read_sfh.get_reduced_filename(input_fname, stellar_mass_cut,
        output_dirname=output_dirname, history=history)
read_sfh.write_reduced_history(input_fname, stellar_mass_cut, output_fname, history=history)
