function N2_rate_constants
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    this function computes rate constants for thermal reactions
%%%    with molecular nitrogen using a Maxwellian EEDF
%%%
%%%    excitation from ground state computed using Itikawa 2005
%%%    state to state ionization computed using Kosarim 2005
%%%
%%%    dissociation processes done elsewhere as of now
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
write_data = 1;
addpath('../');


%%% load cross sections for state-to-state dissociation from v=0
%
load('./WTCS_diss.mat');
ED = WTCS_diss.E;
QD = WTCS_diss.Q;
UD = WTCS_diss.U;

%%% load cross sections for state-to-state ionization from v=0
%
load('../../Xsecs/Kosarim_xsecs.mat');
Kxsecs = Kosarim_xsecs;

%%% load cross sections for excitation from N2(X1Sigma,v=0)
%
load('../../Xsecs/Itikawa_xsecs.mat');
Ixsecs = Itikawa_xsecs;

Te = [0.3:0.1:5 6:1:20 25:5:100 125:25:200];


%Te = [0.5 1 3 5 7 10];
for i = 1:length(Te)
    
    kX1_A3(i)  = MaxRateConst(Ixsecs.UA3,Ixsecs.EA3,Ixsecs.QA3,Te(i),1);
    kX1_B3(i)  = MaxRateConst(Ixsecs.UB3,Ixsecs.EB3,Ixsecs.QB3,Te(i),1);
    kX1_W3(i)  = MaxRateConst(Ixsecs.UW3,Ixsecs.EW3,Ixsecs.QW3,Te(i),1);
    kX1_Bp3(i) = MaxRateConst(Ixsecs.UBp3,Ixsecs.EBp3,Ixsecs.QBp3,Te(i),1); 
    kX1_ap1(i) = MaxRateConst(Ixsecs.Uap1,Ixsecs.Eap1,Ixsecs.Qap1,Te(i),0);
    kX1_a1(i)  = MaxRateConst(Ixsecs.Ua1,Ixsecs.Ea1,Ixsecs.Qa1,Te(i),0);
    kX1_w1(i)  = MaxRateConst(Ixsecs.Uw1,Ixsecs.Ew1,Ixsecs.Qw1,Te(i),0);
    kX1_C3(i)  = MaxRateConst(Ixsecs.UC3,Ixsecs.EC3,Ixsecs.QC3,Te(i),1);
    kX1_E3(i)  = MaxRateConst(Ixsecs.UE3,Ixsecs.EE3,Ixsecs.QE3,Te(i),1);
    kX1_app1(i)= MaxRateConst(Ixsecs.Uapp1,Ixsecs.Eapp1,Ixsecs.Qapp1,Te(i),0);
    kX1_Sum(i) = MaxRateConst(Ixsecs.USum,Ixsecs.ESum,Ixsecs.QSum,Te(i),0);
    kX1_elm(i) = MaxRateConst(0,Ixsecs.Eelm,Ixsecs.Eelm.*Ixsecs.Qelm,Te(i),0)/(1.5*Te(i));
    kX1_mom(i) = MaxMobilityRateConst(Ixsecs.Eeff,Ixsecs.Qeff,Te(i));
    %
    % figure(100); loglog(Ixsecs.Eeff,Ixsecs.Qeff);
    for j = 1:3 % number of ionic states of N2
        kX1_iz(j,i) = MaxRateConst(Kxsecs.UX1(j),Kxsecs.E, ...
                             Kxsecs.QX1(j,:),Te(i),0);
        kA3_iz(j,i) = MaxRateConst(Kxsecs.UA3(j),Kxsecs.E, ...
                             Kxsecs.QA3(j,:),Te(i),0);        
        kB3_iz(j,i) = MaxRateConst(Kxsecs.UB3(j),Kxsecs.E, ...
                             Kxsecs.QB3(j,:),Te(i),0);
        kW3_iz(j,i) = MaxRateConst(Kxsecs.UW3(j),Kxsecs.E, ...
                             Kxsecs.QW3(j,:),Te(i),0);
        kBp3_iz(j,i) = MaxRateConst(Kxsecs.UBp3(j),Kxsecs.E, ...
                             Kxsecs.QBp3(j,:),Te(i),0);
        kap1_iz(j,i) = MaxRateConst(Kxsecs.Uap1(j),Kxsecs.E, ...
                             Kxsecs.Qap1(j,:),Te(i),0);
        ka1_iz(j,i) = MaxRateConst(Kxsecs.Ua1(j),Kxsecs.E, ...
                             Kxsecs.Qa1(j,:),Te(i),0);      
        kw1_iz(j,i) = MaxRateConst(Kxsecs.Uw1(j),Kxsecs.E, ...
                             Kxsecs.Qw1(j,:),Te(i),0);                         
        kC3_iz(j,i) = MaxRateConst(Kxsecs.UC3(j),Kxsecs.E, ...
                             Kxsecs.QC3(j,:),Te(i),0);                         
    end

    [x,y] = min(abs(QD(1,:)-1e-20));
    kXSS(i)  = MaxRateConst(ED(y),ED,QD(1,:),Te(i),0); % not used
    [x,y] = min(abs(QD(2,:)-1e-20));
    kASS(i)  = MaxRateConst(ED(y),ED,QD(2,:),Te(i),0);
    [x,y] = min(abs(QD(3,:)-1e-20));
    kBSD(i)  = MaxRateConst(ED(y),ED,QD(3,:),Te(i),0);
    [x,y] = min(abs(QD(4,:)-1e-20));
    kWSD(i)  = MaxRateConst(ED(y),ED,QD(4,:),Te(i),0);
    [x,y] = min(abs(QD(5,:)-1e-20));
    kBpSP(i) = MaxRateConst(ED(y),ED,QD(5,:),Te(i),0); 
    [x,y] = min(abs(QD(6,:)-1e-20));
    kapDD(i) = MaxRateConst(ED(y),ED,QD(6,:),Te(i),0);
    [x,y] = min(abs(QD(7,:)-1e-20));
    kaDD(i)  = MaxRateConst(ED(y),ED,QD(7,:),Te(i),0);
    [x,y] = min(abs(QD(8,:)-1e-20));
    kwDD(i)  = MaxRateConst(ED(y),ED,QD(8,:),Te(i),0);
    [x,y] = min(abs(QD(9,:)-1e-20));
    kCSD(i)  = MaxRateConst(ED(y),ED,QD(9,:),Te(i),0);
    Te(i)
end
figure(222); loglog(Te,kXSS,'black',Te,kASS,'r',Te,kBSD,'g',Te,kWSD,'b');
hold on; plot(Te,kBpSP,'cyan',Te,kapDD,'magenta',Te,kaDD,'r--',Te,kwDD,'g--');
hold on; plot(Te,kCSD,'b--'); axis([0.3 200 1e-15 1e-5]);

close(figure(1));
f1 = figure(1); set(f1,'position',[0 0 800 800]);
%
subplot(2,2,1);
kE_triplets = Ixsecs.UA3*kX1_A3 + Ixsecs.UB3*kX1_B3 ...
            + Ixsecs.UW3*kX1_W3 + Ixsecs.UBp3*kX1_Bp3 ...
            + Ixsecs.UC3*kX1_C3;
semilogy(Te,Ixsecs.UA3*kX1_A3,'bo');
hold on; plot(Te,Ixsecs.UB3*kX1_B3,'rx');
hold on; plot(Te,Ixsecs.UW3*kX1_W3,'g*');
hold on; plot(Te,Ixsecs.UBp3*kX1_Bp3,'black');
hold on; plot(Te,Ixsecs.UC3*kX1_C3,'magenta');
xlabel('Te [eV]'); ylabel('kE [eV-cm^3/s]');
legend('A^3\Sigma','B^3\Pi','W^3\Delta','B''^3\Sigma','C^3\Pi', ...
       'location','SE');
axis([1 15 1e-11 1e-7]); title('energy loss to triplets');
%
subplot(2,2,2);
kE_singlets = Ixsecs.Uap1*kX1_ap1 + Ixsecs.Ua1*kX1_a1 ...
            + Ixsecs.Uw1*kX1_w1;
semilogy(Te,Ixsecs.Uap1*kX1_ap1,'bo');
hold on; plot(Te,Ixsecs.Ua1*kX1_a1,'rx');
hold on; plot(Te,Ixsecs.Uw1*kX1_w1,'g*');
xlabel('Te [eV]'); ylabel('kE [eV-cm^3/s]');
legend('a''^1\Sigma','a^1\Pi','w^1\Delta','location','SE');
axis([1 15 1e-11 1e-7]); title('energy loss to singlets');
%
subplot(2,2,3);
kE_diss = Ixsecs.UE3*kX1_E3 + Ixsecs.Uapp1*kX1_app1 ...
        + Ixsecs.USum*kX1_Sum;
kE_iz = zeros(size(Te));
for j = 1:3
    kE_iz = kE_iz + Kxsecs.UX1(j)*kX1_iz(j,:);
end
semilogy(Te,kE_diss,'b');
hold on; plot(Te,kE_iz,'r');
% hold on; plot(Te,25*kX1_di,'g');
%hold on; plot(Te,15.6*kiz0,'g'); % from itikawa
%hold on; plot(Te,Ixsecs.Ua1*kX1_a1,'r');
xlabel('Te [eV]'); ylabel('kE [eV-cm^3/s]');
legend('diss','iz','di','location','SE');
axis([1 15 1e-10 1e-6]); title('energy loss to diss and ionization');
%
subplot(2,2,4);
kE_diss = Ixsecs.UE3*kX1_E3 + Ixsecs.Uapp1*kX1_app1 ...
        + Ixsecs.USum*kX1_Sum;
semilogy(Te,kE_triplets+kE_singlets+kE_diss+kE_iz,'black');
hold on; plot(Te,kE_singlets,'b');
hold on; plot(Te,kE_triplets,'r');
hold on; plot(Te,kE_diss,'g');
%hold on; plot(Te,kE_iz+25*kX1_di,'magenta');
xlabel('Te [eV]'); ylabel('kE [eV-cm^3/s]');
legend('total','sing','trip','diss','izn','location','SE');
axis([1 10 1e-9 1e-6]); title('energy loss channels');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%               write rate constants to a file
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if(write_data)
    
    N2_rateconstants.Te = Te;
    
    %%%   excitations from ground state
    %
    N2_rateconstants.X1_A3.k = kX1_A3;
    N2_rateconstants.X1_A3.U = Ixsecs.UA3;
    %
    N2_rateconstants.X1_B3.k = kX1_B3;
    N2_rateconstants.X1_B3.U = Ixsecs.UB3;
    %
    N2_rateconstants.X1_W3.k = kX1_W3;
    N2_rateconstants.X1_W3.U = Ixsecs.UW3;
    %
    N2_rateconstants.X1_Bp3.k = kX1_Bp3;
    N2_rateconstants.X1_Bp3.U = Ixsecs.UBp3;
    %
    N2_rateconstants.X1_ap1.k = kX1_ap1;
    N2_rateconstants.X1_ap1.U = Ixsecs.Uap1;
    %
    N2_rateconstants.X1_a1.k = kX1_a1;
    N2_rateconstants.X1_a1.U = Ixsecs.Ua1;
    %
    N2_rateconstants.X1_w1.k = kX1_w1;
    N2_rateconstants.X1_w1.U = Ixsecs.Uw1;
    %
    N2_rateconstants.X1_C3.k = kX1_C3;
    N2_rateconstants.X1_C3.U = Ixsecs.UC3;
    %
    N2_rateconstants.X1_E3.k = kX1_E3;
    N2_rateconstants.X1_E3.U = Ixsecs.UE3;
    %
    N2_rateconstants.X1_app1.k = kX1_app1;
    N2_rateconstants.X1_app1.U = Ixsecs.Uapp1;
    %
    N2_rateconstants.X1_Sum.k = kX1_Sum;
    N2_rateconstants.X1_Sum.U = Ixsecs.USum;
    
    
    %%%   state-to-state ionization
    %
    N2_rateconstants.X1_iz.k = kX1_iz;  % includes three final ion states
    N2_rateconstants.X1_iz.U = Kxsecs.UX1;
    %
    N2_rateconstants.A3_iz.k = kA3_iz; 
    N2_rateconstants.A3_iz.U = Kxsecs.UA3;
    %
    N2_rateconstants.B3_iz.k = kB3_iz;  
    N2_rateconstants.B3_iz.U = Kxsecs.UB3;
    %
    N2_rateconstants.W3_iz.k = kW3_iz;
    N2_rateconstants.W3_iz.U = Kxsecs.UW3;
    %
    N2_rateconstants.Bp3_iz.k = kBp3_iz; 
    N2_rateconstants.Bp3_iz.U = Kxsecs.UBp3;
    %
    N2_rateconstants.ap1_iz.k = kap1_iz; 
    N2_rateconstants.ap1_iz.U = Kxsecs.Uap1;
    %
    N2_rateconstants.a1_iz.k = ka1_iz; 
    N2_rateconstants.a1_iz.U = Kxsecs.Ua1;
    %
    N2_rateconstants.w1_iz.k = kw1_iz;  
    N2_rateconstants.w1_iz.U = Kxsecs.Uw1;
    %
    N2_rateconstants.C3_iz.k = kC3_iz;  
    N2_rateconstants.C3_iz.U = Kxsecs.UC3;
    
    
    %%%   state-to-state dissociation from excited states
    %
    N2_rateconstants.X1_diss.k = kXSS;
    N2_rateconstants.X1_diss.U = UD(1);
    %
    N2_rateconstants.A3_diss.k = kASS;
    N2_rateconstants.A3_diss.U = UD(2);
    %
    N2_rateconstants.B3_diss.k = kBSD;
    N2_rateconstants.B3_diss.U = UD(3);
    %
    N2_rateconstants.W3_diss.k = kWSD;
    N2_rateconstants.W3_diss.U = UD(4);
    %
    N2_rateconstants.Bp3_diss.k = kBpSP;
    N2_rateconstants.Bp3_diss.U = UD(5);
    %
    N2_rateconstants.ap1_diss.k = kapDD;
    N2_rateconstants.ap1_diss.U = UD(6);
    %
    N2_rateconstants.a1_diss.k = kaDD;
    N2_rateconstants.a1_diss.U = UD(7);
    %
    N2_rateconstants.w1_diss.k = kwDD;
    N2_rateconstants.w1_diss.U = UD(8);
    %
    N2_rateconstants.C3_diss.k = kCSD;
    N2_rateconstants.C3_diss.U = UD(9);
    
    
    %%%   elastic energy exchange and momentum exchange (from mobility)
    %
    N2_rateconstants.X1_elm = kX1_elm;
    N2_rateconstants.X1_mom = kX1_mom;
    %
    save('N2_rateconstants.mat','N2_rateconstants');
    
end

figure(100);
loglog(Te,kX1_elm);


end