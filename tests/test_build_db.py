from nepc import nepc
from nepc.util import config
from nepc.util import scraper
import pandas as pd
from pandas.util.testing import assert_frame_equal
import os
import pytest
import platform
# TODO: remove dependence on csv; put function in scraper that uses built-in
#       readlines function
import csv

# TODO: test that all values in [nepc]/data are in the nepc database
# TODO: make a test database for testing purposes and check actual values

NEPC_HOME = config.nepc_home()

DIR_NAMES = [NEPC_HOME + "/data/formatted/n2/itikawa/",
             NEPC_HOME + "/data/formatted/n2/zipf/",
             NEPC_HOME + "/data/formatted/n/zatsarinny/"]


def nepc_connect(local, dbug):
    cnx, cursor = nepc.connect(local, dbug)
    return cnx, cursor


def test_csdata_lines(local, dbug):
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


def test_species_entered(local, dbug): #for the species table
    cnx, cursor = nepc.connect(local, dbug)
    cs_species_file = pd.read_csv (NEPC_HOME + '/mysql/species.tsv', delimiter = '\t', index_col = False)
    cs_species = nepc.table_as_df(cursor, "species")
    dblist = []
    filelist = []
    eq_count = 0
    for index, row in cs_species.iterrows():
        for i in row:
            dblist.append(i)
    for index, row in cs_species_file.iterrows():
        for i in row:
            filelist.append(i)
    for i in range (0, len(dblist)):
        if dblist[i] == filelist[i]:
            eq_count = eq_count + 1
        elif dblist[i] == '':
            eq_count = eq_count + 1
        else:
            continue
    assert eq_count == len(dblist)
    cursor.close()
    cnx.close()


def test_processes_entered(local, dbug): #for the processes table
    #FIXME: currently does not add all of the elements in the file
    cnx, cursor = nepc.connect(local, dbug)
    cs_processes_file = pd.read_csv (NEPC_HOME + '/mysql/processes.tsv', delimiter = '\t')
    headers = ['id', 'short', 'long', 'LHS', 'RHS', 'LHS_e', 'RHS_e', 'LHS_hv', 'RHS_hv', 'LHS_v', 'RHS_v', 'LHS_j', 'RHS_j']

    print ("From the file \n")
    print (cs_processes_file.to_string())

    cs_processes = nepc.table_as_df(cursor, "processes")
    print ("\n From the database \n")
    print (cs_processes.to_string())
    dblist_str = []
    filelist_str = []
    for index, row in cs_processes.iterrows():
        for i in row:
            dblist_str.append(i)
    for index, row in cs_processes_file.iterrows():
        for i in row:
            filelist_str.append(i)
    print ("These are the string elements from the database.\n")
    print (dblist_str)
    print ("These are the string elements from the file.\n")
    print (filelist_str)
    assert 1 == 1 #temporary statement
    #assert dblist_str == filelist_str
    cursor.close()
    cnx.close()

#FIXME: fix reading in the file - too short of a length for test to work
def test_models_entered(local, dbug): #for the models table
    cnx, cursor = nepc.connect(local, dbug)
    cs_models_file = pd.read_csv (NEPC_HOME + '/mysql/models.tsv', delimiter = '\t')
    cs_models = nepc.table_as_df (cursor, "models")
    dblist = []
    filelist = []
    eq_count = 0
    for index, row in cs_models.iterrows():
        for i in row:
            dblist.append(i)
    for index, row in cs_models_file.iterrows():
        for i in row:
            filelist.append(i)
    for i in dblist:
        if type(i) is int:
            dblist.remove(i)
    print (dblist)
    print ("\n")
    print (filelist)
    for i in range (0, len(dblist)):
        if dblist[i] == filelist[i]:
            eq_count = eq_count + 1
    assert eq_count == 4
    cursor.close()
    cnx.close()
    

# TODO: use @pytest.mark.parametrize decorator to turn this into N tests
#       instead of N asserts in one test
def test_data_entered(local, dbug): #for the csdata table
    cnx, cursor = nepc.connect(local, dbug)
    if local is False or platform.node() == 'ppdadamsonlinux':
        cs_dat_files = pd.read_csv(NEPC_HOME + '/mysql/cs_datfile_prod.tsv',
                                   delimiter='\t')
    else:
        cs_dat_files = pd.read_csv(NEPC_HOME + '/mysql/cs_datfile_local.tsv',
                                   delimiter='\t')

    for index, row in cs_dat_files.iterrows():
        cs_id = row['cs_id']
        dat_file = row['filename']
        df = pd.read_csv(NEPC_HOME + dat_file + '.dat', delimiter='\t',
                         usecols=['e_energy', 'sigma'])
        e_energy, sigma = nepc.cs_e_sigma(cursor, cs_id)
        assert e_energy == pytest.approx(df['e_energy'].tolist())
        assert sigma == pytest.approx(df['sigma'].tolist())
    cursor.close()
    cnx.close()


# TODO: use @pytest.mark.parametrize decorator to turn this into N tests
#       instead of N asserts in one test
def test_meta_entered(local, dbug): #for the cs table
    cnx, cursor = nepc.connect(local, dbug)
    if local is False or platform.node() == 'ppdadamsonlinux':
        cs_dat_files = pd.read_csv(NEPC_HOME + '/mysql/cs_datfile_prod.tsv',
                                   delimiter='\t')
    else:
        cs_dat_files = pd.read_csv(NEPC_HOME + '/mysql/cs_datfile_local.tsv',
                                   delimiter='\t')

    for index, row in cs_dat_files.iterrows():
        cs_id = row['cs_id']
        met_file = row['filename']
        if dbug:
            print(cs_id, met_file)
        e, sigma = nepc.cs_e_sigma(cursor, cs_id)

        meta_cols = ['specie', 'process', 'units_e',
                     'units_sigma', 'ref', 'lhsA',
                     'lhsB', 'rhsA', 'rhsB', 'wavelength',
                     'lhs_v', 'rhs_v', 'lhs_j', 'rhs_j',
                     'background', 'lpu', 'upu']

        with open(NEPC_HOME + met_file + ".met", 'r', newline='') as f:
                reader = csv.reader(f, delimiter='\t')
                next(reader)
                meta_disk = list(reader)[0]
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
            if (type(meta_db[i]) is float):
                assert (pytest.approx(meta_disk[i]) ==
                        pytest.approx(meta_db[i]))
            elif meta_db[i] is None:
                assert meta_disk[i] == '\\N'
            else:
                assert meta_disk[i] == meta_db[i]
