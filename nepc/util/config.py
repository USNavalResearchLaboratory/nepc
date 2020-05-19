"""Contains shortcuts to path directories that can be
used throughout nepc"""
import os


def user_home():
    """Returns the user's home directory"""
    return os.environ.get('HOME')


def nepc_home():
    """Returns the path to the NEPC directory"""
    return os.environ.get('NEPC_HOME')


def nepc_data_home():
    """Returns the path to the NEPC data directory"""
    return os.environ.get('NEPC_DATA_HOME')
