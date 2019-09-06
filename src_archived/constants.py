"""Constants for use in nepc"""
# from Laher & Gilmore (1991)

states_N2 = [
    "N2(X1Sigmag+)",
    "N2(A3Sigmau+)",
    "N2(B3Pig)",
    "N2(W3Deltau)",
    "N2(Bp3Sigmau-)",
    "N2(ap1Sigmau-)",
    "N2(a1Pig)",
    "N2(w1Deltau)",
    "N2(C3Piu)",
    "N2(E3Sigmag+)",
    "N2(D3Sigmau+)"]
states_N2p = [
    "N2+(X2Sigmag+)",
    "N2+(A2Piu)",
    "N2+(B2Sigmau+)",
    "N2+(C2Sigmau+)"]


vib_constants_N2 = [[0.0, 2358.57, 14.324, -2.26E-3, -2.4E-4, 0],
                    [49754.8, 1460.48, 13.775, -1.175E-2, 1.41E-4, -7.29E-5],
                    [59306.8, 1734.38, 14.558, 1.40E-2, -1.13E-3, 0],
                    [59380.2, 1506.53, 12.575, 3.09E-2, -7.1E-4, 0],
                    [65851.3, 1516.88, 12.181, 4.19E-2, -7.3E-4, 0],
                    [67739.3, 1530.25, 12.075, 4.13E-2, -2.9E-4, 0],
                    [68951.2, 1694.21, 13.949, 7.94E-3, 2.9E-4, 0],
                    [71698.4, 1559.50, 12.008, 4.54E-2, 0, 0],
                    [88977.9, 2047.18, 28.445, 2.0883, -5.350E-1, 0],
                    [95774.5, 2218, 16.3, -2.7E-2, -2.6E-3, 0],
                    [103570.9, 2207, 16.3, -2.7E-2, -2.6E-3, 0]]

vib_constants_N2p = [[125667.5, 2207.37, 16.302, -2.67E-3, -2.61E-3, 3.7E-5],
                     [134683.1, 1903.51, 15.029, 2.03E-3, 0, 0],
                     [151233.5, 2420.83, 23.851, -0.3587, -6.192E-2, 0],
                     [190209.5, 2071.5, 9.29, -0.43, 0, 0]]

vib_constants_N2_dict = {"N2(X1Sigmag+)": [0.0, 2358.57, 14.324, -2.26E-3, -2.4E-4, 0],
                         "N2(A3Sigmau+)": [49754.8, 1460.48, 13.775, -1.175E-2, 1.41E-4, -7.29E-5],
                         "N2(B3Pig)": [59306.8, 1734.38, 14.558, 1.40E-2, -1.13E-3, 0],
                         "N2(W3Deltau)": [59380.2, 1506.53, 12.575, 3.09E-2, -7.1E-4, 0],
                         "N2(Bp3Sigmau-)": [65851.3, 1516.88, 12.181, 4.19E-2, -7.3E-4, 0],
                         "N2(ap1Sigmau-)": [67739.3, 1530.25, 12.075, 4.13E-2, -2.9E-4, 0],
                         "N2(a1Pig)": [68951.2, 1694.21, 13.949, 7.94E-3, 2.9E-4, 0],
                         "N2(w1Deltau)": [71698.4, 1559.50, 12.008, 4.54E-2, 0, 0],
                         "N2(C3Piu)": [88977.9, 2047.18, 28.445, 2.0883, -5.350E-1, 0],
                         "N2(E3Sigmag+)": [95774.5, 2218, 16.3, -2.7E-2, -2.6E-3, 0],
                         "N2(D3Sigmau+)": [103570.9, 2207, 16.3, -2.7E-2, -2.6E-3, 0]}

vib_constants_N2p_dict = {"N2+(X2Sigmag+)": [125667.5, 2207.37, 16.302, -2.67E-3, -2.61E-3, 3.7E-5],
                          "N2+(A2Piu)": [134683.1, 1903.51, 15.029, 2.03E-3, 0, 0],
                          "N2+(B2Sigmau+)": [151233.5, 2420.83, 23.851, -0.3587, -6.192E-2, 0],
                          "N2+(C2Sigmau+)": [190209.5, 2071.5, 9.29, -0.43, 0, 0]}

rot_constants_N2 = [[1.99824, 1.7318E-2, -3.3E-5, 0, 0],
                    [1.45499, 1.8385E-2, 1.24E-5, -6.7E-6, 0],
                    [1.63802, 1.8302E-2, -8.4E-6, -3.4E-6, 0],
                    [1.47021, 1.6997E-2, -1.01E-5, 3.3E-7, 0],
                    [1.4731, 1.668E-2, 1.84E-5, -4.5E-7, 0],
                    [1.4799, 1.657E-2, 2.41E-5, 0, 0],
                    [1.6169, 1.793E-2, -2.93E-5, 0, 0],
                    [1.4963, 1.63E-2, 0, 0, 0],
                    [1.8247, 1.868E-2, -2.28E-3, 7.33E-4, -1.5E-4],
                    [1.9368, 1.90E-2, -1.9E-4, 0, 0],
                    [1.9705, 1.90E-2, -1.9E-4, 0, 0]]

rot_constants_N2p = [[1.93177, 1.900E-2, -1.91E-5, -5.00E-6, 4.6E-8],
                     [1.7442, 1.838E-2, -1.76E-4, 4.4E-6, 0],
                     [2.0845, 2.132E-2, -8.5E-4, 0, 0],
                     [1.5114, 1.10E-3, -8.2E-4, 0, 0]]

def return_states_n2():
    """Returns states_N2 constants for testing"""
    return states_N2

def return_states_n2p():
    """Returns states_N2p constants for testing"""
    return states_N2p

def return_vib_constants_n2():
    """Returns vib_constants_N2 constants for testing"""
    return vib_constants_N2

def return_vib_constants_n2p():
    """Returns vib_constants_N2p constants for testing"""
    return vib_constants_N2p

def return_rot_constants_n2():
    """Returns rot_constants_N2 constants for testing"""
    return rot_constants_N2

def return_rot_constants_n2p():
    """Returns rot_constants_N2p constants for testing"""
    return rot_constants_N2p
rot_constants_N2_dict = {"N2(X1Sigmag+)": [1.99824, 1.7318E-2, -3.3E-5, 0, 0],
                    "N2(A3Sigmau+)": [1.45499, 1.8385E-2, 1.24E-5, -6.7E-6, 0],
                    "N2(B3Pig)": [1.63802, 1.8302E-2, -8.4E-6, -3.4E-6, 0],
                    "N2(W3Deltau)": [1.47021, 1.6997E-2, -1.01E-5, 3.3E-7, 0],
                    "N2(Bp3Sigmau-)": [1.4731, 1.668E-2, 1.84E-5, -4.5E-7, 0],
                    "N2(ap1Sigmau-)": [1.4799, 1.657E-2, 2.41E-5, 0, 0],
                    "N2(a1Pig)": [1.6169, 1.793E-2, -2.93E-5, 0, 0],
                    "N2(w1Deltau)": [1.4963, 1.63E-2, 0, 0, 0],
                    "N2(C3Piu)": [1.8247, 1.868E-2, -2.28E-3, 7.33E-4, -1.5E-4],
                    "N2(E3Sigmag+)": [1.9368, 1.90E-2, -1.9E-4, 0, 0],
                    "N2(D3Sigmau+)": [1.9705, 1.90E-2, -1.9E-4, 0, 0]}

rot_constants_N2p_dict = {"N2+(X2Sigmag+)": [1.93177, 1.900E-2, -1.91E-5, -5.00E-6, 4.6E-8],
                     "N2+(A2Piu)": [1.7442, 1.838E-2, -1.76E-4, 4.4E-6, 0],
                     "N2+(B2Sigmau+)": [2.0845, 2.132E-2, -8.5E-4, 0, 0],
                     "N2+(C2Sigmau+)": [1.5114, 1.10E-3, -8.2E-4, 0, 0]}


# reduced mass of nitrogen
mu_nitrogen = 7.00335 # amu
mu_nitrogen_kg = 1.16294E-26 # kg

# ionization potential for nitrogen: NIST eval.
J_ionization = 15.581 # eV

# coulomb force constant: calculated from 1/(4*pi*epsilon_naught)
k_e = 8987551787 # N*m^2/C^2

# conversion value for eV to wavenumber
wavenumber_per_ev = 8065.6

# number of valence electrons in N2
#TODO: Verify this number
n_valence = 2
