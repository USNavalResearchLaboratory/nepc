%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   this script loads the atomic nitrogen cross sections from
%%%   "B-spline R-matrix-with-pseudostates calculations for electron-impact
%%%   excitaiton and ionization of nitrogen" by Yang Wang et al.
%%%   Physical Review A 89, 062714 (2014).
%%%
%%%   SEE read_me file in ../../Xsecs/N_BSR_690 !!!!!!!!!!!!
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
write_total_momentum = 1;
%
plot_ionization = 0;
plot_metastable = 0;
plot_allowed4S = 0;
plot_allowed2D = 0; % note not all are allowed
plot_allowed2P = 0; % note not all are allowed
plot_momentum = 0;
plot_total_momentum = 0;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   load ionization cross sections
%
A = importdata('../../Xsecs/N_BSR_690/ion_001'); % from N(4S)
ES1 = A.data(:,1);        % energy [eV]
QS1 = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/ion_002'); % from N(2D)
ED1 = A.data(:,3);        % energy [eV]
QD1 = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/ion_003'); % from N(2P)
EP1 = A.data(:,3);        % energy [eV]
QP1 = A.data(:,2)*1e-16;  % xsec [cm^2]

if(plot_ionization)
    close(figure(111));
    figure(111); plot(ES1,QS1*1e16,'b*');
    hold on; plot(ED1, QD1*1e16,'r*');
    hold on; plot(EP1, QP1*1e16,'g*');
    xlabel('electron energy [eV]'); 
    ylabel('cross section [1\times 10^-^1^6cm^2]');
    title('Ionization: e+N(*) => 2e+N^+');
    axis([0 150 0 2.5]); 
    set(gca,'XTick',0:20:140);
    set(gca,'YTick',0:0.5:2.5);
    legend('^4S','^2D','^2P','location','SE');
end

%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   load metastable transitions
%
A = importdata('../../Xsecs/N_BSR_690/tr_001_002'); % 4S->2D
ESD = A.data(:,1);        % energy [eV]
QSD = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_001_003'); % 4S->2P
ESP = A.data(:,1);        % energy [eV]
QSP = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_002_003'); % 2D->2P
EDP = A.data(:,1)-2.384;  % energy [eV]
QDP = A.data(:,2)*1e-16;  % xsec [cm^2]

if(plot_metastable==1)
    close(figure(2));
    figure(2); plot(ESD,QSD*1e16);
    hold on; plot(ESP, QSP*1e16,'r');
    hold on; plot(EDP, QDP*1e16,'g');
    xlabel('electron energy [eV]'); 
    ylabel('cross section [1\times 10^-^1^6cm^2]');
    title('Metastable Transitions');
    axis([0 50 0 1]); 
    set(gca,'XTick',0:10:50);
    set(gca,'YTick',0:0.2:1);
    legend('^4S->^2D','^4S->^2P','^2D->^2P','location','NE');
end

%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   load optically allowed from N(4S)
%
A = importdata('../../Xsecs/N_BSR_690/tr_001_004'); % 4S->3s 4P
ES3s4P = A.data(:,1);        % energy [eV]
QS3s4P = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_001_006'); % 4S->2p4 4P
ES2p44P = A.data(:,1);        % energy [eV]
QS2p44P = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_001_018'); % 4S->3d 4P ?
ES3d4P = A.data(:,1);        % energy [eV]
QS3d4P = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_001_008'); % 4S->3p 4D ?
ES3p4D = A.data(:,1);        % energy [eV]
QS3p4D = A.data(:,2)*1e-16;  % xsec [cm^2]


if(plot_allowed4S==1)
    close(figure(3));
    f3=figure(3); set(f3,'position',[10 100 600 600]);
    %
    title('Allowed from N(^4S)');
    subplot(3,2,3);
    plot(ES3s4P,QS3s4P*1e16,'r');
    ylabel('cross section [1\times 10^-^1^6cm^2]');
    title('Allowed Transitions from N(^4S)');
    axis([0 120 0 0.8]); 
    set(gca,'XTick',0:20:120);
    set(gca,'YTick',0:0.2:0.8);
    legend('^4S->3s ^4P','location','best');
    %
    subplot(3,2,4);
    plot(ES2p44P, QS2p44P*1e16,'r');
    title('Allowed Transitions from N(^4S)');
    axis([0 120 0 0.6]); 
    set(gca,'XTick',0:20:120);
    set(gca,'YTick',0:0.2:0.6);
    legend('^4S->2p^4 ^4P','location','best');
    %
    subplot(3,2,5);
    plot(ES3d4P, QS3d4P*1e16,'r');
    axis([0 120 0 0.1]); 
    set(gca,'XTick',0:20:120);
    set(gca,'YTick',0:0.03:0.09);
    legend('^4S->3d ^4P','location','best');
    xlabel('electron energy [eV]'); 
    %
    subplot(3,2,6);
    plot(ES3p4D, QS3p4D*1e16,'r');
    axis([0 120 0 0.06]); 
    set(gca,'XTick',0:20:120);
    set(gca,'YTick',0:0.02:0.06);
    legend('^4S->3p ^4D ?','location','best');
    xlabel('electron energy [eV]'); 
end

%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   load optically allowed from N(2D)
%
U2D = 2.391;
%
A = importdata('../../Xsecs/N_BSR_690/tr_002_006'); % 2D->2p4 4P
ED2p44P = A.data(:,1)-U2D;        % energy [eV]
QD2p44P = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_002_005'); % 2D->3s 2P
ED3s2P = A.data(:,1)-U2D;        % energy [eV]
QD3s2P = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_002_016'); % 2D->3d 2P
ED3d2P = A.data(:,1)-U2D;        % energy [eV]
QD3d2P = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_002_013'); % 2D->3s 2D
ED3s2D = A.data(:,1)-U2D;        % energy [eV]
QD3s2D = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_002_007'); % 2D->3p 2S
ED3p2S = A.data(:,1)-U2D;        % energy [eV]
QD3p2S = A.data(:,2)*1e-16;  % xsec [cm^2]


if(plot_allowed2D==1)
    close(figure(4));
    f4 = figure(4); set(f4,'position',[10 100 600 600]);
    %
    title('Allowed from N(^2D)');
    subplot(3,2,2); plot(ED2p44P, QD2p44P*1e16,'r');
    axis([0 50 0 0.3]); 
    set(gca,'XTick',0:10:50);
    set(gca,'YTick',0:0.05:0.3);
    legend('^2D->2p^4 ^4P','location','best');
    %
    subplot(3,2,3); plot(ED3s2P,QD3s2P*1e16,'r');
    %hold on; plot(ED3d2P, QD3d2P*1e16,'r');
    ylabel('cross section [1\times 10^-^1^6cm^2]');
    title('Allowed from N(^2D)');
    axis([0 120 0 0.15]); 
    set(gca,'XTick',0:20:120);
    set(gca,'YTick',0:0.05:0.15);
    legend('^2D->3s ^2P','location','best');
    %
    subplot(3,2,4); plot(ED3d2P, QD3d2P*1e16,'r');
    axis([0 120 0 0.006]); 
    set(gca,'XTick',0:20:120);
    set(gca,'YTick',0:0.002:0.06);
    legend('^2D->3d ^2P','location','best');
    %
    subplot(3,2,5); plot(ED3s2D, QD3s2D*1e16,'r');
    axis([0 120 0 0.15]); 
    set(gca,'XTick',0:20:120);
    set(gca,'YTick',0:0.05:0.15);
    xlabel('electron energy [eV]'); 
    legend('^2D->3s ^2D','location','best');
    %
    subplot(3,2,6); plot(ED3p2S, QD3p2S*1e16,'r');
    axis([0 120 0 0.01]); 
    set(gca,'XTick',0:20:120);
    set(gca,'YTick',0:0.002:0.01);
    xlabel('electron energy [eV]'); 
    legend('^2D->3p ^2S','location','best');
end

%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   load optically allowed from N(2P) ( see Fig 6 of Wang 2014)
%
U2P = 3.568;
A = importdata('../../Xsecs/N_BSR_690/tr_003_004'); % 2P->3s 4P
EP3s4P = A.data(:,1)-U2P;        % energy [eV]
QP3s4P = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_003_006'); % 2P->2p4 4P
EP2p44P = A.data(:,1)-U2P;        % energy [eV]
QP2p44P = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_003_005'); % 2P->3s 2P
EP3s2P = A.data(:,1)-U2P;        % energy [eV]
QP3s2P = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_003_013'); % 2P->3s 2D
EP3s2D = A.data(:,1)-U2P;        % energy [eV]
QP3s2D = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_003_011'); % 2P->3p 2D
EP3p2D = A.data(:,1)-U2P;        % energy [eV]
QP3p2D = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_003_016'); % 2P->3d 2P
EP3d2P = A.data(:,1)-U2P;        % energy [eV]
QP3d2P = A.data(:,2)*1e-16;  % xsec [cm^2]

if(plot_allowed2P==1)
    close(figure(5));
    f5 = figure(5); set(f5,'position',[10 100 600 600]);
    subplot(3,2,1); plot(EP3s4P,QP3s4P*1e16,'r');
    %xlabel('electron energy [eV]'); 
    %ylabel('cross section [1\times 10^-^1^6cm^2]');
    title('Allowed from N(^2P)');
    axis([0 50 0 0.15]); 
    set(gca,'XTick',0:10:50);
    set(gca,'YTick',0:0.05:0.15);
    legend('^2P->3s ^4P','location','best');
    %
    subplot(3,2,2); plot(EP2p44P, QP2p44P*1e16,'r');
    %xlabel('electron energy [eV]'); 
    %ylabel('cross section [1\times 10^-^1^6cm^2]');
    %title('Allowed from N(^2D)');
    axis([0 50 0 0.3]); 
    set(gca,'XTick',0:10:50);
    set(gca,'YTick',0:0.1:0.3);
    legend('^2P->2p^4 ^4P','location','best');
    %
    subplot(3,2,3); plot(EP3s2P, QP3s2P*1e16,'r');
    %xlabel('electron energy [eV]'); 
    ylabel('cross section [1\times 10^-^1^6cm^2]');
    %title('Allowed from N(^2D)');
    axis([0 120 0 0.3]); 
    set(gca,'XTick',0:20:120);
    set(gca,'YTick',0:0.1:0.3);
    legend('^2P->3s ^2P','location','best');
    %
    subplot(3,2,4); plot(EP3s2D, QP3s2D*1e16,'r');
    axis([0 120 0 0.1]); 
    set(gca,'XTick',0:20:120);
    set(gca,'YTick',0:0.02:0.1);
    legend('^2P->3s ^2D','location','best');
    %
    subplot(3,2,5); plot(EP3p2D, QP3p2D*1e16,'r');
    axis([0 120 0 0.04]); 
    set(gca,'XTick',0:20:120);
    set(gca,'YTick',0:0.01:0.04);
    xlabel('electron energy [eV]'); 
    legend('^2P->3p ^2D','location','best');
    %
    subplot(3,2,6); plot(EP3d2P, QP3d2P*1e16,'r');
    xlabel('electron energy [eV]'); 
    %ylabel('cross section [1\times 10^-^1^6cm^2]');
    %title('Allowed from N(^2D)');
    axis([0 120 0 0.05]); 
    set(gca,'XTick',0:20:120);
    set(gca,'YTick',0:0.01:0.05);
    legend('^2P->3d ^2P','location','best');
end

%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   elastic momentum and total momentum cross sections
%
A = importdata('../../Xsecs/N_BSR_690/mt_001'); % from N(4S)
EelmS = A.data(:,1);        % energy [eV]
QelmS = A.data(:,2)*1e-16;  % xsec [cm^2]
%
EmomS = EelmS;
QexcS = zeros(size(EelmS));
QiznS = zeros(size(EelmS));
for i = 1:length(EmomS)
    if (EmomS(i)<=14.5)
        QiznS(i) = 0;
    else
        QiznS(i) = interp1(ES1,QS1,EmomS(i),'pchirp');
    end
end
for j = 2:27
    if (j<=9)
        A = importdata(['../../Xsecs/N_BSR_690/tr_001_00',num2str(j)]);
    else
        A = importdata(['../../Xsecs/N_BSR_690/tr_001_0',num2str(j)]);
    end
    E = A.data(:,1);
    Q = A.data(:,2);
    for i = 1:length(EmomS)
        if (EmomS(i)<=E(1))
            QexcS(i) = QexcS(i) + 0;
        else
            QexcS(i) = QexcS(i) + interp1(E,Q*1e-16,EmomS(i),'pchirp');
        end
    end

end
QmomS = QelmS + QexcS + QiznS; % total momentum transfer
%
%
%
A = importdata('../../Xsecs/N_BSR_690/mt_002'); % from N(2D)
EelmD = A.data(:,1)-2.391;        % energy [eV]
QelmD = A.data(:,2)*1e-16;  % xsec [cm^2]
%
EmomD = EelmD;
QexcD = zeros(size(EelmD));
QiznD = zeros(size(EelmD));
QdexD = zeros(size(EelmD));
QiznD = interp1(ED1,QD1,EmomD,'pchirp');
EDS = ESD-2.391;
QDS = 4/10*ESD./EDS.*QSD; % ? Qji(E) = gi/gj*(E+Uij)/E*Qij(E+Uij) and Uij=Uj-Ui
QdexD = interp1(EDS,QDS,EmomD,'pchirp');
for i = 1:length(EmomD)
    if (EmomD(i)<=14.5-2.391)
        QiznD(i) = 0;
    end
end
for j = 3:27
    if (j<=9)
        A = importdata(['../../Xsecs/N_BSR_690/tr_002_00',num2str(j)]);
    else
        A = importdata(['../../Xsecs/N_BSR_690/tr_002_0',num2str(j)]);
    end
    E = A.data(:,1)-2.391;
    Q = A.data(:,2);
    for i = 1:length(EmomD)
        if (EmomD(i)<=E(1))
            QexcD(i) = QexcD(i) + 0;
        else
            QexcD(i) = QexcD(i) + interp1(E,Q*1e-16,EmomD(i),'pchirp');
        end
    end

end
QmomD = QelmD + QdexD + QexcD + QiznD; % total momentum transfer
%
%
%
A = importdata('../../Xsecs/N_BSR_690/mt_003'); % from N(2P)
EelmP = A.data(:,1)-3.568;        % energy [eV]
QelmP = A.data(:,2)*1e-16;  % xsec [cm^2]
%
EmomP = EelmP;
QexcP = zeros(size(EelmP));
QiznP = zeros(size(EelmP));
QdexP = zeros(size(EelmP));
QiznP = interp1(EP1,QP1,EmomP,'pchirp');
EPS = ESP-3.568;
QPS = 4/6*ESP./EPS.*QSP;
QdexP = interp1(EPS,QPS,EmomP,'pchirp');
EPD = EDP-(3.568-2.391);
QPD = 10/6*EDP./EPD.*QDP;
QdexP = QdexP + interp1(EPD,QPD,EmomP,'pchirp');
for i = 1:length(EmomP)
    if (EmomP(i)<=14.5-3.568)
        QiznP(i) = 0;
    end
end
for j = 4:27
    if (j<=9)
        A = importdata(['../../Xsecs/N_BSR_690/tr_003_00',num2str(j)]);
    else
        A = importdata(['../../Xsecs/N_BSR_690/tr_003_0',num2str(j)]);
    end
    E = A.data(:,1)-3.568;
    Q = A.data(:,2);
    for i = 1:length(EmomP)
        if (EmomP(i)<=E(1))
            QexcP(i) = QexcP(i) + 0;
        else
            QexcP(i) = QexcP(i) + interp1(E,Q*1e-16,EmomP(i),'pchirp');
        end
    end

end
QmomP = QelmP + QdexP + QexcP + QiznP; % total momentum transfer


A = importdata('../../Xsecs/N_BSR_690/mt_003'); % from N(2P)
EelmP = A.data(:,1)-3.576;        % energy [eV]
QelmP = A.data(:,2)*1e-16;  % xsec [cm^2]

if(plot_momentum)
    close(figure(11));
    f11=figure(11); set(f11,'position',[10 100 600 600]);
    %
    subplot(2,1,1);
    plot(EelmS,QelmS*1e16,'b');
    hold on; plot(EelmD, QelmD*1e16,'r');
    hold on; plot(EelmP, QelmP*1e16,'g');
    xlabel('electron energy [eV]'); 
    ylabel('cross section [1\times 10^-^1^6cm^2]');
    title('elastic momentum exchange');
    axis([0 50 0 15]); 
    set(gca,'XTick',0:10:50);
    set(gca,'YTick',0:3:15);
    legend('^4S','^2D','^2P','location','NE');
    %
    subplot(2,1,2);
    loglog(EelmS,QelmS*1e16,'b');
    xlabel('electron energy [eV]'); 
    ylabel('cross section [1\times 10^-^1^6cm^2]');
    title('elastic momentum exchange with N(^4S)');
    axis([1e-2 1e2 1 1e3]); 
    set(gca,'XTick',[1e-2 1e-1 1e0 1e1 1e2]);
    set(gca,'YTick',[1,10,100,1e3]);
    legend('^4S','location','NE');
end


if(plot_total_momentum)
    close(figure(13));
    f13=figure(13); set(f13,'position',[10 100 600 600]);
    %
    subplot(2,1,1);
    plot(EmomS,QmomS*1e16,'black');
    hold on; plot(EmomS, QelmS*1e16,'r');
    hold on; plot(EmomS, QexcS*1e16,'b');
    hold on; plot(EmomS, QiznS*1e16,'g');
   % hold on; plot(ES1,QS1*1e16,'g*');
    xlabel('electron energy [eV]'); 
    ylabel('cross section [1\times 10^-^1^6cm^2]');
    title('total momentum exchange with N(^4S)');
    axis([0 50 0 15]); 
    set(gca,'XTick',0:10:50);
    set(gca,'YTick',0:3:15);
    legend('tot','elm','exc','izn','location','NE');
    %
    subplot(2,1,2);
    plot(EmomD,QmomD*1e16,'black');
    hold on; plot(EmomD, QelmD*1e16,'r');
    hold on; plot(EmomD, QdexD*1e16,'magenta');
    hold on; plot(EmomD, QexcD*1e16,'b');
    hold on; plot(EmomD, QiznD*1e16,'g');
   % hold on; plot(ES1,QS1*1e16,'g*');
    xlabel('electron energy [eV]'); 
    ylabel('cross section [1\times 10^-^1^6cm^2]');
    title('total momentum exchange with N(^2D)');
    axis([0 50 0 15]); 
    set(gca,'XTick',0:10:50);
    set(gca,'YTick',0:3:15);
    legend('tot','elm','dex','exc','izn','location','NE');
    %
    close(figure(15));
    figure(15);
    plot(EmomP,QmomP*1e16,'black');
    hold on; plot(EmomP, QelmP*1e16,'r');
    hold on; plot(EmomP, QdexP*1e16,'magenta');
    hold on; plot(EmomP, QexcP*1e16,'b');
    hold on; plot(EmomP, QiznP*1e16,'g');
   % hold on; plot(ES1,QS1*1e16,'g*');
    xlabel('electron energy [eV]'); 
    ylabel('cross section [1\times 10^-^1^6cm^2]');
    title('total momentum exchange with N(^2P)');
    axis([0 50 0 15]); 
    set(gca,'XTick',0:10:50);
    set(gca,'YTick',0:3:15);
    legend('tot','elm','dex','exc','izn','location','NE');
end

%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if(write_total_momentum)
    momentum.N4S.E = EmomS; % [eV]
    momentum.N4S.Q = QmomS; % total momentum [cm^2]
    momentum.N4S.Qelm = QelmS;
    momentum.N4S.Qexc = QexcS;
    momentum.N4S.Qizn = QiznS;
    %
    momentum.N2D.E = EmomD; % [eV]
    momentum.N2D.Q = QmomD; % total momentum [cm^2]
    momentum.N2D.Qelm = QelmD;
    momentum.N2D.Qexc = QexcD;
    momentum.N2D.Qizn = QiznD;
    %
    momentum.N2P.E = EmomP; % [eV]
    momentum.N2P.Q = QmomP; % total momentum [cm^2]
    momentum.N2P.Qelm = QelmP;
    momentum.N2P.Qexc = QexcP;
    momentum.N2P.Qizn = QiznP;

    save('momentum.mat','momentum');
end
