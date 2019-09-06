"""Tests for nepc/nepc.py"""
import pandas as pd
import mysql.connector
import pytest
from nepc import nepc


def test_connect():
    """Verify that nepc.connect() method connects to the NEPC
    database when local is True and when local is False"""

    cnx, cursor = nepc.connect(local=False)
    assert isinstance(cnx,
                      mysql.connector.connection_cext.CMySQLConnection)
    assert isinstance(cursor,
                      mysql.connector.cursor_cext.CMySQLCursor)
    cursor.close()
    cnx.close()
    cnx, cursor = nepc.connect(local=True)
    assert isinstance(cnx,
                      mysql.connector.connection_cext.CMySQLConnection)
    assert isinstance(cursor,
                      mysql.connector.cursor_cext.CMySQLCursor)
    cursor.close()
    cnx.close()


@pytest.mark.usefixtures("nepc_connect")
def test_count_table_rows(nepc_connect):
    """Verify that nepc.count_table_rows returns an integer value"""
    rows = nepc.count_table_rows(nepc_connect[1], "species")
    assert isinstance(rows, int)


@pytest.mark.usefixtures("nepc_connect")
def test_cs_e_sigma(nepc_connect):
    """Verify that nepc.cs_e_sigma returns
    proper formats for the e_energy and sigma values"""
    # TODO: check some actual e, sigma values from the files
    e_energy, sigma = nepc.cs_e_sigma(nepc_connect[1], 1)
    assert isinstance(e_energy, list)
    assert isinstance(sigma, list)
    assert isinstance(e_energy[0], float)
    assert isinstance(sigma[0], float)


@pytest.mark.usefixtures("nepc_connect")
def test_cs_e(nepc_connect):
    """Verify that nepc.cs_e returns
    proper formats for the e_energy values for a single cs_id"""
    # TODO: check some actual e_energy values from the files
    e_energy = nepc.cs_e(nepc_connect[1], 1)
    assert isinstance(e_energy, list)
    assert isinstance(e_energy[0], float)


@pytest.mark.usefixtures("nepc_connect")
def test_cs_sigma(nepc_connect):
    """Verify that nepc.cs_sigma returns
    proper formats for the sigma values for a single cs_id"""
    # TODO: check some actual sigma values from the files
    sigma = nepc.cs_sigma(nepc_connect[1], 1)
    assert isinstance(sigma, list)
    assert isinstance(sigma[0], float)


@pytest.mark.usefixtures("nepc_connect")
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


@pytest.mark.usefixtures("nepc_connect")
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


@pytest.mark.usefixtures("nepc_connect")
def test_model(nepc_connect):
    """Verify that nepc.model returns a list of dictionaries"""
    # TODO: create a model class and test that we can retrieve it from
    # the NEPC database
    model = nepc.model(nepc_connect[1], "angus")
    assert isinstance(model, list)
    assert isinstance(model[0], dict)
    assert isinstance(model[0]['specie'], str)


@pytest.mark.usefixtures("nepc_connect")
def test_table_as_df(nepc_connect):
    """Verify when nepc.table_as_df is called it
    returns a DataFrame copy of what is included in the
    table used as an argument"""
    statef = nepc.table_as_df(nepc_connect[1], "states")
    assert isinstance(statef, pd.DataFrame)
    processf = nepc.table_as_df(nepc_connect[1], "processes",
                                columns=["id", "name"])
    assert isinstance(processf, pd.DataFrame)


@pytest.mark.usefixtures("nepc_connect")
def test_reaction_latex(nepc_connect):
    """Verify when nepc.reaction_latex is called it
    returns a string representing the LaTeX
    for the reaction from a nepc cross section"""
    # TODO: verify latex is correct
    for i in range(1, 100):
        metadata = nepc.cs_metadata(nepc_connect[1], i)
        e_energy, sigma = nepc.cs_e_sigma(nepc_connect[1], i)
        cs_dict = nepc.cs_dict_constructor(metadata, e_energy, sigma)
        assert isinstance(nepc.reaction_latex(cs_dict), str)


@pytest.mark.usefixtures("nepc_connect")
def test_model_summary_df(nepc_connect):
    """Verify nepc.model_summary_df returns a dataframe"""
    # TODO: check formatting of summary dataframe
    model = nepc.model(nepc_connect[1], "angus")
    df = nepc.model_summary_df(model, lower=0, upper=10)
    assert isinstance(df, pd.io.formats.style.Styler)
    df = nepc.model_summary_df(model, upper=10)
    assert isinstance(df, pd.io.formats.style.Styler)
    df = nepc.model_summary_df(model, lower=10)
    assert isinstance(df, pd.io.formats.style.Styler)


@pytest.mark.usefixtures("nepc_connect")
def test_cs_subset(nepc_connect):
    """Verify that nepc.cs_subset returns a proper
    subset of cross sections from the NEPC MySQL database"""
    # TODO: test for lhsB and rhsB
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
    cs_subset = nepc.cs_subset(nepc_connect[1], specie="N",
                               process="excitation",
                               ref='wang2014', rhsA='N_2s22p3_2Do',
                               sigma_cutoff=sigma_cutoff)
    assert isinstance(cs_subset, list)
    assert isinstance(cs_subset[0], dict)


@pytest.mark.usefixtures("nepc_connect")
def test_cs_subset_exception(nepc_connect):
    """When prompted with an exception in test_cs_subset
    verify that nepc.cs_subset does indeed return a value"""
    with pytest.raises(Exception):
        assert nepc.cs_subset(nepc_connect[1])
