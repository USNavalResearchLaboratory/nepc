function nitrogen_metastable_xsecs
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    Compute the metastable transition and ionizaton xsecs for N 
%%%    and N+. Use YangWang 2014 for metastable transitions with N
%%%    and use Henry 1969 for metastable transitions with N+.
%%%    Also see Berrington 1975 for N transitions. State-to-state
%%%    ionization from N to N+ computed using Kim 2002. Ionization
%%%    of N+(*) states computed using Lotz and stat weight scaling
%%%    used by Kim
%%%
%%%    N(4S,2D,2P); 
%%%    N+(3P,1D,1S);
%%%
%%%

write_data = 1;
plot_excitation = 1;
plot_ionization = 1;
%
gI  = [4 10 6];              % stat weights of neutral states
gII = [9 5 1];               % stat weights of ionic states
UI  = [0 2.38 3.58];         % energy of neutral states
UII = [14.54 16.43 18.59];   % energy of ionic states
%
Ry   = 13.6;     % hydrogen ionization potential [eV]
a0  = 5.29e-9;  % bohr radius [cm]


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%        metastable transitions
%%%


%%%  N(4S)->N(2D,2P) and N(2D)->N(2P)
%
A = importdata('../../Xsecs/N_BSR_690/tr_001_002'); % 4S->2D
E4S2D = A.data(:,1);        % energy [eV]
Q4S2D = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_001_003'); % 4S->2P
E4S2P = A.data(:,1);        % energy [eV]
Q4S2P = A.data(:,2)*1e-16;  % xsec [cm^2]
%
A = importdata('../../Xsecs/N_BSR_690/tr_002_003'); % 2D->2P
E2D2P = A.data(:,1)-2.384;  % energy [eV]
Q2D2P = A.data(:,2)*1e-16;  % xsec [cm^2]


%%%  N+(3P)->N+(1D,1S) and N+(1D)->N+(1S)
%
E3P = [1:0.1:40 45:5:100 150:50:1e3];
Omega3P1D = 2.98;
Omega3P1S = 0.395;
Omega1D1S = 0.410;
Q3P1D = 1.197e-15/gII(1)./(E3P)*Omega3P1D;
Q3P1S = 1.197e-15/gII(1)./(E3P)*Omega3P1S;
Q1D1S = 1.197e-15/gII(2)./(E3P-1.89)*Omega1D1S;
for l = 1:length(E3P)
    if(E3P(l)<=1.89)
        Q3P1D(l) = 0;
    end
    if(E3P(l)<=4.05)
        Q3P1S(l) = 0;
    end
    if(E3P(l)<=4.05-1.89)
        Q1D1S(l) = 0;
    end
end


if(plot_excitation==1)
    close(figure(1));
    f1=figure(1); set(f1,'position',[0 0 400 800]);
    subplot(2,1,1);
    plot(E4S2D,Q4S2D*1e16);
    hold on; plot(E4S2P, Q4S2P*1e16,'r');
    hold on; plot(E2D2P, Q2D2P*1e16,'g');
    xlabel('electron energy [eV]'); 
    ylabel('cross section [1\times 10^-^1^6cm^2]');
    title('Metastable Transitions with neutral N');
    axis([0 40 0 1]); 
    set(gca,'XTick',0:10:50);
    set(gca,'YTick',0:0.2:1);
    legend('^4S->^2D','^4S->^2P','^2D->^2P','location','NE');
    %
    subplot(2,1,2);
    plot(E3P,Q3P1D*1e16);
    hold on; plot(E3P, Q3P1S*1e16,'r');
    hold on; plot(E3P, Q1D1S*1e16,'g');
    xlabel('electron energy [eV]'); 
    ylabel('cross section [1\times 10^-^1^6cm^2]');
    title('Metastable Transitions with N^+');
    axis([0 20 0 3]); 
    set(gca,'XTick',0:4:20);
    set(gca,'YTick',0:0.5:3);
    legend('^3P->^1D','^3P->^1S','^1D->^1S','location','NE');
end

%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %%%
% %%%    superlastic transitions (g4S = 4, g2D = 10, g2P = 6)
% %%%
% 
% sig2D4S = zeros(1,length(E));
% sig2P4S = zeros(1,length(E));
% sig2P2D = zeros(1,length(E));
% %
% for m = 2:length(E)
%     %
%     Eprime = E(m)+2.38;
%     this_sigI_4S2D = 10.^interp1(log10(1e-40+E),log10(1e-40+sig4S2D), ...
%                                  log10(1e-40+Eprime),'pchip');
%     sig2D4S(m) = 4/10*Eprime/E(m)*this_sigI_4S2D;
%     %
%     Eprime = E(m)+3.58;
%     this_sigI_4S2P = 10.^interp1(log10(1e-40+E),log10(1e-40+sig4S2P), ...
%                                  log10(1e-40+Eprime),'pchip');
%     sig2P4S(m) = 4/6*Eprime/E(m)*this_sigI_4S2P;
%     %
%     Eprime = E(m)+1.20;
%     this_sigI_2D2P = 10.^interp1(log10(1e-40+E),log10(1e-40+sig2D2P), ...
%                                  log10(1e-40+Eprime),'pchip');
%     sig2P2D(m) = 10/6*Eprime/E(m)*this_sigI_2D2P;
% end
% 
% %%%
% %%%
% %%%
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%         cross sections from kim 2002 for neutral ionization
%%%
EKim = [10.9 12:2:20 25:5:50 60:10:100 120:30:180 2e2:50:5e2 6e2:1e2:1e3 ...
        2e3:1e3:5e3]; % [eV]
    
%%% e+N(4S) => 2e+N+
%
QKim4S = [0 0 0 0.0415 0.132 0.235 0.464 0.669 0.843 0.979 1.084 1.166 ...
          1.278 1.343 1.378 1.394 1.396 1.377 1.321 1.255 1.210 1.105 ...
          1.014 0.935 0.868 0.810 0.759 0.675 0.609 0.555 0.510 0.473 ...
          0.278 0.200 0.158 0.131]*1e-16; % [cm^2]

%%% e+N(2D) => 2e+N+
%
QKim2D = [0 0 0.274 0.492 0.684 0.849 1.166 1.406 1.594 1.733 1.834 ...
          1.907 1.995 2.031 2.037 2.025 2.001 1.934 1.817 1.702 ...
          1.630 1.470 1.337 1.226 1.132 1.052 0.983 0.871 0.783 ...
          0.712 0.653 0.604 0.352 0.253 0.199 0.165]*1e-16; % [cm^2]

%%% e+N(2P) => 2e+N+
%
QKim2P = [0 0.123 0.300 0.481 0.661 0.822 1.137 1.370 1.559 1.700 1.804 ...
          1.879 1.971 2.010 2.019 2.008 1.985 1.921 1.806 1.692 ...
          1.620 1.461 1.328 1.218 1.124 1.044 0.976 0.864 0.776 ...
          0.705 0.647 0.599 0.348 0.250 0.197 0.163]*1e-16; % [cm^2]
%
Q4Siz(1,:) = gII(1)/(sum(gII))*( ...
             QBEBLS(EKim,51.034,14.534,1.9975) + QBEBLS(EKim,51.094,15.439,1.0025) ...
           + QBEBLS(EKim,65.656,25.828,2) + QBEBLS(EKim,598.726,425.469,2));
Q4Siz(2,:) = gII(2)/(sum(gII))*( ...
             QBEBLS(EKim,51.034,14.534+1.89,1.9975) + QBEBLS(EKim,51.094,15.439+1.89,1.0025) ...
           + QBEBLS(EKim,65.656,25.828+1.89,2) + QBEBLS(EKim,598.726,425.469+1.89,2));
Q4Siz(3,:) = gII(3)/(sum(gII))*( ...
             QBEBLS(EKim,51.034,14.534+4.05,1.9975) + QBEBLS(EKim,51.094,15.439+4.05,1.0025) ...
           + QBEBLS(EKim,65.656,25.828+4.05,2) + QBEBLS(EKim,598.726,425.469+4.05,2));
%
Q2Diz(1,:) = gII(1)/(sum(gII))*( ...
             QBEBLS(EKim,49.34,12.150,2) + QBEBLS(EKim,50.187,14.314,1) ...
           + QBEBLS(EKim,66.35,26.33,2) + QBEBLS(EKim,598.752,426.483,2));
Q2Diz(2,:) = gII(2)/(sum(gII))*( ...
             QBEBLS(EKim,49.34,12.150+1.89,2) + QBEBLS(EKim,50.187,14.314+1.89,1) ...
           + QBEBLS(EKim,66.35,26.33+1.89,2) + QBEBLS(EKim,598.752,426.483+1.89,2));
Q2Diz(3,:) = gII(3)/(sum(gII))*( ...
             QBEBLS(EKim,49.34,12.150+4.05,2) + QBEBLS(EKim,50.187,14.314+4.05,1) ...
           + QBEBLS(EKim,66.35,26.33+4.05,2) + QBEBLS(EKim,598.752,426.483+4.05,2));
Q2Dauto = QKim2D - sum(Q2Diz);
Q2Diz(1,:) = Q2Diz(1,:) + Q2Dauto; % all auto goes to ground state
%
Q2Piz(1,:) = gII(1)/(sum(gII))*( ...
             QBEBLS(EKim,48.423,10.959,2) + QBEBLS(EKim,50.466,14.348,1) ...
           + QBEBLS(EKim,58.273,27.403,2) + QBEBLS(EKim,607.475,426.78,2));
Q2Piz(2,:) = gII(2)/(sum(gII))*( ...
             QBEBLS(EKim,48.423,10.959+1.89,2) + QBEBLS(EKim,50.466,14.348+1.89,1) ...
           + QBEBLS(EKim,58.273,27.403+1.89,2) + QBEBLS(EKim,607.475,426.78+1.89,2));
Q2Piz(3,:) = gII(3)/(sum(gII))*( ...
             QBEBLS(EKim,48.423,10.959+4.05,2) + QBEBLS(EKim,50.466,14.348+4.05,1) ...
           + QBEBLS(EKim,58.273,27.403+4.05,2) + QBEBLS(EKim,607.475,426.78+4.05,2));
Q2Pauto = QKim2P - sum(Q2Piz);
Q2Piz(1,:) = Q2Piz(1,:) + Q2Pauto; % all auto goes to ground state 


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%              using Lotz for ionization of N+
%%%
ELotz = [29:1:100 110:10:200 250:50:1e4];


%%% Lotz 1968
%
a = [3.9 4.4 3.9 4.4 3.9 4.4]*1e-14; 
b = [0.46 0.4 0.46 0.4 0.46 0.4]; 
c = [0.62 0.6 0.62 0.6 0.62 0.6]; 
q = [2 2 2 2 2 2]; 
P = [29.6 36.7 29.6-1.89 36.7 29.6-4.05 36.7];
%
QLotz = zeros(length(a),length(ELotz));
for k = 1:length(a)
    for j = 1:length(ELotz)
        if(ELotz(j)>=P(k))
            QLotz(k,j) = a(k)*q(k).*log(ELotz(j)/P(k))/(ELotz(j)*P(k)) ...
                      .* (1-b(k)*exp(-c(k)*(ELotz(j)/P(k)-1)));
        end
    end
end
QNIIiz(1,:) = QLotz(1,:) + QLotz(2,:);
QNIIiz(2,:) = QLotz(3,:) + QLotz(4,:);
QNIIiz(3,:) = QLotz(5,:) + QLotz(6,:);

%
%
%

if(plot_ionization==1)
    close(figure(2)); f2=figure(2); set(f2,'position',[500 0 800 800]);
    subplot(2,2,1); plot(EKim,QKim4S*1e16,'black');
    hold on; plot(EKim,Q4Siz*1e16);
    axis([10 1e3 0.0 2.5]);
    xlabel('E [eV]'); ylabel('\sigma [1\times 10^-^1^6cm^2]');
    title('e+N(^4S)->e+N^+(^3P,^1D,^1S)');
    legend('total','^4S->^3P','^4S->^1D','^4S->^1S');
    %
    subplot(2,2,2);
    plot(EKim,QKim2D*1e16,'black');
    hold on; plot(EKim,Q2Diz*1e16);
    axis([10 1e3 0.0 2.5]);
    xlabel('E [eV]'); ylabel('\sigma [1\times 10^-^1^6cm^2]');
    title('e+N(^2D)->e+N^+(^3P,^1D,^1S)');
    legend('total','^2D->^3P','^2D->^1D','^2D->^1S');
    %
    subplot(2,2,3);
    plot(EKim,QKim2P*1e16,'black');
    hold on; plot(EKim,Q2Piz*1e16);
    axis([10 1e3 0.0 2.5]);
    xlabel('E [eV]'); ylabel('\sigma [1\times 10^-^1^6cm^2]');
    title('e+N(^2P)->e+N^+(^3P,^1D,^1S)');
    legend('total','^2P->^3P','^2P->^1D','^2P->^1S');
    %
    subplot(2,2,4);
    plot(ELotz,QNIIiz*1e16);
    axis([10 1e3 0.0 0.8]);
    xlabel('E [eV]'); ylabel('\sigma [1\times 10^-^1^6cm^2]');
    title('e+N+(^3P,^1D,^1S)->e+N^+^+');
    legend('^3P','^1D','^1S');
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if(write_data)
    
    nitrogen_xsecs.E4S2D = E4S2D;  % [eV]
    nitrogen_xsecs.Q4S2D = Q4S2D;  % [cm^2]
    nitrogen_xsecs.U4S2D = UI(2);  % [eV]
    %
    nitrogen_xsecs.E4S2P = E4S2P;  % [eV]
    nitrogen_xsecs.Q4S2P = Q4S2P;  % [cm^2]
    nitrogen_xsecs.U4S2P = UI(3);  % [eV]
    %
    nitrogen_xsecs.E2D2P = E2D2P;  % [eV]
    nitrogen_xsecs.Q2D2P = Q2D2P;  % [cm^2]
    nitrogen_xsecs.U2D2P = UI(3)-UI(2);  % [eV]
    %
    nitrogen_xsecs.E3P1D = E3P;  % [eV]
    nitrogen_xsecs.Q3P1D = Q3P1D;  % [cm^2]
    nitrogen_xsecs.U3P1D = UII(2)-UII(1);  % [eV]
    %
    nitrogen_xsecs.E3P1S = E3P;  % [eV]
    nitrogen_xsecs.Q3P1S = Q3P1S;  % [cm^2]
    nitrogen_xsecs.U3P1S = UII(3)-UII(1);  % [eV]
    %
    nitrogen_xsecs.E1D1S = E3P;  % [eV]
    nitrogen_xsecs.Q1D1S = Q1D1S;  % [cm^2]
    nitrogen_xsecs.U1D1S = UII(3)-UII(2);  % [eV]
    %
    %
    %
    nitrogen_xsecs.E4Siz = EKim;  % [eV]
    nitrogen_xsecs.Q4Siz = Q4Siz;  % [cm^2]
    nitrogen_xsecs.U4Siz = UII;  % [eV]
    %
    nitrogen_xsecs.E2Diz = EKim;  % [eV]
    nitrogen_xsecs.Q2Diz = Q2Diz;  % [cm^2]
    nitrogen_xsecs.U2Diz = UII-UI(2);  % [eV]
    %
    nitrogen_xsecs.E2Piz = EKim;  % [eV]
    nitrogen_xsecs.Q2Piz = Q2Piz;  % [cm^2]
    nitrogen_xsecs.U2Piz = UII-UI(3);  % [eV]
        %
    nitrogen_xsecs.ENIIiz = ELotz;  % [eV]
    nitrogen_xsecs.QNIIiz = QNIIiz;  % [cm^2]
    nitrogen_xsecs.UNIIiz = 29.5 - [0 1.89 4.05];  % [eV]
    
    save('nitrogen_metastable_xsecs.mat','nitrogen_xsecs');
    
end






%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


function [Q] = QBEBLS(E,U,B,N)

    %%%  See Kim 2002 Eq. 1 (Note error in their equation fixed here)
    %
    t = E/B;
    u = U/B;
    Q = zeros(size(t));
    for i = 1:length(E)
        if(t(i)>1)
            Q(i) = 4*pi*a0^2*N*Ry^2/B^2/(t(i)+u+1).*(0.5*log(t(i)).*(1-1./t(i)^2)+1-1/t(i)-log(t(i))/(1+t(i)));
        end
    end
  
end


end
