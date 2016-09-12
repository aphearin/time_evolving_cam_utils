"""
"""
import os
import fnmatch


def fname_generator(input_dirname, filepat):
    """ Yield all the files in ``input_dirname`` with basenames matching
    the specified file pattern.
    """
    for path, dirlist, filelist in os.walk(input_dirname):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)


def parse_fname(fname, fname_prefix="sfh_catalog_", fname_suffix=".txt.gz"):
    """
    """
    basename = os.path.basename(fname)
    s = basename[len(fname_prefix):-len(fname_suffix)]
    filenum = int(s.split('.')[-1])
    scale_factor = float(''.join(s[:-len(str(filenum))-1]))
    return scale_factor, filenum
