"""Tests for nepc/nepc.py"""
import pandas as pd
import pytest
import mysql.connector
import nepc


@pytest.mark.usefixtures("nepc_connect")
def test_connect(nepc_connect):
    """Verify that nepc.connect() method connects to the NEPC database
    """
    assert isinstance(nepc_connect[0],
                      mysql.connector.connection_cext.CMySQLConnection)
    assert isinstance(nepc_connect[1],
                      mysql.connector.cursor_cext.CMySQLCursor)


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
def test_CS_class(nepc_connect):
    """Verify that the nepc.CS class has metadata and data attributes,
    and that each attribute is of the correct type"""
    # FIXME: randomly sample a few cross sections in the database
    cs = nepc.CS(nepc_connect[1], 1)
    # FIXME: add assert for each key in metadata
    assert isinstance(cs.metadata, dict)
    assert isinstance(cs.data, dict)
    assert isinstance(cs.metadata["cs_id"], int)
    assert isinstance(cs.metadata["specie"], str)
    assert isinstance(cs.metadata["units_e"], float)
    assert isinstance(cs.data["e"], list)
    assert isinstance(cs.data["e"][0], float)
    assert isinstance(cs.data["sigma"], list)
    assert isinstance(cs.data["sigma"][0], float)
    # test len()
    # FIXME: use length of data file to get length of sampled cross section
    assert len(cs) == 21


@pytest.mark.usefixtures("nepc_connect")
def test_CustomCS_class(nepc_connect):
    """Verify that the nepc.CustomCS class has metadata and data attributes,
    and that each attribute is of the correct type"""
    cs = nepc.CustomCS(nepc_connect[1], cs_id=1)
    # FIXME: add assert for each in key in metadata
    # FIXME: test edge cases of changing NEPC cross sections
    # FIXME: check that process, specie, state are in NEPC database
    assert isinstance(cs.metadata, dict)
    assert isinstance(cs.data, dict)
    assert cs.metadata["cs_id"] is None
    assert isinstance(cs.metadata["specie"], str)
    assert isinstance(cs.metadata["units_e"], float)
    assert isinstance(cs.data["e"], list)
    assert isinstance(cs.data["e"][0], float)
    assert isinstance(cs.data["sigma"], list)
    assert isinstance(cs.data["sigma"][0], float)
    cs = nepc.CustomCS(nepc_connect[1], cs_id=1,
                       metadata={'cs_id': -1,
                                 'specie': 'O2'},
                       data={'e': [0.0, 1.0, 2.0],
                             'sigma': [0.0, 0.1, 0.2]})
    assert isinstance(cs.metadata, dict)
    assert isinstance(cs.data, dict)
    assert cs.metadata["cs_id"] == -1
    assert cs.metadata["specie"] == 'O2'
    assert isinstance(cs.metadata["units_e"], float)
    assert isinstance(cs.data["e"], list)
    assert isinstance(cs.data["e"][0], float)
    assert isinstance(cs.data["sigma"], list)
    assert isinstance(cs.data["sigma"][0], float)
    assert cs.data['e'] == [0.0, 1.0, 2.0]
    assert cs.data['sigma'] == [0.0, 0.1, 0.2]
    """option not implemented
    cs = nepc.CustomCS(metadata={'cs_id': -1,
                                 'specie': 'N2',
                                 'process': 'excitation',
                                 'lhsA': 'N2(X1Sigmag+)',
                                 'rhsA': 'N2(W3Deltau)',
                                 'units_e': 1.0,
                                 'units_sigma': 1.0,
                                 'threshold': 7.36,
                                 'background': 'N2 W3DELTA-CARTWRIGHT 1977.'},
                       data={'e': [0.0, 1.0, 2.0],
                             'sigma': [0.0, 0.1, 0.2]})
    assert isinstance(cs.metadata, dict)
    assert isinstance(cs.data, dict)
    assert cs.metadata["cs_id"] == -1
    assert cs.metadata["specie"] == 'N2'
    assert cs.metadata["process"] == 'excitation'
    assert cs.metadata["lhsA"] == 'N2(X1Sigmag+)'
    assert cs.metadata["lhsB"] == '\\N'
    assert cs.metadata["rhsA"] == 'N2(X1Sigmag+)'
    assert cs.metadata["rhsB"] == '\\N'
    assert cs.metadata["background"] == 'N2 W3DELTA-CARTWRIGHT 1977.'
    assert cs.metadata["units_e"] == 1.0
    assert cs.metadata["units_sigma"] == 1.0
    assert cs.metadata["threshold"] == 7.36
    assert cs.metadata["lpu"] == -1
    assert cs.metadata["upu"] == -1
    assert isinstance(cs.metadata["units_e"], float)
    assert isinstance(cs.data["e"], list)
    assert isinstance(cs.data["e"][0], float)
    assert isinstance(cs.data["sigma"], list)
    assert isinstance(cs.data["sigma"][0], float)
    assert cs.data['e'] == [0.0, 1.0, 2.0]
    assert cs.data['sigma'] == [0.0, 0.1, 0.2]
    """


@pytest.mark.usefixtures("nepc_connect")
def test_Model_class(nepc_connect):
    """Verify that the nepc.Model class is a list of CS type and
    test the methods within the Class."""
    fict = nepc.Model(nepc_connect[1], "fict")
    # FIXME: randomly sample the models in the database
    # FIXME: randomly sample the cross sections in the model
    assert isinstance(fict.cs, list)
    assert isinstance(fict.cs[0].metadata, dict)
    assert isinstance(fict.cs[0].data, dict)
    assert isinstance(fict.cs[0].metadata['specie'], str)
    # test len method
    # FIXME use data in .mod files to determine number of CS in Model for assert
    assert len(fict) == 30

@pytest.mark.usefixtures("nepc_connect")
def test_CustomModel_class(nepc_connect):
    """Verify that the nepc.CustomModel class is a list of CS 
    and CustomCS type and
    test the methods within the Class."""
    fict = nepc.CustomModel(cursor=nepc_connect[1], model_name="fict")
    # FIXME: randomly sample the models in the database
    # FIXME: randomly sample the cross sections in the model
    assert isinstance(fict.cs, list)
    assert isinstance(fict.cs[0].metadata, dict)
    assert isinstance(fict.cs[0].data, dict)
    assert isinstance(fict.cs[0].metadata['specie'], str)
    assert len(fict.cs) == 30
    fict_mod = nepc.CustomModel(cursor=nepc_connect[1], 
            model_name="fict", 
            cs_id_list=[1, 2])
    # FIXME: randomly sample the models in the database
    # FIXME: randomly sample the cross sections in the model
    assert isinstance(fict_mod.cs, list)
    assert isinstance(fict_mod.cs[0].metadata, dict)
    assert isinstance(fict_mod.cs[0].data, dict)
    assert isinstance(fict_mod.cs[0].metadata['specie'], str)
    assert len(fict_mod.cs) == 32
    fict_subset = nepc.CustomModel(cursor=nepc_connect[1], 
            model_name="fict",
            metadata={'process': 'excitation'})
    # FIXME: randomly sample the models in the database
    # FIXME: randomly sample the cross sections in the model
    assert isinstance(fict_subset.cs, list)
    assert isinstance(fict_subset.cs[0].metadata, dict)
    assert isinstance(fict_subset.cs[0].data, dict)
    assert isinstance(fict_subset.cs[0].metadata['specie'], str)
    assert len(fict_subset.cs) == 15


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
    # FIXME: verify latex is correct
    # FIXME: randomly sample cross sections
    for i in range(1, 30):
        cs = nepc.CS(nepc_connect[1], i)
        assert isinstance(nepc.reaction_latex(cs), str)


@pytest.mark.usefixtures("nepc_connect")
def test_model_summary_df(nepc_connect):
    """Verify nepc.model_summary_df returns a dataframe"""
    # TODO: check formatting of summary dataframe
    # FIXME: randomly sample models
    fict = nepc.Model(nepc_connect[1], "fict")
    df = fict.summary(lower=0, upper=10)
    assert isinstance(df, pd.io.formats.style.Styler)


@pytest.mark.usefixtures("nepc_connect")
def test_model_subset(nepc_connect):
    """Verify that Model.subset returns a proper
    subset of cross sections from a model within the NEPC MySQL database"""
    # TODO: test for lhsB and rhsB
    # FIXME: randomly sample models and cross sections within the model
    fict = nepc.Model(nepc_connect[1], "fict")
    fict_subset = fict.subset({'process': 'excitation',
                               'lhsA': 'N2(X1Sigmag+)'})
    assert isinstance(fict_subset, list)
    assert isinstance(fict_subset[0].metadata, dict)
    assert isinstance(fict_subset[0].data, dict)
    with pytest.raises(Exception):
        assert fict.subset()


@pytest.mark.usefixtures("nepc_connect")
def test_cs_subset_exception(nepc_connect):
    """When prompted with an exception in test_cs_subset
    verify that nepc.cs_subset does indeed return a value"""
    with pytest.raises(Exception):
        assert nepc.cs_subset(nepc_connect[1])
