import numpy as np
from scipy.constants import elementary_charge as ELEMENTARY_CHARGE
from scipy.constants import Planck as PLANCK
from scipy.constants import speed_of_light as SPEED_OF_LIGHT
from scipy.constants import Avogadro as AVOGADRO
from numpy import pi as PI
from nepc import nepc
from nepc.util.constants import WAVENUMBER_PER_EV as WAVENUMBER_PER_EV
from nepc.util.constants import K_E as K_E
from nepc.util.constants import vib_constants_N2
from nepc.util.constants import vib_constants_N2p

incident_ee = np.asarray([16.0,16.5,17.0,17.5,18.0,18.5,19.0,19.5,20.0,20.5,21.0,21.5,
                          22.0,22.5,23.0,23.5,24.0,24.5,25.0,30.0,35.0,40.0,45.0,50.0,
                          55.0,60.0,65.0,70.0,75.0,80.0,85.0,90.0,95.0,100.0,110.0,120.0,
                          140.0,160.0,180.0,200.0,225.0,250.0,275.0,300.0,350.0,400.0,
                          450.0,500.0,550.0,600.0,650.0,700.0,750.0,800.0,850.0,900.0,
                          950.0,1000.0])

def universal_function(reduced_energy):
    """based off of Paul's fitting coefficients"""
    return np.float64(47.3 * (reduced_energy - 1)/((reduced_energy + 2.4) * (reduced_energy + 9.2)))

def gv_poly(v_level, we_spec, wexe_spec, weye_spec, weze_spec=0, weae_spec=0):
    """Vibrational energy level polynomial: Table 1 in Laher and Gilmore (1991)"""
    return (we_spec*(v_level + 1/2) - wexe_spec*(v_level + 1/2)**2 + weye_spec*(v_level + 1/2)**3 +
            weze_spec*(v_level + 1/2)**4 + weae_spec*(v_level + 1/2)**5)

def te_energy(v_level, t0_spec, we_spec, wexe_spec, weye_spec, weze_spec=0, weae_spec=0):
    """Energy at minimum of well; Equilibrium term value: Table 1 in Laher and Gilmore (1991)"""
    return (t0_spec - we_spec/2 + wexe_spec/4 - weye_spec/8 - weze_spec/16 - weae_spec/32)

def tv_energy(v_level, t0_spec, we_spec, wexe_spec, weye_spec, weze_spec=0, weae_spec=0):
    """Energy difference from minimum to vibrational energy level: Table 1 in Laher and Gilmore (1991)"""
    return (te_energy(v_level, t0_spec, we_spec, wexe_spec, weye_spec, weze_spec, weae_spec) +
            gv_poly(v_level, we_spec, wexe_spec, weye_spec, weze_spec, weae_spec))

def pcs(p_state, vp_level, pp_state, vpp_level, fcf, electron_energy='NaN'):
    """returns an array of the partial cross section (m^2) of the respective incident electron energy (eV)"""
    if electron_energy=='NaN':
        electron_energy = incident_ee

    if p_state == 'N2(X1Sigmag+)':
        (p_t0, p_we, p_wexe, p_weye, p_weze, p_weae) = vib_constants_N2[0]
    if pp_state == 'N2+(X2Sigmag+)':
        num_valence = 2
        (pp_t0, pp_we, pp_wexe, pp_weye, pp_weze, pp_weae) = vib_constants_N2p[0]
    elif pp_state == 'N2+(A2Piu)':
        num_valence = 4
        (pp_t0, pp_we, pp_wexe, pp_weye, pp_weze, pp_weae) = vib_constants_N2p[1]
    elif pp_state == 'N2+(B2Sigmau+)':
        num_valence = 2
        (pp_t0, pp_we, pp_wexe, pp_weye, pp_weze, pp_weae) = vib_constants_N2p[2]

    tv_vp = tv_energy(vp_level, p_t0, p_we, p_wexe, p_weye, p_weze, p_weae)
    tv_vpp = tv_energy(vpp_level, pp_t0, pp_we, pp_wexe, pp_weye, pp_weze, pp_weae)

    tv_vppvp = t_vpp - t_vp
    tv_vppvp_ev = tvpp_vp / WAVENUMBER_PER_EV

    pcs_list = []
    for i in electron_energy:
        sigma_pp_vpp = num_valence * K_E**2 * PI * ELEMENTARY_CHARGE**4 * universal_function(i/tv_vppvp_ev) * fcf / (tv_vppvp_ev * ELEMENTARY_CHARGE)**2
        pcs_list.append([i, sigma_pp_vpp])

    return pcs_list

