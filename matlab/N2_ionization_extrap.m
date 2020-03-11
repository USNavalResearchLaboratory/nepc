%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   extend cross sections for ionization of N2
%%%   using formulas from Taylor 1988.
%%%
%%%   See Zipf 1980, Taylor 1988, Slinker 1990, and Itikawa 2005
%%%   
%%%
clear all;

writedata = 0;
%%% set some needed constants
%
R = 13.6;       % hydrogen ionization potential [eV]
mc2 = 0.511e6;  % electron rest mass energy [eV]
a0  = 5.29e-9;  % bohr radius [cm]


%%% set stuff
%
IN2 = 15.6;                 % N2 ionization potential
E=10.^[log10(8):0.01:7];    % energy grid [eV]
E=[0 E];
beta = sqrt(1-mc2^2./(mc2+E).^2);
gamma = 1./sqrt(1-beta.^2);
Et = E.*beta.^2/2./(gamma-1); % this is E used in Taylors paper


%%% set xsec from model given in Taylor 1988
%
CN2 = 0.18;  AN2 = 4.25;
Idi = 15.6+9.75;  Cdi = 1;      Adi = 1.31; 
Iddi= 70;         Cddi= 1.2;      Addi= .133; 
Iix = 15.6-6.2;   Cix = 0.19;   Aix = 1.43;
%
sigmaN2 = AN2*4*pi*a0^2*R^2*(Et/IN2-1)./Et.^2.*(log(4*CN2*Et/IN2./(1-beta.^2))-beta.^2);
sigmadi = Adi*4*pi*a0^2*R^2*(Et/Idi-1)./Et.^2.*(log(4*Cdi*Et/Idi./(1-beta.^2))-beta.^2);
sigmaddi= Addi*4*pi*a0^2*R^2*(Et/Iddi-1)./Et.^2.*(log(4*Cddi*Et/Iddi./(1-beta.^2))-beta.^2);
sigmaix = Aix*4*pi*a0^2*R^2*(Et/Iix-1)./Et.^2.*(log(4*Cix*Et/Iix./(1-beta.^2))-beta.^2); % ionization of N2(A3)
%Aix = Aix*2.1635e-16/max(sigmaix);


for i = 1:length(E)
    if(Et(i)<=IN2)
        sigmaN2(i) = 0;
    end
    if(sigmaN2(i)<=0)
        sigmaN2(i) = 0;
    end
    %
    if(Et(i)<=Idi)
        sigmadi(i) = 0;
    end
    if(sigmadi(i)<=0)
        sigmadi(i) = 0;
    end
    %
    if(Et(i)<=Iddi)
        sigmaddi(i) = 0;
    end
    if(sigmadi(i)<=0)
        sigmaddi(i) = 0;
    end
    %
    if(Et(i)<=Iix)
        sigmaix(i) = 0;
    end
    if(sigmaix(i)<=0)
        sigmaix(i) = 0;
    end
end


% %%% set dissociation xsec from itikawa
% %
% Ed = [0 10:2:20 25 30 40 50 60 80 100 125 150 175 200];
% Xd = [0    0    0.01 0.04 0.20 0.36 0.52 0.87 1.04 1.15 ...
%       1.23 1.23 1.20 1.16 1.10 1.04 0.99 0.95]*1e-16;
% 
%   
% %%% set dissociation xsec from ZIPF 1980 ( note that I fudged last few data
% %%% points just a tad to make it smooth)
% %
% Ed1 = [10.5 11 12 13:0.5:16 17:1:20 22:2:30 33:3:45 50:5:60 70:10:100 120:20:200 250:50:400];
% Xd1 = [0.0187 0.0249 0.0492 0.112 0.160 0.243 0.285 0.358 0.400 0.475 0.565 0.682 0.782 0.856 ...
%        1.05   1.20   1.36   1.47  1.58  1.67  1.75  1.82  1.88  1.94  2.03  2.10  2.16  2.24 ...
%        2.27   2.27   2.24   2.16  2.05  1.94  1.86  1.76  1.55  1.39  1.22  1.12]*1e-16;
% 
% 
% Id = 9.75;
% Cd = 1;
% Ad = 1.35;
% sigmad0 = Ad*4*pi*a0^2*R^2*(Et/Id-1)./Et.^2.*(log(4*Cd*Et/Id./(1-beta.^2))-beta.^2);
% %
% f = 3.4; c = 2; a = 0.8;
% sigmad1 = f*4*pi*a0^2*R^2/Id^2*(1-Id./Et).^c.*(Id./Et).^a;
% for i = 1:length(E)
%     if(Et(i)<=Id)
%         sigmad0(i) = 0;
%         sigmad1(i) = 0;
%     end
%     if(sigmad0(i)<=0)
%         sigmad0(i) = 0;
%         sigmad1(i) = 0;
%     end
% end

   
%%% set N2 ionization from itikawa
%
num = 10;
A=importdata('../Boltzmann/xsecs_ionization_itikawa.txt','\t',num);
E0   = A.data(:,1);
Sig0 = A.data(:,2)*1e4;
%
num = num + length(E0) + 12;
A=importdata('../Boltzmann/xsecs_ionization_itikawa.txt','\t',num);
Etot   = A.data(:,1);
Sigtot = A.data(:,2)*1e4;
%
num = num + length(Etot) + 12;
A=importdata('../Boltzmann/xsecs_ionization_itikawa.txt','\t',num);
Edi  = A.data(:,1);
Sigdi = A.data(:,2)*1e4;
%
num = num + length(Edi) + 12;
A=importdata('../Boltzmann/xsecs_ionization_itikawa.txt','\t',num);
Eddi  = A.data(:,1);
Sigddi = A.data(:,2)*1e4;
%
% figure(10); loglog(E0,Sig0,'b',Edi,Sigdi,'r', ...
%                    Eddi,Sigddi,'g',Etot,Sigtot,'black');
% axis([10 1e3 1e-19 1e-15]);
% legend('e+N_2=>2e+N_2^+','e+N_2=>2e+N_2^+',...
%        'e+N_2=>2e+N+N^+','e+N_2=>3e+N+N^+^+','location','best');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%% plot stuff
%
close(figure(1));
figure(1); 
loglog(Etot,Sigtot,'black','linewidth',2);
hold on; plot(E0,Sig0,'g*');                % e + N2 => 2e + N2+
hold on; plot(Edi,Sigdi,'b*');              % e + N2 => 2e + N + N+
hold on; plot(Eddi,Sigddi,'r*');            % e + N2 => 3e + N + N++
legend('tot','e+N_2 => 2e+N_2^+','e+N_2 => 2e+N+N^+','e+N_2 => 3e+N+N^+^+');
hold on; plot(E,sigmaN2,'g','linewidth',2);      % large energy fit
hold on; plot(E,sigmadi,'b','linewidth',2);
%axis([200 3e3 8e-18 1e-16]);
xlabel('electron energy [eV]');
ylabel('\simga [cm^2]');
%
% hold on; plot(Ed, Xd);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%  add things together and write to files
%
[thisE,thisi] = min(abs(E-max(E0)));
thisE = E(thisi);
thisi = thisi+1;
%
E0 = [E0;  E(thisi:length(E))'];
E1 = [Edi; E(thisi:length(E))'];
E2 = [Eddi;E(thisi:length(E))'];
%
Sig0 = [Sig0;   sigmaN2(thisi:length(E))'];
Sig1 = [Sigdi;  sigmadi(thisi:length(E))'];
Sig2 = [Sigddi; sigmaddi(thisi:length(E))'];
%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%% data from J. Bacri and A. Medani, 'Electron Diatomic Molecule 
%%% Weighted Total Cross Section Calculation', Physica 112C (1982).
%%%
%

%%% create electron energy array
%
Eb0 = 4.5:0.5:10;
Eb1 = 10.5:0.5:11.5;
Eb2 = 13.0:1.0:27.0;
Eb3 = 35.0:5.0:55.0;
Eb4 = 70.0:10.0:150.0;
Ebacri = [Eb0';Eb1';Eb2';Eb3';Eb4'];


%%% xsection for ionization of N2(A3)
%
xsec_N2A_N2p = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ...
            0.013, ...
            0.072 + 0.010, ... 
            0.172 + 0.083, ...
            0.509 + 0.841, ...
            0.733 + 1.712 + 0.003, ...
            0.942 + 2.639 + 0.073, ...
            1.134 + 3.544 + 0.293, ...
            1.306 + 4.398 + 0.630, ...
            1.459 + 5.187 + 0.989 + 0.018, ...
            1.594 + 5.908 + 1.349 + 0.111, ...
            1.714 + 6.561 + 1.699 + 0.243, ...
            1.819 + 7.1 + 2.032 + 0.384, ...
            1.910 + 7.7 + 2.345 + 0.528, ...
            1.991 + 8.148 + 2.637 + 0.670, ...
            2.061 + 8.569 + 2.908 + 0.808, ...
            2.122 + 8.944 + 3.158 + 0.940, ...
            2.175 + 9.276 + 3.387 + 1.065, ...
            2.220 + 9.572 + 3.598 + 1.184, ...
            2.410 + 10.964+ 4.735 + 1.892, ...
            2.434 + 11.288+ 5.106 + 2.160, ...
            2.422 + 11.391+ 5.321 + 2.339, ...
            2.389 + 11.357+ 5.434 + 2.455, ...
            2.345 + 11.241+ 5.480 + 2.528, ...
            2.188 + 10.667+ 5.396 + 2.591, ...
            2.081 + 10.225+ 5.255 + 2.566, ...
            1.975 + 9.786 + 5.091 + 2.517, ...
            1.887 + 9.367 + 4.920 + 2.456, ...
            1.801 + 8.974 + 4.750 + 2.390, ...
            1.723 + 8.609 + 4.586 + 2.322, ...
            1.650 + 8.270 + 4.429 + 2.255, ...
            1.584 + 7.956 + 4.281 + 2.190, ...
            1.523 + 7.666 + 4.142 + 2.127];
xsec_N2A_N2p = xsec_N2A_N2p*1e-17; % cm^2


%%%  add things together and write to files
%
[thisE,thisi] = min(abs(E-max(Ebacri)));
thisE = E(thisi);
thisi = thisi+1;
%
E4 = [Ebacri',E(thisi:length(E))];
%
Sigix2 = [xsec_N2A_N2p, sigmaix(thisi:length(E))];


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



close(figure(2));
figure(2); loglog(E0,Sig0,'black');
hold on; loglog(E1,Sig1,'color',[0 0.5 0]);
hold on; loglog(E2,Sig2,'r');
%hold on; plot(Ebacri,xsec_N2A_N2p,'r*'); 
hold on; plot(E4,Sigix2,'b');
%legend('e+N_2->2e+N_2^+','e+N_2->2e+N+N^+','e+N_2(A)->2e+N_2^+');
legend('\sigma_m_i','\sigma_d_i','\sigma_d_d_i','\sigma_m_i_x','location','NE');
xlabel('electron energy [eV]');
ylabel('\sigma [cm^2]');
title('Cross Sections for Ionization of N_2');
axis([10 1e7 5e-21 5e-16]);
set(gca,'xtick',[10 1e2 1e3 1e4 1e5 1e6 1e7]);
set(gca,'ytick',[1e-20 1e-19 1e-18 1e-17 1e-16 1e-15]);

%
% figure(3); loglog(Ed,Xd);
% hold on; plot(Ed1,Xd1,'g');
% hold on; plot(E,sigmad0,'g*');
% hold on; plot(E,sigmad1,'r*');

%%% write to file to be read in COMSOL
%
if(writedata == 1)
    path = '../Boltzmann/xsecs_extrapolated/';
    fileID = fopen([path,'molecularN2_I.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E0'; Sig0'*1e-4]);
    %
    fileID = fopen([path,'molecularN2_di.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E1'; Sig1'*1e-4]);
    %
    fileID = fopen([path,'molecularN2_ddi.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E2'; Sig2'*1e-4]);
    %
    fileID = fopen([path,'molecularN2A_I.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E4; Sigix2*1e-4]);
    %
end
