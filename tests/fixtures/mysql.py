from nepc import nepc
import pytest


@pytest.fixture
def nepc_connect(local, dbug):
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
    cnx, cursor = nepc.connect(local, dbug, test=True)
    yield [cnx, cursor]
    if dbug:
        print("closing database connection")
    cursor.close()
    cnx.close()
