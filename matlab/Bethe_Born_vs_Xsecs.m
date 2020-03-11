%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%        this script compares the Bethe-Born beam impact rate
%%%        rate constants versus that found using cross sections.
%%%
%
% clear all;


%%% load ionization cross section for low energies
%
hlinesIn = 1104;
fileget='../../air_discharge/xsecs/Electron_N2_modified.txt';  % modified Phelps using data from Itikawa 2004
delimiterIn=' ';
A    = importdata(fileget,delimiterIn,hlinesIn);
Eiz  = A.data(:,2); % energy [eV]
Xsec = A.data(:,3)*1e-20; % ionization Xsec [m^2]


%%% Energy grid
%
Em    = 0.511*1e6;               % electron rest mass energy [eV]
KE    = 10.^(2:0.1:7);           % kinetic energy grid [eV]
gamma = KE/Em+1;                 % relativistic factor
beta  = sqrt(1-(1./gamma).^2);   % v/c


%%% nitrogen params
%
Z     = 7;          % atomic number of Nitrogen
I     = 10*Z;      % 10eV * Z
P     = 760;       % gas pressure [torr]
T     = 300;       % gas temperature [K]
N_los = 2.7e25;    % Loschmidt number [1/m^3]
N     = N_los*P/760*T/273;


%%% electron params
%
re = 2.8179e-15;     % classical electron radius [m]


%%% dE/dx from Voss (WRONG!)
%
% dEdx = log((0.35355*(1+gamma).*beta.*gamma.^2*80^2+ ...
%             1-beta.^2)./beta.^2); % from Voss


%%% dE/dx from wikipedia
%
dEdx = (log(2*Em*beta.^2./(1-beta.^2)/I)-beta.^2)./beta.^2;
dEdx = dEdx*4*pi*Em*N*Z*2*(re)^2;  % [eV/m]


%%% create total ionization Xsec and Energy
%
Etot = [Eiz(2:length(Eiz)); KE(14:length(KE))'];
Xtot = [Xsec(2:length(Eiz)); dEdx(14:length(KE))'/N*1e-2];


%%% plot dEdx
%
close(figure(5));
figure(5); loglog(KE,dEdx/N*1e-2,'r','linewidth',2);
hold on; loglog(Eiz,Xsec,'b','linewidth',2);
hold on; loglog(Etot, Xtot, 'black--','linewidth',2);
axis([1 1e7 1e-23 1e-19]);

