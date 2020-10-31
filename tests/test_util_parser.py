"""Tests for nepc.util.parser.py"""
import os
import pytest
from nepc.util import parser
import mysql.connector
import nepc


def test_format_model_exception_for_unsupported_format():
    """Verify format_model raises an exception if format is
    not supported"""
    with pytest.raises(Exception) as e:
        assert parser.format_model(model=None, format='bsr')
    assert str(e.value) == 'format bsr is not supported'

def test_format_model_exception_for_unsupported_model():
    """Verify format_model raises an exception if model is
    not a nepc.Model"""
    with pytest.raises(Exception) as e:
        assert parser.format_model(model="str_not_model")
    assert str(e.value) == 'model str_not_model is not supported' 

@pytest.mark.usefixtures("nepc_connect")
def test_format_model_write_file(nepc_connect, tmpdir, dbug):
    file = tmpdir.join('lxcat.txt')
    fict = nepc.Model(nepc_connect[1], "fict")
    parser.format_model(fict, format='lxcat', filename=str(file))
    assert file.read() == ''