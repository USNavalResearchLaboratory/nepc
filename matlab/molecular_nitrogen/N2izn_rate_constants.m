%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    this script compares rate constants for N2 ionization using
%%%    different cross sections and a Maxwellian EEDF
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
Qizn_I = Ixsecs.Qizn;
Eizn_I = Ixsecs.Eizn;

Te = [0.3:0.1:5 6:1:20 25:5:100 125:25:200];
for i = 1:length(Te)
    
    kizn_I(i)  = MaxRateConst(15.6,Ixsecs.Eizn,Ixsecs.Qizn,Te(i),0);
    kdizn_I(i) = MaxRateConst(15.6,Ixsecs.Eizn,Ixsecs.Qdizn,Te(i),0);
    %
    for j = 1:3 % number of ionic states of N2
        kX1_iz(j,i) = MaxRateConst(Kxsecs.UX1(j),Kxsecs.E, ...
                             Kxsecs.QX1(j,:),Te(i),0);              
    end

    Te(i)
end

figure(3); plot(Te,kizn_I,'b');
hold on; plot(Te,sum(kX1_iz),'r');

figure(4); plot(Te,kdizn_I,'b'); title('dissociative ionization total');
