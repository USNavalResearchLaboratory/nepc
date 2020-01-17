import numpy as np
from nepc import nepc
from nepc.util.constants import WAVENUMBER_PER_EV as WAVENUMBER_PER_EV
from nepc.util.constants import K_E as K_E
from nepc.util.constants import N2_DIATOMIC_CONSTANTS as N2_DIATOMIC_CONSTANTS
from nepc.methods.mp import Tv as Tv

N2_VALENCE = {'N2(X1Sigmag+)': {'N2+(X2Sigmag+)': 2, 'N2+(A2Piu)': 4, 'N2+(B2Sigmau+)': 2, 'N2+(C2Sigmau+)': 0}}

def gryzinski(p_state, pp_state, vp, vpp, fcf, electron_energy, epsilon=15.581):
    """returns the cross section in terms of m^2
       N_e: the effective number of equivalent electrons in the inital state of the transistion
       E_e: inital energy of the impinging electron
       E_thr: lower limit of the energy gain or threshold energy
       epsilon: initial kinetic energy of the orbital electron to be excited;
                can be set to the ionization potential"""
    sigma_naught = np.float64(6.56e-18)

    N_e = N2_VALENCE[p_state][pp_state]

    p_To = N2_DIATOMIC_CONSTANTS[p_state]['To']
    p_we = N2_DIATOMIC_CONSTANTS[p_state]['we']
    p_wexe = N2_DIATOMIC_CONSTANTS[p_state]['wexe']

    pp_To = N2_DIATOMIC_CONSTANTS[pp_state]['To']
    pp_we = N2_DIATOMIC_CONSTANTS[pp_state]['we']
    pp_wexe = N2_DIATOMIC_CONSTANTS[pp_state]['wexe']

    Tv_vp = Tv(vp, p_To, p_we, p_wexe)
    Tv_vpp = Tv(vpp, pp_To, pp_we, pp_wexe)

    Tv_vppvp = Tv_vpp - Tv_vp
    E_thr = Tv_vppvp / WAVENUMBER_PER_EV

    sigma_list = []
    for i in electron_energy:
        E_e = i
        sigma = np.float64((N_e * sigma_naught / E_thr**2) * np.sqrt(epsilon**2 * E_e / (epsilon + E_e)**3) * (1 - (E_thr / E_e))**((2*epsilon + E_thr) / (epsilon + E_thr)) * ((E_thr / epsilon) + (2 / 3) * (1 - (E_thr / (2 * E_e))) * np.log(np.exp(1) + np.sqrt((E_e - E_thr) / epsilon))))
        if sigma < 0.0:
            sigma_list.append(0.0)
        else:
            sigma_list.append(sigma * fcf)
    return np.asarray(electron_energy), np.asarray(sigma_list)
