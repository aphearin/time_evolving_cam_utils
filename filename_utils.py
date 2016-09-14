"""
"""
import os
import fnmatch

fname_prefix="sfh_catalog_"
fname_suffix=".txt.gz"


def fname_generator(input_dirname, filepat):
    """ Search through all the files in the full directory tree of ``input_dirname``
    for files with basenames matching the specified file pattern.
    """
    for path, dirlist, filelist in os.walk(input_dirname):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)


def subdir_generator(input_dirname, filepat):
    """ Search through the input_dirname and yield the name of
    any subdirectory whose name matches the specified file pattern.
    """
    for path, dirlist, filelist in os.walk(input_dirname):
        for subdirname in fnmatch.filter(dirlist, filepat):
            yield os.path.join(input_dirname, subdirname)


def parse_fname(fname, fname_prefix=fname_prefix, fname_suffix=fname_suffix):
    """
    """
    basename = os.path.basename(fname)
    s = basename[len(fname_prefix):-len(fname_suffix)]
    filenum = int(s.split('.')[-1])
    scale_factor = float(''.join(s[:-len(str(filenum))-1]))
    return scale_factor, filenum
