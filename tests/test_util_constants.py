"""Verify that methods and constants in nepc.util.constants are correct
and properly formatted"""
from nepc.util import constants

def test_return_states_n2():
    """Verify that return_states_N2 returns a list
    representing the states_N2 constant"""
    assert isinstance(constants.return_states_n2(), list)

def test_return_states_n2p():
    """Verify that return_states_N2p returns a list
    representing the states_N2p constant"""
    assert isinstance(constants.return_states_n2p(), list)

def test_return_vib_constants_n2():
    """Verify that return_vib_constants_N2 returns a list of lists
    representing the vib_constants_N2 constant"""
    assert isinstance(constants.return_vib_constants_n2(), list)
    assert isinstance(constants.return_vib_constants_n2()[0], list)

def test_return_vib_constants_n2p():
    """Verify that return_vib_constants_N2p returns a list of lists
    representing the vib_constants_N2p constant"""
    assert isinstance(constants.return_vib_constants_n2p(), list)
    assert isinstance(constants.return_vib_constants_n2p()[0], list)

def test_return_rot_constants_n2():
    """Verify that return_rot_constants_N2 returns a list of lists
    representing the rot_constants_N2 constant"""
    assert isinstance(constants.return_rot_constants_n2(), list)
    assert isinstance(constants.return_rot_constants_n2()[0], list)

def test_return_rot_constants_n2p():
    """Verify that return_rot_constants_N2p returns a list of lists
    representing the rot_constants_N2p constant"""
    assert isinstance(constants.return_rot_constants_n2p(), list)
    assert isinstance(constants.return_rot_constants_n2p()[0], list)
