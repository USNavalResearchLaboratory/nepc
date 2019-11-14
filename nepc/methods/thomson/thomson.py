import nepc.methods.mp as mp
import numpy as np
from numpy import exp
from numpy import power
from scipy.special import binom as binom
from numpy import log10 as log10
from scipy.special import gamma as gamma
from scipy.integrate import simps as simps


def fcf_v(vp_max, vpp_max,
          diatomic_constants_p,
          diatomic_constants_pp,
          reduced_mass,
          k,
          delta_r,
          dbug=False):

    Top = diatomic_constants_p['To']
    wep = diatomic_constants_p['we']
    wexep = diatomic_constants_p['wexe']
    Bep = diatomic_constants_p['Be']
    rep = diatomic_constants_p['re']
    Dep = diatomic_constants_p['De']
    little_ap = mp.little_a_20(mu=reduced_mass, De=Dep, we=wep)

    Topp = diatomic_constants_pp['To']
    wepp = diatomic_constants_pp['we']
    wexepp = diatomic_constants_pp['wexe']
    Bepp = diatomic_constants_pp['Be']
    repp = diatomic_constants_pp['re']
    Depp = diatomic_constants_pp['De']
    little_app = mp.little_a_20(mu=reduced_mass, De=Depp, we=wepp)

    R_LEN, r_array = mp.r_array(rep, repp, delta_r, k)

    jp = 0
    jpp = 0
    big_Ap = mp.big_A_5(Be=Bep, j=jp)
    alphap = mp.alpha_4(big_A=big_Ap, Be=Bep, we=wep)
    r0p = mp.r0_3(re=rep, alpha=alphap)
    C1p = mp.C1_10(big_A=big_Ap, little_a=little_ap, r0=r0p, alpha=alphap)
    C2p = mp.C2_11(big_A=big_Ap, little_a=little_ap, r0=r0p, alpha=alphap)
    D1p = mp.D1_8(De=Dep, little_a=little_ap, re=rep, alpha=alphap)
    D2p = mp.D2_9(De=Dep, little_a=little_ap, re=rep, alpha=alphap)
    K1p = mp.K1_6(D2=D2p, C2=C2p, wexe=wexep)
    K2p = mp.K2_7(D1=D1p, C1=C1p, wexe=wexep, K1=K1p)
    zp = K1p * exp(-little_ap * (r_array - r0p))

    big_App = mp.big_A_5(Be=Bepp, j=jpp)
    alphapp = mp.alpha_4(big_A=big_App, Be=Bepp, we=wepp)
    r0pp = mp.r0_3(re=repp, alpha=alphapp)
    C1pp = mp.C1_10(big_A=big_App, little_a=little_app, r0=r0pp, alpha=alphapp)
    C2pp = mp.C2_11(big_A=big_App, little_a=little_app, r0=r0pp, alpha=alphapp)
    D1pp = mp.D1_8(De=Depp, little_a=little_app, re=repp, alpha=alphapp)
    D2pp = mp.D2_9(De=Depp, little_a=little_app, re=repp, alpha=alphapp)
    K1pp = mp.K1_6(D2=D2pp, C2=C2pp, wexe=wexepp)
    K2pp = mp.K2_7(D1=D1pp, C1=C1pp, wexe=wexepp, K1=K1pp)
    zpp = K1pp * exp(-little_app * (r_array - r0pp))

    fcf_vp_vpp = []
    for vp in np.arange(vp_max+1, dtype=np.int64):
        fcf_vp_vpp.append([])
        log_normp = mp.log_norm(little_ap, K2p, vp)

        log_psi_p = mp.log_psi(zp, K2p, vp)

        laguerre_p = np.float64(0) * np.arange(R_LEN)

        for n_p in np.arange(vp+1, dtype=np.int64):

            laguerre_p += (np.int64(-1)**n_p * binom(vp, n_p) *
                           power(10, log10(gamma(K2p-vp)) +
                                 (vp - n_p) * log10(zp) -
                                 log10(gamma(K2p - vp - n_p))))

        laguerre_p = np.int64(-1)**vp * laguerre_p

        psi_p_r = power(10, log_normp) * power(10, log_psi_p) * laguerre_p

        for vpp in np.arange(vpp_max+1, dtype=np.int64):
            log_normpp = mp.log_norm(little_app, K2pp, vpp)
            log_psi_pp = mp.log_psi(zpp, K2pp, vpp)

            laguerre_pp = np.float64(0) * np.arange(R_LEN)

            for n_pp in np.arange(vpp+1, dtype=np.int64):
                laguerre_pp += (np.int64(-1)**n_pp * binom(vpp, n_pp) *
                                power(10, log10(gamma(K2pp-vpp)) +
                                      (vpp - n_pp) * log10(zpp) -
                                      log10(gamma(K2pp - vpp - n_pp))))

            laguerre_pp = np.int64(-1)**vpp * laguerre_pp

            psi_pp_r = power(10, log_normpp) * power(10, log_psi_pp) * laguerre_pp

            fcf_vp_vpp[vp].append(pow(simps(y=psi_p_r * psi_pp_r, x=r_array), 2))
    return fcf_vp_vpp


def psi_v(vp, vpp,
          diatomic_constants_p,
          diatomic_constants_pp,
          reduced_mass,
          k,
          delta_r,
          dbug=False):

    Top = diatomic_constants_p['To']
    wep = diatomic_constants_p['we']
    wexep = diatomic_constants_p['wexe']
    Bep = diatomic_constants_p['Be']
    rep = diatomic_constants_p['re']
    Dep = diatomic_constants_p['De']
    little_ap = mp.little_a_20(mu=reduced_mass, De=Dep, we=wep)

    Topp = diatomic_constants_pp['To']
    wepp = diatomic_constants_pp['we']
    wexepp = diatomic_constants_pp['wexe']
    Bepp = diatomic_constants_pp['Be']
    repp = diatomic_constants_pp['re']
    Depp = diatomic_constants_pp['De']
    little_app = mp.little_a_20(mu=reduced_mass, De=Depp, we=wepp)

    R_LEN, r_array = mp.r_array(rep, repp, delta_r, k)

    jp = 0
    jpp = 0
    big_Ap = mp.big_A_5(Be=Bep, j=jp)
    alphap = mp.alpha_4(big_A=big_Ap, Be=Bep, we=wep)
    r0p = mp.r0_3(re=rep, alpha=alphap)
    C1p = mp.C1_10(big_A=big_Ap, little_a=little_ap, r0=r0p, alpha=alphap)
    C2p = mp.C2_11(big_A=big_Ap, little_a=little_ap, r0=r0p, alpha=alphap)
    D1p = mp.D1_8(De=Dep, little_a=little_ap, re=rep, alpha=alphap)
    D2p = mp.D2_9(De=Dep, little_a=little_ap, re=rep, alpha=alphap)
    K1p = mp.K1_6(D2=D2p, C2=C2p, wexe=wexep)
    K2p = mp.K2_7(D1=D1p, C1=C1p, wexe=wexep, K1=K1p)
    zp = K1p * exp(-little_ap * (r_array - r0p))

    big_App = mp.big_A_5(Be=Bepp, j=jpp)
    alphapp = mp.alpha_4(big_A=big_App, Be=Bepp, we=wepp)
    r0pp = mp.r0_3(re=repp, alpha=alphapp)
    C1pp = mp.C1_10(big_A=big_App, little_a=little_app, r0=r0pp, alpha=alphapp)
    C2pp = mp.C2_11(big_A=big_App, little_a=little_app, r0=r0pp, alpha=alphapp)
    D1pp = mp.D1_8(De=Depp, little_a=little_app, re=repp, alpha=alphapp)
    D2pp = mp.D2_9(De=Depp, little_a=little_app, re=repp, alpha=alphapp)
    K1pp = mp.K1_6(D2=D2pp, C2=C2pp, wexe=wexepp)
    K2pp = mp.K2_7(D1=D1pp, C1=C1pp, wexe=wexepp, K1=K1pp)
    zpp = K1pp * exp(-little_app * (r_array - r0pp))

    log_normp = mp.log_norm(little_ap, K2p, vp)

    log_psi_p = mp.log_psi(zp, K2p, vp)

    laguerre_p = np.float64(0) * np.arange(R_LEN)

    for n_p in np.arange(vp+1, dtype=np.int64):

        laguerre_p += (np.int64(-1)**n_p * binom(vp, n_p) *
                       power(10, log10(gamma(K2p-vp)) +
                             (vp - n_p) * log10(zp) -
                             log10(gamma(K2p - vp - n_p))))

    laguerre_p = np.int64(-1)**vp * laguerre_p

    psi_p_r = power(10, log_normp) * power(10, log_psi_p) * laguerre_p

    log_normpp = mp.log_norm(little_app, K2pp, vpp)
    log_psi_pp = mp.log_psi(zpp, K2pp, vpp)

    laguerre_pp = np.float64(0) * np.arange(R_LEN)

    for n_pp in np.arange(vpp+1, dtype=np.int64):
        laguerre_pp += (np.int64(-1)**n_pp * binom(vpp, n_pp) *
                        power(10, log10(gamma(K2pp-vpp)) +
                              (vpp - n_pp) * log10(zpp) -
                              log10(gamma(K2pp - vpp - n_pp))))

    laguerre_pp = np.int64(-1)**vpp * laguerre_pp

    psi_pp_r = power(10, log_normpp) * power(10, log_psi_pp) * laguerre_pp

    V_r_p = {'To': Top,
             'we': wep,
             'wexe': wexep,
             'De': Dep,
             'a': little_ap,
             're': rep}
    V_r_pp = {'To': Topp,
              'we': wepp,
              'wexe': wexepp,
              'De': Depp,
              'a': little_app,
              're': repp}

    return r_array, psi_p_r, psi_pp_r, V_r_p, V_r_pp


def print_fcf_calc_ref(fcf_calc, fcf_ref):
    for i in range(len(fcf_calc)):
        print('\nv\'/v\'\': {}'.format(i))
        for j in range(len(fcf_calc[0])):
            print('{}\t{:.2E}\t{:.2E}'.format(j, fcf_ref[i][j], fcf_calc[i][j]))


def fcf_closure(fcf_vp_vpp):
    vp_len = len(fcf_vp_vpp)
    vpp_len = len(fcf_vp_vpp[0])
    closure_vp = np.zeros(vp_len)
    closure_vpp = np.zeros(vpp_len)
    for vp in range(vp_len):
        for vpp in range(vpp_len):
            closure_vp[vp] += fcf_vp_vpp[vp][vpp]
            closure_vpp[vpp] += fcf_vp_vpp[vp][vpp]

    print('v\'\tclosure_vp')
    for vp in range(vp_len):
        print('{}\t{}'.format(vp, closure_vp[vp]))

    print('\nv\'\'\tclosure_vpp')
    for vpp in range(vpp_len):
        print('{}\t{}'.format(vpp, closure_vpp[vpp]))


def rmse_calc_ref(fcf_calc, fcf_ref):
    vp_len = len(fcf_calc)
    vpp_len = len(fcf_calc[0])
    sum_squares = 0.0
    for vp in range(vp_len):
        for vpp in range(vpp_len):
            sum_squares += (fcf_calc[vp][vpp] - fcf_ref[vp][vpp])**2
    return np.sqrt(sum_squares/(vp_len * vpp_len))


def off_diagonal_elements(two_d_array):
    # upper triangle. k=1 excludes the diagonal elements.
    xu, yu = np.triu_indices_from(two_d_array, k=1)
    # lower triangle
    xl, yl = np.tril_indices_from(two_d_array, k=-1)  # Careful, here the offset is -1

    # combine
    x = np.concatenate((xl, xu))
    y = np.concatenate((yl, yu))

    return two_d_array[(x,y)]


def rmse_off_diagonal_elements(two_d_array):
    elem = off_diagonal_elements(two_d_array)
    return np.sqrt(np.sum(elem**2)/len(elem))


def incremental_rmse_off_diagonal_elements(two_d_array):
    for i in range(2,len(two_d_array)+1):
        incremental_two_d_array = two_d_array[0:i,0:i]
        print('i: {}; rmse: {}'.format(i, rmse_off_diagonal_elements(incremental_two_d_array)))


def rmse_diagonal_elements(two_d_array):
    elem = np.diagonal(two_d_array)
    return np.sqrt(np.sum((1.0-elem)**2)/len(elem))


def incremental_rmse_diagonal_elements(two_d_array):
    for i in range(1,len(two_d_array)+1):
        incremental_two_d_array = two_d_array[0:i,0:i]
        print('i: {}; rmse: {}'.format(i, rmse_diagonal_elements(incremental_two_d_array)))
