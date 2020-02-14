import nepc.methods.wunderlich.gryzinski_dr as gryzinski_dr
import numpy as np
import math
from scipy.constants import elementary_charge as ELEMENTARY_CHARGE
from math import pi as PI
from nepc import nepc
from nepc.util.constants import WAVENUMBER_PER_EV as WAVENUMBER_PER_EV
from nepc.util.constants import K_E as K_E
from nepc.util.constants import N2_DIATOMIC_CONSTANTS as N2_DIATOMIC_CONSTANTS
from nepc.methods.mp import Tv as Tv
from pytest import approx as approx

FCF = 0.911
EPSILON = 15.581 # Ionization potential

p_state = 'N2(X1Sigmag+)'
pp_state = 'N2+(X2Sigmag+)'

SIGMA_NAUGHT = 6.56e-18
N_e = 2
P_TO = N2_DIATOMIC_CONSTANTS[p_state]['To']
P_WE = N2_DIATOMIC_CONSTANTS[p_state]['we']
P_WEXE = N2_DIATOMIC_CONSTANTS[p_state]['wexe']
PP_TO = N2_DIATOMIC_CONSTANTS[pp_state]['To']
PP_WE = N2_DIATOMIC_CONSTANTS[pp_state]['we']
PP_WEXE = N2_DIATOMIC_CONSTANTS[pp_state]['wexe']
TV_VP = Tv(0, P_TO, P_WE, P_WEXE)
TV_VPP = Tv(0, PP_TO, PP_WE, PP_WEXE)
TV_VPPVP = TV_VPP - TV_VP
E_THR = float(TV_VPPVP / WAVENUMBER_PER_EV)

def test_g_dr_1():
    assert gryzinski_dr.g_dr(2) == approx(0.66 * math.log(1.25*2) * ((1/2) - (1/2**2)))

def test_g_dr_2():
    assert isinstance(gryzinski_dr.g_dr(2), float)

def test_gryzinski_dr_1():
    assert isinstance(gryzinski_dr.gryzinski_dr(p_state, pp_state, 0, 0, FCF, [16.0], EPSILON), tuple)

def test_gryzinski_dr_2():
    assert isinstance(gryzinski_dr.gryzinski_dr(p_state, pp_state, 0, 0, FCF, [16.0], EPSILON)[0], np.ndarray)

def test_gryzinski_dr_3():
    assert isinstance(gryzinski_dr.gryzinski_dr(p_state, pp_state, 0, 0, FCF, [16.0], EPSILON)[1], np.ndarray)

def test_gryzinski_dr_4():
    assert gryzinski_dr.gryzinski_dr(p_state, pp_state, 0, 0, FCF, [16.0], EPSILON)[1][0] == approx(N_e * (K_E**2 * PI * ELEMENTARY_CHARGE**4 / (E_THR*ELEMENTARY_CHARGE)**2) * gryzinski_dr.g_dr(16.0/E_THR))

