"""Utility methods for the nepc module.

"""
import sys
import shutil
import os
from subprocess import check_output


def wc_fxn(file_to_count):
    """Return the number of lines in a file using the commandline utility ``wc``.

    """
    return int(check_output(["wc", "-l", file_to_count]).split()[0])


def get_size(obj, seen=None):
    """Recursively find the size of an object.

    """
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


def rmdir(outdir):
    """Try to remove a tree and raise an exception if this isn't possible.

    Parameters
    ----------
    outdir : str
        The directory to be removed.

    """
    try:
        shutil.rmtree(outdir)
    except OSError as exc:
        print("Error: %s - %s." % (exc.filename, exc.strerror))


def mkdir(outdir):
    """Try to make a directory and raise an exception if the directory already exists

    Parameters
    ----------
    outdir : str
        The directory to be made.

    """
    try:
        os.mkdir(outdir)
    except OSError as excep:
        print("Error: %s - %s." % (excep.filename, excep.strerror))
