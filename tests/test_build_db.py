from nepc import nepc
from nepc.util import config
from nepc.util import scraper
import os

# TODO: test that all values in [nepc]/data are in the nepc database
# TODO: make a test database for testing purposes and check actual values

HOME = config.userHome()

DIR_NAMES = [HOME + "/projects/nepc/data/formatted/n2/itikawa/",
             HOME + "/projects/nepc/data/formatted/n2/zipf/",
             HOME + "/projects/nepc/data/formatted/n/zatsarinny/"]


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
