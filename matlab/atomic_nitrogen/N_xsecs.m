function N_xsecs
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%      Compute the metastable transition xsecs for N and N+ using
%%%      YangWang 2014 (for N) and Henry 1969 (for N+). Also see
%%%      Berrington 1975 for N transitions
%%%      N(4S,2D,2P); N+(3P,1D,1S)
%%%      UN = 0,2.38,3.58; UN+ = 14.5+ [0,1.98,4.05]
%%%      gN = 4,10,6;      gN+ = 9,5,1
%%%
%%%      Also compute ionization xsecs for e+N(*)=>2e+N+(*)
%%%      using Kim 2002
%%%

writedata = 0;
plot_Forbidden = 0;
plot_Allowed = 0;
plot_Ionization = 1;

%%%    set some needed constants
%
Ry   = 13.6;     % hydrogen ionization potential [eV]
mc2 = 0.511e6;  % electron rest mass energy [eV]
a0  = 5.29e-9;  % bohr radius [cm]
%
E = [0 0.01:0.01:1.5 10.^(0.2:0.02:3)];   % kinetic energy grid (eV)
gamma = E/(mc2)+1;
beta = sqrt(1-1./gamma.^2);
ET = 0.5*mc2*beta.^2;     % 1/2mv^2 (E used in Taylor 1988)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%      forbidden transitions uses formula from Taylor 1988
%%%      See Berrington 1975 to compare
%%%

%%%    4S-2D, 4S-2P, and 2D-2P
%
sig4S2D = TaylorForbidden(2.38,0.025,227.72);
sig4S2P = TaylorForbidden(3.57,0.0175,356.04);
sig2D2P = TaylorForbidden(3,0.03,440); % THIS IS NOT FORBIDDEN!!!!!

%%%    N+(3P)->N+(1D), N+(3P)->N+(1S), N+(1D)->N+(1S) (See Henry 1969)
%
g1 = [9 5 1]; % stat weights of ion states
dU1 = [1.98 4.05 2.07];
Omega3P1D = 2.98;
Omega3P1S = 0.395;
Omega1D1S = 0.410;
sig3P1D = 1.197e-15/g1(1)./(ET)*Omega3P1D;
sig3P1S = 1.197e-15/g1(1)./(ET)*Omega3P1S;
sig1D1S = 1.197e-15/g1(2)./(ET-1.98)*Omega1D1S;
for l = 1:length(ET)
    if(ET(l)<=dU1(1))
        sig3P1D(l) = 0;
    end
    if(ET(l)<=dU1(2))
        sig3P1S(l) = 0;
    end
    if(ET(l)<=dU1(3))
        sig1D1S(l) = 0;
    end
end

if(plot_Forbidden==1)
    close(figure(1));
    figure(1); plot(E,sig4S2D*1e16,'black');
    hold on; plot(E,sig4S2P*1e16,'b');
    hold on; plot(E-1.8,sig2D2P*1e16,'r');
    xlabel('E [eV]'); ylabel('\sigma [1\times 10^-^1^6cm^2]');
    title('Forbidden Cross Sections');
    legend('^4S-^2D','^4S-^2P','^2D-^2P');
    set(gca,'XTick',0:10:50);
    axis([0 50 0 1]);
%     figure(1); plot(E/13.6,sig4S2D/(pi*a0^2),'black');
%     hold on; plot(E/13.6,sig4S2P/(pi*a0^2),'b');
%     hold on; plot(E/13.6,sig2D2P/(pi*a0^2),'r');
%     xlabel('E [13.6 eV]'); ylabel('\sigma/(\pi a_0^2)');
%     title('Forbidden Cross Sections (See Berrington 1975)');
%     legend('4S-2D)','4S-2P','2D-2P');
%     set(gca,'XTick',[0 0.5 1 1.5 2 2.5]);
%     axis([0 2.5 0 1]);
end


%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    superlastic transitions (g4S = 4, g2D = 10, g2P = 6)
%%%

sig2D4S = zeros(1,length(E));
sig2P4S = zeros(1,length(E));
sig2P2D = zeros(1,length(E));
%
for m = 2:length(E)
    %
    Eprime = E(m)+2.38;
    this_sigI_4S2D = 10.^interp1(log10(1e-40+E),log10(1e-40+sig4S2D), ...
                                 log10(1e-40+Eprime),'pchip');
    sig2D4S(m) = 4/10*Eprime/E(m)*this_sigI_4S2D;
    %
    Eprime = E(m)+3.58;
    this_sigI_4S2P = 10.^interp1(log10(1e-40+E),log10(1e-40+sig4S2P), ...
                                 log10(1e-40+Eprime),'pchip');
    sig2P4S(m) = 4/6*Eprime/E(m)*this_sigI_4S2P;
    %
    Eprime = E(m)+1.20;
    this_sigI_2D2P = 10.^interp1(log10(1e-40+E),log10(1e-40+sig2D2P), ...
                                 log10(1e-40+Eprime),'pchip');
    sig2P2D(m) = 10/6*Eprime/E(m)*this_sigI_2D2P;
end

%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%      allowed transitions uses formula from Taylor 1988
%%%      See Kim 2002
%%%

%%%    4S->
%
state =  ['4P3s'   '4P2p4'  '4P4s'   '4P3d'];   % state
Uall =   [10.33    10.93    12.86    13.0];     % energy [eV]
f =      [2.62e-1  8.49e-2  2.42e-2  7.07e-2];  % oscillator
A =      [4.04     1.47     5.78e-1  1.73]*1e8; % Einstein [Hz]
g =      [12       12       12       12];       % stat weight

for k = 1:length(Uall)
    sigall(k,:) = TaylorAllowed(Uall(k),1.0,0.3125,f(k),0);
end

if(plot_Allowed==1)
    close(figure(2));
    figure(2); plot(E,sigall*1e16);
    % plot(E/13.6,sigall/(pi*a0.^2)/10); % compare with Fig 9 Berrington
    % label('E [Ry]'); ylabel('\sigma/\pi a_0^2');
    % axis([0 2.5 0 0.08]);
    xlabel('E [eV]'); ylabel('\sigma [1\times 10^-^1^6cm^2]');
    title('Cross Sections for Allowed from N(^4S)');
    legend('^4S->3s ^4P','^4S->2p^4 ^4P','^4S->4s ^4P','^4S->3d ^4P');
  %  set(gca,'XTick',[0 0.5 1 1.5 2 2.5]);
  %  axis([0 2.5 0 1]);
end


%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%         cross sections from kim 2002
%%%
EKim = [10.9 12:2:20 25:5:50 60:10:100 120:30:180 2e2:50:5e2 6e2:1e2:1e3 ...
        2e3:1e3:5e3]; % [eV]
    
%%% e+N(4S) => 2e+N+
%
QKim4S = [0 0 0 0.0415 0.132 0.235 0.464 0.669 0.843 0.979 1.084 1.166 ...
          1.278 1.343 1.378 1.394 1.396 1.377 1.321 1.255 1.210 1.105 ...
          1.014 0.935 0.868 0.810 0.759 0.675 0.609 0.555 0.510 0.473 ...
          0.278 0.200 0.158 0.131]*1e-20; % [m^2]

%%% e+N(2D) => 2e+N+
%
QKim2D = [0 0 0.274 0.492 0.684 0.849 1.166 1.406 1.594 1.733 1.834 ...
          1.907 1.995 2.031 2.037 2.025 2.001 1.934 1.817 1.702 ...
          1.630 1.470 1.337 1.226 1.132 1.052 0.983 0.871 0.783 ...
          0.712 0.653 0.604 0.352 0.253 0.199 0.165]*1e-20; % [m^2]

%%% e+N(2P) => 2e+N+
%
QKim2P = [0 0.123 0.300 0.481 0.661 0.822 1.137 1.370 1.559 1.700 1.804 ...
          1.879 1.971 2.010 2.019 2.008 1.985 1.921 1.806 1.692 ...
          1.620 1.461 1.328 1.218 1.124 1.044 0.976 0.864 0.776 ...
          0.705 0.647 0.599 0.348 0.250 0.197 0.163]*1e-20; % [m^2]
%

if(plot_Ionization==1)
    close(figure(3));
    figure(3); plot(EKim,QKim4S*1e4*1e16,'b');
    hold on; plot(EKim,QKim2D*1e4*1e16,'r');
    hold on; plot(EKim,QKim2P*1e4*1e16,'g');
    axis([10 1e3 0.0 2.5]);
    xlabel('E [eV]'); ylabel('\sigma [1\times 10^-^1^6cm^2]');
    title('Ionization Cross Sections (See Kim 2002)');
    legend('^4S','^2D','^2P');
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%       write total and effective cross sections data to files
%%%
%%%       total is for rate constants, effective is for energy transfer
%%%
%
if(writedata == 1)
    %path = '../Boltzmann/xsecs_atomic_Taylor/';
    %   

    atomicSDP.E = E;
    %  
    atomicSDP.Forbidden.sig4S2D.xsec = sig4S2D*1e-4; % [m^2]
    atomicSDP.Forbidden.sig4S2D.deltaE = 2.38;       % [eV]
    atomicSDP.Forbidden.sig4S2P.xsec = sig4S2P*1e-4;
    atomicSDP.Forbidden.sig4S2P.deltaE = 3.58;
    atomicSDP.Forbidden.sig2D2P.xsec = sig2D2P*1e-4;
    atomicSDP.Forbidden.sig2D2P.deltaE = 1.20;
    %
    atomicSDP.Forbidden.sig3P1D.xsec = sig3P1D*1e-4;
    atomicSDP.Forbidden.sig3P1D.deltaE = 1.98;
    atomicSDP.Forbidden.sig3P1S.xsec = sig3P1S*1e-4;
    atomicSDP.Forbidden.sig3P1S.deltaE = 4.05;
    atomicSDP.Forbidden.sig1D1S.xsec = sig1D1S*1e-4;
    atomicSDP.Forbidden.sig1D1S.deltaE = 4.05-2.98;
    %
    atomicSDP.Allowed.sig4S4P3s.xsec = sigall(1,:)*1e-4; % [m^2]
    atomicSDP.Allowed.sig4S4P3s.deltaE = Uall(1); % [m^2]
    atomicSDP.Allowed.sig4S4P2p4.xsec = sigall(2,:)*1e-4;
    atomicSDP.Allowed.sig4S4P2p4.deltaE = Uall(2);
    atomicSDP.Allowed.sig4S4P4s.xsec = sigall(3,:)*1e-4;
    atomicSDP.Allowed.sig4S4P4s.deltaE = Uall(3);
    atomicSDP.Allowed.sig4S4P3d.xsec = sigall(4,:)*1e-4;
    atomicSDP.Allowed.sig4S4P3d.deltaE = Uall(4);
    %
    %
    QKim4S =  interp1(EKim,QKim4S,E,'pchirp');
    QKim2D =  interp1(EKim,QKim2D,E,'pchirp');
    QKim2P =  interp1(EKim,QKim2P,E,'pchirp');
    for Ei = 1:length(E)
        if(E(Ei)<=14.5)        
            QKim4S(Ei) = 0;
        end
        if(E(Ei)<=12.1)        
            QKim2D(Ei) = 0;
        end
        if(E(Ei)<=10.9)        
            QKim2P(Ei) = 0;
        end   
    end
    atomicSDP.Ionization.sig4S1.xsec = QKim4S; % [m^2]
    atomicSDP.Ionization.sig4S1.deltaE = 14.5;      % [eV]
    atomicSDP.Ionization.sig2D1.xsec = QKim2D; 
    atomicSDP.Ionization.sig2D1.deltaE = 14.5-2.4;   
    atomicSDP.Ionization.sig2P1.xsec = QKim2P; 
    atomicSDP.Ionization.sig2P1.deltaE = 14.5-3.6; 
    
    %
    save('atomicSDP_xsecs.mat','atomicSDP');
    


end



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   create xsecs using expression from Eq. 5 in Taylor 1988
%%%   for optically forbidden transitions
%%%

function [xsec] = TaylorForbidden(Ej,A1,A2)

    for i = 1:length(E)
        if(E(i)<=Ej)
            xsec(i) = 0;
        elseif(E(i)<=40)
            xsec(i)  = A1*4*pi*a0^2*Ry^2./(ET(i)*Ej)*(1-Ej/ET(i));
        else
            xsec(i)  = A2*4*pi*a0^2*Ry^2./(ET(i)*Ej)^3*(1-Ej/ET(i));
        end
    end

end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   create xsecs using expression from Eq. 4 in Taylor 1988
%%%   for optically allowed transitions
%%%

function [xsec] = TaylorAllowed(Ej,A,C,f,Z)

    if (Z==1)
        gaunt = A*sqrt(3)/2/pi.*(log(4*C*ET/Ej.*gamma.^2)-beta.^2);
        for iT = 1:length(gaunt)
            if(gaunt(iT)<=0.2)
               gaunt(iT) = 0.2;
            end
        end
    else
        gaunt = A*sqrt(3)/2/pi*(1-Ej./ET).*(log(4*C*ET/Ej.*gamma.^2)-beta.^2);
    end

    xsec  = 8*pi/sqrt(3)*Ry^2./(ET*Ej)*f*pi*a0^2.*gaunt;
    for iT = 1:length(E)
        if(E(iT)<=Ej)
            xsec(iT) = 0;
        end
    end

end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




end


       