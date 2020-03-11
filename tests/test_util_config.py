"""Tests for nepc.util.config.py"""
import os
from nepc.util import config


def test_user_home():
    """Verify whether user_home() returns a string
    that represents the correct path to the user's home directory"""
    assert isinstance(config.user_home(), str)
    assert config.user_home() == os.environ.get('HOME')


def test_nepc_home():
    """Verify whether nepc_home() returns a string
    that represents the correct path to the NEPC folder"""
    assert isinstance(config.nepc_home(), str)
    assert config.nepc_home() == os.environ.get('NEPC_HOME')
