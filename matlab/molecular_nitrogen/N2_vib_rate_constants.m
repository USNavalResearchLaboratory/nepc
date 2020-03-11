function [Te,kvib,U]=N2_vib_rate_constants
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    this function computes rate constants for vibrational reactions
%%%    with molecular nitrogen using a Maxwellian EEDF. Xsecs are
%%%    taken from Laporta 2014 (See Phy4Entry_eVib_xsecs.m);
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
write_data = 0;
addpath('../');


%%% load cross sections for state-to-state ionization from v=0
%
load('./Laporta_xsecs.mat');
E = Laporta_xsecs.E;
Q = Laporta_xsecs.Q;
U = Laporta_xsecs.Uvib;
%
close(figure(1)); f1 = figure(1);
semilogy(E,squeeze(Q(1,1:10,:)));
xlabel('energy [eV]'); ylabel('\sigma [cm^2]');
title('e+N_2(X^1,v=0)=>e+N_2(X^1,v=0:10)');

Te = [0.1:0.1:5 6:1:20 25:5:100 125:25:200];
%Te = [0.1:0.1:2 2.5:0.5:5];
%Te = 0.1;
%kEvib0 = zeros(size(Te));
kvib = zeros(length(Q(:,1,1)),length(Q(1,:,1)),length(Te));
for k = 1:length(Te)
    for i = 1:59
        for j = 1:59
            thisU = U(j)-U(i);
            kvib(i,j,k)  = MaxRateConst(thisU,E,squeeze(Q(i,j,:)),Te(k),1);
         %   kEvib0(k) = kEvib0(k) + thisU*kvib0(j,k);
        end
    end
    disp(Te(k));
end
close(figure(2)); f2 = figure(2);
semilogy(Te*11605,squeeze(kvib(1,2,:))/1e-9); axis([0 5e4 0.01 40]);
hold on; plot(Te*11605,squeeze(kvib(11,12,:))/1e-9,'color',[0.87 0.49 0]);
hold on; plot(Te*11605,squeeze(kvib(21,22,:))/1e-9,'r');
hold on; plot(Te*11605,squeeze(kvib(31,32,:))/1e-9,'g');
hold on; plot(Te*11605,squeeze(kvib(41,42,:))/1e-9,'b');
hold on; plot(Te*11605,squeeze(kvib(51,52,:))/1e-9,'magenta');
xlabel('T_e [K]'); ylabel('k [10^-^9 cm^3/s]');
title('e+N_2(X^1,v=0)=>e+N_2(X^1,v=0:10)');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%               write rate constants to a file
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if(write_data)
    
    N2_vib_rateconstants.Te = Te; 
    N2_vib_rateconstants.U = U;
    N2_vib_rateconstants.k = kvib;
    save('N2_vib_rateconstants.mat','N2_vib_rateconstants');
    
end



end