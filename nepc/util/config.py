"""Get environment variables used by nepc scripts.
"""
import os


def user_home():
    """Returns the user's home directory.

    """
    return os.environ.get('HOME')


def production():
    """Returns the I.P. address or URL of the production server stored in the NEPC_PRODUCTION environment variable.

    """
    return os.environ.get('NEPC_PRODUCTION')


def nepc_home():
    """Returns the path to the nepc directory stored in the NEPC_HOME environment variable.

    """
    return os.environ.get('NEPC_HOME')


def nepc_cs_home():
    """Returns the path to the nepc_cs directory stored in NEPC_CS_HOME environment variable.

    """
    return os.environ.get('NEPC_CS_HOME')
