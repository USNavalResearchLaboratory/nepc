import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.integrate as integrate
import warnings
from scipy.optimize import curve_fit
from scipy.constants import elementary_charge as elementary_charge
from scipy.constants import Planck as Planck
from scipy.constants import speed_of_light as speed_of_light
from scipy.integrate import quadrature
from scipy import optimize

"""Importing the constants"""
from nepc import nepc
from nepc.util import constants
from nepc.util import itikawa_data
import thomson

"""Plotting the universal function f(E/J) vs the reduced energy (E/J)
    - The fit guesses are also plotted

fig_1 = plt.figure()
ax1 = fig_1.add_subplot(111)
ax1.plot(thomson.reduced_energy(ion_energy_itikawa, constants.J_ionization), 
    thomson.func_ej(cross_section_itikawa, constants.J_ionization, constants.n_valence), 'bo', label='Data')
# plot figure extras
plt.xlabel('Reduced Energy (E/J)')
plt.ylabel('f(E/J)')
plt.legend()
plt.xscale('log')
plt.title('Universal fit: N2+')
plt.show()
"""
# energy levels from itikawa
ion_energy_itikawa = thomson.list_splitter(itikawa_data.ion_cross_N2p, 0)

# total cross sections from itikawa
cross_section_itikawa = thomson.list_splitter(itikawa_data.ion_cross_N2p, 1)

"""Example calculations for the thomson method"""

"""Initial guessed domain that the wavefunctions will cover. This is primarily used to calculate
   the overlap of the wavefunctions for the franck-condon factors so it just needs to encompass
   the whole wavefunction"""
domain_temp = np.linspace(0.0, 3.0, 10000)

"""finding the coefficients for the guessed universal function"""
#universal_coeff = thomson.univ_func_coefficients(thomson.func_guess, thomson.reduced_energy(ion_energy_itikawa, constants.J_ionization), thomson.func_ej(cross_section_itikawa, constants.J_ionization, constants.n_valence))[0]
#print(universal_coeff)

"""making the morse potential fit of a state"""
#morse_N2p = thomson.morse_fit(constants.states_N2p[0], constants.vib_constants_N2p_dict[constants.states_N2p[0]], constants.rot_constants_N2p_dict[constants.states_N2p[0]], 10)
#print(morse_N2p[constants.states_N2p[0]][2])
#print(len(morse_N2p[constants.states_N2p[0]][2]))

"""forming the wavefunction"""
#vasan_N2p = thomson.vasan_wavefunction(constants.states_N2p[0], constants.vib_constants_N2p_dict, morse_N2p, 0, domain_temp)
#print(vasan_N2p)

"""calculating the franck-condon factor between two states"""
FCF_N2 = thomson.franck_condon(constants.states_N2[0], constants.vib_constants_N2[0], constants.rot_constants_N2[0], 15, 0, constants.states_N2p[0], constants.vib_constants_N2p[0], constants.rot_constants_N2p[0], 10, 0, domain_temp)
print(FCF_N2)

FCF_N2p = thomson.franck_condon(constants.states_N2p[0], constants.vib_constants_N2p[0], constants.rot_constants_N2p[0], 10, 0, constants.states_N2p[2], constants.vib_constants_N2p[2], constants.rot_constants_N2p[2], 10, 0, domain_temp)
print(FCF_N2p)

"""lastly, calculating the partial cross sections between two states and vibration modes.
   This is done without needed to calculating something else separately
"""
print('cross section sum for X1 ground to X2 transitions level 0-6')
partial_sigma_X1_X2_0 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[0], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 0, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_X2_1 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[0], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 1, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_X2_2 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[0], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 2, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_X2_3 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[0], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 3, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_X2_4 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[0], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 4, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_X2_5 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[0], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 5, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_X2_6 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[0], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 6, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)

"""adding up the X1 to X2 vibrational states"""
i = 0
total_sigma_X1_X2 = []
while i <len(partial_sigma_X1_X2_0):
    total_sigma_X1_X2.append(partial_sigma_X1_X2_0[i][1] + partial_sigma_X1_X2_1[i][1] + partial_sigma_X1_X2_2[i][1] + partial_sigma_X1_X2_3[i][1] + partial_sigma_X1_X2_4[i][1] + partial_sigma_X1_X2_5[i][1] + partial_sigma_X1_X2_6[i][1])
    i += 1


"""check on cross section by putting it into a list next to the energies"""
total_electron_sigma_X2 = []
i = 0
while i <len(total_sigma_X1_X2):
    total_electron_sigma_X2.append([ion_energy_itikawa[i], total_sigma_X1_X2[i]])
    i += 1
print(total_electron_sigma_X2)

# for plotting purposes
cross_section_itikawa_m2 = [list_item * 10**-20 for list_item in cross_section_itikawa]
#print(cross_section_itikawa_m2)

fig_2 = plt.figure()
ax2 = fig_2.add_subplot(111)
ax2.plot(ion_energy_itikawa, cross_section_itikawa_m2, 'b-', label='itikawa')
ax2.plot(ion_energy_itikawa, total_sigma_X1_X2, 'r-', label='thomson: X1->X2 Jv(0) Jvv(0-6)')
# plot figure extras
plt.xlabel('Electron energy [eV]')
plt.ylabel('Cross section [m^2]')
plt.legend()
plt.xscale('log')
plt.yscale('log')
fig_2.savefig('cross_section__X1_X2.png')

"""X1 to A2"""
print('cross section sum for X1 ground to A2 transitions level 0-6')
partial_sigma_X1_A2_0 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[1], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 0, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_A2_1 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[1], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 1, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_A2_2 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[1], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 2, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_A2_3 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[1], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 3, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_A2_4 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[1], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 4, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_A2_5 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[1], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 5, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_A2_6 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[1], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 6, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)

i = 0
total_sigma_X1_A2 = []
while i <len(partial_sigma_X1_A2_0):
    total_sigma_X1_A2.append(partial_sigma_X1_A2_0[i][1] + partial_sigma_X1_A2_1[i][1] + partial_sigma_X1_A2_2[i][1] + partial_sigma_X1_A2_3[i][1] + partial_sigma_X1_A2_4[i][1] + partial_sigma_X1_A2_5[i][1] + partial_sigma_X1_A2_6[i][1])
    i += 1

"""check on cross section against the energy"""
total_electron_sigma_A2 = []
i = 0
while i <len(total_sigma_X1_A2):
    total_electron_sigma_A2.append([ion_energy_itikawa[i], total_sigma_X1_A2[i]])
    i += 1
print(total_electron_sigma_A2)


fig_3 = plt.figure()
ax2 = fig_3.add_subplot(111)
ax2.plot(ion_energy_itikawa, cross_section_itikawa_m2, 'b-', label='itikawa')
ax2.plot(ion_energy_itikawa, total_sigma_X1_A2, 'r-', label='thomson: X1->A2 Jv(0) Jvv(0-6)')
# plot figure extras
plt.xlabel('Electron energy [eV]')
plt.ylabel('Cross section [m^2]')
plt.legend()
plt.xscale('log')
plt.yscale('log')
#TODO: print the figure in the terminal or save it in a file
fig_3.savefig('cross_section_X1_A2.png')



"""X1 to B2"""
print('cross section sum for X1 ground to B2 transitions level 0-6')
partial_sigma_X1_B2_0 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[2], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 0, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_B2_1 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[2], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 1, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_B2_2 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[2], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 2, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_B2_3 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[2], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 3, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_B2_4 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[2], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 4, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_B2_5 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[2], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 5, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X1_B2_6 = thomson.partial_cross_section(constants.states_N2[0], constants.vib_constants_N2_dict, constants.rot_constants_N2_dict, 0, 15, constants.states_N2p[2], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 6, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)

i = 0
total_sigma_X1_B2 = []
while i <len(partial_sigma_X1_B2_0):
    total_sigma_X1_B2.append(partial_sigma_X1_B2_0[i][1] + partial_sigma_X1_B2_1[i][1] + partial_sigma_X1_B2_2[i][1] + partial_sigma_X1_B2_3[i][1] + partial_sigma_X1_B2_4[i][1] + partial_sigma_X1_B2_5[i][1] + partial_sigma_X1_B2_6[i][1])
    i += 1

"""check on cross section against the energy"""
total_electron_sigma_B2 = []
i = 0
while i <len(total_sigma_X1_B2):
    total_electron_sigma_B2.append([ion_energy_itikawa[i], total_sigma_X1_B2[i]])
    i += 1
print(total_electron_sigma_B2)


fig_4 = plt.figure()
ax2 = fig_4.add_subplot(111)
ax2.plot(ion_energy_itikawa, cross_section_itikawa_m2, 'b-', label='itikawa')
ax2.plot(ion_energy_itikawa, total_sigma_X1_A2, 'r-', label='thomson: X1->B2 Jv(0) Jvv(0-6)')
# plot figure extras
plt.xlabel('Electron energy [eV]')
plt.ylabel('Cross section [m^2]')
plt.legend()
plt.xscale('log')
plt.yscale('log')
#TODO: print the figure in the terminal or save it in a file
fig_4.savefig('cross_section_X1_B2.png')


"""Adding up the total sum of X2 and A2 and B2"""
i = 0
total_sigma_X1_X2_A2 = []
while i <len(partial_sigma_X1_X2_0):
    total_sigma_X1_X2_A2.append(total_sigma_X1_X2[i] + total_sigma_X1_A2[i] + total_sigma_X1_B2[i])
    i += 1

fig_4 = plt.figure()
ax2 = fig_4.add_subplot(111)
ax2.plot(ion_energy_itikawa, cross_section_itikawa_m2, 'b-', label='itikawa')
ax2.plot(ion_energy_itikawa, total_sigma_X1_X2_A2, 'r-', label='thomson: X1->X2_A2_B2 Jv(0) Jvv(0-6)')
# plot figure extras
plt.xlabel('Electron energy [eV]')
plt.ylabel('Cross section [m^2]')
plt.legend()
plt.xscale('log')
plt.yscale('log')
fig_4.savefig('cross_section_Sum_X2_A2_B2.png')



"""X2 to B2"""
print('cross section sum for X2 ground to B2 transitions level 0-6')
partial_sigma_X2_B2_0 = thomson.partial_cross_section(constants.states_N2p[0], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 0, 10, constants.states_N2p[2], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 0, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X2_B2_1 = thomson.partial_cross_section(constants.states_N2p[0], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 0, 10, constants.states_N2p[2], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 1, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X2_B2_2 = thomson.partial_cross_section(constants.states_N2p[0], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 0, 10, constants.states_N2p[2], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 2, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X2_B2_3 = thomson.partial_cross_section(constants.states_N2p[0], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 0, 10, constants.states_N2p[2], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 3, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X2_B2_4 = thomson.partial_cross_section(constants.states_N2p[0], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 0, 10, constants.states_N2p[2], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 4, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X2_B2_5 = thomson.partial_cross_section(constants.states_N2p[0], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 0, 10, constants.states_N2p[2], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 5, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)
partial_sigma_X2_B2_6 = thomson.partial_cross_section(constants.states_N2p[0], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 0, 10, constants.states_N2p[2], constants.vib_constants_N2p_dict, constants.rot_constants_N2p_dict, 6, 10, ion_energy_itikawa, cross_section_itikawa, thomson.func_guess, domain_temp)

i = 0
total_sigma_X2_B2 = []
while i <len(partial_sigma_X2_B2_0):
    total_sigma_X2_B2.append(partial_sigma_X2_B2_0[i][1] + partial_sigma_X2_B2_1[i][1] + partial_sigma_X2_B2_2[i][1] + partial_sigma_X2_B2_3[i][1] + partial_sigma_X2_B2_4[i][1] + partial_sigma_X2_B2_5[i][1] + partial_sigma_X2_B2_6[i][1])
    i += 1

"""check on cross section"""

total_electron_sigma_X2_B2 = []
i = 0
while i <len(total_sigma_X2_B2):
    total_electron_sigma_X2_B2.append([ion_energy_itikawa[i], total_sigma_X2_B2[i]])
    i += 1
print(total_electron_sigma_X2_B2)

