function [E,Qexc,Qelm,Qizn] = BSR_sixninety_xsecs
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   this script loads atomic nitrogen xsecs from
%%%   Wang 2014 and reformats and saves in a .mat file
%%%   to make the data easier to work with
%%%  
%%%   SEE read_me file in ../../Xsecs/N_BSR_690 !!!!!!!!!!!!
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

plot_with4S = 0;
plot_with2D = 0;
plot_with2P = 0;
plot_momentum = 0;

write_data = 1;

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
% momentum = load('momentum.mat');
% momentum = momentum.momentum;
    

%%%   This is the whole shabang for forward excitation
%%%   (k=j) is elastic and not elastic momentum
%
A = importdata('../../Xsecs/N_BSR_690/mt_001');
ESelm = A.data(:,1);              % energy [eV]
QSelm = A.data(:,2)*1e-16;        % xsec [cm^2]
E = [ESelm',137:1:200]';   % energy grid [eV]
% Qmom = zeros(27,length(E));
Qexc = zeros(27,27,length(E));
for i = 1:length(UeV)
    for j = i:length(UeV)
        statei = ['00',num2str(i)];
        statej = ['00',num2str(j)];
        if(i>=10)
            statei = ['0',num2str(i)];
        end
        if(j>=10)
            statej = ['0',num2str(j)];
        end
        A = importdata(['../../Xsecs/N_BSR_690/tr_',statei,'_',statej]);
        thisE = A.data(:,1)-UeV(i);         % energy [eV]
        thisU = UeV(j)-UeV(i);              % transition potential [eV]
        thisQ = A.data(:,2)*1e-16;          % xsec [cm^2]

        
        %%%  deterime if transition is allowed or forbidden
        %
        forbidden = 1;
        S1 = (gS(i)-1)/2; S2 = (gS(j)-1)/2; 
        DS = abs(S2-S1);
        if(DS==0)
            L1 = (gL(i)-1)/2; L2 = (gL(j)-1)/2; 
            DL = abs(L2-L1);
            if(DL==0 || DL==1)
                forbidden = 0; % allowed
            end
        end

        if(forbidden==0)
            Qexc(i,j,:) = InterpAllowed(thisE,thisQ,E,thisU);
        else
            Qexc(i,j,:) = InterpForbidden(thisE,thisQ,E,thisU);
        end
        if(j>i)
            Einv = thisE-thisU;
            Qexinv = g(i)/g(j)*thisE./Einv.*thisQ; % Qji(E) = gi/gj*(E+Uij)/E*Qij(E+Uij)
            Qexc(j,i,:) = max(InterpAllowed(Einv,Qexinv,E,0),0); % state 11 is funny!
        end
       % Qmom(i,:) = Qmom(i,:) + squeeze(Qex(i,j,:))';
        
    end

end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   load elastic momentum and ionization from N(4S,2D,2P)
%%%
Qelm = zeros(3,length(E));
Qizn = zeros(3,length(E));

A = importdata('../../Xsecs/N_BSR_690/mt_001');
ESelm = A.data(:,1);              % energy [eV]
QSelm = A.data(:,2)*1e-16;        % xsec [cm^2]
Qelm(1,:) = InterpAllowed(ESelm,QSelm,E,0);
%figure(2); loglog(ESelm,QSelm,'b',E,Qelm(1,:),'r*');
%
A = importdata('../../Xsecs/N_BSR_690/ion_001');
ES1 = A.data(:,1);                % energy [eV]
US1 = 14.5;                       % potential [eV]
QS1 = A.data(:,2)*1e-16;          % xsec [cm^2]
Qizn(1,:) = InterpAllowed(ES1,QS1,E,US1);
%figure(3); loglog(ES1,QS1,'b',E,Qizn(1,:),'r*');
%
A = importdata('../../Xsecs/N_BSR_690/mt_002');
EDelm = A.data(:,1)-UeV(2);       % energy [eV]
QDelm = A.data(:,2)*1e-16;        % xsec [cm^2]
Qelm(2,:) = InterpAllowed(EDelm,QDelm,E,0);
%figure(2); loglog(EDelm,QDelm,'b',E,Qelm(2,:),'r*');
%
A = importdata('../../Xsecs/N_BSR_690/ion_002');
ED1 = A.data(:,1)-UeV(2);         % energy [eV]
UD1 = 14.5-UeV(2);                % potential [eV]
QD1 = A.data(:,2)*1e-16;          % xsec [cm^2]
Qizn(2,:) = InterpAllowed(ED1,QD1,E,UD1);
%figure(3); loglog(ED1,QD1,'b',E,Qizn(2,:),'r*');
%
A = importdata('../../Xsecs/N_BSR_690/mt_003');
EPelm = A.data(:,1)-UeV(3);       % energy [eV]
QPelm = A.data(:,2)*1e-16;        % xsec [cm^2]
Qelm(3,:) = InterpAllowed(EPelm,QPelm,E,0);
%Qelm(3,:) = 10.^(InterpAllowed(log10(EDelm),log10(QDelm),log10(E),-3));
%figure(2); loglog(EPelm,QPelm,'b',E,Qelm(3,:),'r*');
%
A = importdata('../../Xsecs/N_BSR_690/ion_003');
EP1 = A.data(:,1)-UeV(3);         % energy [eV]
UP1 = 14.5-UeV(3);                % potential [eV]
QP1 = A.data(:,2)*1e-16;          % xsec [cm^2]
Qizn(3,:) = InterpAllowed(EP1,QP1,E,UP1);
%figure(3); loglog(EP1,QP1,'b',E,Qizn(3,:),'r*');

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
    
    YangWang_xsecs.UeV = UeV;
    YangWang_xsecs.gS  = gS;
    YangWang_xsecs.gL  = gL;
    %
    YangWang_xsecs.E = E;
    %
    YangWang_xsecs.Qexc = Qexc;
    YangWang_xsecs.Qelm = Qelm;
    YangWang_xsecs.Qizn = Qizn;
    
    save('YangWang_xsecs.mat','YangWang_xsecs');
    
end
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


end