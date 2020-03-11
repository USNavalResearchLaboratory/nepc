function O2_rate_constants
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    this function computes rate constants for thermal reactions
%%%    with molecular oxygen using a Maxwellian EEDF
%%%
%%%    attachment is from Phelps
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
write_data = 0;
addpath('../');

%%%   Phelps Diss-attach (e+O2 => e + O + O-)
%
Eatt = [4.4 4.9 5.38 5.86 6.10 6.48 6.77 7.05 7.30 7.53 7.77 8.00 ...
        8.25 8.73 9.20 9.68 10.15 100]; % [eV]
Qatt = [0 0 0.23 0.72 1.08 1.38 1.52 1.56 1.48 1.31 1.10 0.84 0.54  ...
        0.28 0.14 0.08 0 0]*1e-18;    % [cm^2]
    
%%%   Itikawa Diss-attach (e+O2 => e + O + O-)
%
Eatt2 = [4.2:0.1:6.3 6.5:0.1:9.6 9.8 9.9]; % [eV]
Qatt2 = [0 8.8e-5 2.64e-4 4.40e-4 7.04e-4 9.68e-4 1.32e-3 1.76e-3 2.20e-3 ...
         2.90e-3 3.61e-3 4.49e-3 5.37e-3 6.33e-3 7.48e-3 8.53e-3 ...
         9.59e-3 1.05e-2 1.14e-2 1.23e-2 1.31e-2 1.36e-2 1.41e-2 1.40e-2 ...
         1.37e-2 1.34e-2 1.28e-2 1.22e-2 1.14e-2 1.06e-2 9.85e-3 8.97e-3 8.18e-3 ...
         7.39e-3 6.42e-3 5.72e-3 5.01e-3 4.49e-3 3.87e-3 3.34e-3 2.82e-3 2.38e-3 ...
         2.02e-3 1.67e-3 1.41e-3 1.23e-3 1.06e-3 8.80e-4 7.04e-4 7.04e-4 6.16e-4 ...
         5.28e-4 4.40e-4 4.40e-4 3.52e-4 3.52e-4]*1e-16;    % [cm^2]
    
%%%   3-body (e+O2+(O2,N2) => e + O2- + (O2,N2))
%
Eatt3b = [0 5.8e-2 7.3e-2 8.3e-2 8.9e-2 9.5e-2 1.03e-1 1.09e-1 1.50e-1 ...
          1.70e-1 0.2 0.21 0.23 0.32 0.33 0.35 0.44 0.45 0.47 0.56 0.57 0.59 0.68 ...
          0.69 0.71 0.79 -.8 0.82 0.9 0.91 0.93 1.02 1.03 1.05 1.5]; % [eV]
Qatt3b = [0 0 5.61e-1 1.8 0.42 0.84 1.8 0 0 0 0 0.357 0 0 0.23 0 0 ...
          0.145 0 0 0.11 0 0 0.08 0 0 0.07 0 0 0.055 0 0 0.042 0 0]*1e-40*1e4;    % [cm^2/N]

Te = [0.3:0.1:5 6:1:20 25:5:100 125:25:200];
%Te = [0.5 1 3 5 7 10 20 50];
for i = 1:length(Te)
    
    k_O2att(i)  = MaxRateConst(4.9,Eatt,Qatt,Te(i),1);
    k_O2att2(i) = MaxRateConst(4.3,Eatt2,Qatt2,Te(i),1);
    K_O2att3b(i) = MaxRateConst(5.8e-2,Eatt3b,Qatt3b,Te(i),1);

end
close(figure(1));
f1 = figure(1); set(f1,'position',[0 0 800 800]);
plot(Te,k_O2att,'b'); 
hold on; plot(Te,k_O2att2,'r'); 
hold on; plot(Te,K_O2att3b*3.22e16*760,'g');
legend('e+O_2=>e+O+O^- (Phelps)', 'e+O_2=>e+O+O^- (Itikawa)','3body at 1atm');
xlabel('electron energy [eV]'); axis([0 50 0 4e-11]);
ylabel('k [cm^3/s]'); title('Oxygen Attachment Rate Constants');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%               write rate constants to a file
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if(write_data)
    
    O2_rateconstants.Te = Te;
    
    %%%   attachment from ground state
    %
    O2_rateconstants.X1_A3.k = k_O2att2;
    O2_rateconstants.X1_A3.U = 3/2*Te;
    

    save('O2_rateconstants.mat','O2_rateconstants');
    
end



end