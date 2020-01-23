import numpy as np
import math
from scipy.constants import elementary_charge as ELEMENTARY_CHARGE
from math import pi as PI
from nepc import nepc
from nepc.util.constants import WAVENUMBER_PER_EV as WAVENUMBER_PER_EV
from nepc.util.constants import K_E as K_E
from nepc.util.constants import N2_DIATOMIC_CONSTANTS as N2_DIATOMIC_CONSTANTS
from nepc.methods.mp import Tv as Tv

N2_VALENCE = {'N2(X1Sigmag+)': {'N2+(X2Sigmag+)': 2, 'N2+(A2Piu)': 4, 'N2+(B2Sigmau+)': 2, 'N2+(C2Sigmau+)': 0}}

def g_dr(x):
    return 0.66 * math.log(1.25*x) * ((1/x) - (1/x**2))

def gryzinski_dr(p_state, pp_state, vp, vpp, fcf, electron_energy, epsilon=15.581):
    """returns the cross section in terms of m^2
       N_e: the effective number of equivalent electrons in the inital state of the transistion
       E_e (also noted E_2): inital energy of the impinging electron
       E_thr: lower limit of the energy gain or threshold energy
       epsilon (also noted I): initial kinetic energy of the orbital electron to be excited;
                can be set to the ionization potential"""

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
    E_thr = float(Tv_vppvp / WAVENUMBER_PER_EV)

    sigma_list = []
    for i in electron_energy:
        E_e = i
        sigma = N_e * (K_E**2 * PI * ELEMENTARY_CHARGE**4 / (E_thr*ELEMENTARY_CHARGE)**2) * g_dr(i/E_thr)
        if type(sigma) == complex:
            sigma_list.append(0.0)
        elif sigma < 0.0:
            sigma_list.append(0.0)
        else:
            sigma_list.append(sigma * fcf)
    return np.asarray(electron_energy), np.asarray(sigma_list)

