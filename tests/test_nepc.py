"""Tests whether the functions of nepc.py work as intended"""
import pandas as pd
import mysql.connector
import pytest
from nepc import nepc


# The following is from a failed attempt to use pytest_mysql
# def test_mysql_nepc_proc(mysql_nepc_proc):
#     """Check server fixture factory works."""
#     assert mysql_nepc_proc.running()


#     e_energy, sigma = nepc.cs_e_sigma(cursor, 1)
#     cs_dict = nepc.cs_dict_constructor(metadata, e_energy, sigma)
#     angus = nepc.model(cursor, "angus")
#
#
# def teardown_module(module):

# TODO: refactor into a testing module
# TODO: setup database connection once for the session using a pytest fixture
def nepc_connect(local, dbug):
    """Establishes a connection with the NEPC database

    Parameters
    ----------
    local : boolean
    Checks whether the database is locally based or based off of 'ppdadamsonlinux'
    dbug : boolean
    Checks whether debug mode is on or off

    Returns
    -------
    cnx : MySQLConnection
    A connection to the official NEPC MySQL database
    cursor : MySQLCursor
    A MySQLCursor object for executing SQL queries"""
    cnx, cursor = nepc.connect(local, dbug)
    return cnx, cursor


def test_connect(local, dbug):
    """Verify that nepc.connect() method connects to the NEPC
    database when local is True and when local is False"""
    if local is False:
        cnx, cursor = nepc.connect(local=False, DBUG=dbug)
        assert isinstance(cnx, mysql.connector.connection.MySQLConnection)
        assert isinstance(cnx, mysql.connector.cursor.MySQLCursor)
        cursor.close()
        cnx.close()
    cnx, cursor = nepc.connect(local=True, DBUG=dbug)
    assert isinstance(cnx, mysql.connector.connection.MySQLConnection)
    assert isinstance(cnx, mysql.connector.cursor.MySQLCursor)
    cursor.close()
    cnx.close()


def test_count_table_rows(local, dbug):
    """Verify that nepc.count_table_rows returns an integer value"""
    cnx, cursor = nepc_connect(local, dbug)
    rows = nepc.count_table_rows(cursor, "species")
    assert isinstance(rows, int)
    cursor.close()
    cnx.close()


def test_cs_e_sigma(local, dbug):
    """Verify that nepc.cs_e_sigma returns
    proper formats for the e_energy and sigma values"""
    cnx, cursor = nepc_connect(local, dbug)
    e_energy, sigma = nepc.cs_e_sigma(cursor, 1)
    assert isinstance(e_energy, list)
    assert isinstance(sigma, list)
    assert isinstance(e_energy[0], float)
    assert isinstance(sigma[0], float)
    cursor.close()
    cnx.close()


def test_cs_metadata(local, dbug):
    """Verify that nepc.cs_metadata returns the
    metadata as a list containing an int
    in the first index, a str in the second index,
    and a float in the fourth index"""
    cnx, cursor = nepc_connect(local, dbug)
    metadata = nepc.cs_metadata(cursor, 1)
    assert isinstance(metadata, list)
    assert isinstance(metadata[0], int)
    assert isinstance(metadata[1], str)
    assert isinstance(metadata[3], float)
    cursor.close()
    cnx.close()


def test_cs_dict_constructor(local, dbug):
    """Verify that nepc.cs_dict_constructor
    makes a dictionary out of the three terms as
    parameters, and that each term is represented
    in its accurate format"""
    cnx, cursor = nepc_connect(local, dbug)
    metadata = nepc.cs_metadata(cursor, 1)
    e_energy, sigma = nepc.cs_e_sigma(cursor, 1)
    cs_dict = nepc.cs_dict_constructor(metadata, e_energy, sigma)
    assert isinstance(cs_dict, dict)
    assert isinstance(cs_dict["cs_id"], int)
    assert isinstance(cs_dict["specie"], str)
    assert isinstance(cs_dict["units_e"], float)
    assert isinstance(cs_dict["e"], list)
    assert isinstance(cs_dict["e"], float)
    cursor.close()
    cnx.close()


# TODO: make this test complete
def test_model(local, dbug):
    """Verify nepc returns a model."""
    cnx, cursor = nepc_connect(local, dbug)
    angus = nepc.model(cursor, "angus")
    assert isinstance(angus, list)
    assert isinstance(angus[0], dict)
    assert isinstance(angus[0]["cs_id"], int)
    assert isinstance(angus[0]["specie"], str)
    assert isinstance(angus[0]["units_e"], float)
    assert isinstance(angus[0]["e"], list)
    assert isinstance(angus[0]["e"][0], float)
    cursor.close()
    cnx.close()


def test_table_as_df(local, dbug):
    """Verify when nepc.table_as_df is called it 
    returns a DataFrame copy of what is included in the
    table used as an argument"""
    cnx, cursor = nepc_connect(local, dbug)
    statef = nepc.table_as_df(cursor, "states")
    assert isinstance(statef, pd.DataFrame)
    processf = nepc.table_as_df(cursor, "processes", columns=["id", "name"])
    assert isinstance(processf, pd.DataFrame)
    cursor.close()
    cnx.close()


def test_reaction_latex(local, dbug):
    """Verify when nepc.reaction_latex is called it
    returns a string representing the LaTeX
    for the reaction from a nepc cross section"""
    cnx, cursor = nepc_connect(local, dbug)
    metadata = nepc.cs_metadata(cursor, 1)
    e_energy, sigma = nepc.cs_e_sigma(cursor, 1)
    cs_dict = nepc.cs_dict_constructor(metadata, e_energy, sigma)
    angus = nepc.model(cursor, "angus")
    assert isinstance(nepc.reaction_latex(cs_dict), str)
    assert isinstance(nepc.reaction_latex(angus[0]), str)
    cursor.close()
    cnx.close()


def test_model_summary_df(local, dbug):
    """Verify when nepc.model_summary_df is called it
    returns a Styler object representing the summary of
    a NEPC model as a DataFrame"""
    cnx, cursor = nepc_connect(local, dbug)
    angus = nepc.model(cursor, "angus")
    assert isinstance(nepc.model_summary_df(angus), pd.io.formats.style.Styler)
    cursor.close()
    cnx.close()


def test_cs_subset(local, dbug):
    """Verify that nepc.cs_subset returns a proper
    subset of cross sections from the NEPC MySQL database"""
    cnx, cursor = nepc_connect(local, dbug)
    sigma_cutoff = 1E-21
    cs_subset = nepc.cs_subset(cursor, specie="N", process="excitation",
                               ref='wang2014', lhsA='N_2s22p3_4So',
                               sigma_cutoff=sigma_cutoff)
    assert isinstance(cs_subset, list)
    assert isinstance(cs_subset[0], dict)
    sigma_max = 1
    for cross in cs_subset:
        if max(cross["sigma"]) < sigma_max:
            sigma_max = max(cross["sigma"])
    assert sigma_max > sigma_cutoff
    cursor.close()
    cnx.close()


def test_cs_subset_exception(local, dbug):
    """When prompted with an exception in test_cs_subset
    verify that nepc.cs_subset does indeed return a value"""
    cnx, cursor = nepc_connect(local, dbug)
    with pytest.raises(Exception):
        assert nepc.cs_subset(cursor)
    cursor.close()
    cnx.close()
