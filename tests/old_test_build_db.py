"""Verify that all of the values in the database are correct
and in the proper format"""
import os
import csv
import platform
import pytest
import pandas as pd
from nepc import nepc
#from nepc.util import config
from nepc.util import scraper

NEPC_HOME = '/home/neha/nepc'

DIR_NAMES = [NEPC_HOME + "/data/formatted/n2/itikawa/",
             NEPC_HOME + "/data/formatted/n2/zipf/",
             NEPC_HOME + "/data/formatted/n/zatsarinny/"]


def nepc_connect(local, dbug):
    """Establishes a connection with the NEPC database
    Parameters
    ----------
    local : boolean
    Checks if the database has been built locally or on 'ppdadamsonlinux'

    dbug : boolean
    Checks if debug mode is on

    Returns
    -------
    cnx : MySQLConnection
    A connection to the MySQL database

    cursor : MySQLCursor
    The cursor of the NEPC MySQL database
    """
    cnx, cursor = nepc.connect(local, dbug)
    return cnx, cursor


def test_csdata_lines(local, dbug):
    """Verify that csdata has the same number of rows as in
    all of the files"""
    cnx, cursor = nepc_connect(local, dbug)
    cs_lines = 0
    for directoryname in DIR_NAMES:
        directory = os.fsencode(directoryname)

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".met") or filename.endswith(".mod"):
                continue
            else:
                # subtract 1 to account for header
                cs_lines += scraper.wc_fxn(directoryname + filename) - 1

    assert cs_lines == nepc.count_table_rows(cursor, "csdata")
    cursor.close()
    cnx.close()

def iterate_cs_dat_files(local, dbug):
    """Iterate through cs_dat_files and return e_energy and sigma values for
    parametrization"""
    cnx, cursor = nepc.connect(local, dbug)
    if local is False or platform.node() == 'ppdadamsonlinux':
        cs_dat_files = pd.read_csv(NEPC_HOME + '/mysql/cs_datfile_prod.tsv',
                                   delimiter='\t')
    else:
        cs_dat_files = pd.read_csv(NEPC_HOME + '/mysql/cs_datfile_local.tsv',
                                   delimiter='\t')

    for index, row in cs_dat_files.iterrows():
        if dbug:
            print(index)
        cs_id = int(row['cs_id'])
        dat_file = row['filename']
        datf = pd.read_csv(NEPC_HOME + dat_file + '.dat', delimiter='\t',
                           usecols=['e_energy', 'sigma'])
        yield [pytest.approx(datf['e_energy'].tolist()),
               pytest.approx(datf['sigma'].tolist()),
               nepc.cs_e(cursor, cs_id),
               nepc.cs_sigma(cursor, cs_id)]
    cursor.close()
    cnx.close()

def data_param():
    """Create argument full of data values for parametrization"""
    d_param = []
    for elem in iterate_cs_dat_files(False, False):
        d_param.append((elem[2], elem[0]))
        d_param.append((elem[3], elem[1]))
    return d_param

@pytest.mark.parametrize("dat_column, fil_column", data_param())
def test_data_entered(dat_column, fil_column):
    """Verify that the data in each .dat file matches that of
    the database"""
    assert dat_column == fil_column

def iterate_cs_met_files(local, dbug):
    """Iterate through all metadata files and return
    pairs of database and file values to compare against
    in testing"""
    cnx, cursor = nepc.connect(local, dbug)
    if dbug:
        print(cnx)
    if local is False or platform.node() == 'ppdadamsonlinux':
        cs_dat_files = pd.read_csv(NEPC_HOME + '/mysql/cs_datfile_prod.tsv',
                                   delimiter='\t')
    else:
        cs_dat_files = pd.read_csv(NEPC_HOME + '/mysql/cs_datfile_local.tsv',
                                   delimiter='\t')

    for index, row in cs_dat_files.iterrows():
        if dbug:
            print(index)
        cs_id = int(row['cs_id'])
        met_file = row['filename']
        if dbug:
            print(cs_id, met_file)

        meta_cols = ['specie', 'process', 'units_e',
                     'units_sigma', 'ref', 'lhsA',
                     'lhsB', 'rhsA', 'rhsB', 'wavelength',
                     'lhs_v', 'rhs_v', 'lhs_j', 'rhs_j',
                     'background', 'lpu', 'upu']
        """fil = NEPC_HOME + met_file + ".met"
        lst = scraper.reader(fil, '\t')
        meta_disk = lst[0]"""
        with open(NEPC_HOME + met_file + ".met", 'r', newline='') as fil:
            reader = csv.reader(fil, delimiter='\t')
            next(reader)
            #lst = scraper.reader(fil, '\t')
            lst = list(reader)
            meta_disk = lst[0]
        meta_disk = [meta_disk[i] for i in list(range(1, 18))]
        for i in [2, 3, 9, 15, 16]:
            meta_disk[i] = (float(meta_disk[i]) if meta_disk[i] != '\\N'
                            else meta_disk[i])

        for i in [10, 11, 12, 13]:
            meta_disk[i] = (int(meta_disk[i]) if meta_disk[i] != '\\N'
                            else meta_disk[i])

        meta_db = [nepc.cs_metadata(cursor, cs_id)[i]
                   for i in list(range(1, 18))]
        for i in range(len(meta_cols)):
            yield [meta_disk[i], meta_db[i]]
            if isinstance(meta_db[i], float):
                assert (pytest.approx(meta_disk[i]) ==
                        pytest.approx(meta_db[i]))
            elif meta_db[i] is None:
                assert meta_disk[i] == '\\N'
            else:
                assert str(meta_disk[i]) == str(meta_db[i])

def meta_param():
    """Return a pair of values in metadata for parametrization"""
    m_param = []
    for elem in iterate_cs_met_files(False, False):
        m_param.append(elem[0], elem[1])
    return m_param

@pytest.mark.parametrize("meta_disk, meta_db", meta_param())
def test_meta_entered(meta_disk, meta_db):
    """Verify that the metadata in each .met file matches that of the database"""
    if isinstance(meta_db, float):
        assert (pytest.approx(meta_disk) ==
                pytest.approx(meta_db))
    elif meta_db is None:
        assert meta_disk == '\\N'
    else:
        assert str(meta_disk) == str(meta_db)
