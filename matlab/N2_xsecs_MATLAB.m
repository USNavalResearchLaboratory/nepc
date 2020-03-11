%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%% This script loads and plots N2 cross sections
%%% versus energy in eV. Also creates files for COMSOL
%%% 0D beam impact reactions
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear all;
filename='Ar_xsecs.txt';
delimiterIn=' ';
write_data = 1; % 1 for true

%%% Get elastic cross section %%%
%%%
hlinesIn = 5;
A = importdata(filename,delimiterIn,hlinesIn);
Energy = A.data(:,1);
Xsec_elast = A.data(:,2);
figure(1);
loglog(Energy,Xsec_elast,'black','Linewidth',2);
title('Argon cross sections','fontname','Verdana','fontsize',20);
set(gca,'fontname','Verdana','fontsize',16);
xlabel('Electron Energy [eV]','fontweight','B');
ylabel('Cross Section [m^2]','fontweight','B');

%%% Get excitation cross section %%%
%%%
hlinesIn = hlinesIn+length(A.data(:,1))+8;
A = importdata(filename,delimiterIn,hlinesIn);
Energy_exc0 = A.data(:,1);
Xsec_exc0 = A.data(:,2);
log_Energy_exc = linspace(log10(Energy_exc0(2)),log10(Energy_exc0(length(Energy_exc0))),20*length(Energy_exc0));
log_Xsec_exc = interp1(log10(Energy_exc0(2:length(Xsec_exc0))),log10(Xsec_exc0(2:length(Xsec_exc0))+1e-30),log_Energy_exc,'PCHIP');
%Xsec_exc = interp1(Energy_exc,Xsec_exc,Energy);
hold on;
loglog(10.^log_Energy_exc,10.^log_Xsec_exc,'r','Linewidth',2);

%%% Get ionization cross section %%%
%%% e+Ar => 2e+Ar+
%%%
hlinesIn2 = hlinesIn+length(A.data(:,1))+8;
A = importdata(filename,delimiterIn,hlinesIn2);
Energy_ion0 = A.data(:,1);
Xsec_ion0 = A.data(:,2);
log_Energy_ion = linspace(log10(Energy_ion0(2)),log10(Energy_ion0(length(Energy_ion0))),20*length(Energy_ion0));
log_Xsec_ion = interp1(log10(Energy_ion0(2:length(Xsec_ion0))),log10(Xsec_ion0(2:length(Xsec_ion0))+1e-30),log_Energy_ion,'PCHIP');
%Xsec_ion = interp1(Energy_ion,Xsec_ion,Energy);
hold on;
loglog(10.^log_Energy_ion,10.^log_Xsec_ion,'blue','Linewidth',2);

%%% plot total cross section for Argon
%%%
% Xsec_tot = Xsec_elast+Xsec_exc+Xsec_ion;
% hold on;
% loglog(Energy,Xsec_tot,'green:','Linewidth',2);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%% load de-excitation data from saved file
%%% e+Ars => e+Ar
%%%
load('Arg_dexc.mat');
hold on; 
%figure(2);
loglog(Energy_dexc,Xsec_dexc,'r--','Linewidth',2);

%%% Get excited ionizaton cross sections %%%
%%% e+Ars => 2e+Ar+
%%%
hlinesIn3 = hlinesIn2+length(A.data(:,1))+9;
A = importdata(filename,delimiterIn,hlinesIn3);
Energy_eion = A.data(:,1);
Xsec_eion = A.data(:,2);
Xsec_eion = interp1(Energy_eion,Xsec_eion,Energy_dexc,'PCHIP');
hold on;
loglog(Energy_dexc,Xsec_eion,'b--','Linewidth',2); 
axis([1e-2 1e3 1e-25 1e-18]);

%%% plot total cross section for excited Argon
%%%
% Xsec_tot = Xsec_dexc+Xsec_eion;
% hold on;
% loglog(Energy_dexc,Xsec_tot,'green:','Linewidth',2);

g=legend([A.textdata{1,1},': ',A.textdata{2,1}], ...
       [A.textdata{hlinesIn-4,1},': ',A.textdata{hlinesIn-3,1}], ...
       [A.textdata{hlinesIn2-4,1},': ',A.textdata{hlinesIn2-3,1}], ...
       'SUPERELASTIC: e+Ars=>e+Ar', ...
       [A.textdata{hlinesIn3-4,1},': ',A.textdata{hlinesIn3-3,1}], ...
       'Location','SouthWest');
   
%%%
%%% Write Xsecs to txt file to use in as interpolation in COMSOL
%
if (write_data==1)
   dlmwrite('../Xsecs/Xsec_elast.txt',[log10(Energy(2:length(Energy))), ...
   log10(Xsec_elast(2:length(Energy)))],'delimiter','\t','precision','%.6f');
   %idlmwrite('../Xsecs/Xsec_ion.txt',[log10(Energy(2:length(Energy))), ...
   %log10(Xsec_ion(2:length(Energy)))],'delimiter','\t','precision','%.6f');
   dlmwrite('../Xsecs/Xsec_ion.txt',[log_Energy_ion',log_Xsec_ion'], ...
            'delimiter','\t','precision','%.6f');
   dlmwrite('../Xsecs/Xsec_exc.txt',[log_Energy_exc',log_Xsec_exc'], ...
            'delimiter','\t','precision','%.6f');
   dlmwrite('../Xsecs/Xsec_eion.txt',[Energy_dexc',Xsec_eion'], ...
            'delimiter','\t','precision',6);
   dlmwrite('../Xsecs/Xsec_dexc.txt',[Energy_dexc',Xsec_dexc'], ...
            'delimiter','\t','precision',6);
end

%dlmwrite('./Beam_Rate_Constants/K_DB.txt',[t',K_DB'],'delimiter','\t','precision',6);
%dlmwrite('./Beam_Rate_Constants/K_EIB.txt',[t',K_EIB'],'delimiter','\t','precision',6);


   