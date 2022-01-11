"""Tests for nepc.util.parser.py"""
import pytest
from nepc.util.parser import format_model
import nepc
import hashlib


def test_format_model_exception_for_unsupported_format():
    """Verify format_model raises an exception if format is
    not supported"""
    with pytest.raises(Exception) as e:
        assert format_model(model=None, type='bsr')
    assert str(e.value) == 'type bsr is not supported'


def test_format_model_exception_for_unsupported_model():
    """Verify format_model raises an exception if model is
    not a nepc.Model"""
    with pytest.raises(Exception) as e:
        assert format_model(model="str_not_model")
    assert str(e.value) == 'model str_not_model is not supported' 


@pytest.mark.usefixtures("nepc_connect")
def test_format_model_write_file(nepc_connect, tmpdir):
    file = tmpdir.join('lxcat.txt')
    fict = nepc.Model(nepc_connect[1], "fict")
    format_model(fict, type='lxcat', filename=str(file))
    lines = file.read().splitlines()
    assert len(lines) == 1951
    assert lines[0] == 'EXCITATION'
    assert lines[99] == '3.000000e+03\t6.300000e-21'
    assert lines[179] == 'COLUMNS: Energy (eV) | Cross section (m2)'
    with open(str(file), 'rb') as f:
        fb = f.read()
        readable_hash = hashlib.md5(fb).hexdigest()
    assert readable_hash == 'b0c0d9564c3f9c722a27c6e5a4d27260'
