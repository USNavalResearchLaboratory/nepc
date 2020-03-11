%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%% This script loads and plots N2 cross sections
%%% versus energy in eV
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


clear all;
%fileget='Electron_N2.txt'; % original Phelps document
fileget='../../air_discharge/xsecs/Electron_N2_modified.txt';  % modified Phelps using data from Itikawa 2004
delimiterIn=' ';
write_data = 1; % 1 for true
savepath = './';
savename = 'N2_xsecs.txt';
format shortEng;


%%% Get effective momentum transfer cross section %%%
%
hlinesIn = 244;
A = importdata(fileget,delimiterIn,hlinesIn);
Energy = A.data(:,2);            % [eV]
Xsec_m_eff = A.data(:,3)*1e-0;   % [m^2]

close(figure(1)); figure(1); set(gcf,'position',[10 300 1000 400]);
subplot(1,2,1); loglog(Energy,Xsec_m_eff,'black','Linewidth',2); 
axis([1e-3 1e3 1e-2 100]);grid;
title('N2 cross sections','fontname','Verdana','fontsize',20);
set(gca,'fontname','Verdana','fontsize',14,'fontweight','B');
set(gca,'xtick',[1e-2,1e-1,1e0,1e1,1e2]);
xlabel('energy [eV]','fontweight','B');
ylabel('\sigma_m [1E-20 m^2]','fontweight','B');


%%% Get rotational cross section %%%
%
for i=1:2
  hlinesIn = hlinesIn+length(A.data(:,1))+6;
  deltaE = dlmread(fileget,'',[hlinesIn-4 0 hlinesIn-4 0]); % energy loss
  A = importdata(fileget,delimiterIn,hlinesIn);
  this_energy = A.data(:,2);
  this_xsec   = A.data(:,3)*1e-0;

  if i==1
    Energy_rot = this_energy;
    Xsec_rot1   = this_xsec;
    U1 = deltaE; % energy loss
  else
    U2 = deltaE; % energy loss
    Xsec_rot2 = interp1(this_energy,this_xsec,Energy_rot,'pchirp');
    Xsec_rot = Xsec_rot1 + Xsec_rot2;
    U_rot = (U1*Xsec_rot1+U2*Xsec_rot2)./(Xsec_rot);
  end
  %hold on;loglog(this_energy,this_xsec,'b','Linewidth',2);
end
hold on; loglog(Energy_rot,Xsec_rot,'b','Linewidth',2);


% for i = 2:length(Xsec_rot)
%     if(Xsec_rot(i)==0) 
%         Xsec_rot(i) = 1e-5*Xsec_rot(i-1);
%     end
% end
log10_E_rot = log10(Energy_rot(2:length(Xsec_rot)-3));
log10_X_rot = log10(1e-20*Xsec_rot(2:length(Xsec_rot)-3));
log10_U_rot = log10(U_rot(2:length(Xsec_rot)-3));


%%% Get vibrational cross sections %%%
%
for i=1:9
  hlinesIn = hlinesIn+length(A.data(:,1))+6;
  deltaE = dlmread(fileget,'',[hlinesIn-4 0 hlinesIn-4 0]); % energy loss
  A = importdata(fileget,delimiterIn,hlinesIn);
  this_energy = A.data(:,2);
  this_xsec   = A.data(:,3)*1e-0;

  if i==1
    Energy_vib = this_energy;
    Xsec_vib   = this_xsec;
    U_vib = deltaE*Xsec_vib;
  else
    this_xsec2 = interp1(this_energy,this_xsec,Energy_vib,'pchirp');
    U_vib = U_vib + deltaE*this_xsec2;  
    Xsec_vib = Xsec_vib + this_xsec2;
  end
  %hold on;
  %loglog(this_energy,this_xsec,'r','Linewidth',2);
end
U_vib = U_vib./(Xsec_vib);
hold on; loglog(Energy_vib,Xsec_vib,'r','Linewidth',2);


log10_E_vib = log10(Energy_vib(2:length(Xsec_vib)-2));
log10_X_vib = log10(1e-20*Xsec_vib(2:length(Xsec_vib)-2));
log10_U_vib = log10(U_vib(2:length(Xsec_vib)-2));


%%% Get excitation cross sections %%%
%
for i=1:13
  hlinesIn = hlinesIn+length(A.data(:,1))+6;
  deltaE = dlmread(fileget,'',[hlinesIn-4 0 hlinesIn-4 0]); % energy loss
  A = importdata(fileget,delimiterIn,hlinesIn);
  this_energy = A.data(:,2);
  this_xsec   = A.data(:,3)*1e-0;

  if i==1
    Energy_exc = this_energy;
    Xsec_exc   = this_xsec;
    U_exc = deltaE*this_xsec;
  else
    this_xsec2 = interp1(this_energy,this_xsec,Energy_exc,'pchirp');
    U_exc = U_exc + deltaE*this_xsec2;  
    Xsec_exc = Xsec_exc + this_xsec2;
  end
%   hold on;
%   if i==13
%     loglog(this_energy,this_xsec,'g:','Linewidth',2); 
%   end
end
U_exc = U_exc./Xsec_exc;
hold on; loglog(Energy_exc,Xsec_exc,'g','Linewidth',2);


log10_E_exc = log10(Energy_exc(3:length(Xsec_exc)));
log10_X_exc = log10(1e-20*Xsec_exc(3:length(Xsec_exc)));
log10_U_exc = log10(U_exc(3:length(Xsec_exc)));


%%% Get ionization cross sections         %%%
%%% includes dissociation ionization also %%%
%
for i=1:5
  hlinesIn = hlinesIn+length(A.data(:,1))+6;
  deltaE = dlmread(fileget,'',[hlinesIn-4 0 hlinesIn-4 0]); % energy loss
  A = importdata(fileget,delimiterIn,hlinesIn);
  this_energy = A.data(:,2);
  this_xsec   = A.data(:,3)*1e-0;

  
  if i==1
    close(figure(2)); figure(2); set(gcf,'position',[10 300 1000 400]);
    subplot(1,2,1);loglog(this_energy,this_xsec,'black*','Linewidth',2);
    axis([10 1000 1e-3 10]); grid;
    title('N2 ionizaton cross sections','fontname','Verdana','fontsize',20);
    set(gca,'fontname','Verdana','fontsize',14,'fontweight','B'); 
    xlabel('energy [eV]','fontweight','B');
    ylabel('\sigma_i_o_n [m^2]','fontweight','B');
  elseif i==2
    hold on;
    loglog(this_energy,this_xsec,'blacko','Linewidth',2);
  elseif i==3
      
      
    log10_E_ion = log10(this_energy(2:length(this_energy)));
    log10_X_ion = log10(1e-20*this_xsec(2:length(this_energy)));
      
      
    figure(1); hold on; loglog(this_energy,this_xsec,'magenta','Linewidth',2);
    hold off; figure(2); hold on;
    loglog(this_energy,this_xsec,'black','Linewidth',2);
  elseif i==4
    hold on;
    loglog(this_energy,this_xsec,'blackx','Linewidth',2);
  else
    hold on;
    loglog(this_energy,this_xsec,'blacks','Linewidth',2);
  end
end
h=legend('e+N2 => 2e+N2+ (X+A Phelps)','e+N2 => 2e+N2+ (B Phelps)', ...
         'e+N2 => 2e+N2+ (X+A+B Itikawa)','e+N2 => 2e+N+N+ (Itikawa)', ...
         'e+N2 => 3e+N+N++ (Itikawa)');
set(h,'position',[0.55 0.8 0.24 0.1]);


%%% Get dissociation cross section                  %%%
%%% e+N2 => e+2N (dissotiation to neutral products) %%%
%
hlinesIn = hlinesIn+length(A.data(:,1))+135
A = importdata(fileget,delimiterIn,hlinesIn);
deltaE = dlmread(fileget,'',[hlinesIn-4 0 hlinesIn-4 0]); % energy loss
this_energy = A.data(:,1);
this_xsec   = A.data(:,2)*1e-0;


log10_E_dis = log10(this_energy(3:length(this_energy)));
log10_X_dis = log10(1e-20*this_xsec(3:length(this_energy)));


figure(1);
hold on;loglog(this_energy,this_xsec,'blackx','Linewidth',2);
h=legend('effective momentum','rotatonal','vibrational','excitation', ...
          'ionization','dissoxsciation');
set(h,'position',[0.55 0.7 0.24 0.1]);


%%% Write Xsecs to txt file to use in as interpolation in COMSOL
%
if (write_data==1)
    %
    dlmwrite('../xsecs/Xsec_rot.txt',[log10_E_rot,log10_X_rot], ...
             'delimiter','\t','precision','%.6f');
    dlmwrite('../xsecs/U_rot.txt',[log10_E_rot,log10_U_rot], ...
             'delimiter','\t','precision','%.6f');
    %
    dlmwrite('../Xsecs/Xsec_vib.txt',[log10_E_vib,log10_X_vib], ...
             'delimiter','\t','precision','%.6f');
    dlmwrite('../Xsecs/U_vib.txt',[log10_E_vib,log10_U_vib], ...
             'delimiter','\t','precision','%.6f');
    %
    dlmwrite('../Xsecs/Xsec_exc.txt',[log10_E_exc,log10_X_exc], ...
             'delimiter','\t','precision','%.6f');
    dlmwrite('../Xsecs/U_exc.txt',[log10_E_exc,log10_U_exc], ...
             'delimiter','\t','precision','%.6f');
    %     
    dlmwrite('../Xsecs/Xsec_ion.txt',[log10_E_ion,log10_X_ion], ...
             'delimiter','\t','precision','%.6f');
    %
    dlmwrite('../Xsecs/Xsec_dis.txt',[log10_E_dis,log10_X_dis], ...
             'delimiter','\t','precision','%.6f');
    %
end


% 
%  
%