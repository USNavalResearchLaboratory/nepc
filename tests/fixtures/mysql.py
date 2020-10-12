from nepc import nepc
from nepc.util import config
import pytest
import os


@pytest.fixture
def data_config(travis):
    if travis:
        NEPC_HOME = os.getcwd()
    else:
        NEPC_HOME = config.nepc_home()

    NEPC_DATA = NEPC_HOME + "/tests/data/"
    DIR_NAMES = [NEPC_HOME + "/tests/data/cs/lxcat/n2/fict/",
                 NEPC_HOME + "/tests/data/cs/lumped/n2/fict_total/"]
    yield [NEPC_DATA, DIR_NAMES]


@pytest.fixture
def nepc_connect(local, dbug, travis):
    """Establishes a connection with the nepc_test database

    Parameters
    ----------
    local : boolean
        Checks whether the database is locally based or based off
        of 'ppdadamsonlinux'
    dbug : boolean
        Checks whether debug mode is on or off

    Returns
    -------
    cnx : MySQLConnection
        A connection to the official NEPC MySQL database
    cursor : MySQLCursor
        A MySQLCursor object for executing SQL queries
    """
    if dbug:
        print("opening database connection")
    cnx, cursor = nepc.connect(local, dbug, test=True, travis=travis)
    yield [cnx, cursor]
    if dbug:
        print("closing database connection")
    cursor.close()
    cnx.close()
