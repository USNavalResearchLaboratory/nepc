"""Tests the thomson.py module"""

import thomson

#TODO: create a constants file with all the constants we're going to use
ionization_energy = 15.885 # eV

def test_reduced_energy():
    """Checks the object type returned for the reduced energy is a list"""
    value_type = type(thomson.reduced_energy([1, 2, 3], ionization_energy))
    assert value_type == list

def test_func_ej():
    """Checks the object typed returned for the universal fit is a list"""
    value_type = type(thomson.func_ej([1, 2, 3], ionization_energy, 2))
    assert value_type == list

def test_guess_1():
    """Checks the object type returned from the guess is a list"""
    value_type = type(thomson.func_guess_1([1, 2, 3], 1, 1, 1))
    assert value_type == list

def test_guess_2():
    """Checks the object type returned from the guess is a list"""
    value_type = type(thomson.func_guess_2([1, 2, 3], 1, 1, 1, 1))
    assert value_type == list
