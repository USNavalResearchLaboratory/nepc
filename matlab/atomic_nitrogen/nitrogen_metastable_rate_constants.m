function nitrogen_metastable_rate_constants
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    this function computes rate constants for thermal reactions
%%%    with metastable atomic nitrogen (NI and NII)
%%%
%%%    See nitrogen_metastable_xsecs for information on xsecs
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

write_data = 0;
plot_excitation = 1;
plot_ionization = 1;
addpath('../');

%%% load cross sections for state-to-state excitation and ionization
%
load('./nitrogen_metastable_xsecs.mat');
x = nitrogen_xsecs;

Te = [0.3:0.1:5 6:1:20 30:10:100];

for i = 1:length(Te)
    
    k4S2D(i) = MaxRateConst(x.U4S2D,x.E4S2D,x.Q4S2D,Te(i),1);
    k4S2P(i) = MaxRateConst(x.U4S2P,x.E4S2P,x.Q4S2P,Te(i),1);
    k2D2P(i) = MaxRateConst(x.U2D2P,x.E2D2P,x.Q2D2P,Te(i),0);
    %
    k3P1D(i) = MaxRateConst(x.U3P1D,x.E3P1D,x.Q3P1D,Te(i),1);
    k3P1S(i) = MaxRateConst(x.U3P1S,x.E3P1S,x.Q3P1S,Te(i),1);
    k1D1S(i) = MaxRateConst(x.U1D1S,x.E1D1S,x.Q1D1S,Te(i),1);
    %
    for j = 1:3
        k4Siz(j,i) = MaxRateConst(x.U4Siz(j),x.E4Siz,x.Q4Siz(j,:),Te(i),0);
        k2Diz(j,i) = MaxRateConst(x.U2Diz(j),x.E2Diz,x.Q2Diz(j,:),Te(i),0);
        k2Piz(j,i) = MaxRateConst(x.U2Piz(j),x.E2Piz,x.Q2Piz(j,:),Te(i),0);
        kNIIiz(j,i) = MaxRateConst(x.UNIIiz(j),x.ENIIiz,x.QNIIiz(j,:),Te(i),0);
    end
    
    
end


if(plot_excitation);
    
    close(figure(1));
    f1 = figure(1); set(f1,'position',[0 0 400 800]);
    %
    subplot(2,1,1);
    plot(Te,k4S2D,'b');
    hold on; plot(Te,k4S2P,'r');
    hold on; plot(Te,k2D2P,'g');
    xlabel('Te [eV]'); ylabel('k [cm^3/s]');
    legend('^4S->^2D','^2D->^2P','^2D->^2P', ...
           'location','NE');
    axis([1 20 0 1.2e-8]); title('metastable transitions with NI');
    %
    %
    subplot(2,1,2);
    plot(Te,k3P1D,'b');
    hold on; plot(Te,k3P1S,'r');
    hold on; plot(Te,k1D1S,'g');
    xlabel('Te [eV]'); ylabel('k [cm^3/s]');
    legend('^3P->^1D','^3P->^1S','^1D->^1S', ...
           'location','NE');
    axis([1 20 0 1.2e-8]); title('metastable transitions with NII');

end

if(plot_ionization==1)
    close(figure(2)); f2=figure(2); set(f2,'position',[500 0 800 800]);
    subplot(2,2,1); plot(Te,sum(k4Siz),'black');
    hold on; plot(Te,k4Siz);
    axis([1 20 0.0 4e-8]);
    xlabel('T_e [eV]'); ylabel('k [cm^3/s]');
    title('e+N(^4S)->e+N^+(^3P,^1D,^1S)');
    legend('total','^4S->^3P','^4S->^1D','^4S->^1S','location','NW');
    %
    subplot(2,2,2);
    plot(Te,sum(k2Diz),'black');
    hold on; plot(Te,k2Diz);
    axis([1 20 0.0 4e-8]);
    xlabel('T_e [eV]'); ylabel('k [cm^3/s]');
    title('e+N(^2D)->e+N^+(^3P,^1D,^1S)');
    legend('total','^2D->^3P','^2D->^1D','^2D->^1S','location','NW');
    %
    subplot(2,2,3);
    plot(Te,sum(k2Piz),'black');
    hold on; plot(Te,k2Piz);
    axis([1 20 0.0 4e-8]);
    xlabel('T_e [eV]'); ylabel('k [cm^3/s]');
    title('e+N(^2P)->e+N^+(^3P,^1D,^1S)');
    legend('total','^2P->^3P','^2P->^1D','^2P->^1S','location','NW');
    %
    subplot(2,2,4);
    plot(Te,kNIIiz);
    axis([1 40 0.0 2e-8]);
    xlabel('T_e [eV]'); ylabel('k [cm^3/s]');
    title('e+N+(^3P,^1D,^1S)->e+N^+^+');
    legend('^3P','^1D','^1S','location','NW');
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if(write_data)
    
    nitrogen_krates.Te = Te;  % [eV]
    %
    nitrogen_krates.k4S2D = k4S2D;    % [cm^2]
    nitrogen_krates.U4S2D = x.U4S2D;  % [eV]
    %
    nitrogen_krates.k4S2P = k4S2P;  % [cm^2]
    nitrogen_krates.U4S2P = x.U4S2P;  % [eV]
    %
    nitrogen_krates.k2D2P = k2D2P;  % [cm^2]
    nitrogen_krates.U2D2P = x.U2D2P;  % [eV]
    %
    nitrogen_krates.k3P1D = k3P1D;  % [cm^2]
    nitrogen_krates.U3P1D = x.U3P1D;  % [eV]
    %
    nitrogen_krates.k3P1S = k3P1S;  % [cm^2]
    nitrogen_krates.U3P1S = x.U3P1S;  % [eV]
    %
    nitrogen_krates.k1D1S = k1D1S;  % [cm^2]
    nitrogen_krates.U1D1S = x.U1D1S;  % [eV]
    %
    %
    %
    nitrogen_krates.k4Siz = k4Siz;  % [cm^2]
    nitrogen_krates.U4Siz = x.U4Siz;  % [eV]
    %
    nitrogen_krates.k2Diz = k2Diz;  % [cm^2]
    nitrogen_krates.U2Diz = x.U2Diz;  % [eV]
    %
    nitrogen_krates.k2Piz = k2Piz;  % [cm^2]
    nitrogen_krates.U2Piz = x.U2Piz;  % [eV]
    %
    nitrogen_krates.kNIIiz = kNIIiz;  % [cm^2]
    nitrogen_krates.UNIIiz = x.UNIIiz;  % [eV]
    
    save('nitrogen_metastable_rate_constants.mat','nitrogen_krates');
    
end


end