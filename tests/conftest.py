import pytest
from fixtures.mysql import mysql_config
from fixtures.mysql import nepc_connect

def pytest_addoption(parser):
    parser.addoption("--travis", action="store_true", default=False)