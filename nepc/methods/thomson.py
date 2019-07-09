"""Module for computing the ionization cross sections from Thomson scattering"""
import numpy as np

def reduced_energy(energy, ionization_potential):
    """calculates the reduced energy for ionization"""
    return [list_item / ionization_potential for list_item in energy]

def func_ej(cross_section, ionization_potential, n_valence): # using joules instead of eV
    """sets the f(E/J) equal to equation 5 in Kosarim with the added coulomb constant"""
    return [list_item * 10**-20 * (ionization_potential * elec_charge)**2 /
            (n_valence * np.pi * elec_charge**4 * ke**2) for list_item in cross_section]

def func_guess_1(pos_x, a_coef, b_coef, d_coef):
    """this is the first guess for what could fit the f(E/J) data"""
    return [(a_coef * (list_item + b_coef)) /
            (np.pi * list_item * (list_item + d_coef)) for list_item in pos_x]

def func_guess_2(pos_x, a_coef, b_coef, d_coef, e_coef):
    """this is the second guess for what could fit the f(E/J) data"""
    return [(a_coef * (list_item + b_coef)) /
            (np.pi * (list_item + e_coef) * (list_item + d_coef)) for list_item in pos_x]
