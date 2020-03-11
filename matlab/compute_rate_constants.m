%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%
%%%   calculate rate constants by integrating xsecs over Maxwellian EEDF
%%%
%%%   See N2_dissocation.m and Taylor_1988.m
%%%   Seee N_xsecs.m
%%%
clear all;
write_data = 0;

%%% create energy grid and Maxwellian EEDF
%
gamma = sqrt(2*1.7588e11); % sqrt(2*e/me)
Te = 0.1:0.1:50;           % electron temperature [eV]
for i = 1:length(Te)
    

    E = 0:Te(i)/2e2:50*Te(i);     % electron kinetic energy [eV]
    FM = 2/sqrt(pi)/Te(i)^(3/2)*exp(-E/Te(i));  % Maxwellian EEDF

    %%% check to make sure grid is refined enough using 0th and 2nd moments
    %
    test0 = trapz(E,FM.*E.^(1/2));   % should be one
    error0 = 100*abs(1-test0);
    if(error0>=1)
        warning('0th velocity moment not converged');
    end
    %
    ebar = trapz(E,FM.*E.^(3/2));    % should be 3*Te/2;
    error2 = 100*abs(ebar-3*Te(i)/2)/(3*Te(i)/2);
    if(error2>=1)
        warning('2nd velocity moment not converged');
    end

    % close(figure(1));
    % figure(1);
    % semilogy(E,FM);
    % xlabel('kinetic energy [eV]');
    % ylabel('EEDF [eV^-^3^/^2]');

    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%
    %%%    load diss xsecs from data file (XSEC MUST BE IN SI UNITS!!!!!!)
    %%%
    
    load('N2_dissociation_xsecs.mat');
    E_xsecs = N2_diss_xsecs.E;
    %
    xsec = N2_diss_xsecs.N2X_dn_4S4S;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    k1(i) = gamma*trapz(E,E.*xsec_interp.*FM); % [m^3/s]
    %
    xsec = N2_diss_xsecs.N2X_dn_4S2D;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    k2(i) = gamma*trapz(E,E.*xsec_interp.*FM); % [m^3/s]
    %
    xsec = N2_diss_xsecs.N2X_dn_4S2P;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    k3(i) = gamma*trapz(E,E.*xsec_interp.*FM); % [m^3/s]
    %
    xsec = N2_diss_xsecs.N2X_dn_2D2D;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    k4(i) = gamma*trapz(E,E.*xsec_interp.*FM); % [m^3/s]
    %
    xsec = N2_diss_xsecs.N2X_di_i4S;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    k5(i) = gamma*trapz(E,E.*xsec_interp.*FM); % [m^3/s]
    %
    xsec = N2_diss_xsecs.N2X_di_i4S;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    k6(i) = gamma*trapz(E,E.*xsec_interp.*FM); % [m^3/s]
    %
    %
    %
    xsec = N2_diss_xsecs.N2A_dn_4S4S;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    kA1(i) = gamma*trapz(E,E.*xsec_interp.*FM); % [m^3/s]
    %
    xsec = N2_diss_xsecs.N2A_dn_4S2D;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    kA2(i) = gamma*trapz(E,E.*xsec_interp.*FM); % [m^3/s]
    %
    xsec = N2_diss_xsecs.N2A_dn_4S2P;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    kA3(i) = gamma*trapz(E,E.*xsec_interp.*FM); % [m^3/s]
    %
    xsec = N2_diss_xsecs.N2A_dn_2D2D;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    kA4(i) = gamma*trapz(E,E.*xsec_interp.*FM); % [m^3/s]
    %
    xsec = N2_diss_xsecs.N2A_di_i4S;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    kA5(i) = gamma*trapz(E,E.*xsec_interp.*FM); % [m^3/s]
    %
    xsec = N2_diss_xsecs.N2A_di_i4S;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    kA6(i) = gamma*trapz(E,E.*xsec_interp.*FM); % [m^3/s]
    %
    %
    %
    load('N2_ionization_xsecs.mat');
    E_xsecs = N2_ioniz_xsecs.E;
    %
    xsec = N2_ioniz_xsecs.sigiz;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    kXiz(i) = gamma*trapz(E,E.*xsec_interp.*FM);
    %
    xsec = N2_ioniz_xsecs.sigdi;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    kXdi(i) = gamma*trapz(E,E.*xsec_interp.*FM);
    %
    xsec = N2_ioniz_xsecs.sigdii;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    kXdii(i) = gamma*trapz(E,E.*xsec_interp.*FM);
    
%     close(figure(7));
%     figure(7);
%     plot(Te,kXiz+kXdi,'b');
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%
    %%%    load atomic xsecs from file
    %%%
    load('Natomic_xsecs.mat'); % uses Taylor
    E_xsecs = atomic.E; % see N_xsecs_Taylor.m
    
    load('./atomic_nitrogen/atomicSDP_xsecs.mat'); % uses Berrington 1975 and Kim 2002
    ESDP = atomicSDP.E; % see N_xsecs.m
    
    %%%   xsecs for N(4S)
    %
    xsec = atomicSDP.Forbidden.sig4S2D.xsec;
    xsec_interp = interp1(ESDP,xsec,E,'pchirp');
    deltaE = atomicSDP.Forbidden.sig4S2D.deltaE;
    k4S2D(i) = gamma*trapz(E,E.*xsec_interp.*FM);    % [m^3/s]
    k4S2D_fit = 3.2e-8*exp(-3.33./Te)./sqrt(Te)*1e-6; % [m^3/s]
    kE_4S2D(i) = deltaE*k4S2D(i);    % [eV-m^3/s]
    %
    xsec = atomicSDP.Forbidden.sig4S2P.xsec;
    xsec_interp = interp1(ESDP,xsec,E,'pchirp');
    deltaE = atomicSDP.Forbidden.sig4S2P.deltaE;
    k4S2P(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    k4S2P_fit = 9.5e-9*exp(-5.0./Te)./sqrt(Te)*1e-6; % [m^3/s]
    kE_4S2P(i) = deltaE*k4S2P(i);    % [eV-m^3/s]
    %
    %
    %
    xsec = atomic.allowed.N4S_NAll.xsec_eff;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    deltaE = atomic.allowed.N4S_NAll.energy_avg;
    k4SAll(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    kE_4SAll(i) = deltaE*k4SAll(i);    % [eV-m^3/s]
    %
    %
    %
    xsec = atomicSDP.Allowed.sig4S4P3s.xsec;
    deltaE = atomicSDP.Allowed.sig4S4P3s.deltaE;
  %  xsec_interp = interp1(ESDP,xsec.*ESDP./(ESDP+14.53+deltaE),E,'pchirp');
    xsec_interp = interp1(ESDP,xsec,E,'pchirp');
    k4S_4P3s(i) = gamma*trapz(E,E.*xsec_interp.*FM);  % [m^3/s]
    %
    xsec = atomicSDP.Allowed.sig4S4P2p4.xsec;
    deltaE = atomicSDP.Allowed.sig4S4P2p4.deltaE;
  %  xsec_interp = interp1(ESDP,xsec.*ESDP./(ESDP+14.53+deltaE),E,'pchirp');
    xsec_interp = interp1(ESDP,xsec,E,'pchirp');
    k4S_4P2p4(i) = gamma*trapz(E,E.*xsec_interp.*FM);  % [m^3/s]
    %
    %
    %
    xsec = atomic.Rydberg.N4S_NRyd.xsec_eff;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    deltaE = atomic.Rydberg.N4S_NRyd.energy_avg;
    k4SRyd(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    kE_4SRyd(i) = deltaE*k4SRyd(i);    % [eV-m^3/s]
    %
    xsec = atomicSDP.Ionization.sig4S1.xsec;
    xsec_interp = interp1(ESDP,xsec,E,'pchirp');
    deltaE = atomicSDP.Ionization.sig4S1.deltaE;
    k4SNII(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    k4SNII_fit = 2.5e-6/(14.5^1.5)*sqrt(Te/14.5).*exp(-14.5./Te)*1e-6; % [m^3/s]
    kE_4SNII(i) = deltaE*k4SNII(i);    % [eV-m^3/s]
    %
    xsec = atomic.effective.N4S.xsec;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    if(Te(i)<=2)
        mueN4S(i) = gamma/3/Te(i)*trapz(E,E./(xsec_interp).*FM);
    else   % has hard time for low temperature with growth term
        mueN4S(i) = gamma/3/Te(i)*trapz(E,E./(xsec_interp+k4SNII(i)/gamma./sqrt(E)).*FM); % [m^3/s]
    end
    
    
    %%%   xsecs for N(2D)
    %
    xsec = atomicSDP.Forbidden.sig2D2P.xsec;
    xsec_interp = interp1(ESDP,xsec,E,'pchirp');
    deltaE = atomicSDP.Forbidden.sig2D2P.deltaE;
    k2D2P(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    k2D2P_fit = 1.1e-7*exp(-1.9./Te)./sqrt(Te)*1e-6; % [m^3/s]
    kE_2D2P(i) = deltaE*k2D2P(i);    % [eV-m^3/s]
    %
    xsec = atomic.allowed.N2D_NAll.xsec_eff;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    deltaE = atomic.allowed.N2D_NAll.energy_avg;
    k2DAll(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    kE_2DAll(i) = deltaE*k2DAll(i);    % [eV-m^3/s]
    %
    xsec = atomic.superelastic.N2D_N4S.xsec;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    deltaE = atomic.superelastic.N2D_N4S.energy;
    k2D4S(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    kE_2D4S(i) = deltaE*k2D4S(i);    % [eV-m^3/s]
    %
    xsec = atomicSDP.Ionization.sig2D1.xsec;
    xsec_interp = interp1(ESDP,xsec,E,'pchirp');
    deltaE = atomicSDP.Ionization.sig2D1.deltaE;
    k2DNII(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    k2DNII_fit = 2.5e-6/(12.1^1.5)*sqrt(Te/12.1).*exp(-12.1./Te)*1e-6; % [m^3/s]
    kE_2DNII(i) = deltaE*k2DNII(i);    % [eV-m^3/s]
    %
    xsec = atomic.effective.N2D.xsec;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    if(Te(i)<=2)
        mueN2D(i) = gamma/3/Te(i)*trapz(E,E./(xsec_interp).*FM);
    else   % has hard time for low temperature with growth term
        mueN2D(i) = gamma/3/Te(i)*trapz(E,E./(xsec_interp+k2DNII(i)/gamma./sqrt(E)).*FM); % [m^3/s]
    end
    
    
    %%%   xsecs for N(2P)
    %
    xsec = atomic.allowed.N2P_NAll.xsec_eff;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    deltaE = atomic.allowed.N2P_NAll.energy_avg;
    k2PAll(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    kE_2PAll(i) = deltaE*k2PAll(i);    % [eV-m^3/s]
    %
    xsec = atomic.superelastic.N2P_N4S.xsec;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    deltaE = atomic.superelastic.N2P_N4S.energy;
    k2P4S(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    kE_2P4S(i) = deltaE*k2P4S(i);    % [eV-m^3/s]
    %
    xsec = atomic.superelastic.N2P_N2D.xsec;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    deltaE = atomic.superelastic.N2P_N2D.energy;
    k2P2D(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    kE_2P2D(i) = deltaE*k2P2D(i);    % [eV-m^3/s]
    %
    xsec = atomicSDP.Ionization.sig2P1.xsec;
    xsec_interp = interp1(ESDP,xsec,E,'pchirp');
    deltaE = atomicSDP.Ionization.sig2P1.deltaE;
    k2PNII(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    k2PNII_fit = 2.5e-6/(10.9^1.5)*sqrt(Te/10.9).*exp(-10.9./Te)*1e-6; % [m^3/s]
    kE_2PNII(i) = deltaE*k2PNII(i);    % [eV-m^3/s]
    %
    xsec = atomic.effective.N2P.xsec;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    if(Te(i)<=2)
        mueN2P(i) = gamma/3/Te(i)*trapz(E,E./(xsec_interp).*FM);
    else   % has hard time for low temperature with growth term
        mueN2P(i) = gamma/3/Te(i)*trapz(E,E./(xsec_interp+k2PNII(i)/gamma./sqrt(E)).*FM); % [m^3/s]
    end
    
    
    %%%   xsecs for NII (a.ka. N+)
    %
    xsec = atomic.forbidden.NII_NIIFor1D.xsec;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    deltaE = atomic.forbidden.NII_NIIFor1D.energy;
    kIIFor1D(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    kE_IIFor1D(i) = deltaE*kIIFor1D(i);    % [eV-m^3/s]
    %
    xsec = atomic.forbidden.NII_NIIFor1S.xsec;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    deltaE = atomic.forbidden.NII_NIIFor1S.energy;
    kIIFor1S(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    kE_IIFor1S(i) = deltaE*kIIFor1S(i);    % [eV-m^3/s]
    %
    %%%%  below is effective
    %
    xsec = atomic.forbidden.NII_NIIFor.xsec_eff;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    deltaE = atomic.forbidden.NII_NIIFor.energy_avg;
    kIIFor(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    kE_IIFor(i) = deltaE*kIIFor(i);    % [eV-m^3/s]
    %
    %%%%
    %
    xsec = atomic.allowed.NII_NIIAll.xsec_eff;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    deltaE = atomic.allowed.NII_NIIAll.energy_avg;
    kIIAll(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    kE_IIAll(i) = deltaE*kIIAll(i);    % [eV-m^3/s]
    %
    xsec = atomic.Rydberg.NII_NIIRyd.xsec_eff;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    deltaE = atomic.Rydberg.NII_NIIRyd.energy_avg;
    kIIRyd(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    kE_IIRyd(i) = deltaE*kIIRyd(i);    % [eV-m^3/s]
    %
    xsec = atomic.ionization.NII_NIII.xsec;
    xsec_interp = interp1(E_xsecs,xsec,E,'pchirp');
    deltaE = atomic.ionization.NII_NIII.energy;
    kNIIiz(i) = gamma*trapz(E,E.*xsec_interp.*FM);   % [m^3/s]
    kE_NIIiz(i) = deltaE*kNIIiz(i);    % [eV-m^3/s]
    
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
%%%  
%%%           plot stuff
%%%

close(figure(3));
figure(3);
loglog(Te,(k1+k2+k3+k4+k5+k6)*1e6*3.217e16,'black');
hold on; plot(Te,(kA1+kA2+kA3+kA4+kA5+kA6)*1e6*3.217e16,'r');
axis([1 40 1e6 4e10]); xlabel('T_e [eV]'); ylabel('\nu [Hz]');
title('Dissociation rates in 1 Torr Nitrogen for Maxwellian EEDF');
legend('e+N_2(X)=>e+2N','e+N_2(A)=>e+2N','location','best');
%
% kN2Xfit = 4.11e-33*(11605*Te).^6.16.*exp(-113263/11605./Te);
% kN2Afit = 4.11e-33*(11605*Te).^6.16.*exp(-113263/11605./Te);
% figure(3); hold on; plot(Te,kN2Xfit*3.217e16,'b*');
%
%      plot mobilities
%
close(figure(2));
figure(2);
plot(log10(Te),log10(mueN4S));
hold on; plot(log10(Te),log10(mueN2D),'r--');
hold on; plot(log10(Te),log10(mueN2P),'g--');
axis([log10(0.1) log10(40) 23 26]);  xlabel('T_e [eV]'); ylabel('\mu_e [Hz]');
title('Mobilities'); legend('N(^4S)','N(^2D)','N(^2P)','location','best');
%
logTe = log10(Te);
mueN4S_fit = 10.^(0.089*logTe.^3+0.028*logTe.^2-0.905*logTe+24.8);
hold on; plot(logTe,log10(mueN4S_fit),'r*');
%
%      plot superelastic
%
close(figure(1));
figure(1);
loglog(Te,k2D4S,'b');
hold on; plot(Te,k2P4S,'r');
hold on; plot(Te,k2P2D,'g');
legend('N2D->N4S','N2P->N4S','N2P->N2D','location','best');
hold on; plot(Te,k4S2D*4/10.*exp(2.38./Te),'b*');
hold on; plot(Te,k4S2P*4/6.*exp(3.58./Te),'r*');
hold on; plot(Te,k2D2P*10/6.*exp(1.20./Te),'g*');
%axis([0.1 40 1e23 1e26]);  
xlabel('T_e [eV]'); ylabel('k_s_u_p_e_r [m^3/s]');
title('Inverse rate constants'); 
%
%      plot forbidden
%
close(figure(11));
figure(11);
plot(Te,k4S2D*1e6,'b');
hold on; plot(Te,k4S2P*1e6,'r');
hold on; plot(Te,k2D2P*1e6,'g');
axis([0.1 40 0 1e-6]);  
xlabel('T_e [eV]'); ylabel('k [cm^3/s]');
title('Forbidden rate constants'); 
legend('N4S->N2D','N4S->N2P','N2D->N2P','location','best');%
% hold on; plot(Te,k4S2D_fit,'b*');
% hold on; plot(Te,k4S2P_fit,'r*');
% hold on; plot(Te,k2D2P_fit,'g*');
%
%      plot ionization
%
close(figure(12));
figure(12);
loglog(Te,k4SNII*1e6,'b');
hold on; plot(Te,k2DNII*1e6,'r');
hold on; plot(Te,k2PNII*1e6,'g');
axis([0.1 40 1e-30 1e-12]);  
xlabel('T_e [eV]'); ylabel('k [cm^3/s]');
title('Ionization rate constants'); 
%legend('N4S->N2D','N4S->N2P','N2D->N2P','location','best');
hold on; plot(Te,k4SNII_fit,'b*');
hold on; plot(Te,k2DNII_fit,'r*');
hold on; plot(Te,k2PNII_fit,'g*');
%
%      plot allowed
%
close(figure(22));
figure(22); semilogy(Te,k4S_4P3s*1e6,'b');
hold on; plot(Te,k4S_4P2p4*1e6,'r');
title('allowed with N(^4S)');
xlabel('T_e [eV]'); ylabel('k [cm^3/s]');
axis([2 12 1e-10 1e-7]); title('compare with Frost 1998');
set(gca,'XTick',2:1:12); grid on;
legend('4S->4P3s','4S->4P2p4');
% Uij = 10.33;
% fij = 2.62e-1;
% k4S_4P3s_2 = 1.6e-5*fij/Uij./sqrt(Te).*exp(-10.33./Te);
% hold on; plot(Te,k4S_4P3s_2,'b--');
% hold on; plot(Te,k4S_4P2p4*1e6*10,'r--');
%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 


if(write_data==1)
    
    diss_thermal.Te = Te;
    %
    diss_thermal.kdn_4S4S = k1*1e6; % [cm^3/s]
    diss_thermal.kdn_4S2D = k2*1e6; % [cm^3/s]
    diss_thermal.kdn_4S2P = k3*1e6; % [cm^3/s]
    diss_thermal.kdn_2D2D = k4*1e6; % [cm^3/s]
    diss_thermal.kdi_i4S = k5*1e6;  % [cm^3/s]
    diss_thermal.kdi_i2D = k6*1e6;  % [cm^3/s]
    %
    diss_thermal.kdnx_4S4S = kA1*1e6; % [cm^3/s]
    diss_thermal.kdnx_4S2D = kA2*1e6; % [cm^3/s]
    diss_thermal.kdnx_4S2P = kA3*1e6; % [cm^3/s]
    diss_thermal.kdnx_2D2D = kA4*1e6; % [cm^3/s]
    diss_thermal.kdix_i4S = kA5*1e6;  % [cm^3/s]
    diss_thermal.kdix_i2D = kA6*1e6;  % [cm^3/s]

    save('diss_thermal.mat','diss_thermal');
   
    
    %%%   write atomic rate constants
    %    
    atomic_thermal.Te = Te;
    %
    atomic_thermal.kSD = k4S2D*1e6;
    atomic_thermal.kSP = k4S2P*1e6;
    atomic_thermal.kDP = k2D2P*1e6;
    atomic_thermal.kIIFor1D = kIIFor1D*1e6;
    atomic_thermal.kIIFor1S = kIIFor1S*1e6;
    %
    atomic_thermal.kDS = k2D4S*1e6;
    atomic_thermal.kPS = k2P4S*1e6;
    atomic_thermal.kPD = k2P2D*1e6;
    %
    atomic_thermal.kSi = k4SNII*1e6;
    atomic_thermal.kDi = k2DNII*1e6;
    atomic_thermal.kPi = k2PNII*1e6;
    atomic_thermal.kii = kNIIiz*1e6;
    %
    %   for momentum transfer
    %
    econst  = 1.6022e-19;
    meconst = 9.1094e-31;
    atomic_thermal.kmS = (econst/meconst./mueN4S-k4SNII)*1e6;
    atomic_thermal.kmD = (econst/meconst./mueN2D-k2DNII)*1e6;
    atomic_thermal.kmP = (econst/meconst./mueN2P-k2PNII)*1e6;
    %
    %   for energy transfer with higher states
    %
    atomic_thermal.kE_exc_higherS = (kE_4SAll+kE_4SRyd)*1e6;
    atomic_thermal.kE_exc_higherD = kE_2DAll*1e6;
    atomic_thermal.kE_exc_higherP = kE_2PAll*1e6;
    atomic_thermal.kE_exc_alli = (kE_IIFor + kE_IIAll + kE_IIRyd)*1e6;
    atomic_thermal.kE_exc_Fori = kE_IIFor*1e6;
    atomic_thermal.kE_exc_higheri = (kE_IIAll + kE_IIRyd)*1e6;
    
    %
    %  allowed transitions
    %
    atomic_thermal.k4S_4P3s  = k4S_4P3s*1e6;
    atomic_thermal.k4S_4P2p4 = k4S_4P2p4*1e6;

    save('atomic_thermal.mat','atomic_thermal');
    
end







