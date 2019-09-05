"""Tests whether the functions of nepc.py work as intended"""
import pandas as pd
import mysql.connector
import pytest
from nepc import nepc


@pytest.fixture
def nepc_connect(local, dbug):
    """Establishes a connection with the NEPC database

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
    A MySQLCursor object for executing SQL queries"""
    cnx, cursor = nepc.connect(local, dbug)
    print(type(cnx))
    print(type(cursor))
    yield [cnx, cursor]
    cursor.close()
    cnx.close()


def nonfix_nepc_connect(local, dbug):
    cnx, cursor = nepc.connect(local, dbug)
    return cnx, cursor


def test_connect(nepc_connect):
    """Verify that nepc.connect() method connects to the NEPC
    database when local is True and when local is False"""
    assert isinstance(nepc_connect[0],
                      mysql.connector.connection_cext.CMySQLConnection)
    assert isinstance(nepc_connect[1],
                      mysql.connector.cursor_cext.CMySQLCursor)


def test_count_table_rows(nepc_connect):
    """Verify that nepc.count_table_rows returns an integer value"""
    rows = nepc.count_table_rows(nepc_connect[1], "species")
    assert isinstance(rows, int)


def test_cs_e_sigma(nepc_connect):
    """Verify that nepc.cs_e_sigma returns
    proper formats for the e_energy and sigma values"""
    e_energy, sigma = nepc.cs_e_sigma(nepc_connect[1], 1)
    assert isinstance(e_energy, list)
    assert isinstance(sigma, list)
    assert isinstance(e_energy[0], float)
    assert isinstance(sigma[0], float)


def test_cs_metadata(nepc_connect):
    """Verify that nepc.cs_metadata returns the
    metadata as a list containing an int
    in the first index, a str in the second index,
    and a float in the fourth index"""
    metadata = nepc.cs_metadata(nepc_connect[1], 1)
    assert isinstance(metadata, list)
    assert isinstance(metadata[0], int)
    assert isinstance(metadata[1], str)
    assert isinstance(metadata[3], float)


def test_cs_dict_constructor(nepc_connect):
    """Verify that nepc.cs_dict_constructor
    makes a dictionary out of the three terms as
    parameters, and that each term is represented
    in its accurate format"""
    metadata = nepc.cs_metadata(nepc_connect[1], 1)
    e_energy, sigma = nepc.cs_e_sigma(nepc_connect[1], 1)
    cs_dict = nepc.cs_dict_constructor(metadata, e_energy, sigma)
    assert isinstance(cs_dict, dict)
    assert isinstance(cs_dict["cs_id"], int)
    assert isinstance(cs_dict["specie"], str)
    assert isinstance(cs_dict["units_e"], float)
    assert isinstance(cs_dict["e"], list)
    assert isinstance(cs_dict["e"][0], float)


def test_table_as_df(nepc_connect):
    """Verify when nepc.table_as_df is called it
    returns a DataFrame copy of what is included in the
    table used as an argument"""
    statef = nepc.table_as_df(nepc_connect[1], "states")
    assert isinstance(statef, pd.DataFrame)
    processf = nepc.table_as_df(nepc_connect[1], "processes",
                                columns=["id", "name"])
    assert isinstance(processf, pd.DataFrame)


def test_reaction_latex(nepc_connect):
    """Verify when nepc.reaction_latex is called it
    returns a string representing the LaTeX
    for the reaction from a nepc cross section"""
    metadata = nepc.cs_metadata(nepc_connect[1], 1)
    e_energy, sigma = nepc.cs_e_sigma(nepc_connect[1], 1)
    cs_dict = nepc.cs_dict_constructor(metadata, e_energy, sigma)
    assert isinstance(nepc.reaction_latex(cs_dict), str)


def test_cs_subset(nepc_connect):
    """Verify that nepc.cs_subset returns a proper
    subset of cross sections from the NEPC MySQL database"""
    sigma_cutoff = 1E-21
    cs_subset = nepc.cs_subset(nepc_connect[1], specie="N",
                               process="excitation",
                               ref='wang2014', lhsA='N_2s22p3_4So',
                               sigma_cutoff=sigma_cutoff)
    assert isinstance(cs_subset, list)
    assert isinstance(cs_subset[0], dict)
    sigma_max = 1
    for cross in cs_subset:
        if max(cross["sigma"]) < sigma_max:
            sigma_max = max(cross["sigma"])
    assert sigma_max > sigma_cutoff


def test_cs_subset_exception(nepc_connect):
    """When prompted with an exception in test_cs_subset
    verify that nepc.cs_subset does indeed return a value"""
    with pytest.raises(Exception):
        assert nepc.cs_subset(nepc_connect[1])
