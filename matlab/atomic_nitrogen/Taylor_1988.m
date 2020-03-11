function Taylor_1988
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%          Computes the excitation and ionization
%%%          cross sections for e+N(4S) and e+N+(3P) (ground states)
%%%          for all processes given in Taylor 1988
%%%          "Energy deposition in N and N+ by high--energy electron beams"
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
E = [0 10.^(0:0.02:7)];   % kinetic energy grid (eV)
gamma = E/(mc2)+1;
beta = sqrt(1-1./gamma.^2);
ET = 0.5*mc2*beta.^2;     % 1/2mv^2 (E used in Taylor 1988)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%        optically allowed transitions (TABLE I and Eq 4)
%%%


%%%    with N
%
%stateI_All = ['4P3S', '4P2p4'];
EI_All  = [10.33, 10.92];   % excitation energy [eV]
fI_All  = [0.130, 0.350];   % oscillator strength
sigI_All = zeros(length(EI_All),length(E));
%
for k = 1:length(EI_All)
    sigI_All(k,:) = TaylorAllowed(EI_All(k),1.0,0.3125,fI_All(k),0);
end
%
sigI_Allowed = sum(sigI_All);                 % total cross section
EI_All_avg   = sum(EI_All)/length(EI_All);    % average energy
sigI_All_eff = (EI_All*sigI_All)/EI_All_avg;  % effective cross section


%%%    with N(2D) (2.4eV)
%
EI_All_2D = EI_All - 2.4;
sigI_All_2D = zeros(length(EI_All_2D),length(E));
for k = 1:length(EI_All_2D)
    sigI_All_2D(k,:) = TaylorAllowed(EI_All_2D(k), 1.0, 0.3125, ...
                                     fI_All(k), 0);
end
%
sigI_Allowed_2D = sum(sigI_All_2D);                    % total cross section
EI_All_avg_2D   = sum(EI_All_2D)/length(EI_All_2D);    % average energy
sigI_All_eff_2D = (EI_All_2D*sigI_All_2D)/EI_All_avg_2D;  % effective cross section


%%%    with N(2P) (3.6eV)
%
EI_All_2P = EI_All - 3.6;
sigI_All_2P = zeros(length(EI_All_2P),length(E));
for k = 1:length(EI_All_2P)
    sigI_All_2P(k,:) = TaylorAllowed(EI_All_2P(k), 1.0, 0.3125, ...
                                     fI_All(k), 0);
end
%
sigI_Allowed_2P = sum(sigI_All_2P);                    % total cross section
EI_All_avg_2P   = sum(EI_All_2P)/length(EI_All_2P);    % average energy
sigI_All_eff_2P = (EI_All_2P*sigI_All_2P)/EI_All_avg_2P;  % effective cross section

%figure(7);
%loglog(E,sigI_Allowed,'b',E,sigI_Allowed_2DP,'r');

%%%    with N+
%
%stateII_All = ['3D02p3', '3P02p3', '3P03s', '3S02p3', '3D03d', '3P03d'];
EII_All = [11.42, 13.52, 18.45, 19.21, 23.22, 23.39];
fII_All = [0.170, 0.220, 0.089, 0.230, 0.260, 0.082];
sigII_All = zeros(length(EII_All),length(E));
%
for k = 1:length(EII_All)
    sigII_All(k,:) = TaylorAllowed(EII_All(k),1.0,0.3125,fII_All(k),1);
end
%
sigII_Allowed = sum(sigII_All);                   % total cross section
EII_All_avg   = sum(EII_All)/length(EII_All);     % average energy
sigII_All_eff = (EII_All*sigII_All)/EII_All_avg;  % effective cross section


%%%    plot Allowed state cross sections
%
if(plot_Allowed==1)
    close(figure(1));
    f2=figure(1);
    set(f2,'Position',[1 scrsz(4)/2 scrsz(3)/1.5 scrsz(4)/2.5]);
    %
    subplot(1,2,1);
    loglog(E,sigI_All); title('Allowed with N');
    xlabel('\epsilon [eV]'); ylabel('\sigma [cm^2]');
    %set(gca,'Xtick',[1,1e2,1e4,1e6]);
    %
    subplot(1,2,2);
    loglog(E,sigII_All); title('Allowed with N^+');
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
%%%      forbidden transitions (TABLE II and Eq 5) (and Eq 12)
%%%


%%%    with N
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
figure(9); loglog(E,sigI_For_2D)

%%%    with N+
%
EII_For  = [1.89, 4.04];   % excitation energy [eV]
OmeII_For= [2.98, 0.395];  % collision strength
%
sigII_For = zeros(length(EII_For),length(E));
for k = 1:length(EII_For)
    sigII_For(k,:) = TaylorOther(EII_For(k),OmeII_For(k));
end
%
sigII_Forbidden = sum(sigII_For);                   % total cross section
EII_For_avg     = sum(EII_For)/length(EII_For);     % average energy
sigII_For_eff   = (EII_For*sigII_For)/EII_For_avg;  % effective cross section


%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%                Rydberg-states (TABLE 3 and Eq 6)
%%%


%%%    with N
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


%%%    with N(2D) (2.4eV)
%
EI_Ryd_2D = EI_Ryd - 2.4;
sigI_Ryd_2D = zeros(length(EI_Ryd_2D),length(E));
for k = 1:length(EI_Ryd_2D)
    sigI_Ryd_2D(k,:) = TaylorRydberg(EI_Ryd_2D(k), cjI_Ryd(k), fjI_Ryd(k), ...
                                     aI_Ryd(k), cI_Ryd(k));
end
%
sigI_Rydberg_2D = sum(sigI_Ryd_2D);                     % total cross section for excitation
EI_Ryd_avg_2D   = sum(EI_Ryd_2D)/length(EI_Ryd_2D);    % average energy for energy loss
sigI_Ryd_eff_2D = (EI_Ryd_2D*sigI_Ryd_2D)/EI_Ryd_avg_2D;  % effective cross section for energy loss


%%%    with N(2P) (3.6eV)
%
EI_Ryd_2P = EI_Ryd - 3.6;
sigI_Ryd_2P = zeros(length(EI_Ryd_2P),length(E));
for k = 1:length(EI_Ryd_2P)
    sigI_Ryd_2P(k,:) = TaylorRydberg(EI_Ryd_2P(k), cjI_Ryd(k), fjI_Ryd(k), ...
                                     aI_Ryd(k), cI_Ryd(k));
end
%
sigI_Rydberg_2P = sum(sigI_Ryd_2P);                     % total cross section for excitation
EI_Ryd_avg_2P   = sum(EI_Ryd_2P)/length(EI_Ryd_2P);    % average energy for energy loss
sigI_Ryd_eff_2P = (EI_Ryd_2P*sigI_Ryd_2P)/EI_Ryd_avg_2P;  % effective cross section for energy loss


%figure(7);
%loglog(E,sigI_Rydberg,'b',E,sigI_Rydberg_2DP,'r');


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
sigI_Iz     = TaylorIonization(I1,2.20,0.25);
sigI_Iz_2D = TaylorIonization(I1_2D,2.20,0.25);
sigI_Iz_2P = TaylorIonization(I1_2P,2.20,0.25);
sigII_Iz    = TaylorIonization(I2,2.00,0.39);


% figure(7);
% loglog(E,sigI_Iz,'b',E,sigI_Iz_2DP,'r');

%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%            create total xsecs and inelastic Loss functions
%%%


%%%    with N(4S)
%
LossI_tot = EI_All_avg*sigI_All_eff + EI_For_avg*sigI_For_eff ...
          + EI_Ryd_avg*sigI_Ryd_eff + I1*sigI_Iz;
sigI_tot = sigI_Allowed+sigI_Forbidden+sigI_Rydberg+sigI_Iz;


%%%    with N(2D)
%
LossI_tot_2D = EI_All_avg_2D*sigI_All_eff_2D + (3.57-2.38)*sigI_For_2D ...
          + EI_Ryd_avg_2D*sigI_Ryd_eff_2D + I1_2D*sigI_Iz_2D;
sigI_tot_2D = sigI_Allowed_2D+sigI_For_2D+sigI_Rydberg_2D+sigI_Iz_2D;


%%%    with N+
%
LossII_tot = EII_All_avg*sigII_All_eff + EII_Ryd_avg*sigII_Ryd_eff ...
           + EII_For_avg*sigII_For_eff + I2*sigII_Iz;
sigII_tot  = sigII_Allowed+sigII_Rydberg+sigII_Forbidden+sigII_Iz;


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
A01 = importdata('../Boltzmann/xsecs_nitrogen_atomic.txt','\t',num);
EA = A01.data(:,1);            % energy [eV]
sigma_eff = A01.data(:,2)*1e4; % effective momentum [cm^2]
%num = num + length(A01.data(:,1))+7;

[thisE,thisi1] = min(abs(E-1e4));  % get index for E=1e3
[thisE,thisi2] = min(abs(E-1e5));  % get index for E=1e4
thisE1 = E(thisi1);
thisE2 = E(thisi2);
%

Sig_eff_test = [sigma_eff',1.3*sigI_tot(thisi1),sigI_tot(thisi2)];
E_test       = [EA', thisE1, thisE2]'; % good enough for gov. work

[thisE3,thisi3] = min(abs(E-max(EA)));  % get index for E=40
E_sub = E(thisi3:thisi1);
E_test2 = [EA',E_sub];
Sig_eff_test2 = interp1(log10(1e-20+E_test),log10(1e-20+Sig_eff_test), ...
                        log10(1e-20+E_test2),'pchip');
Sig_eff_test2 = 10.^(Sig_eff_test2);   % Sig_eff on refined grid


%%% now interp sigI_tot to E_test2 grid
%
sigI_test = interp1(log10(1e-20+E),log10(1e-20+sigI_tot), ...
                       log10(1e-20+E_test2),'pchip');
sigI_test = 10.^sigI_test;


%%% subtract to get elastic momentum
%
Sig_eff = Sig_eff_test2;
Sig_elm = Sig_eff_test2 - sigI_test;


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
hold on; plot(E_test2,Sig_eff,'go');
hold on; plot(E_test2,Sig_elm,'r*');
axis([1 1e7 1e-19 1e-15]);
title('Total cross section for N');
xlabel('\epsilon [eV]'); ylabel('\sigma [cm^2]');
set(gca,'Xtick',[1,1e2,1e4,1e6]);
legend('\sigma_t','\sigma_e','\sigma_i');
%
subplot(1,2,2);
loglog(E,sigII_tot,'black','linewidth',1);
hold on; plot(E,sigII_Allowed+sigII_Rydberg+sigII_Forbidden,'r--','linewidth',1);
hold on; plot(E,sigII_Iz,'b--','linewidth',1);
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
hold on; plot(E,LossII_tot - I2*sigII_Iz,'r--','linewidth',1);
hold on; plot(E,I2*sigII_Iz,'b--','linewidth',1);
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
    path = '../Boltzmann/xsecs_atomic_Taylor/';
    %
%     fileID = fopen([path,'NI_elm.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E_test2; max(Sig_elm,0)*1e-4]); % m2 units for xsec
%     

    %%%   xsecs for N(4S)
    %
    atomic.elasticmom.N4S_N4S.xsec = Sig_elm*1e-4;
    atomic.elasticmom.N4S_N4S.mM = 3.92e-5;
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
    atomic.Rydberg.N2D_NRyd.xsec_tot = sigI_Rydberg_2D*1e-4;
    atomic.Rydberg.N2D_NRyd.xsec_eff = sigI_Ryd_eff_2D*1e-4;
    atomic.Rydberg.N2D_NRyd.energy_avg = EI_Ryd_avg_2D;
    %
    atomic.ionization.N2D_NII.xsec = sigI_Iz_2D*1e-4;
    atomic.ionization.N2D_NII.energy = I1_2D;
    
    
    %%%   xsecs for N(2P)
    %
    atomic.allowed.N2P_NAll.xsec_tot = sigI_Allowed_2P*1e-4;
    atomic.allowed.N2P_NAll.xsec_eff = sigI_All_eff_2P*1e-4;
    atomic.allowed.N2P_NAll.energy_avg = EI_All_avg_2P;
    %
    atomic.Rydberg.N2P_NRyd.xsec_tot = sigI_Rydberg_2P*1e-4;
    atomic.Rydberg.N2P_NRyd.xsec_eff = sigI_Ryd_eff_2P*1e-4;
    atomic.Rydberg.N2P_NRyd.energy_avg = EI_Ryd_avg_2P;
    %
    atomic.ionization.N2P_NII.xsec = sigI_Iz_2P*1e-4;
    atomic.ionization.N2P_NII.energy = I1_2P;
    
    
    %%%   xsecs for NII (a.k.a N+)
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
    atomic.ionization.NII_NIII.xsec = sigII_Iz*1e-4;
    atomic.ionization.NII_NIII.energy = I2;
    
    
%     fileID = fopen([path,'NI_2D.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_For(1,:)*1e-4]); % m2 units for xsec
%     fileID = fopen([path,'NI_2P.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_For(2,:)*1e-4]); % m2 units for xsec
%     fileID = fopen([path,'NI_Forbidden_eff_',num2str(EI_For_avg,3),'.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_For_eff*1e-4]); % m2 units for xsec
%     %
%     fileID = fopen([path,'NI_Allowed_.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_Allowed*1e-4]);
%     fileID = fopen([path,'NI_Allowed_eff_',num2str(EI_All_avg,3),'.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_All_eff*1e-4]);
%     %
%     fileID = fopen([path,'NI_Rydberg_.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_Rydberg*1e-4]);
%     fileID = fopen([path,'NI_Rydberg_eff_',num2str(EI_Ryd_avg,3),'.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_Ryd_eff*1e-4]);
%     %
%     fileID = fopen([path,'NI_iz_',num2str(I1,3),'.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_Iz*1e-4]); % m2 units for xsec

    
%     fileID = fopen([path,'NI_2D.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_For(1,:)*1e-4]); % m2 units for xsec
%     fileID = fopen([path,'NI_2P.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_For(2,:)*1e-4]); % m2 units for xsec
%     fileID = fopen([path,'NI_Forbidden_eff_',num2str(EI_For_avg,3),'.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_For_eff*1e-4]); % m2 units for xsec
%     %
    %
    %
    %
%     fileID = fopen([path,'NI_Allowed_2D.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_Allowed_2D*1e-4]);
%     fileID = fopen([path,'NI_Allowed_eff_2D_',num2str(EI_All_avg_2D,3),'.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_All_eff_2D*1e-4]);
%     %
%     fileID = fopen([path,'NI_Rydberg_2D.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_Rydberg_2D*1e-4]);
%     fileID = fopen([path,'NI_Rydberg_eff_2D_',num2str(EI_Ryd_avg_2D,3),'.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_Ryd_eff_2D*1e-4]);
%     %;
%     fileID = fopen([path,'NI_iz_2D_',num2str(I1_2D,3),'.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_Iz_2D*1e-4]); % m2 units for xsecs
    
    %
    %
    %
%     fileID = fopen([path,'NI_Allowed_2P.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_Allowed_2P*1e-4]);
%     fileID = fopen([path,'NI_Allowed_eff_2P_',num2str(EI_All_avg_2P,3),'.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_All_eff_2P*1e-4]);
%     %
%     fileID = fopen([path,'NI_Rydberg_2P.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_Rydberg_2P*1e-4]);
%     fileID = fopen([path,'NI_Rydberg_eff_2P_',num2str(EI_Ryd_avg_2P,3),'.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_Ryd_eff_2P*1e-4]);
%     %;
%     fileID = fopen([path,'NI_iz_2P_',num2str(I1_2P,3),'.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigI_Iz_2P*1e-4]); % m2 units for xsecs
    
    %
    %
    %
    
%     fileID = fopen([path,'NII_Forbidden_.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigII_Forbidden*1e-4]);
%     fileID = fopen([path,'NII_Forbidden_eff_',num2str(EII_For_avg,3),'.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigII_For_eff*1e-4]);
%     %
%     fileID = fopen([path,'NII_Allowed_.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigII_Allowed*1e-4]);
%     fileID = fopen([path,'NII_Allowed_eff_',num2str(EII_All_avg,3),'.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigII_All_eff*1e-4]);
%     %
%     fileID = fopen([path,'NII_Rydberg_.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigII_Rydberg*1e-4]);
%     fileID = fopen([path,'NII_Rydberg_eff_',num2str(EII_Ryd_avg,3),'.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigII_Ryd_eff*1e-4]);
%     %
%     %
%     path = '../Boltzmann/xsecs_extrapolated/';
%     fileID = fopen([path,'NII_iz_',num2str(I2,3),'.txt'],'w');
%     fprintf(fileID,'%e    %e\n',[E; sigII_Iz*1e-4]); % m2 units for xsec
    
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


       