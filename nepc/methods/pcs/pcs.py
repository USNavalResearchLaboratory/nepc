import numpy as np
from scipy.constants import elementary_charge as ELEMENTARY_CHARGE
from scipy.constants import Planck as PLANCK
from scipy.constants import speed_of_light as SPEED_OF_LIGHT
from scipy.constants import Avogadro as AVOGADRO
from numpy import pi as PI
from nepc import nepc
from nepc.util.constants import WAVENUMBER_PER_EV as WAVENUMBER_PER_EV
from nepc.util.constants import K_E as K_E
from nepc.util.constants import N2_DIATOMIC_CONSTANTS as N2_DIATOMIC_CONSTANTS
from nepc.methods.mp import Te as Te
from nepc.methods.mp import Tv as Tv

N2_VALENCE = {'N2+(X2Sigmag+)': 2, 'N2+(A2Piu)': 4, 'N2+(B2Sigmau+)': 2}

incident_ee = np.asarray([16.0,16.5,17.0,17.5,18.0,18.5,19.0,19.5,20.0,20.5,21.0,21.5,
                          22.0,22.5,23.0,23.5,24.0,24.5,25.0,30.0,35.0,40.0,45.0,50.0,
                          55.0,60.0,65.0,70.0,75.0,80.0,85.0,90.0,95.0,100.0,110.0,120.0,
                          140.0,160.0,180.0,200.0,225.0,250.0,275.0,300.0,350.0,400.0,
                          450.0,500.0,550.0,600.0,650.0,700.0,750.0,800.0,850.0,900.0,
                          950.0,1000.0])

def universal_function(ej, a, b, c):
    """universal function from fit to total cross section data"""
    return np.float64(a * (ej - 1)/((ej + b) * (ej + c)))

def pcs(p_state, pp_state, vp, vpp, fcf, a=47.3, b=2.4, c=9.2, electron_energy=incident_ee):
    """returns an array of the partial cross section (m^2) of the respective incident electron energy (eV)"""
    """default values a, b, c for universal function are from fit to N2 total cross section data"""

    valence = N2_VALENCE[pp_state]

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
            pcs_list.append([i, 0.0])
        else:
            pcs_list.append([i, sigma])

    return pcs_list

