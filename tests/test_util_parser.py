"""Tests for nepc.util.parser.py"""
import pytest
from nepc.util import parser
import nepc
import hashlib


def test_format_model_exception_for_unsupported_format():
    """Verify format_model raises an exception if format is
    not supported"""
    with pytest.raises(Exception) as e:
        assert parser.format_model(model=None, type='bsr')
    assert str(e.value) == 'type bsr is not supported'


def test_format_model_exception_for_unsupported_model():
    """Verify format_model raises an exception if model is
    not a nepc.Model"""
    with pytest.raises(Exception) as e:
        assert parser.format_model(model="str_not_model")
    assert str(e.value) == 'model str_not_model is not supported' 


@pytest.mark.usefixtures("nepc_connect")
def test_format_model_write_file(nepc_connect, tmpdir):
    file = tmpdir.join('lxcat.txt')
    fict = nepc.Model(nepc_connect[1], "fict")
    parser.format_model(fict, type='lxcat', filename=str(file))
    lines = file.read().splitlines()
    assert len(lines) == 1981
    assert lines[0] == 'EXCITATION'
    assert lines[99] == '1.500000e+03\t1.130000e-20'
    assert lines[184] == 'COLUMNS: Energy (eV) | Cross section (m2)'
    with open(str(file), 'rb') as f:
        fb = f.read()
        readable_hash = hashlib.md5(fb).hexdigest()
    assert readable_hash == '8f8c7935e3d80ea20ca9fffd98391ade'
