%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   Compare rate constants from Lotz 1968 for ionization of neutral
%%%   nitrogen with those shown from more detailed calculations in
%%%   Huo 2008 "electron impact excitation and ionization in air"
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear all;
Te = 0.3:0.1:10;

%%%  first compute rate constants for ionization of ground state
%

%%% Lotz 1968
%
a = [3.2 4.0]; b = [0.83 0.7]; c = [0.22 0.5]; q = [3 2]; P = [14.5 20.3];
%
SLotz = zeros(size(Te));
for i = 1:length(a)
    SLotz = SLotz ...
          + a(i)*q(i)./Te.^(1.5).*( Te/P(i).*expint(P(i)./Te) ...
          - b(i)*Te*exp(c(i))./(Te*c(i)+P(i)).*expint(P(i)./Te+c(i)) );
end
SLotz = SLotz*6.7e-7;

%%% Corona Model
%
chi = [14.5 29.6]; eta = [5 4];
SCorona = 2.5e-6/(chi(1)^1.5)*eta(1)*sqrt(Te/chi(1)).*exp(-chi(1)./Te)./ ...
            (1+Te/chi(1));
        
        
%%% FLYCHK (reduced Lotz for highly ionized)
%
SFly =  2.97e-6*eta(1)/14.5./sqrt(Te).*expint(14.5./Te);


%%% plot and compare
%
close(figure(1));
figure(1);
loglog(Te,SLotz,'black',Te,SCorona','r',Te,SFly,'g');
xlabel('T_e [eV]'); ylabel('k  [cm^3/s]');
title('rate constants for e+N(^4S)=>e+N^+');
legend('Lotz','Corona','FLYCHK','location','SE');
axis([0.3 10 1e-14 1e-7]);



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%%%  now compute from excited states using a b and c from ground
%

%%% Lotz 1968
%
a = 3.2; b = 0.83; c = 0.22;
%
P = [14.5 12.1 10.9 4.208 4.076 3.854 2.784 2.697 1.557 1.518];
q = [3    3    3    1     1     1     1     1     1     1];
SLotz = zeros(length(P),length(Te));
for i = 1:length(P)
    SLotz(i,:) = SLotz(i,:) ...
          + a*q(i)./Te.^(1.5).*( Te/P(i).*expint(P(i)./Te) ...
          - b*Te*exp(c)./(Te*c+P(i)).*expint(P(i)./Te+c) );
end
SLotz = SLotz*6.7e-7;


close(figure(2));
f2=figure(2); set(f2,'position',[170 329 515 477]);
semilogy(Te*11605,SLotz(1,:)*6.0221e23,'black');
hold on; plot(Te*11605,SLotz(2,:)*6.0221e23,'b');
hold on; plot(Te*11605,SLotz(3,:)*6.0221e23,'r');
semilogy(Te*11605,SLotz(4,:)*6.0221e23,'linewidth',2,'color',[0 0.5 0]);
hold on; plot(Te*11605,SLotz(7,:)*6.0221e23,'r--','linewidth',2);
hold on; plot(Te*11605,SLotz(8,:)*6.0221e23,'b-.','linewidth',2);
hold on; plot(Te*11605,SLotz(9,:)*6.0221e23,'black-.','linewidth',2);
hold on; plot(Te*11605,SLotz(10,:)*6.0221e23,'linestyle','--', ...
                 'color',[0 0.5 0],'linewidth',2);
hold on; plot(Te*11605,SLotz(6,:)*6.0221e23,'r-.','linewidth',2);
hold on; plot(Te*11605,SLotz(5,:)*6.0221e23,'b--', ...
                 'color',[0.48 0.06 0.89],'linewidth',2);
xlabel('T_e [K]'); ylabel('k [cm^3/s/mol]');
axis([0.5e4 5e4 1e2 1e18]);
set(gca,'YTick',10.^(2:2:18));
legend('^4S^0','^2D^0','^2P^0','^4P','^4D^0','^4P^0','^4F','^4D','^2P','^2D');