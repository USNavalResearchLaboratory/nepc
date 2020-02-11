import nepc.methods.thomson as thomson
import numpy as np
from numpy import exp
from numpy import power
from scipy.special import binom as binom
from numpy import log10 as log10
from scipy.special import gamma as gamma
from scipy.integrate import simps as simps
from nepc.util.constants import N2_DIATOMIC_CONSTANTS as N2_DIATOMIC_CONSTANTS
from nepc.util.constants import MU_NITROGEN_KG as REDUCED_MASS
from pytest import approx as approx

TO = N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)']['To'],
WE = N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)']['we']
WEXE = N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)']['wexe']
BE = N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)']['Be']
RE = N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)']['re']
DE = N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)']['De']

VP = 0
VPP = 0
K_term = 15
DELTA_R = 0.5

def test_fcf_v_1():
    assert isinstance(thomson.fcf_v(VP, VPP, N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'],
                         N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'], REDUCED_MASS, K_term,
                         DELTA_R, dbug=False), list)

def test_fcf_v_2():
    assert thomson.fcf_v(VP, VPP, N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'],
                         N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'], REDUCED_MASS, K_term,
                         DELTA_R, dbug=False)[0][0] == approx(1.0)

FCF = thomson.fcf_v(VP, VPP, N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'],
                         N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'], REDUCED_MASS, K_term,
                         DELTA_R, dbug=False)

def test_psi_v_1():
    assert isinstance(thomson.psi_v(VP, VPP, N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'],
                         N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'], REDUCED_MASS, K_term,
                         DELTA_R, dbug=False), tuple)
def test_psi_v_2():
    assert isinstance(thomson.psi_v(VP, VPP, N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'],
                         N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'], REDUCED_MASS, K_term,
                         DELTA_R, dbug=False)[0], np.ndarray)
def test_psi_v_3():
    assert isinstance(thomson.psi_v(VP, VPP, N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'],
                         N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'], REDUCED_MASS, K_term,
                         DELTA_R, dbug=False)[1], np.ndarray)

def test_psi_v_4():
    assert isinstance(thomson.psi_v(VP, VPP, N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'],
                         N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'], REDUCED_MASS, K_term,
                         DELTA_R, dbug=False)[2], np.ndarray)

def test_psi_v_5():
    assert isinstance(thomson.psi_v(VP, VPP, N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'],
                         N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'], REDUCED_MASS, K_term,
                         DELTA_R, dbug=False)[3], dict)

def test_psi_v_5():
    assert isinstance(thomson.psi_v(VP, VPP, N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'],
                         N2_DIATOMIC_CONSTANTS['N2(X1Sigmag+)'], REDUCED_MASS, K_term,
                         DELTA_R, dbug=False)[4], dict)

def test_rmse_diagonal_elements():
    assert isinstance(thomson.rmse_diagonal_elements(np.asarray(FCF)), np.float64)

"""Fix this
def test_incremental_rmse_diagonal_elements():
    assert isinstance(thomson.incremental_rmse_diagonal_elements(np.asarray(FCF)), None)
"""

def test_rmse_off_diagonal_elements():
    assert isinstance(thomson.rmse_off_diagonal_elements(np.asarray(FCF)), np.float64)

