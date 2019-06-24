from nepc import nepc
import pandas as pd


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
    cnx, cursor = nepc.connect(local, dbug)
    return cnx, cursor


def test_count_table_rows(local, dbug):
    cnx, cursor = nepc_connect(local, dbug)
    rows = nepc.count_table_rows(cursor, "species")
    assert type(rows) is int
    cursor.close()
    cnx.close()


def test_cs_e_sigma(local, dbug):
    cnx, cursor = nepc_connect(local, dbug)
    e_energy, sigma = nepc.cs_e_sigma(cursor, 1)
    assert type(e_energy) is list
    assert type(sigma) is list
    assert type(e_energy[0]) is float
    assert type(sigma[0]) is float
    cursor.close()
    cnx.close()


def test_cs_metadata(local, dbug):
    cnx, cursor = nepc_connect(local, dbug)
    metadata = nepc.cs_metadata(cursor, 1)
    assert type(metadata) is list
    assert type(metadata[0]) is int
    assert type(metadata[1]) is str
    assert type(metadata[3]) is float
    cursor.close()
    cnx.close()


def test_cs_dict_constructor(local, dbug):
    cnx, cursor = nepc_connect(local, dbug)
    metadata = nepc.cs_metadata(cursor, 1)
    e_energy, sigma = nepc.cs_e_sigma(cursor, 1)
    cs_dict = nepc.cs_dict_constructor(metadata, e_energy, sigma)
    assert type(cs_dict) is dict
    assert type(cs_dict["cs_id"]) is int
    assert type(cs_dict["specie"]) is str
    assert type(cs_dict["units_e"]) is float
    assert type(cs_dict["e"]) is list
    assert type(cs_dict["e"][0]) is float
    cursor.close()
    cnx.close()


def test_model(local, dbug):
    cnx, cursor = nepc_connect(local, dbug)
    angus = nepc.model(cursor, "angus")
    assert type(angus) is list
    assert type(angus[0]) is dict
    assert type(angus[0]["cs_id"]) is int
    assert type(angus[0]["specie"]) is str
    assert type(angus[0]["units_e"]) is float
    assert type(angus[0]["e"]) is list
    assert type(angus[0]["e"][0]) is float
    cursor.close()
    cnx.close()


def test_table_as_df(local, dbug):
    cnx, cursor = nepc_connect(local, dbug)
    df = nepc.table_as_df(cursor, "states")
    assert type(df) is pd.DataFrame
    df = nepc.table_as_df(cursor, "processes", columns=["id", "name"])
    assert type(df) is pd.DataFrame
    cursor.close()
    cnx.close()


def test_reaction_latex(local, dbug):
    cnx, cursor = nepc_connect(local, dbug)
    metadata = nepc.cs_metadata(cursor, 1)
    e_energy, sigma = nepc.cs_e_sigma(cursor, 1)
    cs_dict = nepc.cs_dict_constructor(metadata, e_energy, sigma)
    angus = nepc.model(cursor, "angus")
    assert type(nepc.reaction_latex(cs_dict)) is str
    assert type(nepc.reaction_latex(angus[0])) is str
    cursor.close()
    cnx.close()


def test_model_summary_df(local, dbug):
    cnx, cursor = nepc_connect(local, dbug)
    angus = nepc.model(cursor, "angus")
    assert type(nepc.model_summary_df(angus)) is pd.DataFrame
    cursor.close()
    cnx.close()


def test_cs_subset(local, dbug):
    cnx, cursor = nepc_connect(local, dbug)
    sigma_cutoff = 1E-21
    cs_subset = nepc.cs_subset(cursor, specie="N", process="excitation",
                               ref='wang2014', lhsA='N_2s22p3_4So',
                               sigma_cutoff=sigma_cutoff)
    assert type(cs_subset) is list
    assert type(cs_subset[0]) is dict
    sigma_max = 1
    for cs in cs_subset:
        if max(cs["sigma"]) < sigma_max:
            sigma_max = max(cs["sigma"])
    assert sigma_max > sigma_cutoff
