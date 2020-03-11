%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   This script creates the total loss function for Nitrogen.
%%%   For low energies, total xsecs written from write_N2_xsecs.m
%%%   are used. For high energies, Bethe-Born is used
%%%
%%%   see S. Slinker J. Appl. Phys., Vol. 67, No. 2 (1990)
%%%
%%%   NOTE that my calculation does not include energy of secondary
%%%   (last term in Eq. 6 of above reference)
%%%
%%%
%
clear all;
write_data = 0;

%%% load xsecs from files
%
fileget='../Xsecs/';  % path to Xsecs
delimiterIn='\t';
M=dlmread([fileget,'Xsec_rot.txt']);
E_rot = 10.^M(:,1);
X_rot = 10.^M(:,2);
M=dlmread([fileget,'U_rot.txt']);
U_rot = 10.^M(:,2);
M=dlmread([fileget,'Xsec_vib.txt']);
E_vib = 10.^M(:,1);
X_vib = 10.^M(:,2);
M=dlmread([fileget,'U_vib.txt']);
U_vib = 10.^M(:,2);
M=dlmread([fileget,'Xsec_exc.txt']);
E_exc = 10.^M(:,1);
X_exc = 10.^M(:,2);
M=dlmread([fileget,'U_exc.txt']);
U_exc = 10.^M(:,2);
M=dlmread([fileget,'Xsec_dis.txt']);
E_dis = 10.^M(:,1);
X_dis = 10.^M(:,2);
M=dlmread([fileget,'Xsec_ion.txt']);
E_ion = 10.^M(:,1);
X_ion = 10.^M(:,2);


%%% extend the vibrational energy domain on low end to get rotational
%
L_vib = E_vib.*X_vib;
E_vib0 = [E_rot(1:26);E_vib];      
L_vib0 = [zeros(26,1);L_vib];


%%% extend the rotational energy domain on high end to get vibrational
%
L_rot = E_rot.*X_rot;
E_rot0 = [E_rot; E_vib(25:length(E_vib))];      
L_rot0 = [L_rot; ones(length(E_vib)-24,1)*0];


%%% inerpolate to add rotational and vibrational together
%
L_vib0 = interp1(E_vib0,L_vib0,E_rot0);
L1 = L_vib0+L_rot0;
E1 = E_rot0;


%%% add ionization and excitation together
%
L_exc = X_exc.*U_exc;
L_ion = X_ion*20;
E_ion0 = [E_exc(1:9); E_ion];
L_ion0 = [0*E_exc(1:9); L_ion];
L_ion0 = interp1(E_ion0,L_ion0,E_exc);
L2 = L_exc + L_ion0;
E2 = E_exc;


% %%% add L1 and L2 together
% %
E1_0 = [E1; E2(21:length(E2))];
L1_0 = [L1; 0*L2(21:length(L2))];
E2_0 = [E1(1:42); E2];
L2_0 = [0*L1(1:42); L2];
L1_0 = interp1(E1_0,L1_0,E2_0,'cubic');
L = L2_0+L1_0;
E = E2_0;

%%% Energy grid
%
Em    = 0.511*1e6;               % electron rest mass energy [eV]
KEB    = 10.^(3:0.1:7);           % kinetic energy grid [eV]
gamma = KEB/Em+1;                 % relativistic factor
beta  = sqrt(1-(1./gamma).^2);   % v/c


%%% nitrogen params and constants
%
Z  = 7;           % atomic number of Nitrogen
I  = 11.7*Z;      % mean excitation potential
me = 9.1094e-28;  % electron mass [g]
mM2= 1.95E-05;    % me/M_N2
M_N2 = me/mM2;    % mass of N2 [g]
M_N  = 0.5*M_N2;  % mass of N [g]
re = 2.8179e-13;  % classical electron radius [m]


%%% L = dE/dx/N from wikipedia (note expression below is per atom)
%
LB = (log(2*Em*beta.^2./(1-beta.^2)/I)-beta.^2)./beta.^2;
LB = LB*4*pi*Em*Z*re^2;  % [eV*cm^2/atom]


%%% L from http://physics.nist.gov/cgi-bin/Star/e_table.pl
%
M=dlmread('../P_stop.txt');
KEN = 1e6*M(:,1)';
LN  = M_N*M(:,2)'*1e6*1e-4; % [eV*cm^2/atom]

E_tot = [E;KEN'];
L_tot = [L;LN'];


close(figure(2)); figure(2);
loglog(KEB,LB,'black','Linewidth',2);
hold on; loglog(KEN,LN*1e4,'b','Linewidth',2);
hold on; loglog(KES,LS,'r','Linewidth',2);
axis([1e4 1e7 1e-18 1e-14]);
xlabel('Electron Kinetic Energy (eV)','fontsize',14);
ylabel('Loss Function (eV-cm^2/atom)','fontsize',14);
legend('Bethe','NIST','Calculated');
set(gca,'Fontsize',14);
% %%% create total ionization Xsec and Energy
% %
% Etot = [Eiz(2:length(Eiz)); KE(14:length(KE))'];
% Xtot = [Xsec(2:length(Eiz)); L(14:length(KE))'*1e-2];
% 

if(write_data==1)
    dlmwrite('../Xsecs/LossFn.txt',[log10(E_tot),log10(L_tot)], ...
             'delimiter','\t','precision','%.6f');
end     
%
%
%



