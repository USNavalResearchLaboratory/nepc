"""Module for computing the ionization cross sections from Thomson scattering

Ref/Methods
-----------
From Kosarim (2005):
    - Uses Equation 5 to calculate the universal function from electron energy
    and ionization potential #FIXME add reference to where the data is from
        - The equation is missing the coulomb force constant (k_e), which must be squared
    - Uses Equation 11 to calculate the ionization cross section
        - also missing the coulomb force constant (k_e) squared
From Vasan (1982):
    - Morse Potential
        - V(r) = De[1-exp(-Beta(r-re))]^2
    - Normalized Wavefunction
        - Psi = N*exp(-z/2)*z^(b/2)*Lnb(z)

From Gilmore (1965, 1991):
    - Determine Franck-Condon Factors through fitting a Morse Potential
        - turning points determined by RKR method, Gilmore (1964)
        - vibrational and rotational constants are from Gilmore (1991)
        - computes the overlap of the wavefunctions to get the FCF

"""
import numpy as np
from scipy.constants import elementary_charge as elementary_charge

# Coulomb force constant
k_e = 8987551787 # m/F

def reduced_energy(energy, ionization_potential):
    """returns a list of reduced energies per Kosarim eq. 5, fig. 1
    with a list of electron energies (E) and the ionization potential (J_v'_v'')

    Parameters
    ----------
    energy: list of floats
        Electron energies taken from #FIXME: add reference

    ionization_potential: float
        The ionization potential is taken from the NIST WebBook, Trickl (1989) evaluated
    """
    return [list_item / ionization_potential for list_item in energy]

def func_ej(cross_section, ionization_potential, n_valence): # using joules instead of eV
    """sets f(E/J) equal to equation 5, Kosarim (2005), with the added coulomb constant
    and is used to find the universal function

    Parameters
    ----------
    cross_section: list of floats
        Ionization cross sections for N2+

    ionization_potential: float
        The ionization potential is taken from the NIST WebBook, Trickl (1989) evaluated

    n_valence: integer
        The number of valence electrons in N2+
    """
    return [list_item * 10**-20 * (ionization_potential * elementary_charge)**2 /
            (n_valence * np.pi * elementary_charge**4 * k_e**2) for list_item in cross_section]

def func_guess_1(pos_x, a_coef, b_coef, c_coef):
    """this is the first guess for what could fit the f(E/J) data:
        Taken from equation 6, Kosarim (2005)

    Parameters
    ----------
    pos_x: list of floats
        These are the reduced energies that serve as the independent variable

    a_coef: float
        First coefficient fitting constant

    b_coef: float
        Second coefficient fitting constant

    c_coef: float
        Third coefficient fitting constant
    """
    return [(a_coef * (list_item + b_coef)) /
            (np.pi * list_item * (list_item + c_coef)) for list_item in pos_x]

def func_guess_2(pos_x, a_coef, b_coef, c_coef, d_coef):
    """this is the second guess for what could fit the f(E/J) data:
        Taken from equation 7, Kosarim (2005)

    Parameters
    ----------
    pos_x: list of floats
        These are the reduced energies that serve as the independent variable

    a_coef: float
        First coefficient fitting constant

    b_coef: float
        Second coefficient fitting constant

    c_coef: float
        Third coefficient fitting constant

    d_coef: float
        Fourth coefficient fitting constant
    """
    return [(a_coef * (list_item + b_coef)) /
            (np.pi * (list_item + c_coef) * (list_item + d_coef)) for list_item in pos_x]
