from nepc.methods.mp import mp
import numpy as np
from numpy import e as EULER
from numpy import sqrt
from numpy import exp
from numpy import power
from numpy import log10
from numpy import log
from scipy.special import loggamma
from scipy.special import factorial
from scipy.constants import Planck as PLANCK
from scipy.constants import Avogadro as AVOGADRO
from scipy.constants import speed_of_light as SPEED_OF_LIGHT
from scipy.constants import pi as PI
from nepc.util.constants import N2_DIATOMIC_CONSTANTS as N2_DIATOMIC_CONSTANTS
from nepc.util.constants import MU_NITROGEN_KG as REDUCED_MASS
from pytest import approx as approx

PLANCK, AVOGADRO, SPEED_OF_LIGHT, PI, EULER = np.float64(
        (PLANCK, AVOGADRO, SPEED_OF_LIGHT, PI, EULER))

TO = N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)']['To'],
WE = N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)']['we']
WEXE = N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)']['wexe']
BE = N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)']['Be']
RE = N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)']['re']
DE = N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)']['De']

def test_big_A_5():
    assert mp.big_A_5(BE, 0) == approx(BE * 0 * (0 + 1))

BIG_A = mp.big_A_5(BE, 0)

def test_alpha_4():
    assert mp.alpha_4(BIG_A, BE, WE) == approx(np.int64(4) * BIG_A * BE / WE**2)

ALPHA = mp.alpha_4(BIG_A, BE, WE)

def test_r0_3():
    assert mp.r0_3(RE, ALPHA) == approx(RE * (np.int64(1) + ALPHA))

R0 = mp.r0_3(RE, ALPHA)

def test_De():
    assert mp.De(WE, WEXE) == approx(power(WE, np.int64(2)) / (np.int64(4) * WEXE))

def test_little_a_20():
    assert mp.little_a_20(REDUCED_MASS, DE, WE) == approx(np.float64(2E-9) * PI * SPEED_OF_LIGHT
                                                           * WE * sqrt(REDUCED_MASS /(np.int64(2)
                                                           * PLANCK * SPEED_OF_LIGHT * DE)))
