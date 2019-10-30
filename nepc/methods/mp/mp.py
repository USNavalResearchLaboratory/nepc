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


PLANCK, AVOGADRO, SPEED_OF_LIGHT, PI, EULER = np.float64(
        (PLANCK, AVOGADRO, SPEED_OF_LIGHT, PI, EULER))


"""Creating the functions needed to reproduce the Chakraborty wavefunctions.
The end numbers on the function name correspond to the equation number in Chakraborty (1982)"""
def r0_3(re, alpha):
    return re * (np.int64(1) + alpha)


def alpha_4(big_A, Be, we):
    return np.int64(4) * big_A * Be / we**2


def big_A_5(Be, j):
    return Be * j * (j + 1)


def K1_6(D2, C2, wexe):
    return np.int64(2) * sqrt((D2-C2)/wexe)


def K2_7(D1, C1, wexe, K1):
    return np.int64(2) * (np.int64(2) * D1 - C1)/(wexe * K1)


def D1_8(De, little_a, re, alpha):
    return De * exp(-little_a * re * alpha)


def D2_9(De, little_a, re, alpha):
    return De * exp(-np.int64(2) * little_a * re * alpha)


def C1_10(big_A, little_a, r0, alpha):
    return ((big_A/(little_a * r0 * power(np.int64(1) + alpha, np.int64(2)))) *
            (np.int64(4) - (np.int64(6) / (little_a * r0))))


def C2_11(big_A, little_a, r0, alpha):
    return ((big_A/(little_a * r0 * power(np.int64(1) + alpha, np.int64(2)))) *
            (np.int64(1) - (np.int64(3) / (little_a * r0))))


def little_a_20(mu, De, we):
    return (np.float64(2E-9) * PI * SPEED_OF_LIGHT * we *
            sqrt(mu/(np.int64(2) * PLANCK * SPEED_OF_LIGHT *De)))


def De(we, wexe):
    return power(we, np.int64(2))/(np.int64(4) * wexe)


def log_norm(little_a, K2, v):
    return ((log10(little_a * (K2 - np.int64(2) * v - np.int64(1)))
             - log10(factorial(v, exact=True))
             - loggamma(K2 - v)/log(np.int64(10))) / np.int64(2))


def log_psi(z, K2, v):
    return ((-z/np.int64(2)) * log10(EULER)
            + ((K2 - np.int64(2)*v - np.int64(1))/np.int64(2)) * log10(z))


def r_array(rep, repp, delta_r, k):
    r_len = 2**k + 1
    r = ((rep + repp)/2.0 -
         delta_r * np.sinh(1 - np.arange(r_len) * pow(2, 1 - k)) / np.sinh(1))
    return r_len, r


def Gv(v, To, we, wexe):
    Te = To - we/2 + wexe/4
    return Te + we*(v+1/2) - wexe*(v+1/2)**2
