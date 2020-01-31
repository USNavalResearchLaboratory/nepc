"""Tests for nepc/methods/pcs.py"""
import pytest
import nepc
import numpy as np
import nepc.methods.pcs.pcs as pcs
from pytest import approx
from nepc.util.constants import WAVENUMBER_PER_EV as WAVENUMBER_PER_EV
from nepc.util.constants import K_E as K_E
from scipy.constants import elementary_charge as ELEMENTARY_CHARGE
from scipy.constants import pi as PI

def test_universal_function():
    assert pcs.universal_function(16/15.581, 2.563, 1.009, 11.746) == approx(np.float64(2.563 * (16/15.581 - 1)/((16/15.581 + 1.009) * (16/15.581 + 11.746))))

def test_pcs():
    assert pcs.pcs("N2(X1Sigmag+)", "N2+(X2Sigmag+)", 0, 0, 0.911, 2.563, 1.009, 11.746, [16.0])[1][0] == approx(np.float64(2 * K_E**2 * PI * ELEMENTARY_CHARGE**4 * (np.float64(2.563 * (16.0/15.581 - 1)/((16.0/15.581 + 1.009) * (16.0/15.581 + 11.746))) * 0.911 / (15.851 * ELEMENTARY_CHARGE)**2)))

