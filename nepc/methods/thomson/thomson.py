import nepc.methods.mp as mp
import numpy as np
from numpy import exp
from numpy import power
from scipy.special import binom as binom
from numpy import log10 as log10
from scipy.special import gamma as gamma
from scipy.integrate import simps as simps


def fcf(p_list, pp_list,
        vp_list, vpp_list,
        jp_list, jpp_list,
        diatomic_constants,
        reduced_mass,
        k,
        delta_r,
        psi_p_keep=[[], [], []],
        psi_pp_keep=[[], [], []],
        dbug=False):

    psi_p = []
    psi_pp = []
    fcf = []
    saved_psi_pp = (len(pp_list)+len(vpp_list)+len(jpp_list))*[False]

    i_p = 0
    for p in p_list:
        fcf.append([])
        wep=diatomic_constants[p]['we']
        wexep=diatomic_constants[p]['wexe']
        Bep=diatomic_constants[p]['Be']
        rep=diatomic_constants[p]['re']
        Dep = mp.De(we=wep, wexe=wexep)
        little_ap = mp.little_a_20(mu=reduced_mass, De=Dep, we=wep)

        i_pp = 0
        for pp in pp_list:
            fcf[i_p].append([])
            wepp=diatomic_constants[pp]['we']
            wexepp=diatomic_constants[pp]['wexe']
            Bepp=diatomic_constants[pp]['Be']
            repp=diatomic_constants[pp]['re']
            Depp = mp.De(we=wepp, wexe=wexepp)
            little_app = mp.little_a_20(mu=reduced_mass, De=Depp, we=wepp)

            R_LEN, r_array = mp.r_array(rep, repp, delta_r, k)

            if dbug is True:
                print("rep: ", rep)
                print("repp: ", repp)

            for jp in jp_list:
                fcf[i_p][i_pp].append([])
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

                for jpp in jpp_list:
                    fcf[i_p][i_pp][jp].append([])

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

                    for vp in vp_list:
                        fcf[i_p][i_pp][jp][jpp].append([])

                        if dbug:
                            print("\ncomputing log_normp")
                        log_normp = mp.log_norm(little_ap, K2p, vp)

                        if dbug:
                            print("\ncomputing log_psi_p")
                        log_psi_p = mp.log_psi(zp, K2p, vp)

                        laguerre_p = np.float64(0) * np.arange(R_LEN)

                        for n_p in np.arange(vp+1, dtype=np.int64):

                            if dbug:
                                print("computing laguerre_p in loop for n_p: ", n_p)
                            laguerre_p += (np.int64(-1)**n_p * binom(vp, n_p) *
                                           power(10,
                                                 log10(gamma(K2p-vp))
                                                 + (vp - n_p) * log10(zp)
                                                 - log10(gamma(K2p - vp - n_p))))

                        if dbug:
                            print("\ncomputing final laguerre_p")
                        laguerre_p = np.int64(-1)**vp * laguerre_p

                        if dbug:
                            print("\ncomputing final psi_p")
                        psi_p_r = power(10, log_normp) * power(10, log_psi_p) * laguerre_p
                        if p in psi_p_keep[0] and vp in psi_p_keep[1] and jp in psi_p_keep[2]:
                            psi_p.append({'state':p,
                                          'v':vp,
                                          'j':jp,
                                          'r_array':r_array,
                                          'psi_r':psi_p_r})
                        #psi_p[jp][jpp][vp].append(power(10, log_normp) * power(10, log_psi_p) * laguerre_p)

                        i_pp_vpp_jpp = 0
                        for vpp in vpp_list:
                            if dbug:
                                print("computing log_normpp")
                            log_normpp = mp.log_norm(little_app, K2pp, vpp)
                            if dbug:
                                print("computing log_psi_pp")
                            log_psi_pp = mp.log_psi(zpp, K2pp, vpp)

                            laguerre_pp = np.float64(0) * np.arange(R_LEN)

                            for n_pp in np.arange(vpp+1, dtype=np.int64):
                                if dbug:
                                    print("computing laguerre_pp in loop for n_pp: ", n_pp)
                                laguerre_pp += (np.int64(-1)**n_pp * binom(vpp, n_pp) *
                                                power(10, 
                                                      log10(gamma(K2pp-vpp))
                                                      + (vpp - n_pp) * log10(zpp)
                                                      - log10(gamma(K2pp - vpp - n_pp))))

                            if dbug:
                                print("computing final laguerre_pp")
                            laguerre_pp = np.int64(-1)**vpp * laguerre_pp

                            
                            if dbug:
                                print("computing final psi_pp")
                            psi_pp_r = power(10, log_normpp) * power(10, log_psi_pp) * laguerre_pp
                            if (saved_psi_pp[i_pp_vpp_jpp] is False and pp in psi_pp_keep[0] and 
                                vpp in psi_pp_keep[1] and jpp in psi_pp_keep[2]):
                                psi_pp.append({'state':pp,
                                               'v':vpp,
                                               'j':jpp,
                                               'r_array':r_array,
                                               'psi_r':psi_pp_r})
                                saved_psi_pp[i_pp_vpp_jpp] = True
                            i_pp_vpp_jpp += 1
                            #psi_pp[jp][jpp][vp].append(power(10, log_normpp) * power(10, log_psi_pp) * laguerre_pp)               


                            #test_ints([vp, vpp, jp, jpp])

                            if dbug is True:
                                print("\t".join(["\nstate_p", "state_pp"]))
                                print('\t'.join([p, pp]))
                                print("\t".join(["\np", "vp", "jp", "pp", "vpp", "jpp"]))
                                print('\t'.join([str(p), str(vp), str(jp), str(pp), str(vpp), str(jpp)]))

                            if (dbug is True):
                                print("\nDep, Depp")
                                print(Dep, Depp)

                            if (dbug is True):
                                print("\nbig_Ap, big_App")
                                print(big_Ap, big_App)

                            if (dbug is True):
                                print("\nalphap, alphapp")
                                print(alphap, alphapp)

                            if (dbug is True):
                                print("\nr0p, r0pp")
                                print(r0p, r0pp)

                            if (dbug is True):
                                print("\t".join(["little_ap", "little_app"]))
                                print('\t'.join([str(little_ap), str(little_app)]))

                            if (dbug is True):
                                print("\nC1p, C1pp")
                                print(C1p, C1pp)

                            if (dbug is True):
                                print("\nC2p, C2pp")
                                print(C2p, C2pp)

                            if (dbug is True):
                                print("\nD1p, D1pp")
                                print(D1p, D1pp)

                            if (dbug is True):
                                print("\nD2p, D2pp")
                                print(D2p, D2pp)

                            if (dbug is True):
                                print("\nK1p, K1pp")
                                print(K1p, K1pp)

                            if (dbug is True):
                                print("\nK2p, K2pp")
                                print(K2p, K2pp)

                            #test_floats([Dep, Depp, big_Ap, big_App, alphap, alphapp, 
                            #             r0p, r0pp, little_ap, little_app, C1p, C1pp, C2p, C2pp,
                            #             D1p, D1pp, D2p, D2pp, K1p, K1pp, K2p, K2pp, log_normp, log_normpp])                        

                            fcf[i_p][i_pp][jp][jpp][vp].append(
                                pow(simps(y=psi_p_r * psi_pp_r, x=r_array), 2))
            i_pp += 1
        i_p += 1
    return psi_p, psi_pp, fcf
