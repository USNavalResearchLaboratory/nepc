function atomicN_allowed
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   Computes the cross section and rate constant for optically 
%%%   allowed transitions using two different expressions
%%%   See Van Regemorter 1962
%%%   Taylor 1988 (drawin)
%%%   Fisher 1996 (improved gaunt factor for delta n = 0)
%%%   Kim 2001 (scaled Born)
%%%
%%%   See J. Phys. Chem. Ref. Data, Vol. 36, No. 4, 2007
%%%
writedata = 0;

%%%    set some needed constants
%
Ry   = 13.6;    % hydrogen ionization potential [eV]
mc2 = 0.511e6;  % electron rest mass energy [eV]
a0  = 5.29e-9;  % bohr radius [cm]
%
E = [0 10.^(0:0.02:3)];   % kinetic energy grid (eV)
gamma = E/(mc2)+1;
beta = sqrt(1-1./gamma.^2);
ET = 0.5*mc2*beta.^2;     % 1/2mv^2 (E used in Taylor 1988)

   
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%           Define data for 4S transitions (29 total)
%%%

%%%   4S -> 3s 4P, 2p4 4P
%%%   2D -> 3s 2P, 3s 2D
%%%   2P -> 3s 2P, 3s 2P
%
tran =  ['4S->3s4P' '4S->2p44P' '2D->3s2P'  '2D->3s2D'  '2P->3s2P'  '2P->3s2D'];  % state
U =     [10.33      10.93       10.69-2.38  12.36-2.38  10.69-3.58  10.69-3.58];  % energy [eV]
f =     [0.278      0.079       0.068       0.059       0.06        0.03];        % oscillator
A =     [4.04       1.47        3.45        3.45        1.26        0.54]*1e8;    % Einstein [Hz]
g =     [12         12          6           10          6           10];          % stat weight
deltan= [1          0           1           1           1           1];  % change in principle quantum number
Uiz   = [14.53      14.53       14.53-2.38  14.53-2.38  14.53-3.58  14.53-3.58];
  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 
%%%      compare cross sections from different models
%%%

%%%   compute cross sections using Eq. 4 in Taylor 1988
%
sigTaylor = zeros(length(U),length(E));
sigVan  = zeros(length(U),length(E));
sigFish = zeros(length(U),length(E));
sigKim  = zeros(length(U),length(E));
%
for k = 1:length(U)
    sigTaylor(k,:) = TaylorAllowed(U(k),1.0,0.3125,f(k),0);
    %
    geff = max(0,3*sqrt(3)/(2*pi)*(1-U(k)./E));    % low energies
   % geff = max(0,3*sqrt(3)/(2*pi)*log(4*E/U(k))); % high energies
    sigVan(k,:) = 8*pi/sqrt(3)*Ry^2./(U(k)*E)*f(k).*geff*pi*a0^2;
    %
    for j = 1:length(E)
        if(E(j)<=U(k))
            gfish(j) = 0;
        else 
            if(deltan(k)==0)
                gfish(j) = (0.33-0.3/(E(j)/U(k))+0.08/(E(j)/U(k)).^2).*log(E(j)/U(k));
            else
                gfish(j) = (0.276-0.18./(E(j)/U(k))).*log(E(j)/U(k));
            end
        end
        sigFish(k,j)= 8*pi/sqrt(3)*Ry^2./(U(k)*E(j))*f(k).*gfish(j)*pi*a0^2;
    end
    % can't make sense of this from text...but sigJohn should be same
    %
    Eb = [1 1.2  1.5  2    3    5    10   30   100]*U(k);
    b  = [0 0.03 0.06 0.11 0.21 0.33 0.56 0.98 1.33];
    for j = 1:length(E)
        thisb = interp1(Eb,b,E(j),'pchirp');
        thisb = max(0,thisb);
        sigJohn(k,j) = 8*pi/sqrt(3)*pi*a0^2*Ry^2/(E(j)*U(k))*f(k)*thisb;
        % John Apruzee gave me this from a text book...
    end
    %
    sigKim(k,:) = sigTaylor(k,:).*E./(E+Uiz(k)+U(k)); % ?
   % sigKim(k,:) = sigTaylor(k,:).*E./(E+U12+U(k));
end


close(figure(1));
f1=figure(1);
loglog(E,sigTaylor(1:4,:));
%legend('3s ^4P','2p^4 ^4P');
legend('3s ^4P','2p^4 ^4P','4s ^4P','3d ^4P');
%hold on; plot(E,sigVan(1:2,:),'Marker','o');
hold on; plot(E,sigJohn(1:4,:),'Marker','*');
hold on; plot(E,sigKim(1:4,:),'Marker','x');
xlabel('E [eV]'); ylabel('\sigma [cm^2]');
title('optically allowed cross sections in atomic nitrogen')
%
close(figure(11));
f11=figure(11); set(f11,'position',[179 386 560 800]);
%
subplot(2,1,1);
plot(E,sigTaylor(1,:)*1e16,'bs');
hold on; plot(E,sigJohn(1,:)*1e16,'r','Marker','o');
hold on; plot(E,sigFish(1,:)*1e16,'g','Marker','x');
legend('Taylor','Van','Fish','location','SE');
xlabel('E [eV]'); ylabel('\sigma [1\times 10^-^1^6cm^2]');
title('e+N(^4S) => e+N(^3s ^4P)');
axis([0 120 0 0.6]);
%
subplot(2,1,2);
plot(E,sigTaylor(2,:)*1e16,'bs');
hold on; plot(E,sigJohn(2,:)*1e16,'r','Marker','o');
hold on; plot(E,sigFish(2,:)*1e16,'g','Marker','x');
legend('Taylor','Van','Fish','location','NE');
xlabel('E [eV]'); ylabel('\sigma [1\times 10^-^1^6cm^2]');
title('e+N(^4S) => e+N(^3s ^4P)');
axis([0 120 0 0.6]);
%
close(figure(12));
f12=figure(12); set(f12,'position',[179 386 560 800]);
%
subplot(2,1,1);
%plot(E,sigTaylor(3,:)*1e16,'bs');
%hold on; 
plot(E,sigJohn(3,:)*1e16,'r','Marker','o');
hold on; plot(E,sigKim(3,:)*1e16,'g','Marker','x');
legend('Van','Kim','location','SE');
xlabel('E [eV]'); ylabel('\sigma [1\times 10^-^1^6cm^2]');
title('e+N(^2D) => e+N(3s ^2P)');
axis([0 120 0 0.2]);
%
subplot(2,1,2);
%plot(E,sigTaylor(4,:)*1e16,'bs');
%hold on; 
plot(E,sigJohn(4,:)*1e16,'r','Marker','o');
hold on; plot(E,sigKim(4,:)*1e16,'g','Marker','x');
legend('Van','Kim','location','NE');
xlabel('E [eV]'); ylabel('\sigma [1\times 10^-^1^6cm^2]');
title('e+N(^2D) => e+N(3s ^2D)');
axis([0 120 0 0.15]);
%
close(figure(13));
f13=figure(13); set(f13,'position',[179 386 560 800]);
%
subplot(2,1,1);
%plot(E,sigTaylor(5,:)*1e16,'bs');
%hold on; 
plot(E,sigJohn(5,:)*1e16,'r','Marker','o');
hold on; plot(E,sigKim(5,:)*1e16,'g','Marker','x');
legend('Van','Kim','location','SE');
xlabel('E [eV]'); ylabel('\sigma [1\times 10^-^1^6cm^2]');
title('e+N(^2P) => e+N(3s ^2P)');
axis([0 120 0 0.25]);
%
subplot(2,1,2);
%plot(E,sigTaylor(6,:)*1e16,'bs');
%hold on; 
plot(E,sigJohn(6,:)*1e16,'r','Marker','o');
hold on; plot(E,sigKim(6,:)*1e16,'g','Marker','x');
legend('Van','Kim','location','NE');
xlabel('E [eV]'); ylabel('\sigma [1\times 10^-^1^6cm^2]');
title('e+N(^2P) => e+N(3s ^2D)');
axis([0 120 0 0.15]);

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 
%%%      compare rate constants using maxwellian
%%%

Te = 0.3:0.1:40;
for k = 1:length(U)
for i = 1:length(Te)
    
    Esub = 0:Te(i)/2e2:50*Te(i);     % electron kinetic energy [eV]
    FM = 2/sqrt(pi)/Te(i)^(3/2)*exp(-Esub/Te(i));  % Maxwellian EEDF

    %%% check to make sure grid is refined enough using 0th and 2nd moments
    %
    test0 = trapz(Esub,FM.*Esub.^(1/2));   % should be one
    error0 = 100*abs(1-test0);
    if(error0>=1)
        warning('0th velocity moment not converged');
    end
    %
    ebar = trapz(Esub,FM.*Esub.^(3/2));    % should be 3*Te/2;
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
     QTinterp =  interp1(E,sigTaylor(k,:),Esub,'pchirp');
     QKinterp =  interp1(E,sigKim(k,:),Esub,'pchirp');
     for Ei = 1:length(Esub)
         if(Esub(Ei)<=U(k))        
             QTinterp(Ei) = 0;
             QKinterp(Ei) = 0;
         end
     end
     kTaylor(k,i) = sqrt(2*1.7588e11)*trapz(Esub,Esub.*QTinterp*1e-4.*FM); % m^3/s
     kKim(k,i) = sqrt(2*1.7588e11)*trapz(Esub,Esub.*QKinterp*1e-4.*FM); % m^3/s
     %
end
end


close(figure(2)); figure(2);
semilogy(Te,kTaylor*1e6);
hold on; plot(Te,kKim*1e6,'Marker','*');
xlabel('T_e [eV]'); ylabel('k [cm^3/s]');
title('optically allowed rate consants in atomic nitrogen');
axis([0.3 5 1e-20 1e-8]); 


% close(figure(3)); figure(3);
% semilogy(Te,100*abs(kTaylor-kKim)./kKim);

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


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


       