from nepc import nepc
from nepc.util import config
from nepc.util import util
import pandas as pd
import os
import pytest
import platform
# TODO: remove dependence on csv; put function in scraper that uses built-in
#       readlines function
import csv

# TODO: test that all values in [nepc]/data are in the nepc database

NEPC_HOME = config.nepc_home()
NEPC_DATA = NEPC_HOME + "/data/"

DIR_NAMES = [NEPC_HOME + "/data/cs/n2/itikawa/",
             NEPC_HOME + "/data/cs/n2/zipf/",
             NEPC_HOME + "/data/cs/n/zatsarinny/"]


@pytest.mark.usefixtures("nepc_connect")
def test_csdata_lines(nepc_connect):
    cs_lines = 0
    for directoryname in DIR_NAMES:
        directory = os.fsencode(directoryname)

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".met") or filename.endswith(".mod"):
                continue
            else:
                # subtract 1 to account for header
                cs_lines += util.wc_fxn(directoryname + filename) - 1

    assert cs_lines == nepc.count_table_rows(nepc_connect[1], "csdata")


@pytest.mark.usefixtures("nepc_connect")
def test_data_entered(nepc_connect, local):
    if local is False or platform.node() == 'ppdadamsonlinux':
        cs_dat_files = pd.read_csv(NEPC_DATA + 'cs_datfile_prod.tsv',
                                   delimiter='\t')
    else:
        cs_dat_files = pd.read_csv(NEPC_DATA + 'cs_datfile_local.tsv',
                                   delimiter='\t')

    for index, row in cs_dat_files.iterrows():
        cs_id = row['cs_id']
        dat_file = row['filename']
        df = pd.read_csv(NEPC_HOME + dat_file + '.dat', delimiter='\t',
                         usecols=['e_energy', 'sigma'])
        e_energy, sigma = nepc.cs_e_sigma(nepc_connect[1], cs_id)
        # assert e_energy == pytest.approx(df['e_energy'].tolist())
        assert sigma == pytest.approx(df['sigma'].tolist())


@pytest.mark.usefixtures("nepc_connect")
def test_meta_entered(nepc_connect, local, dbug):
    if local is False or platform.node() == 'ppdadamsonlinux':
        cs_dat_files = pd.read_csv(NEPC_DATA + 'cs_datfile_prod.tsv',
                                   delimiter='\t')
    else:
        cs_dat_files = pd.read_csv(NEPC_DATA + 'cs_datfile_local.tsv',
                                   delimiter='\t')

    for index, row in cs_dat_files.iterrows():
        cs_id = row['cs_id']
        met_file = row['filename']
        if dbug:
            print(cs_id, met_file)
        e, sigma = nepc.cs_e_sigma(nepc_connect[1], cs_id)

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

        meta_db = [nepc.cs_metadata(nepc_connect[1], cs_id)[i]
                   for i in list(range(1, 18))]
        for i in range(len(meta_cols)):
            if (type(meta_db[i]) is float):
                assert (pytest.approx(meta_disk[i]) ==
                        pytest.approx(meta_db[i]))
            elif meta_db[i] is None:
                assert meta_disk[i] == '\\N'
            else:
                assert meta_disk[i] == meta_db[i]
