%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   This script compares Bethe with NIST with Sean for Loss fn in 
%%%   Nitrogen
%%%
%%%   see S. Slinker J. Appl. Phys., Vol. 67, No. 2 (1990)
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


%%% nitrogen params and constants
%
Z    = 7;           % atomic number of Nitrogen
%I    = 11.7*Z;      % mean excitation potential
I    = 85;
Em   = 0.511*1e6;   % electron rest mass energy [eV]
me   = 9.1094e-28;  % electron mass [g]
mM2  = 1.95E-05;    % me/M_N2
M_N2 = me/mM2;      % mass of N2 [g]
M_N  = 0.5*M_N2;    % mass of N [g]
re   = 2.8179e-13;  % classical electron radius [cm]


%%% Energy grid
%
KEB    = 10.^(3:0.1:9);           % kinetic energy grid [eV]
gamma = KEB/Em+1;                 % relativistic factor
beta  = sqrt(1-(1./gamma).^2);    % v/c


%%% L = dE/dx/N from wikipedia (note expression below is per atom density)
%
LB = (log(2*Em*beta.^2.*gamma.^2/I)-beta.^2)./beta.^2;
LB = LB*4*pi*Em*Z*re^2;  % [eV/cm/(#atom/cm^3)]


%%% L from http://physics.nist.gov/cgi-bin/Star/e_table.pl
%
M=dlmread('../P_stop.txt');
KEN = 1e6*M(:,1)';
LN  = M_N*M(:,2)'*1e6; % [eV*cm^2/atom]


%%% L from Eq. 66, pg 34 of Seans paper
%
KES = 10.^(3:0.1:9);   
LS = 1.78*M_N*(KES/1e6).^(-0.1454+0.08*log(KES/1e6))*1e6; % [eV*cm^2/atom]


close(figure(1)); figure(1);
loglog(KEN,LN,'black','Linewidth',4);
hold on; loglog(KEB,LB,'b','Linewidth',4);
hold on; loglog(KES,LS,'ro','Linewidth',2);
axis([1e3 1e8 1e-17 1e-14]);
title('Nitrogen Loss Function / atom','fontsize',16,'fontweight','b');
xlabel('Electron Kinetic Energy (eV)','fontsize',16,'fontweight','b');
set(gca,'xtick',[1e3,1e4,1e5,1e6,1e7,1e8]);
set(gca,'ytick',[1e-16,1e-15,1e-14]);
ylabel('L (eV-cm^2/atom)','fontsize',16,'fontweight','b');
legend('NIST','Bethe','Fit (1e4eV<E<1e9eV)');
set(gca,'Fontsize',16,'fontweight','n');


%%% plot dE/dx for 1 Torr Nitrogen
%
Ng = 2.6868e19*1/760*273/300/100;  % number of molecules / cc
Na = 2*Ng;                     % number of atoms / cc
close(figure(2)); figure(2);
loglog(KEB,Na*LB,'black');
axis([1e4 2e7 1e0/100 1e2/10]);
title('Bethe-Born Stopping Power in 1 Torr Nitrogen');
xlabel('Electron Kinetic Energy (eV)');
set(gca,'xtick',[1e4,1e5,1e6,1e7]);
set(gca,'ytick',[1/100,10/100,1e2/100]);
ylabel('dE/dx (eV/cm)');


%
%
%



