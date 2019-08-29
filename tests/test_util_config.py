"""Tests whether config.py in the nepc module has fully functioning functions"""
import os
from nepc.util import config

def test_nepc_home():
    """Verify whether nepc_home() returns a string
    that represents the correct path to the NEPC folder"""
    assert isinstance(config.nepc_home(), str)
    assert config.nepc_home() == os.environ.get('NEPC_HOME')

def test_remove_crs():
    """Verify whether remove_crs() returns a string in
    the proper format"""
    example = (
        "Somebody once told me the world is" +
        "\ngonna roll me, I ain't the sharpest" +
        "\ntool in the shed")
    assert isinstance(config.remove_crs(example), str)
