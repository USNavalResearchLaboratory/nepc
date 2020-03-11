function N2_ionization
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   extend cross sections for ionization of N2
%%%   using formulas from Taylor 1988.
%%%
%%%   See Zipf 1980, Taylor 1988, Slinker 1990, and Itikawa 2005
%%%   
%%%
writedata = 0;
%%% set some needed constants
%
R = 13.6;       % hydrogen ionization potential [eV]
mc2 = 0.511e6;  % electron rest mass energy [eV]
a0  = 5.29e-9;  % bohr radius [cm]


%%% set xsec from model given in Taylor 1988
%
[EN2,sigmaN2]    = TaylorCreate(1e7,15.6,     1,4.1);
[EA,sigmaix]     = TaylorCreate(1e7,15.6-6.2, 1,4.1); % e+N2(A)=>2e+N2+
%
[Edi0,sigmadi]   = TaylorCreate(1e7,14.5+9.75,1,1.8);
[EAd,sigmaAdi]   = TaylorCreate(1e7,14.5+9.75-6.2,1,1.8); % e+N2(A)=>2e+N+N+
%
[Eddi0,sigmaddi]   = TaylorCreate(1e7,70,      1,0.21);
[EAddi0,sigmaAddi] = TaylorCreate(1e7,70-6.2,  1,0.21); % e+N2(A)=>3e+N+N++


   
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

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%% plot itikawa stuff
%
close(figure(11));
figure(11); 
loglog(Etot,Sigtot,'black','linewidth',2);
hold on; plot(E0,Sig0,'g*');                % e + N2 => 2e + N2+
hold on; plot(Edi,Sigdi,'b*');              % e + N2 => 2e + N + N+
hold on; plot(Eddi,Sigddi,'r*');            % e + N2 => 3e + N + N++
legend('tot','e+N_2 => 2e+N_2^+','e+N_2 => 2e+N+N^+','e+N_2 => 3e+N+N^+^+');
%hold on; plot(E,sigmaN2,'g','linewidth',2);      % large energy fit
%hold on; plot(E,sigmadi,'b','linewidth',2);
%axis([200 3e3 8e-18 1e-16]);
xlabel('electron energy [eV]');
ylabel('\simga [cm^2]');
title('ionization from Itikawa 2005');
%
% hold on; plot(Ed, Xd);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
[E0,Sig0] = TaylorExtrap(E0',Sig0',1e7,15.6,1);
[E1,Sig1] = TaylorExtrap(Edi',Sigdi',1e7,14.5+9.75,1);
Sig1 = interp1(E1,Sig1,E0,'pchirp');
E1 = E0;
[E2,Sig2] = TaylorExtrap(Eddi',Sigddi',1e7,29.5+14.5+9.75,1);
Sig2 = interp1(E2,Sig2,E0,'pchirp');
E2 = E0;

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

[EA3,SigiA3] = TaylorExtrap(Ebacri',xsec_N2A_N2p,1e7,15.6-6.2,1);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



close(figure(22));
figure(22); loglog(E0,Sig0,'black');
hold on; loglog(E1,Sig1,'b');
%hold on; loglog(E2,Sig2,'r');
%hold on; plot(Ebacri,xsec_N2A_N2p,'r*'); 
hold on; plot(EA,sigmaix,'black--');
hold on; plot(EAd,sigmaAdi,'b--');
%hold on; plot(EAddi0,sigmaAddi,'ro');
legend('e+N_2(X)->2e+N_2^+','e+N_2(X)->2e+N(S)+N^+','e+N_2(A)->2e+N_2^+','e+N_2(A)->2e+N(S)+N^+');
%legend('\sigma_m_i','\sigma_d_i','\sigma_d_d_i','\sigma_m_i_x','location','NE');
xlabel('electron energy [eV]');
ylabel('\sigma [cm^2]');
title('Cross Sections for Ionization of N_2');
axis([5 1e7 1e-19 1e-15]);
set(gca,'xtick',[10 1e2 1e3 1e4 1e5 1e6 1e7]);
set(gca,'ytick',[1e-19 1e-18 1e-17 1e-16 1e-15]);

%hold on; loglog(Eddi0,sigmaddi,'r*');
hold on; loglog(EA3,SigiA3,'b*');
%hold on; loglog(EN2,sigmaN2,'black*');
%hold on; loglog(Edi0,sigmadi,'g*');

% size(Sig0)
% size(E0)
% figure(10);
% loglog(E0,Sig0)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%              write to file to be read in COMSOL
%%%

if(writedata == 1)
    path = '../Boltzmann/xsecs_extrapolated/';
    fileID = fopen([path,'molecularN2_I.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E0; Sig0*1e-4]);
    %
    fileID = fopen([path,'molecularN2_di.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E1; Sig1*1e-4]);
    %
    fileID = fopen([path,'molecularN2_ddi.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E2; Sig2*1e-4]);
    %
    fileID = fopen([path,'molecularN2A_I.txt'],'w');
    fprintf(fileID,'%e    %e\n',[EA; sigmaix*1e-4]);
    %
    fileID = fopen([path,'molecularN2A_di.txt'],'w');
    fprintf(fileID,'%e    %e\n',[EAd; sigmaAdi*1e-4]);
    %
    fileID = fopen([path,'molecularN2A_ddi.txt'],'w');
    fprintf(fileID,'%e    %e\n',[EAddi0; sigmaAddi*1e-4]);
    %
    N2_ioniz_xsecs.E = E0;
    N2_ioniz_xsecs.sigiz  = Sig0*1e-4; % [m^2]
    N2_ioniz_xsecs.sigdi  = Sig1*1e-4; % [m^2]
    N2_ioniz_xsecs.sigdii = Sig2*1e-4; % [m^2]
    %
    save('N2_ionization_xsecs.mat','N2_ioniz_xsecs');
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   extrapolate xsecs using expression from Eq. 4 in Taylor 1988
%%%

function [E,xsec] = TaylorExtrap(E0,xsec0,Emax,deltaE,C)

    E = 10.^(log10(max(E0)+1):0.02:log10(Emax)); % extrapolated energy grid (eV)
    %mc2 = 0.511e6;         % electron rest mass energy (eV)
    beta = sqrt(1-mc2^2./(mc2+E).^2);
    gamma = 1./sqrt(1-beta.^2);
    Et = E.*beta.^2/2./(gamma-1); % E in Eq. 4 of Taylor 1988
    fEt = (Et/deltaE-1)./Et.^2.*(log(C*Et/deltaE.*gamma.^2)-beta.^2);
    %
    if(min(E0)==0)
        E = [E0 E];                           % total enegy grid
        xsec = [xsec0 xsec0(length(E0))*fEt/fEt(1)]; % total xsec
    else
        E = [0 E0 E];
        xsec = [0 xsec0 xsec0(length(E0))*fEt/fEt(1)]; % total xsec
    end

end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   create xsecs using expression from Eq. 4 in Taylor 1988
%%%

function [E,xsec] = TaylorCreate(Emax,deltaE,C,A)

    E = [0 10.^(log10(max(deltaE)):0.02:log10(Emax))]; % extrapolated energy grid (eV)
    %mc2 = 0.511e6;         % electron rest mass energy (eV)
    beta = sqrt(1-mc2^2./(mc2+E).^2);
    gamma = 1./sqrt(1-beta.^2);
    Et = E.*beta.^2/2./(gamma-1); % E in Eq. 4 of Taylor 1988
    fEt = (Et/deltaE-1)./Et.^2.*(log(C*Et/deltaE.*gamma.^2)-beta.^2);
    %
    xsec = A*4*pi*a0^2*R^2*fEt;
    xsec(1) = 0;
    xsec(2) = 0;

end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


end
