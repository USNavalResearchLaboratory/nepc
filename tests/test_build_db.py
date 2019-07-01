from nepc import nepc
from nepc.util import config
from nepc.util import scraper
import pandas as pd
import os
import pytest

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


def test_data_entered(local, dbug):
    cnx, cursor = nepc.connect(local, dbug)
    cs_dat_files = pd.read_csv(NEPC_HOME + '/mysql/cs_dat_file.tsv',
                               delimiter='\t')
    for index, row in cs_dat_files.iterrows():
        cs_id = row['cs_id']
        dat_file = row['filename']
        df = pd.read_csv(NEPC_HOME + dat_file, delimiter='\t',
                         usecols=['e_energy', 'sigma'])
        e_energy, sigma = nepc.cs_e_sigma(cursor, cs_id)
        assert e_energy == pytest.approx(df['e_energy'].tolist())
        assert sigma == pytest.approx(df['sigma'].tolist())
    cursor.close()
    cnx.close()
