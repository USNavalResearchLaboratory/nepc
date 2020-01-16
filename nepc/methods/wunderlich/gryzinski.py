import numpy as np

def gryzinski(N_e, E_e, E_thr, epsilon):
    """returns the cross section in terms of m^2
       N_e: the effective number of equivalent electrons in the inital state of the transistion
       E_e: inital energy of the impinging electron
       E_thr: lower limit of the energy gain or threshold energy
       epsilon: initial kinetic energy of the orbital electron to be excited;
                can be set to the ionization potential"""
    sigma_naught = 6.56e-18

    sigma = ((N_e * sigma_naught / E_thr**2) * np.sqrt(epsilon**2 * E_e / (epsilon + E_e)**3) *
            (1 - (E_thr / E_e))**((2*epsilon + E_thr) / (epsilon + E_thr)) *
            ((E_thr / epsilon) + (2 / 3) * (1 - (E_thr / (2 * E_e))) * np.log(np.exp(1) + np.sqrt((E_e - E_thr) / epsilon))))
    return sigma
