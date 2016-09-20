"""
"""
import os

default_halocat_dirname = "/Users/aphearin/work/sims/bolplanck/halo_catalogs/halotools_v0p4"
default_halocat_basename = "hlist_0.08037.list.gz"
default_halocat_fname = os.path.join(default_halocat_dirname, default_halocat_basename)


def create_output_dir(halocat_fname=default_halocat_fname):
    output_base_dirname = os.path.dirname(halocat_fname)
    halocat_basename = os.path.basename(halocat_fname)
    try:
        # sanity check on string formatting
        first_idx, last_idx = len('hlist_'), -len('.list.gz')
        a = float(halocat_basename[first_idx:last_idx])
        assert a > 0.
    except:
        raise ValueError("halocat_fname basename {0} not formatted as expected".format(halocat_basename))

    a_substring = 'a' + halocat_basename[first_idx-1: last_idx]
    output_binaries_dirname = os.path.join(output_base_dirname, a_substring)
    try:
        os.makedirs(output_binaries_dirname)
    except OSError:
        pass

    return output_binaries_dirname
