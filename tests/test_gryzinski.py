import nepc.methods.wunderlich.gryzinski as gryzinski
import numpy as np
import math
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

def test_gryzinski_1():
    assert isinstance(gryzinski.gryzinski(p_state, pp_state, 0, 0, FCF, [16.0], EPSILON), tuple)

def test_gryzinski_2():
    assert  isinstance(gryzinski.gryzinski(p_state, pp_state, 0, 0, FCF, [16.0], EPSILON)[0], np.ndarray)

def test_gryzinski_3():
    assert  isinstance(gryzinski.gryzinski(p_state, pp_state, 0, 0, FCF, [16.0], EPSILON)[0], np.ndarray)

def test_gryzinski_4():
    assert gryzinski.gryzinski(p_state, pp_state, 0, 0, FCF, [16.0], EPSILON)[1][0] == approx(((N_e * SIGMA_NAUGHT / E_THR**2) *
                                                                                              math.sqrt(EPSILON**2 * 16.0 / (EPSILON + 16.0)**3) *
                                                                                              (1 - (E_THR / 16.0))**((2*EPSILON + E_THR) / (EPSILON + E_THR)) *
                                                                                              ((E_THR / EPSILON) + (2/3) * (1 - (E_THR / (2 * 16.0))) *
                                                                                              math.log(math.exp(1) + math.sqrt(abs(16.0 - E_THR) / EPSILON)))))
