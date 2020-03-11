function N_xsecs_Taylor
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%      Computes the excitation and ionization
%%%      cross sections for e+N(4S,2D,2P) and e+N+(3P)
%%%      using expressions given in Taylor 1988
%%%      "Energy deposition in N and N+ by high--energy electron beams"
%%%


writedata = 0;
plot_Allowed = 0;
plot_Rydberg = 0;
scrsz = get(0,'ScreenSize');


%%%    set some needed constants
%
R   = 13.6;     % hydrogen ionization potential [eV]
mc2 = 0.511e6;  % electron rest mass energy [eV]
a0  = 5.29e-9;  % bohr radius [cm]
%
E = [0 0.01:0.01:1.5 10.^(0.2:0.02:7)];   % kinetic energy grid (eV)
gamma = E/(mc2)+1;
beta = sqrt(1-1./gamma.^2);
ET = 0.5*mc2*beta.^2;     % 1/2mv^2 (E used in Taylor 1988)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%     optically allowed transitions (TABLE I and Eq 4 of Taylor 1988)
%%%     Also see W.L. Wiese and J.R. Fuhr J. Phys. Chem. Ref. Data. Vol.
%%%     36, No. 4, 2007 for most recent data
%%%


%%%    with N(4S)
%
%stateI_All = ['4P3S', '4P2p4', '4P4s', '4P3d'];
EI_All  = [10.33    10.93    12.86    13.0];     % excitation energy [eV]
fI_All  = [2.62e-1  8.49e-2  2.42e-2  7.07e-2];  % oscillator strength
sigI_All = zeros(length(EI_All),length(E));
%
for k = 1:length(EI_All)
    sigI_All(k,:) = TaylorAllowed(EI_All(k),1.0,0.3125,fI_All(k),0);
end
%
sigI_Allowed = sum(sigI_All);                 % total cross section
EI_All_avg   = sum(EI_All)/length(EI_All);    % average energy
sigI_All_eff = (EI_All*sigI_All)/EI_All_avg;  % effective cross section
%figure(99); loglog(E,sigI_All_eff*EI_All_avg);

%%%    with N(2D) (2.4eV)
%
%stateI_All = ['2P3s', '2D3s', '2P4s', '2P3d', '2F3d', '2D3d'];
EI_All_2D  = [8.30    9.97    10.53   10.59   10.62   10.65];    % excitation energy [eV]
fI_All_2D  = [6.91e-2 8.00e-2 1.22e-2 1.30e-2 2.99e-2 6.52e-3];  % oscillator strength 
sigI_All_2D = zeros(length(EI_All_2D),length(E));
for k = 1:length(EI_All_2D)
    sigI_All_2D(k,:) = TaylorAllowed(EI_All_2D(k), 1.0, 0.3125, ...
                                     fI_All_2D(k), 0);
end
%
sigI_Allowed_2D = sum(sigI_All_2D);                    % total cross section
EI_All_avg_2D   = sum(EI_All_2D)/length(EI_All_2D);    % average energy
sigI_All_eff_2D = (EI_All_2D*sigI_All_2D)/EI_All_avg_2D;  % effective cross section
%figure(99); hold on; loglog(E,sigI_All_eff_2D*EI_All_avg_2D,'r');

%%%    with N(2P) (3.6eV)
%
%stateI_All = [2P3s 2D3s 2P4s 2P3d 2D3d];
EI_All_2P  = [7.11    8.78    9.34    9.40    9.45];     % excitation energy [eV]
fI_All_2P  = [5.72e-2 2.69e-2 2.58e-3 1.90e-2 3.32e-2];  % oscillator strength 
sigI_All_2P = zeros(length(EI_All_2P),length(E));
for k = 1:length(EI_All_2P)
    sigI_All_2P(k,:) = TaylorAllowed(EI_All_2P(k), 1.0, 0.3125, ...
                                     fI_All_2P(k), 0);
end
%
sigI_Allowed_2P = sum(sigI_All_2P);                    % total cross section
EI_All_avg_2P   = sum(EI_All_2P)/length(EI_All_2P);   % average energy
sigI_All_eff_2P = (EI_All_2P*sigI_All_2P)/EI_All_avg_2P;  % effective cross section
%figure(99); loglog(E,sigI_All_eff_2P*EI_All_avg_2P,'g');

%%%    with N+
%
%stateII_All = ['3D02p3', '3P02p3', '3P03s', '3S02p3', '3D03d', '3P03d'];
EII_All = [11.43   13.53   18.46   19.22   23.23   23.41];
fII_All = [1.10e-1 1.60e-1 7.44e-2 2.22e-1 3.02e-1 1.03e-1];
sigII_All = zeros(length(EII_All),length(E));
%
for k = 1:length(EII_All)
    sigII_All(k,:) = TaylorAllowed(EII_All(k),1.0,0.3125,fII_All(k),1);
end
%
sigII_Allowed = sum(sigII_All);                   % total cross section
EII_All_avg   = sum(EII_All)/length(EII_All);     % average energy
sigII_All_eff = (EII_All*sigII_All)/EII_All_avg;  % effective cross section
figure(99); loglog(E,sigII_All_eff*EII_All_avg,'black');

%%%    plot Allowed state cross sections
%
if(plot_Allowed==1)
    close(figure(1));
    f2=figure(1);
    set(f2,'Position',[1 scrsz(4)/2 scrsz(3)/1.5 scrsz(4)]);
    %
    subplot(2,2,1);
    loglog(E,sigI_All); title('Allowed with N(4S)');
    xlabel('\epsilon [eV]'); ylabel('\sigma [cm^2]');
    %set(gca,'Xtick',[1,1e2,1e4,1e6]);
    %
    subplot(2,2,4);
    loglog(E,sigII_All); title('Allowed with N^+');
    xlabel('\epsilon [eV]'); ylabel('\sigma [cm^2]');
    % axis([1 1e7 1e-20 1e-16]);
    % set(gca,'Xtick',[1,1e2,1e4,1e6]);
    %
    subplot(2,2,2);
    loglog(E,sigI_All_2D); title('Allowed with N(2D)');
    xlabel('\epsilon [eV]'); ylabel('\sigma [cm^2]');
    %
    subplot(2,2,3);
    loglog(E,sigI_All_2P); title('Allowed with N(2P)');
    xlabel('\epsilon [eV]'); ylabel('\sigma [cm^2]');
end


%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%      forbidden transitions (TABLE II and Eq 5) (and Eq 12)
%%%


%%%    with N(4S)
%
%stateI_All = ['4S->2D', '4S->2P'];
EI_For  = [2.38,   3.57];    % excitation energy [eV]
AI_For  = [0.025,  0.0175];
AI_For2 = [227.72, 356.04];
sigI_For = zeros(length(EI_For),length(E));
%
for k = 1:length(EI_For)
    sigI_For(k,:) = TaylorForbidden(EI_For(k),AI_For(k),AI_For2(k));
end
%
sigI_Forbidden = sum(sigI_For);               % total cross section
EI_For_avg   = sum(EI_For)/length(EI_For);    % average energy
sigI_For_eff = (EI_For*sigI_For)/EI_For_avg;  % effective cross section


%%%    with N(2D)
%
sigI_For_2D = TaylorForbidden(3.57-2.38,0.04,85);
EI_For_2D     = 3.57-2.38;    % average energy


%%%    with N+
%
EII_For  = [1.89, 4.04  4.04-1.89];   % excitation energy [eV]
OmeII_For= [2.98, 0.395 0.41];  % collision strength
%
sigII_For = zeros(length(EII_For),length(E));
for k = 1:length(EII_For)
    sigII_For(k,:) = TaylorOther(EII_For(k),OmeII_For(k));
end
%
sigII_Forbidden = sum(sigII_For);                   % total cross section
EII_For_avg     = sum(EII_For)/length(EII_For);     % average energy
sigII_For_eff   = (EII_For*sigII_For)/EII_For_avg;  % effective cross section
figure(100); loglog(E,sigII_For);
%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%        superlastic transitions (g4S = 4, g2D = 10, g2P = 6)
%%%

sigI_2D4S = zeros(1,length(E));
sigI_2P4S = zeros(1,length(E));
sigI_2P2D = zeros(1,length(E));
%
for m = 2:length(E)
    %
    Eprime = E(m)+2.38;
    this_sigI_4S2D = 10.^interp1(log10(1e-40+E),log10(1e-40+sigI_For(1,:)), ...
                                 log10(1e-40+Eprime),'pchip');
    sigI_2D4S(m) = 4/10*Eprime/E(m)*this_sigI_4S2D;
    %
    Eprime = E(m)+3.58;
    this_sigI_4S2P = 10.^interp1(log10(1e-40+E),log10(1e-40+sigI_For(2,:)), ...
                                 log10(1e-40+Eprime),'pchip');
    sigI_2P4S(m) = 4/6*Eprime/E(m)*this_sigI_4S2P;
    %
    Eprime = E(m)+1.20;
    this_sigI_2D2P = 10.^interp1(log10(1e-40+E),log10(1e-40+sigI_For_2D), ...
                                 log10(1e-40+Eprime),'pchip');
    sigI_2P2D(m) = 10/6*Eprime/E(m)*this_sigI_2D2P;
end

figure(10);
loglog(E,sigI_2D4S,'b'); 
% hold on; loglog(E,sigI_2P4S,'r');
% hold on; loglog(E,sigI_2P2D,'g');

%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%           Rydberg with N(4S), N(2D), N(2P), and N+
%%%


%%%    with N(4S)
%
EI_Ryd = [10.68, 11.60, 11.75, 11.84, 11.99, 12.00, 12.12, ...
          12.35, 12.97, 12.98, 12.99, 12.99, 13.01, 13.03, ...
          13.70, 13.72, 13.92, 14.41, 14.89, 14.94, 13.70];
cjI_Ryd= [0.40,  0.30,  0.10,  1.50,  0.07,   0.14,  0.40, ...
          0.40,  0.40,  0.10,  0.14,  1.50,   0.10,  0.14, ...
          0.14,  0.14,  0.14,  0.14,  0.14,  0.14,  1.50];
fjI_Ryd= [0.150, 0.191, 0.130, 0.130, 0.150, 0.140, 0.150, ...
          0.150, 0.150, 0.130, 0.140, 0.130, 0.130, 0.140, ...
          0.140, 0.140, 0.140, 0.140, 0.140, 0.140, 0.109];
aI_Ryd = [2,2,1,0.7,0.7,2,2,2,2,1,2,0.7,1,2,2,2,2,2,2,2,0.7];
cI_Ryd = [1,1,1,2.5,0.5,1,1,1,1,1,1,2.5,1,1,1,1,1,1,1,1,2.5];
%
sigI_Ryd = zeros(length(EI_Ryd),length(E));
for k = 1:length(EI_Ryd)
    sigI_Ryd(k,:) = TaylorRydberg(EI_Ryd(k), cjI_Ryd(k), fjI_Ryd(k), ...
                                  aI_Ryd(k), cI_Ryd(k));
end
%
sigI_Rydberg = sum(sigI_Ryd);                 % total cross section
EI_Ryd_avg   = sum(EI_Ryd)/length(EI_Ryd);    % average energy
sigI_Ryd_eff = (EI_Ryd*sigI_Ryd)/EI_Ryd_avg;  % effective cross section
%figure(99); hold on; loglog(E,sigI_Ryd_eff*EI_Ryd_avg,'r');

%%%    with N+
%
EII_Ryd = [17.86, 18.47, 20.39, 20.63, 20.65, 20.92, 21.13, 21.57, ...
           22.08, 23.11, 23.17, 23.45, 23.55, 26.98, 27.82, 27.85];
cjII_Ryd= [0.40,   0.30,  0.30,  1.50,  0.30,  1.50,  0.07, 0.40, ...
           0.40,   0.10,  0.40,  0.14,  0.30,  0.07,  1.50, 0.07];
fjII_Ryd= [0.210, 0.110, 0.110, 0.077, 0.310, 0.077, 0.089, 0.089 ...
           0.089, 0.077, 0.089, 0.083, 0.110, 0.036, 0.032, 0.036];
aII_Ryd = [2,2,2,0.7,2,0.7,0.7,2,2,1,2,2,2,0.7,0.7,0.7];
cII_Ryd = [1,1,1,2.5,1,2.5,0.5,1,1,1,1,1,1,0.5,2.5,0.5];
%
sigII_Ryd = zeros(length(EII_Ryd),length(E));
for k = 1:length(EII_Ryd)
    sigII_Ryd(k,:) = TaylorRydberg(EII_Ryd(k),cjII_Ryd(k),fjII_Ryd(k), ...
                                   aII_Ryd(k),cII_Ryd(k));
end
%
sigII_Rydberg = sum(sigII_Ryd);                   % total cross section for excitation
EII_Ryd_avg   = sum(EII_Ryd)/length(EII_Ryd);     % average energy for energy loss
sigII_Ryd_eff = (EII_Ryd*sigII_Ryd)/EII_Ryd_avg;  % effective cross section for energy loss
%figure(99); hold on; loglog(E,sigII_Ryd_eff*EI_Ryd_avg,'r');

%%%    plot Rydberg state cross sections
%
if(plot_Rydberg==1)
    close(figure(2));
    f2=figure(2);
    scrsz = get(0,'ScreenSize');
    set(f2,'Position',[1 scrsz(4)/2 scrsz(3)/1.5 scrsz(4)/2.5]);
    %
    subplot(1,2,1);
    loglog(E,sigI_Ryd); title('Rydberg with N');
    xlabel('\epsilon [eV]'); ylabel('\sigma [cm^2]');
    %set(gca,'Xtick',[1,1e2,1e4,1e6]);
    %
    subplot(1,2,2);
    loglog(E,sigII_Ryd); title('Rydberg with N^+');
    xlabel('\epsilon [eV]'); ylabel('\sigma [cm^2]');
    % axis([1 1e7 1e-20 1e-16]);
    % set(gca,'Xtick',[1,1e2,1e4,1e6]);
end


%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%            Ionization (TABLE V and Eq 13)
%%%


I1 = 14.5; I1_2D = I1-2.4; I1_2P = I1-3.6; I2 = 29.6;
sigI_Iz    = TaylorIonization(I1,2.20,0.25);
sigI_Iz_2D = TaylorIonization(I1_2D,2.20,0.25);
sigI_Iz_2P = TaylorIonization(I1_2P,2.20,0.25);
sigII_Iz_3P   = TaylorIonization(I2,2.00,0.39);
sigII_Iz_1D   = TaylorIonization(I2-1.98,2.00,0.39);
sigII_Iz_1S   = TaylorIonization(I2-4.05,2.00,0.39);

%figure(99); hold on; loglog(E,sigII_Iz_3P*I2,'r');
% figure(7);
% loglog(E,sigI_Iz,'b',E,sigI_Iz_2DP,'r');

%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%       create total xsecs and inelastic Loss functions
%%%


%%%    with N(4S)
%
LossI_tot = EI_All_avg*sigI_All_eff + EI_For_avg*sigI_For_eff ...
          + EI_Ryd_avg*sigI_Ryd_eff + I1*sigI_Iz;
sigI_tot = sigI_Allowed+sigI_Forbidden+sigI_Rydberg+sigI_Iz;


%%%    with N(2D)
%
LossI_tot_2D = EI_All_avg_2D*sigI_All_eff_2D + (3.57-2.38)*sigI_For_2D ...
             + I1_2D*sigI_Iz_2D;
sigI_tot_2D = sigI_Allowed_2D + sigI_For_2D + sigI_Iz_2D;


%%%    with N+
%
LossII_tot = EII_All_avg*sigII_All_eff + EII_Ryd_avg*sigII_Ryd_eff ...
           + EII_For_avg*sigII_For_eff + I2*sigII_Iz_3P;;
sigII_tot  = sigII_Allowed+sigII_Rydberg+sigII_Forbidden+sigII_Iz_3P;

%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%       load effective momentum xsec and extrapolate to match 
%%%       sigI_tot, then subtract to get elastic momentum transfer
%%%


%%% import cross section data from file
%
num = 5;
A01 = importdata('../../Boltzmann/xsecs_nitrogen_atomic.txt','\t',num);
EA = A01.data(:,1);            % energy [eV]
sigma_eff = A01.data(:,2)*1e4; % effective momentum [cm^2]
sigma_eff(1) = sigma_eff(2);
%num = num + length(A01.data(:,1))+7;

[thisE,thisi1] = min(abs(E-1e4));  % get index for E=1e3
[thisE,thisi2] = min(abs(E-1e5));  % get index for E=1e4
thisE1 = E(thisi1);
thisE2 = E(thisi2);
%

Sig_eff_test = [sigma_eff',1.2*sigI_tot(thisi1),sigI_tot(thisi2)];
E_test       = [EA', thisE1, thisE2]'; % good enough for gov. work

[thisE3,thisi3] = min(abs(E-max(EA)));  % get index for E=40
E_sub = E(thisi3:thisi1);
E_test2 = [EA',E_sub];
Sig_eff_test2 = interp1(log10(1e-20+E_test),log10(1e-20+Sig_eff_test), ...
                        log10(1e-20+E_test2),'pchip');
Sig_eff_test2 = 10.^(Sig_eff_test2);   % Sig_eff on refined grid

Sig_eff_test2 = [Sig_eff_test2, sigI_tot(thisi1+1:length(E))];
E_test2 = [E_test2, E(thisi1+1:length(E))];

%%% now interp Sig_eff_test_2 to E grid
%
Sig_eff_test2 = interp1(log10(1e-20+E_test2),log10(1e-20+Sig_eff_test2), ...
                       log10(1e-20+E),'pchip');
Sig_eff_test2 = 10.^Sig_eff_test2;


%%% subtract to get elastic momentum
%
Sig_eff = Sig_eff_test2;
Sig_eff(1:10);
E(1:10);
Sig_elm = Sig_eff_test2 - sigI_tot;


%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

close(figure(3));
f3=figure(3);
set(f3,'Position',[1 scrsz(4)/2 scrsz(3)/1.5 scrsz(4)/2.5]);
%
subplot(1,2,1);
loglog(E,sigI_tot,'black');
hold on; loglog(E,sigI_Allowed+sigI_Forbidden+sigI_Rydberg,'r--');
hold on; plot(E,sigI_Iz,'b--');
hold on; plot(E,Sig_eff,'go');
hold on; plot(E,Sig_elm,'r*');
axis([1 1e7 1e-19 1e-15]);
title('Total cross section for N');
xlabel('\epsilon [eV]'); ylabel('\sigma [cm^2]');
set(gca,'Xtick',[1,1e2,1e4,1e6]);
legend('\sigma_t','\sigma_e','\sigma_i');
%
subplot(1,2,2);
loglog(E,sigII_tot,'black','linewidth',1);
hold on; plot(E,sigII_Allowed+sigII_Rydberg+sigII_Forbidden,'r--','linewidth',1);
hold on; plot(E,sigII_Iz_3P,'b--','linewidth',1);
axis([1 1e7 1e-19 1e-15]);
title('Total cross section for N+');
xlabel('\epsilon [eV]'); ylabel('\sigma [cm^2]');
set(gca,'Xtick',[1,1e2,1e4,1e6]);
legend('\sigma_t','\sigma_e','\sigma_i');

%%%%%%%%%%%%%%%%%%

close(figure(4));
f4=figure(4);
set(f4,'Position',[1 scrsz(4)/2 scrsz(3)/1.5 scrsz(4)/2.5]);
%
subplot(1,2,1);
loglog(E,LossI_tot,'black');
hold on; loglog(E,LossI_tot - I1*sigI_Iz,'r--');
hold on; plot(E,I1*sigI_Iz,'b--');
%hold on; plot(E,sigI_Allowed,'magenta');
axis([1 1e7 1e-18 1e-14]);
title('Partial Loss Functions for N');
xlabel('\epsilon [eV]'); ylabel('Loss Function [eV-cm^2]');
set(gca,'Xtick',[1,1e2,1e4,1e6]);
legend('L_e+L_i','L_e','L_i');
%
subplot(1,2,2);
loglog(E,LossII_tot,'black','linewidth',1);
hold on; plot(E,LossII_tot - I2*sigII_Iz_3P,'r--','linewidth',1);
hold on; plot(E,I2*sigII_Iz_3P,'b--','linewidth',1);
axis([1 1e7 1e-18 1e-14]);
% title('Total cross section for N+');
xlabel('\epsilon [eV]'); ylabel('Loss Function [eV-cm^2]');
set(gca,'Xtick',[1,1e2,1e4,1e6]);
legend('L_e+L_i','L_e','L_i');


%%%       write total and effective cross sections data to files
%%%
%%%       total is for rate constants, effective is for energy transfer
%%%
%
if(writedata == 1)
    %path = '../Boltzmann/xsecs_atomic_Taylor/';
    %
%     fileID = fopen([path,'NI_elm.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E_test2; max(Sig_elm,0)*1e-4]); % m2 units for xsec
%     

    atomic.E = E;
    
    %%%   effective cross sections for mobility computations
    %
    atomic.elasticmom.xsec = Sig_elm*1e-4;
    atomic.elasticmom.mM = 3.92e-5;
    atomic.effective.N4S.xsec = Sig_eff*1e-4;
    
    %%%   xsecs for N(4S)
    %
    atomic.effective.N4S.xsec = Sig_eff*1e-4;
    %
    atomic.forbidden.N4S_N2D.xsec = sigI_For(1,:)*1e-4;
    atomic.forbidden.N4S_N2D.energy = EI_For(1);
    atomic.forbidden.N4S_N2P.xsec = sigI_For(2,:)*1e-4;
    atomic.forbidden.N4S_N2P.energy = EI_For(2);
    %
    atomic.allowed.N4S_NAll.xsec_tot = sigI_Allowed*1e-4;
    atomic.allowed.N4S_NAll.xsec_eff = sigI_All_eff*1e-4;
    atomic.allowed.N4S_NAll.energy_avg = EI_All_avg;
    %
    atomic.Rydberg.N4S_NRyd.xsec_tot = sigI_Rydberg*1e-4;
    atomic.Rydberg.N4S_NRyd.xsec_eff = sigI_Ryd_eff*1e-4;
    atomic.Rydberg.N4S_NRyd.energy_avg = EI_Ryd_avg;
    %
    atomic.ionization.N4S_NII.xsec = sigI_Iz*1e-4;
    atomic.ionization.N4S_NII.energy = I1;
    
    
    %%%   xsecs for N(2D)
    %
    atomic.forbidden.N2D_N2P.xsec = sigI_For_2D*1e-4;
    atomic.forbidden.N2D_N2P.energy = EI_For_2D;
    %
    atomic.allowed.N2D_NAll.xsec_tot = sigI_Allowed_2D*1e-4;
    atomic.allowed.N2D_NAll.xsec_eff = sigI_All_eff_2D*1e-4;
    atomic.allowed.N2D_NAll.energy_avg = EI_All_avg_2D;
    %
    atomic.ionization.N2D_NII.xsec = sigI_Iz_2D*1e-4;
    atomic.ionization.N2D_NII.energy = I1_2D;
    %
    %
    atomic.superelastic.N2D_N4S.xsec = sigI_2D4S*1e-4;
    atomic.superelastic.N2D_N4S.energy = 2.38;
    %
    atomic.effective.N2D.xsec = (Sig_elm + sigI_For_2D + sigI_2D4S...
                              +  sigI_Allowed_2D +  sigI_Iz_2D)*1e-4;
    
    %%%   xsecs for N(2P)
    %
    atomic.allowed.N2P_NAll.xsec_tot = sigI_Allowed_2P*1e-4;
    atomic.allowed.N2P_NAll.xsec_eff = sigI_All_eff_2P*1e-4;
    atomic.allowed.N2P_NAll.energy_avg = EI_All_avg_2P;
    %
    atomic.ionization.N2P_NII.xsec = sigI_Iz_2P*1e-4;
    atomic.ionization.N2P_NII.energy = I1_2P;
    %
    atomic.superelastic.N2P_N4S.xsec = sigI_2P4S*1e-4;
    atomic.superelastic.N2P_N4S.energy = 3.58;
    atomic.superelastic.N2P_N2D.xsec = sigI_2P2D*1e-4;
    atomic.superelastic.N2P_N2D.energy = 1.20;
    %
    atomic.effective.N2P.xsec = (Sig_elm + sigI_Allowed_2P ...
                              +  sigI_2P4S + sigI_2P2D + sigI_Iz_2P)*1e-4;
    
        
    %%%   xsecs for NII (a.k.a N+)
    %
    atomic.forbidden.NII_NIIFor1D.xsec = sigII_For(1,:)*1e-4;
    atomic.forbidden.NII_NIIFor1S.xsec = sigII_For(2,:)*1e-4;
    atomic.forbidden.NII_NIIFor1D.energy = 1.89;
    atomic.forbidden.NII_NIIFor1S.energy = 4.05;
    %
    atomic.forbidden.NII_NIIFor.xsec_tot = sigII_Forbidden*1e-4;
    atomic.forbidden.NII_NIIFor.xsec_eff = sigII_For_eff*1e-4;
    atomic.forbidden.NII_NIIFor.energy_avg = EII_For_avg;
    %
    atomic.allowed.NII_NIIAll.xsec_tot = sigII_Allowed*1e-4;
    atomic.allowed.NII_NIIAll.xsec_eff = sigII_All_eff*1e-4;
    atomic.allowed.NII_NIIAll.energy_avg = EII_All_avg;
    %
    atomic.Rydberg.NII_NIIRyd.xsec_tot = sigII_Rydberg*1e-4;
    atomic.Rydberg.NII_NIIRyd.xsec_eff = sigII_Ryd_eff*1e-4;
    atomic.Rydberg.NII_NIIRyd.energy_avg = EII_Ryd_avg;
    %
    atomic.ionization.NII3P_NIII.xsec = sigII_Iz_3P*1e-4;
    atomic.ionization.NII3P_NIII.energy = I2;
    atomic.ionization.NII1D_NIII.xsec = sigII_Iz_1D*1e-4;
    atomic.ionization.NII1D_NIII.energy = I2-1.89;
    atomic.ionization.NII1S_NIII.xsec = sigII_Iz_1S*1e-4;
    atomic.ionization.NII1S_NIII.energy = I2-4.05;
    
    save('Natomic_xsecs.mat','atomic');
  
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   create xsecs using expression from Eq. 4 in Taylor 1988
%%%   for optically allowed transitions
%%%

function [xsec] = TaylorAllowed(Ej,A,C,f,Z)

    if (Z==1)
        gaunt = A*sqrt(3)/2/pi.*(log(4*C*ET/Ej.*gamma.^2)-beta.^2);
        for i = 1:length(gaunt)
            if(gaunt(i)<=0.2)
               gaunt(i) = 0.2;
            end
        end
    else
        gaunt = A*sqrt(3)/2/pi*(1-Ej./ET).*(log(4*C*ET/Ej.*gamma.^2)-beta.^2);
    end

    xsec  = 8*pi/sqrt(3)*R^2./(ET*Ej)*f*pi*a0^2.*gaunt;
    for i = 1:length(E)
        if(E(i)<=Ej)
            xsec(i) = 0;
        end
    end

end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   create xsecs using expression from Eq. 5 in Taylor 1988
%%%   for optically forbidden transitions
%%%

function [xsec] = TaylorForbidden(Ej,A1,A2)

    for i = 1:length(E)
        if(E(i)<=Ej)
            xsec(i) = 0;
        elseif(E(i)<=40)
            xsec(i)  = A1*4*pi*a0^2*R^2./(ET(i)*Ej)*(1-Ej/ET(i));
        else
            xsec(i)  = A2*4*pi*a0^2*R^2./(ET(i)*Ej)^3*(1-Ej/ET(i));
        end
    end

end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   create xsecs using expression from Eq. 6 in Taylor 1988
%%%   for high-lying Rydberg state transitions
%%%

function [xsec] = TaylorRydberg(Ej,cj,fj,a,c)

    fEt = (1-Ej./ET).^c.*(Ej./ET).^a;
    %
    xsec = cj*fj*4*pi*a0^2*R^2*fEt/Ej^2;
    for i = 1:length(E)
        if(E(i)<=Ej)
            xsec(i) = 0;
        end
    end

end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   create xsecs using expression from Eq. 12 in Taylor 1988
%%%   for other N+ transitions
%%%

function [xsec] = TaylorOther(Ej,Omegaj)

    gi = 9; % stat weight of ground state N+(3P)
    xsec = 1.197e-15/gi./ET*Omegaj;
    for i = 1:length(xsec)
        if(E(i)<=Ej)
            xsec(i) = 0;
        end
    end

end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   create xsecs using expression from Eq. 13 in Taylor 1988
%%%   for ionization
%%%

function [xsec] = TaylorIonization(Ej,A,C)

    for i = 1:length(E)
        if(E(i)<=Ej)
            xsec(i) = 0;
        else
            xsec(i)  = A*4*pi*a0^2*R^2/(ET(i)^2)*(ET(i)/Ej-1) ...
                      *(log(4*C*ET(i)/Ej*gamma(i)^2)-beta(i)^2) ;
        end
    end

end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



end


       