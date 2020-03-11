function atomicN_ionization

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%  compare ionization cross sections and rate constants (maxwellian)
%%%  for ionization of atomic N(4S), N(2D), and N(2P) 
%%%  see Brooks 1978, Kim 2002, and Taylor 1988
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Ry   = 13.6;     % hydrogen ionization potential [eV]
mc2 = 0.511e6;  % electron rest mass energy [eV]
a0 = 5.29e-9; % Bohr radius [cm^2]

%%%   cross section for e+N(70%4S + 30%2D) => 2e+N+ from Brooks 1978
%
EBrooks = [11.4 11.9 12.4 12.9 13.9 14.9 15.9 16.9 17.9 19.9 21.9 23.9 ...
           26.9 31.9 36.9 37   47   67   77   87   97   147  197  297 ...
           397  497  597  797  997]; % [eV]
QBrooks = [0.087 0.007 0.035 0.054 0.113 0.122 0.248 0.232 0.280 0.372 ...
           0.568 0.608 0.799 0.945 1.157 1.117 1.341 1.513 1.590 1.608 ...
           1.586 1.445 1.289 1.097 0.914 0.816 0.697 0.587 0.490]*1e-20; % [m^2]
       
close(figure(1));
figure(1);
%semilogx(EBrooks,QBrooks*1e4,'black*'); axis([10 1e3 0.0e-16 2.5e-16]);
xlabel('E [eV]'); ylabel('\sigma [cm^2]');
title('e + N(^4S,^2D,^2P) => 2e + N+');




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
%
UBEB = 51.034;
BBEB = 14.534;
NBEB = 1.9975;
t = EKim/BBEB;
u = UBEB/BBEB;
for i = 1:length(t)
    if(t(i)>=1)
        QBEB(i) =  4*pi*a0^2*NBEB*(Ry/BBEB)^2./(t(i)+u+1).* ...
                   (log(t(i))/2.*(1-1./t(i).^2)+1-1./t(i)-log(t(i))./(1+t(i)));
    end
end
UBEB = 51.094;
BBEB = 15.439;
NBEB = 1.0025;
t = EKim/BBEB;
u = UBEB/BBEB;
for i = 1:length(t)
    if(t(i)>=1)
        QBEB(i) = QBEB(i) + 4*pi*a0^2*NBEB*(Ry/BBEB)^2./(t(i)+u+1).* ...
                   (log(t(i))/2.*(1-1./t(i).^2)+1-1./t(i)-log(t(i))./(1+t(i)));
    end
end
UBEB = 65.655;
BBEB = 25.828;
NBEB = 2;
t = EKim/BBEB;
u = UBEB/BBEB;
for i = 1:length(t)
    if(t(i)>=1)
        QBEB(i) = QBEB(i) + 4*pi*a0^2*NBEB*(Ry/BBEB)^2./(t(i)+u+1).* ...
                   (log(t(i))/2.*(1-1./t(i).^2)+1-1./t(i)-log(t(i))./(1+t(i)));
    end
end
UBEB = 598.726;
BBEB = 425.469;
NBEB = 2;
t = EKim/BBEB;
u = UBEB/BBEB;
for i = 1:length(t)
    if(t(i)>=1)
        QBEB(i) = QBEB(i) + 4*pi*a0^2*NBEB*(Ry/BBEB)^2./(t(i)+u+1).* ...
                   (log(t(i))/2.*(1-1./t(i).^2)+1-1./t(i)-log(t(i))./(1+t(i)));
    end
end
QBEB = 9/15*QBEB;
%

close(figure(1)); figure(1);
semilogx(EBrooks,QBrooks*1e4*1e16,'black*'); axis([10 1e3 0 4]);
xlabel('E [eV]'); ylabel('\sigma [cm^2]');
title('e + N(^4S) => 2e + N+');
close(figure(2)); figure(2);
semilogx(EBrooks,QBrooks*1e4*1e16,'black*'); axis([10 1e3 0 4]);
xlabel('E [eV]'); ylabel('\sigma [cm^2]');
title('e + N(^2D) => 2e + N+');
close(figure(3)); figure(3);
semilogx(EBrooks,QBrooks*1e4*1e16,'black*'); axis([10 1e3 0 4]);
xlabel('E [eV]'); ylabel('\sigma [cm^2]');
title('e + N(^2P) => 2e + N+');
%hold on; plot(EKim,QBEB,'bx');

figure(1); hold on; plot(EKim,QKim4S*1e4*1e16,'b');

%%% e+N(2D) => 2e+N+
%
QKim2D = [0 0 0.274 0.492 0.684 0.849 1.166 1.406 1.594 1.733 1.834 ...
          1.907 1.995 2.031 2.037 2.025 2.001 1.934 1.817 1.702 ...
          1.630 1.470 1.337 1.226 1.132 1.052 0.983 0.871 0.783 ...
          0.712 0.653 0.604 0.352 0.253 0.199 0.165]*1e-20; % [m^2]

figure(2); hold on; plot(EKim,QKim2D*1e4*1e16,'r');

%%% e+N(2P) => 2e+N+
%
QKim2P = [0 0.123 0.300 0.481 0.661 0.822 1.137 1.370 1.559 1.700 1.804 ...
          1.879 1.971 2.010 2.019 2.008 1.985 1.921 1.806 1.692 ...
          1.620 1.461 1.328 1.218 1.124 1.044 0.976 0.864 0.776 ...
          0.705 0.647 0.599 0.348 0.250 0.197 0.163]*1e-20; % [m^2]

figure(3); hold on; plot(EKim,QKim2P*1e4*1e16,'g');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%   cross section from Taylor 1988 (Drawin 1969 and Taylor 1987)
%
%
E0 = [0 10.^(0:0.02:4)];   % kinetic energy grid (eV)
gamma = E0/(mc2)+1;
beta = sqrt(1-1./gamma.^2);
ET = 0.5*mc2*beta.^2;     % 1/2mv^2 (E used in Taylor 1988)
QTaylor   = TaylorIonization(14.5,2.2,0.25);
QTaylor2D = TaylorIonization(14.5-2.4,2.2,0.25);
QTaylor2P = TaylorIonization(14.5-3.6,2.2,0.25);
figure(1); hold on; plot(E0,QTaylor*1e16,'b--');
figure(2); hold on; plot(E0,QTaylor2D*1e16,'r--');
figure(3); hold on; plot(E0,QTaylor2P*1e16,'g--');
%legend('Brooks', 'Taylor');

%%%   cross section Lotz 1969
%
a = [3.2 4.0]; b = [0.83 0.7]; c = [0.22 0.5]; q = [3 2]; P = [14.5 20.3];
QLotz   = LotzIonization(ET,a,b,c,q,P);
QLotz2D   = LotzIonization(ET,a,b,c,q,P-2.4);
QLotz2P   = LotzIonization(ET,a,b,c,q,P-3.6);
figure(1); hold on; plot(E0,sum(QLotz)*1e16,'bx');
legend('Brooks 70/30','Kim','Taylor','Lotz','location','best');
figure(2); hold on; plot(E0,sum(QLotz2D)*1e16,'rx');
legend('Brooks 70/30','Kim','Taylor','Lotz','location','best');
figure(3); hold on; plot(E0,sum(QLotz2P)*1e16,'gx');
legend('Brooks 70/30','Kim','Taylor','Lotz','location','best');


%%%   integrate over maxwellian to get rate consant
%
Te = 0.3:0.1:40;
for i = 1:length(Te)
    
    E = 0:Te(i)/2e2:50*Te(i);     % electron kinetic energy [eV]
    FM = 2/sqrt(pi)/Te(i)^(3/2)*exp(-E/Te(i));  % Maxwellian EEDF

    %%% check to make sure grid is refined enough using 0th and 2nd moments
    %
    test0 = trapz(E,FM.*E.^(1/2));   % should be one
    error0 = 100*abs(1-test0);
    if(error0>=1)
        warning('0th velocity moment not converged');
    end
    %
    ebar = trapz(E,FM.*E.^(3/2));    % should be 3*Te/2;
    error2 = 100*abs(ebar-3*Te(i)/2)/(3*Te(i)/2);
    if(error2>=1)
        warning('2nd velocity moment not converged');
    end

    % close(figure(1));
    % figure(1);
    % semilogy(E,FM);
    % xlabel('kinetic energy [eV]');
    % ylabel('EEDF [eV^-^3^/^2]');
    
    
     %%% ionization with N(4S)
     %
     Qinterp =  interp1(E0,QTaylor,E,'pchirp');
     for Ei = 1:length(E)
         if(E(Ei)<=14.5)        
             Qinterp(Ei) = 0;
         end
     end
     kTay4S(i) = sqrt(2*1.7588e11)*trapz(E,E.*Qinterp*1e-4.*FM); % m^3/s
     %
     Qinterp =  interp1(EKim,QKim4S,E,'pchirp');
     for Ei = 1:length(E)
         if(E(Ei)<=14.5)        
             Qinterp(Ei) = 0;
         end
     end
     kKim4S(i) = sqrt(2*1.7588e11)*trapz(E,E.*Qinterp.*FM); % m^3/s
     
     
     %%% ionization with N(2D)
     %
     Qinterp =  interp1(E0,QTaylor2D,E,'pchirp');
     for Ei = 1:length(E)
         if(E(Ei)<=12.1)        
             Qinterp(Ei) = 0;
         end
     end
     kiz2DT(i) = sqrt(2*1.7588e11)*trapz(E,E.*Qinterp*1e-4.*FM); % m^3/s
     %
     Qinterp =  interp1(EKim,QKim2D,E,'pchirp');
     for Ei = 1:length(E)
         if(E(Ei)<=12.1)        
             Qinterp(Ei) = 0;
         end
     end
     kKim2D(i) = sqrt(2*1.7588e11)*trapz(E,E.*Qinterp.*FM); % m^3/s
     
     
     %%% ionization with N(2P)
     %
     Qinterp =  interp1(E0,QTaylor2P,E,'pchirp');
     kiz2PT(i) = sqrt(2*1.7588e11)*trapz(E,E.*Qinterp*1e-4.*FM); % m^3/s
     %
     Qinterp =  interp1(EKim,QKim2P,E,'pchirp');
     for Ei = 1:length(E)
         if(E(Ei)<=10.9)        
             Qinterp(Ei) = 0;
         end
     end
     kKim2P(i) = sqrt(2*1.7588e11)*trapz(E,E.*Qinterp.*FM); % m^3/s
     
end

Navo = 6.0221e23; % particles/mol
close(figure(7));
figure(7); semilogy(Te*11605,kKim4S*1e6*Navo,'black');
hold on; plot(Te*11605,kKim2D*1e6*Navo,'b');
hold on; plot(Te*11605,kKim2P*1e6*Navo,'r');
axis([0.5e4 5e4 100 1e18]); 
xlabel('T [K]'); ylabel('k [cm^3/mol/s]');
%legend('N(^4S)','N(^2D)','N(^2P)');


%%% set rate constants from different ionization models
%
chi = [14.5 29.5]; chi2D = chi(1)-2.4; chi2P = chi(1)-3.6;
eta = [5, 4];
kiz4S_Fly =  2.97e-6*eta(1)/14.5./sqrt(Te).*expint(14.5./Te);
kiz2D_Fly =  2.97e-6*eta(1)/12.1./sqrt(Te).*expint(12.1./Te);
kiz2P_Fly =  2.97e-6*eta(1)/10.9./sqrt(Te).*expint(10.9./Te);

%%% use Lotz for ionization of higher states
%
chi4P = 4.208;
kiz4P_Fly = 2.97e-6*1/chi4P./sqrt(Te).*expint(chi4P./Te);

figure(7); 
hold on; plot(Te*11605,kiz4P_Fly*Navo,'black*');
% hold on; plot(Te*11605,kiz4S_Fly*Navo,'black*');
% hold on; plot(Te*11605,kiz2D_Fly*Navo,'b*');
% hold on; plot(Te*11605,kiz2P_Fly*Navo,'r*');

%%% set rate constants from Corona Model
%
kiz4S_cor = 2.5e-6/(chi(1)^1.5)*eta(1)*sqrt(Te/chi(1)).*exp(-chi(1)./Te)./ ...
            (1+Te/chi(1));
kiz2D_cor = 2.5e-6/(chi2D^1.5)*eta(1)*sqrt(Te/chi2D).*exp(-chi2D./Te)./ ...
            (1+Te/chi2D);
kiz2P_cor = 2.5e-6/(chi2P^1.5)*eta(1)*sqrt(Te/chi2P).*exp(-chi2P./Te)./ ...
            (1+Te/chi2P);
        
%%% set rate constants from Lotz model (full model required for near nuetrals!!)
%
%
SLotz = zeros(size(Te));
for i = 1:length(a)
    SLotz = SLotz ...
          + a(i)*q(i)./Te.^(1.5).*( Te/P(i).*expint(P(i)./Te) ...
          - b(i)*Te*exp(c(i))./(Te*c(i)+P(i)).*expint(P(i)./Te+c(i)) );
end
SLotz = SLotz*6.7e-7;


% figure(2);
% hold on; plot(Te*11605,kiz4S_cor*Navo,'bo');
% hold on; plot(Te*11605,kiz2D_cor*Navo,'ro');
% hold on; plot(Te*11605,kiz2P_cor*Navo,'go');


%%%  compare different models
%
close(figure(33));
f3 = figure(33); set(f3,'position',[0 100 1200 400]);

subplot(1,3,1);
semilogy(Te,kTay4S*1e6,'b',Te,kiz4S_cor,'ro'); % cm^3/s
hold on; plot(Te,kiz4S_Fly,'gx');
hold on; plot(Te,SLotz,'magenta');
axis([0.5 5 1e-13 1e-7]);
xlabel('T [eV]'); ylabel('k [cm^3/s]'); title('e+N(^4S)=>2e+N^+');
legend('Taylor','FlyCHK','Corona','Lotz','location','best');
%
subplot(1,3,2);
semilogy(Te,kiz2DT*1e6,'b',Te,kiz2D_cor,'ro'); % cm^3/s
hold on; plot(Te,kiz2D_Fly,'gx');
axis([0.5 5 1e-13 1e-7]);
xlabel('T [eV]'); ylabel('k [cm^3/s]'); title('e+N(^2D)=>2e+N^+');
legend('Taylor','Lotz','Corona','location','best');
%
subplot(1,3,3);
semilogy(Te,kiz2PT*1e6,'b',Te,kiz2P_cor,'ro'); % cm^3/s
hold on; plot(Te,kiz2P_Fly,'gx');
axis([0.5 5 1e-13 1e-7]);
xlabel('T [eV]'); ylabel('k [cm^3/s]'); title('e+N(^2P)=>2e+N^+');
legend('Taylor','Lotz','Corona','location','best');
%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   create xsecs using expression from Eq. 13 in Taylor 1988
%%%   for ionization
%%%

function [xsec] = TaylorIonization(Ej,A,C)

    for j = 1:length(ET)
        if(ET(j)<=Ej)
            xsec(j) = 0;
        else
            xsec(j)  = A*4*pi*a0^2*Ry^2/(ET(j)^2)*(ET(j)/Ej-1) ...
                      *(log(4*C*ET(j)/Ej*gamma(j)^2)-beta(j)^2) ;
        end
    end

end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   create xsecs using expression from Lotz 1968
%%%   for ionization of atomic nitrogen
%%%

function [xsec] = LotzIonization(Ej,a,b,c,q,P)
 
    for k = 1:length(a)
        for j = 1:length(ET)
            if(ET(j)<=P(k))
                xsec(k,j) = 0;
            else
                xsec(k,j) = 1e-14*a(k)*q(k).*log(ET(j)/P(k))/(ET(j)*P(k)) ...
                          .* (1-b(k)*exp(-c(k)*(ET(j)/P(k)-1)));
            end
        end
    end

end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



end
