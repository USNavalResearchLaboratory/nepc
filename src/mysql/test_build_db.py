from nepc import nepc
from nepc.util import config
import os
from nepc.util import scraper

# TODO: test that all values in [nepc]/data are in the nepc database
# TODO: make a test database for testing purposes and check actual values

HOME = config.userHome()

cnx, cursor = nepc.connect(local=False)

DIR_NAMES = [HOME + "/projects/nepc/data/formatted/n2/itikawa/",
             HOME + "/projects/nepc/data/formatted/n2/zipf/",
             HOME + "/projects/nepc/data/formatted/n/zatsarinny/"]


def test_csdata_lines():
    cs_lines = 0
    for directoryname in DIR_NAMES:
        directory = os.fsencode(directoryname)

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".met") or filename.endswith(".mod"):
                continue
            else:
                cs_lines += scraper.wc_fxn(directoryname + filename)

    assert cs_lines == nepc.count_table_rows(cursor, "csdata")
