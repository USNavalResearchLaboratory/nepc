import numpy as np
from numpy import pi as PI
from scipy.constants import elementary_charge as ELEMENTARY_CHARGE
from nepc import nepc
from nepc.util.constants import WAVENUMBER_PER_EV as WAVENUMBER_PER_EV
from nepc.util.constants import K_E as K_E
from nepc.util.constants import N2_DIATOMIC_CONSTANTS as N2_DIATOMIC_CONSTANTS
from nepc.util.constants import N2_VALENCE as N2_VALENCE
from nepc.util.std_incident_energy import INCIDENT_ENERGY as INCIDENT_ENERGY
from nepc.methods.mp import Tv as Tv

def universal_function(ej, a, b, c):
    """universal function from fit to total cross section data"""
    return np.float64(a * (ej - 1)/((ej + b) * (ej + c)))

def pcs(p_state, pp_state, vp, vpp, fcf, a, b, c, electron_energy=INCIDENT_ENERGY):
    """returns an array of the partial cross section (m^2) of the respective incident electron energy (eV)"""
    """default values a, b, c for universal function are from fit to N2 total cross section data"""

    valence = N2_VALENCE[p_state][pp_state]

    p_To = N2_DIATOMIC_CONSTANTS[p_state]['To']
    p_we = N2_DIATOMIC_CONSTANTS[p_state]['we']
    p_wexe = N2_DIATOMIC_CONSTANTS[p_state]['wexe']

    pp_To = N2_DIATOMIC_CONSTANTS[pp_state]['To']
    pp_we = N2_DIATOMIC_CONSTANTS[pp_state]['we']
    pp_wexe = N2_DIATOMIC_CONSTANTS[pp_state]['wexe']

    Tv_vp = Tv(vp, p_To, p_we, p_wexe)
    Tv_vpp = Tv(vpp, pp_To, pp_we, pp_wexe)

    Tv_vppvp = Tv_vpp - Tv_vp
    Tv_vppvp_ev = Tv_vppvp / WAVENUMBER_PER_EV

    pcs_list = []
    for i in electron_energy:
        sigma = np.float64(valence * K_E**2 * PI * ELEMENTARY_CHARGE**4 *
                           universal_function((i/Tv_vppvp_ev), a=a, b=b, c=c) *
                           np.float64(fcf) / (Tv_vppvp_ev * ELEMENTARY_CHARGE)**2)
        if sigma < 0.0:
            pcs_list.append(0.0)
        else:
            pcs_list.append(sigma)

    return np.asarray(electron_energy), np.asarray(pcs_list)
