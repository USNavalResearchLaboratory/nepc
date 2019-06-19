from nepc import nepc
import pandas as pd

cnx, cursor = nepc.connect(local=True)


def test_count_table_rows():
    rows = nepc.count_table_rows(cursor, "species")
    assert type(rows) is int


""" def test_cs_metadata():
    cs_meta = nepc.cs_metadata(cursor, 0)
    assert type(cs_meta[0]) is int
    """


def test_table_as_df():
    df = nepc.table_as_df(cursor, "states")
    assert type(df) is pd.DataFrame
    df = nepc.table_as_df(cursor, "states", columns=["name", "name_long"])
    assert type(df) is pd.DataFrame

