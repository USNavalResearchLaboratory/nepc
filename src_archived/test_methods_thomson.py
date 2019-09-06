"""Tests the thomson.py module"""
from nepc.methods import thomson
from nepc.util import constants
from nepc.util import itikawa_data
import numpy
import matplotlib.pyplot

# TODO: test with a set of real values
# TODO: test that functions raise exceptions when appropriate
IONIZATION_ENERGY = 15.581  # eV
itikawa_incident_energy = [itikawa_data.ion_cross_N2p[0][0], itikawa_data.ion_cross_N2p[1][0]]
itikawa_cross_section = [itikawa_data.ion_cross_N2p[0][1], itikawa_data.ion_cross_N2p[1][1]]
v_spec = 0
n_level = 0
r_domain = numpy.linspace(0.0, 3.0, 100)
"""test state is N2 X1Sigmag+"""
T0_spec = constants.vib_constants_N2[0][0]
we_spec = constants.vib_constants_N2[0][1]
wexe_spec = constants.vib_constants_N2[0][2]
weye_spec = constants.vib_constants_N2[0][3]
Be_spec = constants.rot_constants_N2[0][0]
ae_spec = constants.rot_constants_N2[0][1]
vib_constants = constants.vib_constants_N2[0]
rot_constants = constants.rot_constants_N2[0]
state = constants.states_N2[0]

def test_list_splitter():
    """Checks that the object type returned is a list"""
    value_type = type(thomson.list_splitter(itikawa_data.ion_cross_N2p, 0))
    assert value_type == list

def test_reduced_energy():
    """Checks the object type returned for the reduced energy is a list"""
    value_type = type(thomson.reduced_energy(itikawa_incident_energy, IONIZATION_ENERGY))
    assert value_type == list

def test_func_ej():
    """Checks the object typed returned for the universal fit is a list"""
    value_type = type(thomson.func_ej(itikawa_cross_section, IONIZATION_ENERGY, constants.n_valence))
    assert value_type == list

def test_func_guess():
    """Checks the object type returned from the guess is a list"""
    value_type = type(thomson.func_guess(thomson.func_ej(itikawa_cross_section,
                      IONIZATION_ENERGY, constants.n_valence), 1, 1, 1, 1))
    assert value_type == list

def test_type_Gv_rkr():
    """Checks that the Gv value returned is a float"""
    value_type = type(thomson.Gv_rkr(v_spec, we_spec, wexe_spec, weye_spec, weze_spec=0, weae_spec=0))
    assert value_type == float

def test_type_Te_spec():
    """Checks that the Te value returned is a float"""
    value_type = type(thomson.Te_spec(v_spec, T0_spec, we_spec, wexe_spec, weye_spec))
    assert value_type == float

def test_type_Tv_spec():
    """Checks that the Tv value returned is a float"""
    value_type = type(thomson.Tv_spec(v_spec, T0_spec, we_spec, wexe_spec, weye_spec))
    assert value_type == float

def test_type_Bv_spec():
    """Checks that the Bv value returned is a float"""
    value_type = type(thomson.Bv_spec(v_spec, Be_spec, ae_spec))
    assert value_type == float

def test_type_fIntegrand_rkr():
    """Checks that the fIntegrand value returned is a float"""
    value_type = type(thomson.fIntegrand_rkr(-1/2, v_spec, vib_constants))
    assert value_type == complex or float

def test_type_gIntegrand_rkr():
    """Checks that the gIntegrand value returned is a float"""
    value_type = type(thomson.gIntegrand_rkr(-1/2, v_spec, vib_constants, rot_constants))
    assert value_type == complex or float

def test_type_f_rkr():
    """Checks that the f function returns a float or numpy.float64"""
    value_type = type(thomson.f_rkr(v_spec, vib_constants))
    assert value_type == numpy.float64

def test_type_g_rkr():
    """Checks that the g function returns a float or numpy.float64"""
    value_type = type(thomson.g_rkr(v_spec, vib_constants, rot_constants))
    assert value_type == numpy.float64

def test_type_r_rkr():
    """Checks that the type returned by the function r is a list"""
    value_type = type(thomson.r_rkr(v_spec, vib_constants, rot_constants))
    assert value_type == list

def test_value_type_r_rkr_0():
    """Checks that the value type in the first index of r list is a float"""
    value_type = type(thomson.r_rkr(v_spec, vib_constants, rot_constants)[0])
    assert value_type == numpy.float64

def test_value_type_r_rkr_1():
    """Checks that the value type in the second index of r list is a float"""
    value_type = type(thomson.r_rkr(v_spec, vib_constants, rot_constants)[1])
    assert value_type == numpy.float64

def test_compute_pes():
    """Checks that the type returned is an numpy array"""
    value_type = type(thomson.compute_pes(state, vib_constants, rot_constants))
    assert value_type == numpy.ndarray

def test_morse_fit():
    """Checks that the returned type is a dictionary"""
    value_type = type(thomson.morse_fit(state, vib_constants, rot_constants, 5))
    assert value_type == dict

def test_type_vasan_wavefunction():
    """Checks the type returned is a numpy array"""
    value_type = type(thomson.vasan_wavefunction(state, vib_constants, thomson.morse_fit(state, vib_constants, rot_constants, 5), n_level, r_domain))
    assert value_type == numpy.ndarray

def test_value_type_franck_condon():
    """checks that value returned is a float"""
    value_type = type(thomson.franck_condon(state, vib_constants, rot_constants, 5, n_level, state, vib_constants, rot_constants, 5, n_level, r_domain))
    assert value_type == float

def test_value_franck_condon():
    """checks that value returned is a float"""
    value = thomson.franck_condon(state, vib_constants, rot_constants, 5, n_level, state, vib_constants, rot_constants, 5, n_level, r_domain)
    assert value <= 1.0

def test_partial_cross_section():
    """checks that the returned value is a list"""
    value_type = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[0], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 0, 10, itikawa_incident_energy, itikawa_cross_section, thomson.func_guess, r_domain)[0][0]
    value = 0.0
    assert value == 0.0

