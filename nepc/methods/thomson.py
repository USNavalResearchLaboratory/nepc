"""Module for computing the ionization cross sections from Thomson scattering

Ref/Methods
-----------
From Kosarim (2005):
    - Uses Equation 5 to calculate the universal function from electron energy
    and ionization potential
        - The equation is missing the coulomb force constant (k_e),
        which must be squared
    - Uses Equation 11 to calculate the ionization cross section
        - also missing the coulomb force constant (k_e) squared

From Vasan (1982):
    - Morse Potential
        - V(r) = De[1-exp(-Beta(r-re))]^2
    - Normalized Wavefunction
        - Psi = N*exp(-z/2)*z^(b/2)*Lnb(z)

From Gilmore (1965, 1991):
    - Determine Franck-Condon Factors through fitting a Morse Potential
        - turning points determined by RKR method, Gilmore (1964)
        - vibrational and rotational constants are from Gilmore (1991)
        - computes the overlap of the wavefunctions to get the FCF

From Itikawa:
    - Contains the incident electron energy and the partial cross section for each
        - used to form universal function, although presently we're using Kosarim's
          equation 7 to make the final cross section calculations
"""
import warnings
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy.optimize import curve_fit
from scipy.constants import elementary_charge
from scipy.constants import Planck
from scipy.constants import speed_of_light
from scipy.integrate import quadrature
from scipy import optimize
from scipy.special import assoc_laguerre
from nepc import nepc
from nepc.util import constants


def list_splitter(specific_list, column):
    """takes a list with multiple indexes and splits it into a single list

    Parameters
    ----------
    specific_list: list
        Any list of values

    index: integer
        Gives the column of data desired
    """
    split_list = []

    i = 0
    while i < len(specific_list):
        split_list.append(specific_list[i][column])
        i += 1

    return split_list


def reduced_energy(energy, ionization_potential):
    """returns a list of reduced energies per Kosarim eq. 5, fig. 1
    with a list of electron energies (E) and the ionization potential
    (J_v'_v'')

    Parameters
    ----------
    energy: list of floats
        Electron energies taken from #FIXME: add reference

    ionization_potential: float
        The ionization potential is taken from the NIST WebBook, Trickl (1989)
        evaluated
    """

    return [list_item / ionization_potential for list_item in energy]


# TODO: document units correctly (using joules instead of eV)
def func_ej(initial_cross_section, ionization_potential, n_valence):
    """sets f(E/J) equal to equation 5, Kosarim (2005), with the added coulomb
    constant and is used to find the universal function

    Parameters
    ----------
    initial_cross_section: list of floats
        Ionization cross sections from LxCat

    ionization_potential: float
        The ionization potential is taken from the NIST WebBook, Trickl (1989)
        evaluated

    n_valence: integer
        The number of valence electrons in N2+

    Calculation notes
    -----------------
    The cross_section comes in as angstrom^2 but is converted to m^2

    The ionization_potential is converted from eV to J

    k_e is in N*m^2/C^2
    """
    return [list_item * 10**-20 *
            (ionization_potential * elementary_charge)**2 /
            (n_valence * np.pi * elementary_charge**4 * constants.k_e**2)
            for list_item in initial_cross_section]


def func_guess(red_energy, a_coef, b_coef, c_coef, d_coef):
    """this is the second guess for what could fit the f(E/J) data:
        Taken from equation 7, Kosarim (2005)

    Parameters
    ----------
    red_energy: list or float
        These are the reduced energies that serve as the independent variable

    a_coef: float
        First coefficient fitting constant

    b_coef: float
        Second coefficient fitting constant

    c_coef: float
        Third coefficient fitting constant

    d_coef: float
        Fourth coefficient fitting constant

    Equation
    --------
    f(E/J) = a(x+b)/(pi(x+c)(x+d))
    """

    return [(a_coef * (list_item + b_coef)) /
            (np.pi * (list_item + c_coef) * (list_item + d_coef))
            for list_item in red_energy]

def kosarim_universal_func(red_energy):
    """This is Kosarim eq. 7. It will be used to make the partial cross section fits
        for the different nitrogen gas states.

    Parameters
    ----------
    red_energy: float
        reduced electron energy
    """
    return 10 * (red_energy - 1) / (np.pi * (red_energy + 1.5) * (red_energy + 9))

def guessed_universal_func(red_energy, a_coef, b_coef, c_coef, d_coef):
    """this is the second guess for what could fit the f(E/J) data:
        Taken from equation 7, Kosarim (2005)

    Parameters
    ----------
    red_energy: float
        energy that serve as the independent variable

    a_coef: float
        First coefficient fitting constant

    b_coef: float
        Second coefficient fitting constant

    c_coef: float
        Third coefficient fitting constant

    d_coef: float
        Fourth coefficient fitting constant

    Equation
    --------
    f(E/J) = a(x+b)/(pi(x+c)(x+d))
    """

    return ((a_coef * (red_energy + b_coef)) /
            (np.pi * (red_energy + c_coef) * (red_energy + d_coef)))


def univ_func_coefficients(func_guess_function, reduced_energy_function, func_ej_function):
    """finds the coefficients of the guessed universal function of the ionization energy
    and cross section. Returns a list of popt and pcov.
        - popt has the coefficients for the guess fit equation

    Parameters
    ----------
    func_guess_function: function
        the separate universal function guess equation

    reduced_energy_function: function
        the separate reduced energy function needed to compute the coefficients
            - have to include the necessary inputs for this

    func_ej_function: function
        the f(E/J) function needed to make the fit
            - have to include the necessary inputs for this
    """
    popt, pcov = curve_fit(func_guess_function, reduced_energy_function, func_ej_function)

    return [popt, pcov]


# These functions are for calculating the turning points of the wavefunction in the potential
def Gv_rkr(v, we_spec, wexe_spec, weye_spec, weze_spec=0, weae_spec=0):
    """Vibrational energy level"""
    return (we_spec*(v+1/2) - wexe_spec*(v+1/2)**2 + weye_spec*(v+1/2)**3 +
            weze_spec*(v+1/2)**4 + weae_spec*(v+1/2)**5)


def Te_spec(v, T0_spec, we_spec, wexe_spec, weye_spec, weze_spec=0, weae_spec=0):
    """Energy at minimum of well"""
    return T0_spec - we_spec/2 + wexe_spec/4 - weye_spec/8 - weze_spec/16 - weae_spec/32


def Tv_spec(v, T0_spec, we_spec, wexe_spec, weye_spec, weze_spec=0, weae_spec=0):
    """Energy difference from minimum to vibrational energy level"""
    return (Te_spec(v, T0_spec, we_spec, wexe_spec, weye_spec, weze_spec, weae_spec) +
            Gv_rkr(v, we_spec, wexe_spec, weye_spec, weze_spec, weae_spec))


def Bv_spec(v, Be_spec, ae_spec, ge_spec=0, de_spec=0, ee_spec=0):
    """Rotational energy level"""
    return (Be_spec - ae_spec*(v+1/2) - ge_spec*(v+1/2)**2 +
            de_spec*(v+1/2)**3 + ee_spec*(v+1/2)**4)


def fIntegrand_rkr(vp, v, vib_constants):
    """Integrand of Gilmore et al (1992) eqn 1"""
    (T0_spec, we_spec, wexe_spec, weye_spec, weze_spec, weae_spec) = vib_constants
    return (1/(Gv_rkr(v, we_spec, wexe_spec, weye_spec, weze_spec) -
               Gv_rkr(vp, we_spec, wexe_spec, weye_spec, weze_spec))**0.5)


def gIntegrand_rkr(vp, v, vib_constants, rot_constants):
    """Integrand of Gilmore et al (1992) eqn 2"""
    (T0_spec, we_spec, wexe_spec, weye_spec, weze_spec, weae_spec) = vib_constants
    (Be_spec, ae_spec, ge_spec, de_spec, ee_spec) = rot_constants
    # using **5 instead of math.sqrt because it wouldn't work with quadrature integrate
    return (Bv_spec(v, Be_spec, ae_spec, ge_spec) /
            (Gv_rkr(v, we_spec, wexe_spec, weye_spec, weze_spec) -
             Gv_rkr(vp, we_spec, wexe_spec, weye_spec, weze_spec))**0.5)


def f_rkr(v, vib_constants):
    """Gilmore et al (1992) eqn 1"""
    I = quadrature(fIntegrand_rkr, -1/2, v, args=(v, vib_constants))
    return 1/(2*np.pi*(2*constants.mu_nitrogen_kg*speed_of_light/Planck))**0.5 * I[0] * 1E8


def g_rkr(v, vib_constants, rot_constants):
    """Gilmore et al (1992) eqn 2"""
    I = quadrature(gIntegrand_rkr, -1/2, v, args=(v, vib_constants, rot_constants))
    return 2*np.pi*(2*constants.mu_nitrogen_kg*speed_of_light/Planck)**0.5 * I[0] * 1E-8


def r_rkr(v, vib_constants, rot_constants):
    """Compute r_inner and r_outer from Gilmore et al (1992) eqn 3"""
    fv_rkr = f_rkr(v, vib_constants)
    gv_rkr = g_rkr(v, vib_constants, rot_constants)
    return [math.sqrt(fv_rkr**2 + fv_rkr/gv_rkr)-fv_rkr,
            math.sqrt(fv_rkr**2 + fv_rkr/gv_rkr)+fv_rkr]


def compute_pes(state, vib_constants, rot_constants, vmax=3):
    """compute vmax*2 points on a potential energy surface defined by
    vibrational constants (vib_constants) and rotational constants (rot_constants)
    for state 'state'

    Arguments
    ---------
    state : string
        the specific state indicating which vib_contants and rot_contants to use

    vib_/rot_constants : list
        spectroscopic vibrational and rotational constants

    vmax : int
        max vibrational mode of interest; vmax * 2 points will be calculated
        (r_inner's and r_outer's)

    Returns
    -------
    pes : numpy.array
        points on the PES (r, Tv)
    """
    pes = []

    #FIXME: Took off [state] from vib_constants and rot_constants
    (T0_spec, we_spec, wexe_spec, weye_spec, weze_spec, weae_spec) = vib_constants

    for vp in range(vmax + 1):
        rvp = r_rkr(vp, vib_constants, rot_constants)
        Tvp = (Tv_spec(vp, T0_spec, we_spec, wexe_spec, weye_spec, weze_spec, weae_spec) /
               constants.wavenumber_per_ev)
        pes.insert(0, [rvp[0], Tvp])
        pes.append([rvp[1], Tvp])

    pes = np.asarray(pes)

    return pes


def morse_fit(state, vib_constants, rot_constants, vmax_mode):
    """Uses the vibrational and rotation constants to create the morse potential
    and then fits it to get the morse potential constants

    Parameters
    ----------
    state: string
        defines the specific state in use

    vib_constants: dict or list
        spectroscopic constants from Laher and Gilmore

    rot_constants: dict or list
        spectroscopic constants form Laher and Gilmore

    vmax_mode: integer
        the number of vibrational modes the morse potential will have

    Notes
    -----
    This function calls several other functions that are used to calculate the
        the morse potential using the RKR method taken from Gilmore (1965).

    This function returns four sets of data:
        - Morse constants: De (cm-1), Beta (ang-1), re (ang), D0 (cm-1)
        - MSQE: mean square error between the computed point and the fit point
        - Jv: the turning point energies
        - turning points: the location of the turning points

    All of these are put into a dictionary with a key corresponding to their state
        and the vibration mode
        - ex: morse_rkr_dict[specific state][vib mode #][0][De=0, Beta=1, re=2, D0=3]
    """

    #TODO: Figure out these warnings and get rid of this
    warnings.filterwarnings('ignore')

    state_pes = compute_pes(state, vib_constants, rot_constants, vmax=vmax_mode)
    fitfunc = lambda p, x: (p[0] * (1.0 - np.exp(-p[1] * (x - p[2]))) *
                            (1.0 - np.exp(-p[1] * (x - p[2]))) + p[3])
    """optimize has a hard time doing the fit with a square in the function.
        You have to decompose it.
       Also, you have to give it a constant (p[3]) for the minimum energy when r=r_e.
       Target function
    """
    errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function

    """This portion fits the data by finding the best coefficient values"""
    # p[0]=De, p[1]=Beta, p[2]=re, p[3]=D0
    p0_0 = [10.0, 0.001, 0.11, -1.0] # Initial guess for the parameters
    p0_1, success0 = optimize.leastsq(errfunc, p0_0[:], args=(state_pes[:, 0],
                                                              state_pes[:, 1]))

    # constants taken from the fit: De (converting to cm-1), Beta (converting to ang-1),
    # re (converting to ang), D0 (converting to cm-1)
    temp_morse_constants = [p0_1[0]*constants.wavenumber_per_ev, p0_1[1]/10, p0_1[2]*10,
                            p0_1[3]*constants.wavenumber_per_ev]

    # adding the turning positions and the turning point energies into dictionaries
    temp_turning_pos = state_pes.T[0].tolist()
    temp_Jv = state_pes.T[1].tolist()

    temp_Jv_fitfunc = []
    for r in temp_turning_pos:
        """the potential values at the turning points based on the fit parameters"""
        temp_Jv_fitfunc.append(p0_1[0]*(1 - np.exp(-p0_1[1]*(r - p0_1[2])))**2 + p0_1[3])

    # inserts the re data point so you can see it on the plot
    x, y = state_pes.T
    x_fit = np.insert(x, vmax_mode + 1, p0_1[2])
    y_fit_nore = fitfunc(p0_1, x)
    y_fit = fitfunc(p0_1, x_fit)
    """
    #plotting
    if msqe_vib_cal < 0.01:
        # Plotting the functions
        fig = plt.figure()
        ax1 = fig.add_subplot(111)

        # Plot of the data and the fit
        plt.plot(x, y, "ro", label = '%s PES' % states_N2[ii])
        plt.plot(x_fit, y_fit, "g-", label = '%s Morse' % states_N2[ii])

        # extra plot things
        plt.title('Vibrational Mode: %s' % i)
        plt.legend(loc='lower right');
        plt.show()
    """

    # calculating the mean square error of between the PES and the fit
    temp_msqe_vib = (np.square(state_pes.T[1] - y_fit_nore)).mean()

    #All of the calculation data is put into the dictionary
    morse_rkr_dict = {}
    morse_rkr_dict[state] = [temp_morse_constants, temp_msqe_vib, temp_Jv, temp_turning_pos,
                             temp_Jv_fitfunc]

    return morse_rkr_dict


def vasan_wavefunction(state, vib_constants, morse_rkr_data, n_level, r_domain):
    """Using eq. 2 from Vasan and Cross (1982), we calculate the normalized wavefunction.

        - Psi = N_n*exp(-z/2)*z^(b/2)*Lnb(z)
        - N_n = (a*b*n!/Gamma(k-n))^1/2

    Parameters
    ----------
    state: string
        specifies what state to be used

    vib_constants: list
        the vibrational spectroscopic constants

    morse_rkr_data: dict
        holds the fit constants to be used

    n_level: integer
        vibration level number

    r_domain: list/array
        acts as the domain of the wavefunctions
    """

    beta = morse_rkr_data[state][0][1]

    re = morse_rkr_data[state][0][2]

    # omegae / omegae_xe
    k_vasan = vib_constants[1] / vib_constants[2]

    b_vasan = k_vasan - 2 * n_level - 1

    z_vasan = k_vasan * np.exp(-beta * (r_domain - re))

    N_n = (beta * b_vasan * math.factorial(n_level) / math.gamma(k_vasan - n_level))**0.5

    # the associated laguerre polynomial
    Lag_nbz = assoc_laguerre(z_vasan, n_level, b_vasan)

    psi_n = N_n * np.exp(-z_vasan / 2) * z_vasan**(b_vasan / 2) * Lag_nbz

    return psi_n


def franck_condon(state_one, vib_constants_one, rot_constants_one, vmax_mode_one, n_level_one,
                  state_two, vib_constants_two, rot_constants_two, vmax_mode_two, n_level_two,
                  r_domain):
    """Computes the Franck-Condon Factors of two wavefunctions
        - the Franck-Condon factor is the overlap of two wavefunctions

    Parameters
    ----------
    state_one: string
        specifies the first state for the wavefunction

    vib_constants_one: list
        the spectroscopic constants for the first state

    vmax_mode_one: integer
        maximum vibrational mode for morse potential

    n_level_one: integer
        vibrational mode for the wavefunction

    state_two: string
        specifies the second state for the wavefunction

    vib_constants_two: list
        the spectroscopic constants for the second state

    vmax_mode_two: integer
        maximum vibrational mode for morse potential

    n_level_two: integer
        vibrational mode for the wavefunction

    r_domain: array or list
        values for the domain of the wavefunctions
    """
    # splits domain for integrating
    start_domain = r_domain[0]

    end_domain = r_domain[len(r_domain)-1]

    # morse fit calculations
    morse_rkr_one = morse_fit(state_one, vib_constants_one, rot_constants_one, vmax_mode_one)

    morse_rkr_two = morse_fit(state_two, vib_constants_two, rot_constants_two, vmax_mode_two)

    """using quad integration from Scipy"""
    integral_result = integrate.quad(lambda r: vasan_wavefunction(state_one,
                                                                  vib_constants_one, morse_rkr_one,
                                                                  n_level_one, r) *
                                     vasan_wavefunction(state_two, vib_constants_two,
                                                        morse_rkr_two, n_level_two, r),
                                     start_domain, end_domain)

    return integral_result[0]**2


def partial_cross_section(state_one, vib_constants_one, rot_constants_one, n_level_one,
                          vmax_mode_one,
                          state_two, vib_constants_two, rot_constants_two, n_level_two,
                          vmax_mode_two,
                          incident_electron_energy, initial_cross_section, function_guess,
                          r_domain):
    """Purpose of this is to determine the partial cross section between two different states.
           - Returns a list of the electron energy provided and the corresponding cross section
             for the states and specific Jv and Jvprime mode (n_level's one and two respectively)

    Parameters
    ----------
    state_one: string
        specifies the state to be used

    vib_constants_one: dict
        spectroscopic constants

    rot_constants_one: dict
        spectroscopic constants

    n_level_one: integer
        specifies which vibrational wavefunction

    vmax_mode_one: integer
        the maximum vibrational mode for the morse potential

    state_two: string
        specifies the state to be used

    vib_constants_two: dict
        spectroscopic constants

    rot_constants_two: dict
        spectroscopic constants

    n_level_two: integer
        specifies which vibrational wavefunction

    vmax_mode_two: integer
        the maximum vibrational mode for the morse potential

    function_guess: function
        the function used to fit the universal function

    incident_electron_energy: list
        the energy of the incident electron

    initial_cross_section: list
        the cross section data from LxCat

    r_domain: list
        domain for wavefunction overlap
    """
    """
    univ_coefficients = univ_func_coefficients(function_guess,
                                               reduced_energy(incident_electron_energy,
                                                              constants.J_ionization),
                                               func_ej(initial_cross_section,
                                                       constants.J_ionization,
                                                       constants.n_valence))[0]
    """
    # first and second morse potential
    morse_state_one = morse_fit(state_one, vib_constants_one[state_one],
                                rot_constants_one[state_one], vmax_mode_one)
    morse_state_two = morse_fit(state_two, vib_constants_two[state_two],
                                rot_constants_two[state_two], vmax_mode_two)

    # corresponding turning point energies
    Jv_state_one = morse_state_one[state_one][4][vmax_mode_one + n_level_one + 2] # eV
    Jv_state_two = morse_state_two[state_two][4][vmax_mode_two + n_level_two + 2] # eV

    """computing the energy level transistion between the two states"""
    J_vvprime = Jv_state_two - Jv_state_one # eV

    """computing the specific franck condon factor"""
    franck_condon_factor = franck_condon(state_one, vib_constants_one[state_one],
                                         rot_constants_one[state_one], vmax_mode_one, n_level_one,
                                         state_two, vib_constants_two[state_two],
                                         rot_constants_two[state_two], vmax_mode_two, n_level_two,
                                         r_domain)

    # list for electron energy and cross section
    partial_electronEnergy_crossSection = []

    for i in incident_electron_energy:
        """calculates the partial cross section of the two states and their n_level
               - partial_sigma holds only the cross section values
               - partial_electronEnergy_crossSection has the energy and the corresponding
                  cross section
        """
        partial_sigma = (constants.n_valence * constants.k_e**2 * np.pi * elementary_charge**4 *
                         (1/(J_vvprime * elementary_charge)**2) *
                         kosarim_universal_func(i / J_vvprime) * franck_condon_factor)
        if partial_sigma < 0.0:
            """The cross section cannot be negative. So, if the value computed is negative,
               it is replaced with 0.0.
            """
            partial_sigma = 0.0

        # adds the cross section to a list with the corresponding energies
        partial_electronEnergy_crossSection.append([i, partial_sigma])

    return partial_electronEnergy_crossSection
