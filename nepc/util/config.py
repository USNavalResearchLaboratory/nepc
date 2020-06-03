"""Get environment variables used by nepc scripts.
"""
import os


def user_home():
    """Returns the user's home directory.

    """
    return os.environ.get('HOME')


def nepc_home():
    """Returns the path to the nepc directory.

    """
    return os.environ.get('NEPC_HOME')


def nepc_cs_home():
    """Returns the path to the nepc_cs directory.

    """
    return os.environ.get('NEPC_CS_HOME')
