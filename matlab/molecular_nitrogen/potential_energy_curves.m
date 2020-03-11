%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    compute potential energy curves for excited states of N2
%%%    and N2+ using RK method. This is superior to Morse potential
%%%
%%%    Loftus 1977, "The Spectrum of Molecular Nitrogen"
%%%    Laher 1991, "Improved Fits for the Vib. and Rot. Const..."
%%%    Kosarim 2005, "Ionization of excited nitrogen molecules by ..."
%%%    Gilmore 1965, "Potential energy curves for N2, N0, 02, and 
%%%    corresponding ions"
%%%
%%%
clear all;
plot_potentials = 1;
%
hconst = 6.6261e-27;             % planks const [erg-s]
econst = 4.8032e-10;             % electron charge
cvac   = 2.9979e10;              % speed of light [cm/s]
erg_eV = 1.6022e-12;             % ergs associatd with 1eV
erg_invcm = 1.9864e-16;          % ergs associated with 1/cm
invcm_to_eV = erg_invcm/erg_eV;  % eV associated with 1/cm
%
mN = 2.32e-23;       % nitrogen mass [g] 
mur = mN*mN/(mN+mN); % reduced mass of N2 [g]

%%% spectroscopic data for ground state N2(X1Sigma)
%%% See Laher 1991 
%%% NOTE THAT C3Pi STATE ONLY FOR v<5
%
State0  = ['X1Sig'   'A3Sig'   'B3Pi'   'W3Delta' ...
           'B3Sigma' 'a1Sigma' 'a1Pi'   'w1Delta' 'C3Pi' ...
           'X2Sig'   'A2Pi'    'B2Sig'  'C3Sigma']; % last 4 are ions
we0 = [2359      1460      1734      1507 ...
       1517      1530      1694      1560    2047  ...  
       2207      1904      2421      2072]; % [1/cm]
xe0 = [14.32    13.78    14.56    12.58 ...
       12.18    12.08    13.95    12.01  28.45 ...    
       16.30    15.03    23.85    9.29]./we0;
ye0 = [-2.26e-3 -1.18e-2  1.40e-2   3.09e-2 ...
        4.19e-2  4.13e-2  7.94e-3   4.54-2  2.09  ...  
       -2.67e-3  2.03e-3  -0.359   -0.43]./we0;
ze0 = [-2.4e-4   1.41e-4  -1.13e-3  -7.1e-4 ...
       -7.3e-4  -2.9e-4    2.9e-4    0   -5.35e-1  ...
       -2.61e-3  0        -6.19e-2   0]./we0;
ae0 = [0      -7.29e-5   0         0 ...
       0       0         0         0   0 ...      
       3.7e-5  0         0         0]./we0;
T0  = [0       49755   59307   59380 ...
       65851   67739   68951   71698   88978  ...
       125668  134683  151234  190210]; % [1/cm]
%
Be     = [1.998  1.455  1.638  1.470 ...
          1.473  1.480  1.617  1.496 1.825 ... 
          1.932  1.744  2.085  1.511];       % [1/cm]
alphae = [1.73e-2  1.84e-2  1.83e-2  1.70e-2 ...
          1.67e-2  1.66e-2  1.79e-2  1.63e-2  1.87e-2  ...
          1.90e-2  1.84e-2  2.13e-2  1.1e-3]; % [1/cm]
gammae =[-3.3e-5    1.24e-5  -8.4e-6  -1.01e-5 ...
          1.84e-5   2.41e-5  -2.93e-5   0  -2.28e-3  ...
         -1.91e-5  -1.76e-4  -8.5e-4 -8.2e-4];   % [1/cm]
deltae = [0        -6.7e-6   -3.4e-6  3.3e-7 ...
         -4.5e-7    0         0       0   7.33e-4  ...
         -5.00e-6   4.4e-6    0       0];         % [1/cm]
etae   = [0         0         0       0 ...
          0         0         0       0  -1.5e-4 ...
          4.6e-8    0         0       0];         % [1/cm]
%

%%% set vibrational energy spectrum
%
v = 0:1:25;  % vibrational quantum number
for i = 1:length(T0)
Gv = we0(i)*( (v+1/2) - xe0(i)*(v+1/2).^2 + ye0(i)*(v+1/2).^3 ...
   +                    ze0(i)*(v+1/2).^4 + ae0(i)*(v+1/2).^5 );
Te = T0(i)-Gv(1);
Tv = Te + Gv;
%
Bv = Be(i) - alphae(i)*(v+1/2) + gammae(i)*(v+1/2).^2 ...
           + deltae(i)*(v+1/2).^3 + etae(i)*(v+1/2).^4;

%%%  now make fine continuous grid for integrating
%
%
    for j = 1:length(v)
        %thisv = 0;
        dvp = 0.001;
        vp  = -1/2+dvp/2:dvp:v(j)-dvp/2; % for v=0 right now
        Gvp = we0(i)*( (vp+1/2) - xe0(i)*(vp+1/2).^2 + ye0(i)*(vp+1/2).^3 ...
            +                     ze0(i)*(vp+1/2).^4 + ae0(i)*(vp+1/2).^5 );
        Bvp = Be(i) - alphae(i)*(vp+1/2) + gammae(i)*(vp+1/2).^2 ...
            +      deltae(i)*(vp+1/2).^3 + etae(i)*(vp+1/2).^5;  
        f0 = 1/(2*pi*sqrt(2*mur*cvac/hconst))*sum(dvp./sqrt(Gv(j)-Gvp));
        g0 = 2*pi*sqrt(2*mur*cvac/hconst)*sum(dvp*Bvp./sqrt(Gv(j)-Gvp));
        %
        r1(i,j) = sqrt(f0^2+f0/g0)-f0;  % inner turning point [cm]
        r2(i,j) = sqrt(f0^2+f0/g0)+f0;  % outer turning point [cm]
        U(i,j) = Tv(j)*invcm_to_eV;     % energy at turning points [eV]
    end
    
end
% [r1,r1i] = sort(r1);
% for i = 1:length(r1)
%     U1(i) = U(r1i(i));
% end
%   
%   
%  
if(plot_potentials)
close(figure(1)); figure(1); 
subplot(1,2,1);
         plot(r1(1,:)/1e-8,U(1,:),'b');
hold on; plot(r1(2,:)/1e-8,U(2,:),'r');
hold on; plot(r1(3,:)/1e-8,U(3,:),'color', [0 0.5 0]);
hold on; plot(r1(9,1:5)/1e-8,U(9,1:5),'color', 'cyan');
legend('X^1\Sigma','A^3\Sigma','B^3\Pi','C^3\Pi','location','SE');
axis([0.8 2 0 13]); grid on;
xlabel('x [angstoms]'); ylabel('U [eV]');
title('potential curves for N_2');
hold on; plot(r2(1,:)/1e-8,U(1,:),'b');
hold on; plot(r2(2,:)/1e-8,U(2,:),'r');
hold on; plot(r2(3,:)/1e-8,U(3,:),'color', [0 0.5 0]);
hold on; plot(r2(9,1:5)/1e-8,U(9,1:5),'color', 'cyan');
%
%
%  plot curves for ion species
%
subplot(1,2,2); 
         plot(r1(10,:)/1e-8,U(10,:),'b');
hold on; plot(r1(11,:)/1e-8,U(11,:),'r');
hold on; plot(r1(12,1:10)/1e-8,U(12,1:10),'color', [0 0.5 0]);
%hold on; plot(r1(4,1:5)/1e-8,U(4,1:5),'color', 'cyan');
legend('X^2\Sigma','A^2\Pi','B^2\Sigma','location','SE');
axis([0.8 2 0 24]); grid on;
xlabel('x [angstoms]'); ylabel('U [eV]');
title('potential curves for N_2^+');
hold on; plot(r2(10,:)/1e-8,U(10,:),'b');
hold on; plot(r2(11,:)/1e-8,U(11,:),'r');
hold on; plot(r2(12,1:10)/1e-8,U(12,1:10),'color', [0 0.5 0]);
%hold on; plot(r2(4,1:5)/1e-8,U(4,1:5),'color', 'cyan');
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    Compute Jvvp and Jvvpp values from Kosarim 2005
%%%
%%%    Note that values computed here are a little bit different
%%%    from those in Tables 2-5 of Kosarim 2005. 
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%   compute values for e+N2(X1Sigma) -> 2e+N2(X2Sigma,A2Pi,B2Sigma)
%
J1_X1 = zeros(4,17);  % Jvvp from Kosarim 2005
J2_X1 = zeros(4,17);  % Jvvpp from Kosarim 2005
si = 1; % index for initial state
for j = 1:4    % for each final ion state
    for i=1:17 % for each vibrational state of initial state
        [thisr,thisir] = min(abs(r1(9+j,:)-r1(si,i)));
        J1_X1(j,i) = U(9+j,thisir)-U(si,i);
        [thisr,thisir] = min(abs(r2(9+j,:)-r2(si,i)));
        J2_X1(j,i) =  U(9+j,thisir)-U(si,i);
    end
end

%%%   compute values for e+N2(A3Sigma) -> 2e+N2(X2Sigma,A2Pi,B2Sigma)
%
J1_A3 = zeros(4,17);  % Jvvp from Kosarim 2005
J2_A3 = zeros(4,17);  % Jvvpp from Kosarim 2005
si = 2; % index for initial state
for j = 1:4    % for each final ion state
    for i=1:17 % for each vibrational state of initial state
        [thisr,thisir] = min(abs(r1(9+j,:)-r1(si,i)));
        J1_A3(j,i) = U(9+j,thisir)-U(si,i);
        [thisr,thisir] = min(abs(r2(9+j,:)-r2(si,i)));
        J2_A3(j,i) =  U(9+j,thisir)-U(si,i);
    end
end

%%%   compute values for e+N2(B3Sigma) -> 2e+N2(X2Sigma,A2Pi,B2Sigma)
%
J1_B3 = zeros(4,17);  % Jvvp from Kosarim 2005
J2_B3 = zeros(4,17);  % Jvvpp from Kosarim 2005
si = 3; % index for initial state
for j = 1:4    % for each final ion state
    for i=1:17 % for each vibrational state of initial state
        [thisr,thisir] = min(abs(r1(9+j,:)-r1(si,i)));
        J1_B3(j,i) = U(9+j,thisir)-U(si,i);
        [thisr,thisir] = min(abs(r2(9+j,:)-r2(si,i)));
        J2_B3(j,i) =  U(9+j,thisir)-U(si,i);
    end
end

%%%   compute values for e+N2(W3Delta) -> 2e+N2(X2Sigma,A2Pi,B2Sigma)
%
J1_W3 = zeros(4,17);  % Jvvp from Kosarim 2005
J2_W3 = zeros(4,17);  % Jvvpp from Kosarim 2005
si = 4; % index for initial state
for j = 1:4    % for each final ion state
    for i=1:17 % for each vibrational state of initial state
        [thisr,thisir] = min(abs(r1(9+j,:)-r1(si,i)));
        J1_W3(j,i) = U(9+j,thisir)-U(si,i);
        [thisr,thisir] = min(abs(r2(9+j,:)-r2(si,i)));
        J2_W3(j,i) =  U(9+j,thisir)-U(si,i);
    end
end

%%%   compute values for e+N2(B'3Sigma) -> 2e+N2(X2Sigma,A2Pi,B2Sigma)
%
J1_Bp3 = zeros(4,17);  % Jvvp from Kosarim 2005
J2_Bp3 = zeros(4,17);  % Jvvpp from Kosarim 2005
si = 5; % index for initial state
for j = 1:4    % for each final ion state
    for i=1:17 % for each vibrational state of initial state
        [thisr,thisir] = min(abs(r1(9+j,:)-r1(si,i)));
        J1_Bp3(j,i) = U(9+j,thisir)-U(si,i);
        [thisr,thisir] = min(abs(r2(9+j,:)-r2(si,i)));
        J2_Bp3(j,i) =  U(9+j,thisir)-U(si,i);
    end
end

%%%   compute values for e+N2(a'1Sigma) -> 2e+N2(X2Sigma,A2Pi,B2Sigma)
%
J1_ap1 = zeros(4,17);  % Jvvp from Kosarim 2005
J2_ap1 = zeros(4,17);  % Jvvpp from Kosarim 2005
si = 6; % index for initial state
for j = 1:4    % for each final ion state
    for i=1:17 % for each vibrational state of initial state
        [thisr,thisir] = min(abs(r1(9+j,:)-r1(si,i)));
        J1_ap1(j,i) = U(9+j,thisir)-U(si,i);
        [thisr,thisir] = min(abs(r2(9+j,:)-r2(si,i)));
        J2_ap1(j,i) =  U(9+j,thisir)-U(si,i);
    end
end

%%%   compute values for e+N2(a1Pi) -> 2e+N2(X2Sigma,A2Pi,B2Sigma)
%
J1_a1 = zeros(4,17);  % Jvvp from Kosarim 2005
J2_a1 = zeros(4,17);  % Jvvpp from Kosarim 2005
si = 7; % index for initial state
for j = 1:4    % for each final ion state
    for i=1:17 % for each vibrational state of initial state
        [thisr,thisir] = min(abs(r1(9+j,:)-r1(si,i)));
        J1_a1(j,i) = U(9+j,thisir)-U(si,i);
        [thisr,thisir] = min(abs(r2(9+j,:)-r2(si,i)));
        J2_a1(j,i) =  U(9+j,thisir)-U(si,i);
    end
end

%%%   compute values for e+N2(w'1Delta) -> 2e+N2(X2Sigma,A2Pi,B2Sigma)
%
J1_w1 = zeros(4,17);  % Jvvp from Kosarim 2005
J2_w1 = zeros(4,17);  % Jvvpp from Kosarim 2005
si = 8; % index for initial state
for j = 1:4    % for each final ion state
    for i=1:17 % for each vibrational state of initial state
        [thisr,thisir] = min(abs(r1(9+j,:)-r1(si,i)));
        J1_w1(j,i) = U(9+j,thisir)-U(si,i);
        [thisr,thisir] = min(abs(r2(9+j,:)-r2(si,i)));
        J2_w1(j,i) =  U(9+j,thisir)-U(si,i);
    end
end

%%%   compute values for e+N2(C3Pi) -> 2e+N2(X2Sigma,A2Pi,B2Sigma)
%
J1_C3 = zeros(4,17);  % Jvvp from Kosarim 2005
J2_C3 = zeros(4,17);  % Jvvpp from Kosarim 2005
si = 9; % index for initial state
for j = 1:4    % for each final ion state
    for i=1:17 % for each vibrational state of initial state
        [thisr,thisir] = min(abs(r1(9+j,:)-r1(si,i)));
        J1_C3(j,i) = U(9+j,thisir)-U(si,i);
        [thisr,thisir] = min(abs(r2(9+j,:)-r2(si,i)));
        J2_C3(j,i) =  U(9+j,thisir)-U(si,i);
    end
end

%%%  save data to file
%
Jvvp_and_Jvvpp.J1_X1 = J1_X1;
Jvvp_and_Jvvpp.J2_X1 = J2_X1;
%
Jvvp_and_Jvvpp.J1_A3 = J1_A3;
Jvvp_and_Jvvpp.J2_A3 = J2_A3;
%
Jvvp_and_Jvvpp.J1_B3 = J1_B3;
Jvvp_and_Jvvpp.J2_B3 = J2_B3;
%
Jvvp_and_Jvvpp.J1_W3 = J1_W3;
Jvvp_and_Jvvpp.J2_W3 = J2_W3;
%
Jvvp_and_Jvvpp.J1_Bp3 = J1_Bp3;
Jvvp_and_Jvvpp.J2_Bp3 = J2_Bp3;
%
Jvvp_and_Jvvpp.J1_ap1 = J1_ap1;
Jvvp_and_Jvvpp.J2_ap1 = J2_ap1;
%
Jvvp_and_Jvvpp.J1_a1 = J1_a1;
Jvvp_and_Jvvpp.J2_a1 = J2_a1;
%
Jvvp_and_Jvvpp.J1_w1 = J1_w1;
Jvvp_and_Jvvpp.J2_w1 = J2_w1;
%
Jvvp_and_Jvvpp.J1_C3 = J1_C3;
Jvvp_and_Jvvpp.J2_C3 = J2_C3;
%
save('Jvvp_and_Jvvpp.mat','Jvvp_and_Jvvpp');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    Compute ionization cross from Kosarim 2005
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


