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
LITTLE_A = mp.little_a_20(REDUCED_MASS, DE, WE)

def test_C1_10():
    assert mp.C1_10(BIG_A, LITTLE_A, R0, ALPHA) == approx((BIG_A / (LITTLE_A * R0 * power(np.int64(1) + ALPHA, np.int64(2)))) *
                                                    (np.int64(4) - (np.int64(6) / LITTLE_A * R0)))
C1 = mp.C1_10(BIG_A, LITTLE_A, R0, ALPHA)

def test_C2_11():
    assert mp.C2_11(BIG_A, LITTLE_A, R0, ALPHA) == approx((BIG_A / (LITTLE_A * R0 * power(np.int64(1) + ALPHA, np.int64(2)))) *
                                                    (np.int64(1) - (np.int64(3) / LITTLE_A * R0)))
C2 = mp.C2_11(BIG_A, LITTLE_A, R0, ALPHA)

def test_D1_8():
    assert mp.D1_8(DE, LITTLE_A, RE, ALPHA) == approx(DE * exp(-LITTLE_A * RE * ALPHA))

D1 = mp.D1_8(DE, LITTLE_A, RE, ALPHA)

def test_D2_9():
    assert mp.D2_9(DE, LITTLE_A, RE, ALPHA) == approx(DE * exp(-np.int(2) * LITTLE_A * RE * ALPHA))

D2 = mp.D2_9(DE, LITTLE_A, RE, ALPHA)

def test_K1_6():
    assert mp.K1_6(D2, C2, WEXE) == approx(np.int(2) * sqrt((D2 - C2) / WEXE))

K1 = mp.K1_6(D2, C2, WEXE)

def test_K2_7():
    assert mp.K2_7(D1, C1, WEXE, K1) == approx(np.int64(2) * (np.int64(2) * D1 - C1) / (WEXE * K1))

K2 = mp.K2_7(D1, C1, WEXE, K1)

V_term = 0

def test_log_norm():
    assert mp.log_norm(LITTLE_A, K2, V_term) == approx((log10(LITTLE_A * (K2 - np.int64(2) * V_term - np.int64(1))) -
                                                        log10(factorial(V_term, exact=True)) -
                                                        loggamma(K2 - V_term) / log(np.int64(10))) / np.int64(2))

DELTA_R = 0.5 # taken from what we use in pcs-optimize.ipynb
K_term = 15 # taken from what we use in pcs-optimize.ipynb

def test_r_array_1():
    assert mp.r_array(RE, RE, DELTA_R, K_term)[0] == approx(2**K_term + 1)

R_LEN =  mp.r_array(RE, RE, DELTA_R, K_term)[0]

def test_r_array_2():
    assert mp.r_array(RE, RE, DELTA_R, K_term)[1] == approx((RE + RE)/2.0 - DELTA_R * np.sinh(1 - np.arange(R_LEN) * pow(2, (1 - K_term))) / np.sinh(1))

R_ARRAY =  mp.r_array(RE, RE, DELTA_R, K_term)[1]

Z_term = K1 * exp(-LITTLE_A * (R_ARRAY - R0))

def test_log_psi():
    assert mp.log_psi(Z_term, K2, V_term) == approx((-Z_term / np.int64(2)) * log10(EULER) +
                                                    ((K2 - np.int64(2) * V_term - np.int64(1)) / np.int64(2)) *
                                                    log10(Z_term))

def test_Te():
    assert mp.Te(TO, WE, WEXE) == approx(TO - WE / 2 + WEXE / 4)

TE = mp.Te(TO, WE, WEXE)

def test_Tv():
    assert mp.Tv(V_term, TO, WE, WEXE) == approx(TE + WE*(V_term + 1/2) - WEXE*(V_term + 1/2)**2)
