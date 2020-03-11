function [Te, kex] = BSR_sixninety_rate_constants
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   this script computes rate constants for atomic nitrogen using the
%%%   cross sections from  "B-spline R-matrix-with-pseudostates 
%%%   calculations for electron-impact excitation and ionization 
%%%   of nitrogen" by Yang Wang et al., Physical Review A 89, 062714 (2014).
%%%
%%%   SEE read_me file in ../../Xsecs/N_BSR_690 !!!!!!!!!!!!
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

plot_with4S = 0;
plot_with2D = 0;
plot_with2P = 0;
plot_momentum = 0;

write_data = 0;

%%% set potential energy of each state (see readme file)
%
UeV = [0 2.391 3.568 10.422 10.774 10.948 11.618 11.785 11.871 12.003 ...
       12.027 12.145 12.373 12.853 12.918 12.963 12.971 12.983 12.986 ...
       13.005 13.021 13.193 13.242 13.268 13.292 13.320 13.348]; % [eV]
gS = [4 2 2 4 2 4 2 4 4 4 2 2 2 4 2 2 4 4 2 4 2 2 4 4 2 4 2]; % 2S+1
S = 1; P = 3; D = 5; F = 7;
gL = [S D P P P P S D P S D P D P P P F P F D D S D P D S P]; % 2L+1
g = gS.*gL; % (2S+1)*(2L+1)
US1 = 14.5; % ionization potential from ground state
%
momentum = load('momentum.mat');
momentum = momentum.momentum;
%
Te = [0.3:0.1:10 11:1:100];
%Te = [1,2,5,10];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   load elastic momentum, excitation, and ionization from N(4S)
%%%
%
EmomS = momentum.N4S.E;
QmomS = momentum.N4S.Q;
%
A = importdata('../../Xsecs/N_BSR_690/mt_001');
ESelm = A.data(:,1);              % energy [eV]
QSelm = A.data(:,2)*1e-16;        % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/ion_001');
ES1 = A.data(:,1);                % energy [eV]
US1 = 14.5;                       % potential [eV]
QS1 = A.data(:,2)*1e-16;          % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_001_002');
ESD = A.data(:,1);                % energy [eV]
USD = UeV(2);                      % potential [eV]
QSD = A.data(:,2)*1e-16;          % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_001_003');
ESP = A.data(:,1);                % energy [eV]
USP = UeV(3);                      % potential [eV]
QSP = A.data(:,2)*1e-16;          % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_001_004');
ES3s4P = A.data(:,1); 
US3s4P = UeV(4);
QS3s4P = A.data(:,2)*1e-16;
%
A = importdata('../../Xsecs/N_BSR_690/tr_001_006');
ES2p44P = A.data(:,1); 
US2p44P = UeV(6);
QS2p44P = A.data(:,2)*1e-16;
%
kex = zeros(27,27,length(Te));
for i = 1:length(Te)
    kmomS(i) = MaxMobility(EmomS,QmomS,Te(i));
    kSD(i) = MaxRateConst(USD,ESD,QSD,Te(i),1);
    kSP(i) = MaxRateConst(USP,ESP,QSP,Te(i),1);
    kS1(i) = MaxRateConst(US1,ES1,QS1,Te(i),0);
    kS3s4P(i) = MaxRateConst(US3s4P,ES3s4P,QS3s4P,Te(i),0);
    kS2p44P(i) = MaxRateConst(US2p44P,ES2p44P,QS2p44P,Te(i),0);
    
    %
    % This is the whole shabang for forward excitation
    % (k=j) is elastic I believe and not elastic momentum
    %
    for j = 1:length(UeV)
        for k = j:length(UeV)
            state1 = ['00',num2str(j)];
            state2 = ['00',num2str(k)];
            if(j>=10)
                state1 = ['0',num2str(j)];
            end
            if(k>=10)
                state2 = ['0',num2str(k)];
            end
            A = importdata(['../../Xsecs/N_BSR_690/tr_',state1,'_',state2]);
            thisE = A.data(:,1)-UeV(j);         % energy [eV]
            thisU = UeV(k)-UeV(j);              % potential [eV]
            thisQ = A.data(:,2)*1e-16;          % xsec [cm^2]
            %
            forbidden = 1;
            S1 = (gS(j)-1)/2; S2 = (gS(k)-1)/2; 
            DS = abs(S2-S1);
            if(DS==0)
                L1 = (gL(j)-1)/2; L2 = (gL(k)-1)/2; 
                DL = abs(L2-L1);
                if(DL==0 || DL==1)
                    forbidden = 0; % allowed
                end
            end
            % j->k
            kex(j,k,i) = MaxRateConst(thisU,thisE,thisQ,Te(i),forbidden);
            gk = gS(k)*gL(k);
            gj = gS(j)*gL(j);
            kex(k,j,i) = gj/gk*kex(j,k,i).*exp(thisU./Te(i)); % k->j
        end
    end
    Te(i)
    %
    %
    %
    
end

if(plot_with4S)
    close(figure(111)); f111 = figure(111);
    set(f111,'position',[179 386 560 800]);
    %
    subplot(2,1,1);
    plot(Te,kSD,'b',Te,kSP,'r',Te,kS1,'g');
    hold on; plot(Te,kS3s4P+kS2p44P,'magenta');
    xlabel('T [eV]'); ylabel('k [cm^3/s]');
    legend('^4S->^2D','^4S->^2P','^4S->+1', ...
           '^4S->3s^4P+2p^4^4P','location','NW');
    axis([0 20 0 2.5e-8]);
    %
    subplot(2,1,2);
    plot(Te,USD*kSD,'b',Te,USP*kSP,'r',Te,US1*kS1,'g');
    hold on; plot(Te,US3s4P*kS3s4P+US2p44P*kS2p44P,'magenta');
    xlabel('T [eV]'); ylabel('kE [eV-cm^3/s]');
    legend('^4S->^2D','^4S->^2P','^4S->+1', ...
           '^4S->3s^4P+2p^4^4P','location','NE');
    axis([0 20 0 10e-8]);
end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   rates with N(2D)
%%%
%
EmomD = momentum.N2D.E;
QmomD = momentum.N2D.Q;
%
A = importdata('../../Xsecs/N_BSR_690/mt_002');
EDelm = A.data(:,1)-UeV(2);       % energy [eV]
QDelm = A.data(:,2)*1e-16;        % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/ion_002');
ED1 = A.data(:,1)-UeV(2);         % energy [eV]
UD1 = 14.5-UeV(2);                % potential [eV]
QD1 = A.data(:,2)*1e-16;          % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_001_002');
EDS = A.data(:,1)-UeV(2);         % energy [eV]
UDS = -UeV(2);                    % potential [eV]
QDS = g(1)/g(2)*ESD./EDS.*QSD;     % xsec
%plot(EDS(2:length(ESD)),QDS(2:length(ESD)))
%
A = importdata('../../Xsecs/N_BSR_690/tr_002_003');
EDP = A.data(:,1)-UeV(2);         % energy [eV]
UDP = UeV(3)-UeV(2);              % potential [eV]
QDP = A.data(:,2)*1e-16;          % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_002_005');
ED3s2P = A.data(:,1)-UeV(2);         % energy [eV]
UD3s2P = UeV(5)-UeV(2);              % potential [eV]
QD3s2P = A.data(:,2)*1e-16;          % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_002_013');
ED3s2D = A.data(:,1)-UeV(2);         % energy [eV]
UD3s2D = UeV(13)-UeV(2);             % potential [eV]
QD3s2D = A.data(:,2)*1e-16;          % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_002_006');
ED2p44P = A.data(:,1)-UeV(2);         % energy [eV]
UD2p44P = UeV(6)-UeV(2);              % potential [eV]
QD2p44P = A.data(:,2)*1e-16;          % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_002_004');
ED3s4P = A.data(:,1)-UeV(2);         % energy [eV]
UD3s4P = UeV(4)-UeV(2);              % potential [eV]
QD3s4P = A.data(:,2)*1e-16;          % xsec [cm^2]
%

for i = 1:length(Te)
    kmomD(i) = MaxMobility(EmomD,QmomD,Te(i));
    kDS(i) = MaxRateConst(0,EDS,QDS,Te(i),1);
    kDP(i) = MaxRateConst(UDP,EDP,QDP,Te(i),1);
    kD1(i) = MaxRateConst(UD1,ED1,QD1,Te(i),0);
    kD3s2P(i) = MaxRateConst(UD3s2P,ED3s2P,QD3s2P,Te(i),0);  
    kD3s2D(i) = MaxRateConst(UD3s2D,ED3s2D,QD3s2D,Te(i),0);
    kD2p44P(i) = MaxRateConst(UD2p44P,ED2p44P,QD2p44P,Te(i),1);
    kD3s4P(i) = MaxRateConst(UD3s4P,ED3s4P,QD3s4P,Te(i),1);
end

if(plot_with2D)
    close(figure(112)); f112 = figure(112);
    set(f112,'position',[179 386 560 800]);
    %
    subplot(2,1,1);
    plot(Te,kDS,'b',Te,kDP,'r',Te,kD1,'g');
%    hold on; plot(Te,g(1)/g(2)*kSD.*exp(USD./Te),'b*');
    hold on; plot(Te,kD3s2P+kD3s2D+kD2p44P,'magenta');
%   hold on; plot(Te,kD3s4P,'blacko');
    xlabel('T [eV]'); ylabel('k [cm^3/s]');
    legend('^2D->^4S','^2D->^2P','^2D->+1', ...
           '^2D->3s^2D+3s^2P+2p^4^4P', ...
           'location','NW');
    axis([0 8 0 2e-8]);
    %
    subplot(2,1,2);
    plot(Te,abs(UDS)*kDS,'b--',Te,UDP*kDP,'r',Te,UD1*kD1,'g');
    hold on; plot(Te,UD3s2P*kD3s2P+UD3s2D*kD3s2D+UD2p44P*kD2p44P,'magenta');
    xlabel('T [eV]'); ylabel('kE [eV-cm^3/s]');
    legend('^2D->^4S','^2D->^2P','^2D->+1', ...
           '^2D->3s^2D+3s^2P+2p^4^4P', ...
           'location','NW');
    axis([0 8 0 5e-8]);
end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   rates with N(2P)
%%%
EmomP = momentum.N2P.E;
QmomP = momentum.N2P.Q;
%
A = importdata('../../Xsecs/N_BSR_690/mt_003');
EPelm = A.data(:,1)-UeV(3);       % energy [eV]
QPelm = A.data(:,2)*1e-16;        % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/ion_003');
EP1 = A.data(:,1)-UeV(3);         % energy [eV]
UP1 = 14.5-UeV(3);                % potential [eV]
QP1 = A.data(:,2)*1e-16;          % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_001_003');
EPS = A.data(:,1)-UeV(3);         % energy [eV]
UPS = -UeV(3);                    % potential [eV]
QPS = g(1)/g(3)*ESP./EPS.*QSP;    % xsec
%plot(EDS(2:length(ESD)),QDS(2:length(ESD)))
%
A = importdata('../../Xsecs/N_BSR_690/tr_002_003');
EPD = A.data(:,1)-UeV(3);         % energy [eV]
UPD = UeV(2)-UeV(3);              % potential [eV]
QPD = g(2)/g(3)*EDP./EPD.*QDP;    % xsec
%
A = importdata('../../Xsecs/N_BSR_690/tr_002_003');
EDP = A.data(:,1)-UeV(2);         % energy [eV]
UDP = UeV(3)-UeV(2);              % potential [eV]
QDP = A.data(:,2)*1e-16;          % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_003_005');
EP3s2P = A.data(:,1)-UeV(3);         % energy [eV]
UP3s2P = UeV(5)-UeV(3);              % potential [eV]
QP3s2P = A.data(:,2)*1e-16;          % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_003_013');
EP3s2D = A.data(:,1)-UeV(3);         % energy [eV]
UP3s2D = UeV(13)-UeV(3);             % potential [eV]
QP3s2D = A.data(:,2)*1e-16;          % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_003_006');
EP2p44P = A.data(:,1)-UeV(3);         % energy [eV]
UP2p44P = UeV(6)-UeV(3);              % potential [eV]
QP2p44P = A.data(:,2)*1e-16;          % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_003_004');
EP3s4P = A.data(:,1)-UeV(3);         % energy [eV]
UP3s4P = UeV(4)-UeV(3);              % potential [eV]
QP3s4P = A.data(:,2)*1e-16;          % xsec [cm^2]
%

for i = 1:length(Te)
    kmomP(i) = MaxMobility(EmomP,QmomP,Te(i));
    kPS(i) = MaxRateConst(0,EPS,QPS,Te(i),1);
    kPD(i) = MaxRateConst(UPD,EPD,QPD,Te(i),1);
    kP1(i) = MaxRateConst(UP1,EP1,QP1,Te(i),0);
    kP3s2P(i) = MaxRateConst(UP3s2P,EP3s2P,QP3s2P,Te(i),0);  
    kP3s2D(i) = MaxRateConst(UP3s2D,EP3s2D,QP3s2D,Te(i),0);
    kP2p44P(i) = MaxRateConst(UP2p44P,EP2p44P,QP2p44P,Te(i),1);
    kP3s4P(i) = MaxRateConst(UP3s4P,EP3s4P,QP3s4P,Te(i),1);
end

if(plot_with2P)
    close(figure(113)); f113 = figure(113);
    set(f113,'position',[179 386 560 800]);
    %
    subplot(2,1,1);
    plot(Te,kPS,'b',Te,kPD,'r',Te,kP1,'g');
   % hold on; plot(Te,g(1)/g(3)*kSP.*exp(USP./Te),'b*');
   % hold on; plot(Te,g(2)/g(3)*kDP.*exp(UDP./Te),'r*');
    hold on; plot(Te,kP3s2P+kP3s2D+kP2p44P+kP3s4P,'magenta');
    xlabel('T [eV]'); ylabel('k [cm^3/s]');
    legend('^2P->^4S','^2P->^2D','^2P->+1', ...
           '^2P->3s^2D+3s^2P+2p^4^4P+3s^4P', ...
           'location','NW');
    axis([0 10 0 3e-8]);
    %
    subplot(2,1,2);
    plot(Te,abs(UPS)*kPS+abs(UPD)*kPD,'b--',Te,UP1*kP1,'g');
    hold on; plot(Te,UP3s2P*kP3s2P+UP3s2D*kP3s2D+UP2p44P*kP2p44P ...
                    +UP3s4P*kP3s4P,'magenta');
    xlabel('T [eV]'); ylabel('kE [eV-cm^3/s]');
    legend('^2P->^4S+^2D','^2P->+1', ...
           '^2P->3s^2D+3s^2P+2p^4^4P+3s^4P', ...
           'location','NW');
    axis([0 10 0 8e-8]);
end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if(plot_momentum)
    close(figure(200)); f200 = figure(200);
  %  set(f200,'position',[179 386 560 800]);
    %
    plot(Te,kmomS,'b',Te,kmomD,'r',Te,kmomP,'g');
    xlabel('T [eV]'); ylabel('k [cm^3/s]');
    legend('^4S','^2D','^2P', ...
           'location','best');
    title('total momentum exchange');
   % axis([0 8 0 2e-8]);
end



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    compute rate constant for Maxwellian EEDF
%%%
%%% 

function [k] = MaxRateConst(U,EQ,Q,Te,forbidden)

    
    E = 0:Te/2e3:20*Te;     % electron kinetic energy [eV]
    FM = 2/sqrt(pi)/Te^(3/2)*exp(-E/Te);  % Maxwellian EEDF
    
    
    %%% check to make sure grid is refined enough using 0th 
    %%% and 2nd moments
    %
    test0 = trapz(E,FM.*E.^(1/2));   % should be one
    error0 = 100*abs(1-test0);
    if(error0>=1)
        warning('0th velocity moment not converged');
    end
    %
    ebar = trapz(E,FM.*E.^(3/2));    % should be 3*Te/2;
    error2 = 100*abs(ebar-3*Te/2)/(3*Te/2);
    if(error2>=1)
        warning('2nd velocity moment not converged');
    end
    
    
    %%% interpolate Q to energy grid and integrate
    %
    if(forbidden)
        Qinterp = InterpForbidden(EQ,Q,E,U);
    else
        Qinterp = InterpAllowed(EQ,Q,E,U);
    end
%     close(figure(2));
%     figure(2); loglog(E,Qinterp,'r*',EQ,Q,'b');
    
    gamma = sqrt(2*1.7588e11); % sqrt(2*e/me)
    k = gamma*trapz(E,E.*Qinterp.*FM)*100; % [cm^3/s]

end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    compute mobility rate constant for Maxwellian EEDF
%%%
%%% 

function [kmom] = MaxMobility(EQ,Q,Te)

    Q = Q*1e-4; % convert from cm^2 to m^2
    E = 0:Te/2e3:20*Te;     % electron kinetic energy [eV]
    FM = 2/sqrt(pi)/Te^(3/2)*exp(-E/Te);  % Maxwellian EEDF
    
    
    %%% check to make sure grid is refined enough using 0th 
    %%% and 2nd moments
    %
    test0 = trapz(E,FM.*E.^(1/2));   % should be one
    error0 = 100*abs(1-test0);
    if(error0>=1)
        warning('0th velocity moment not converged');
    end
    %
    ebar = trapz(E,FM.*E.^(3/2));    % should be 3*Te/2;
    error2 = 100*abs(ebar-3*Te/2)/(3*Te/2);
    if(error2>=1)
        warning('2nd velocity moment not converged');
    end
    
    %%% interpolate Q to energy grid and integrate
    %
    Qinterp = InterpAllowed(EQ,Q,E,-1);
    close(figure(2));
    %figure(2); plot(E,E./Qinterp,'r*',EQ,EQ./Q,'b');
    %figure(2); hold on; plot(E,E./Qinterp.*FM);
    %y = sum(1./Qinterp)
    %min(Qinterp)
    
    gamma = sqrt(2*1.7588e11); % sqrt(2*e/me)
    mueN = gamma/3/Te*trapz(E,E./Qinterp.*FM); % [m^3/s]

    
    %
    econst  = 1.6022e-19;
    meconst = 9.1094e-31;
    kmom = econst/meconst/mueN*1e6; % [cm^3/s]
end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    Interp allowed xsecs (~ln(E)/E at high energy)
%%%

function [Q1] = InterpAllowed(E0,Q0,E1,U)

    Emax = E0(length(E0));
    Qmax = Q0(length(Q0));
    Q1 = interp1(E0,Q0,E1,'pchirp');
    for Ei = 1:length(E1)
        if(E1(Ei)<=U)
            Q1(Ei) = 0;
        end
        if(E1(Ei)>Emax)
            Q1(Ei) = Qmax*log(E1(Ei))./E1(Ei) ...
                   / (log(Emax)/Emax);
        end
    end
    
end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    Interp forbidden xsecs (~1/E^3 at high energy)
%%%

function [Q1] = InterpForbidden(E0,Q0,E1,U)

    Emax = E0(length(E0));
    Qmax = Q0(length(Q0));
    Q1 = interp1(E0,Q0,E1,'pchirp');
    for Ei = 1:length(E1)
        if(E1(Ei)<=U)
            Q1(Ei) = 0;
        end
        if(E1(Ei)>Emax)
            Q1(Ei) = Qmax*(Emax./E1(Ei))^3;
        end
    end
    
end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%                     write date to file
%%%

if(write_data)
    
    YangWang.Te = Te;
    %
    YangWang.kmomS   = kmomS;
    YangWang.kSD     = kSD;
    YangWang.kSP     = kSP;
    YangWang.kS1     = kS1;
    YangWang.kS3s4P  = kS3s4P;
    YangWang.kS2p44P = kS2p44P;
    %
    YangWang.kmomD   = kmomD;
    YangWang.kDS     = kDS;
    YangWang.kDP     = kDP;
    YangWang.kD1     = kD1;
    YangWang.kD3s4P  = kD3s4P;
    YangWang.kD3s2P  = kD3s2P;
    YangWang.kD2p44P = kD2p44P;
    YangWang.kD3s2D  = kD3s2D;
    %
    YangWang.kmomP   = kmomP;
    YangWang.kPS     = kPS;
    YangWang.kPD     = kPD;
    YangWang.kP1     = kP1;
    YangWang.kP3s4P  = kP3s4P;
    YangWang.kP3s2P  = kP3s2P;
    YangWang.kP2p44P = kP2p44P;
    YangWang.kP3s2D  = kP3s2D;
    %
    YangWang.kex = kex;
    YangWang.UeV = UeV;
    YangWang.gS = gS;
    YangWang.gL = gL;
    
    save('YangWang.mat','YangWang');
    
end
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


end