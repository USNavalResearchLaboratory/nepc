%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    write N2 cross sections from Itikawa 2005
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear all;
write_data = 0;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   set triplet excitation cross sections from Tables 8
%%%

%%% e + N2(X1) => e + N2(A3Sigma)
%
EA3 = [6.169 7.65 7.96 8.26 8.52 8.74 9.57 10.4 10.96 11.53 11.88 11.97 12.10 12.23 ...
       12.54 13.15 13.90 14.85 15:1:20 25:5:50];
QA3 = [0 0.005 0.048 0.085 0.125 0.137 0.153 0.168 0.183 0.226 0.251 0.254 0.257 0.254 0.239 0.202 ...
       0.180 0.162 0.160 0.152 0.145 0.138 0.132 0.126 0.099 0.078 0.062 0.049 0.038 0.030]*1e-16;

%%% e + N2(X1) => e + N2(B3Pi)
%
EB3 = [7.353 8.55 9:0.5:15 16:1:20 25:5:50];
QB3 = [0 0.002 0.141 0.202 0.250 0.287 0.313 0.330 0.338 0.339 0.333 0.323 0.308 ...
      0.290 0.270 0.224 0.199 0.177 0.159 0.144 0.092 0.064 0.049 0.036 0.028 0.023]*1e-16;

%%% e + N2(X1) => e + N2(W3Delta)
%
EW3 = [7.362 9:0.5:15 16 16.5 17 18 19 20:5:50];
QW3 = [0 0.017 0.045 0.072 0.096 0.119 0.140 0.159 0.176 0.191 0.205 0.216 0.224 ...
       0.231 0.238 0.238 0.236 0.227 0.209 0.194 0.131 0.088 0.059 0.040 0.027 0.018]*1e-16;

%%% e + N2(X1) => e + N2(Bp3Sigma)
%
EBp3 = [8.165 10:0.5:20 25:5:50];
QBp3 = [0 0.007 0.008 0.019 0.037 0.058 0.082 0.105 0.125 0.143 0.155 0.163 0.165 ...
        0.162 0.153 0.140 0.124 0.110 0.101 0.093 0.086 0.080 0.041 0.024 0.015 ...
        0.010 0.007 0.005]*1e-16;


close(figure(11)); f11=figure(11); set(f11,'position',[0 0 800 300]);
subplot(1,2,1);
plot(EA3,QA3/1e-16); 
hold on; plot(EB3,QB3/1e-16,'r'); axis('square')
hold on; plot(EW3,QW3/1e-16,'g');
hold on; plot(EBp3,QBp3/1e-16,'magenta');
legend('A^3\Sigma','B^3\Pi','W^3\Delta','B''^3\Sigma');
xlabel('electron energy [eV]');
ylabel('\sigma [10^-^1^6 cm^2]');
%title('triplet excitation from Itikawa');
axis([0 60 0 0.4]);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 
%%%   set singlet excitation cross sections from Table 9 and 10
%%%

%%% e + N2(X1) => e + N2(ap1Sigma)
%
Eap1 = [8.399 9.4 9.5 10:0.5:19 20:5:50];
Qap1 = [0 0.006 0.011 0.031 0.042 0.051 0.059 0.069 0.080 0.091 0.101 0.110 ...
        0.113 0.113 0.107 0.095 0.079 0.063 0.056 0.050 0.045 0.041 0.034 ...
        0.018 0.014 0.012 0.011 0.010 0.010]*1e-16;
    
%%% e + N2(X1) => e + N2(a1Pi)
%
Ea1 = [8.549 8:0.5:10 11:1:15 15.5:0.5:18 19 21.5 25:5:50 60:10:100];
Qa1 = [0 0.001 0.016 0.038 0.066 0.099 0.174 0.254 0.329 0.394 0.443 0.459 0.469 ...
       0.473 0.471 0.462 0.446 0.394 0.300 0.258 0.215 0.185 0.161 0.144 0.129 ...
       0.108 0.092 0.081 0.072 0.065]*1e-16;
      
%%% e + N2(X1) => e + N2(w1Delta)
%
Ew1 = [8.89 8.9 9:0.5:16 17:1:20 25:5:50];
Qw1 = [0 1e-4 2e-3 0.024 0.043 0.061 0.076 0.088 0.096 0.102 0.105 0.105 0.103 ...
       0.099 0.093 0.086 0.078 0.062 0.049 0.044 0.04 0.026 0.018 0.013 0.01 0.008 0.006]*1e-16;
   
%%% e + N2(X1) => e + N2(app1Sigma)
%
Eapp1 = [12.255 12.25 13:1:25 27.5 30:5:50];
Qapp1 = [0 0 9e-3 0.022 0.033 0.042 0.05 0.056 0.06 0.063 0.064 0.063 0.062 ...
         0.059 0.055 0.044 0.035 0.025 0.02 0.016 0.014]*1e-16;
   
   
close(figure(2)); f2=figure(2); set(f2,'position',[0 600 800 300]);
subplot(1,2,1);
plot(Eap1,Qap1/1e-16); axis('square');
hold on; plot(Eapp1,Qapp1/1e-16,'r');
hold on; plot(Ew1,Qw1/1e-16,'g');
legend('a''^1\Sigma','a''''^1\Sigma','w^1\Delta');
xlabel('electron energy [eV]');
ylabel('\sigma [10^-^1^6 cm^2]');
%title('singlet excitation from Itikawa');
axis([0 60 0 0.14]);
%
subplot(1,2,2);
plot(Ea1,Qa1/1e-16,'b'); axis([0 120 0 0.6]); axis('square');
legend('a^1\Pi');
xlabel('electron energy [eV]');
ylabel('\sigma [10^-^1^6 cm^2]');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% 
%%%   set triplet excitation cross sections from Table 10
%%%

%%% e + N2(X1) => e + N2(C3Pi)
%
EC3 = [11:0.5:15 15.7 16:0.5:20 25:5:50];
QC3 = [0.001 0.074 0.147 0.229 0.335 0.455 0.551 0.583 0.551 0.478 0.447 0.403 0.353 ...
       0.302 0.276 0.258 0.242 0.226 0.212 0.122 0.077 0.052 0.038 0.028 0.022]*1e-16;

%%% e + N2(X1) => e + N2(E3Sigma)
%
EE3 = [11.875 11.9 11.95 12 12.5 13:1:21 25:5:50];
QE3 = [0 0.148 0.120 0.095 0.029 0.02 0.008 0.003 0.002 0.004 0.007 0.01 ...
       0.012 0.012 0.009 0.007 0.005 0.003 0.0025 0.0018]*1e-16;

%close(figure(3)); figure(3);
figure(11); subplot(1,2,2);
plot(EC3,QC3/1e-16,'b'); axis([0 60 0 0.6]);
hold on; plot(EE3,QE3/1e-16,'r');
legend('C^3\Pi', 'E^3\Sigma');
xlabel('electron energy [eV]');
ylabel('\sigma [10^-^1^6 cm^2]');
%title('singlet excitation from Itikawa');

%figure(1); hold on; plot(EE3,QE3/1e-16,'cyan');
%legend('A^3\Sigma','B^3\Pi','W^3\Delta','B^3\Sigma','E^3\Sigma');


%%%  excitation of optically allowed sum of singlet states from Phelps
%%%  e + N2(X1) => e + N2(b1Pi + b'1Sigma + c'1Sigma)
%%%  These states are believed to all predissociate
%
ESum = [13:1:18 20 22 25 30 40 60 80 100 150 200 250 300 500 700 1e3];
QSum = [0 0.081 0.19 0.25 0.42 0.52 0.75 0.96 1.19 1.48 1.65 1.76 ...
        1.68 1.58 1.33 1.16 1.05 0.96 0.74 0.64 0.53]*1e-16;     

close(figure(4)); figure(4);    
plot(ESum,QSum*1e16);
xlabel('electron energy (eV)'); ylabel('\sigma (10^-^1^6 cm^2)');
title('Sum of singlets from Phelps');


%%%  v=0 -> v=1 from Itikawa
%
Evib = [0.5 1.0 1.5 1.98 2.1 2.46 2.605 3.0 5.0 7.5 10 15 18 20. 22.5 25 30];
Qvib = [0.005 0.009 0.089 4.560 1.970 1.650 4.400 1.370 0.080 0.031 0.015 ...
        0.039 0.076 0.195 0.126 0.082 0.027]*1e-16;     

close(figure(44)); figure(44);    
plot(Evib,Qvib*1e16);
xlabel('electron energy (eV)'); ylabel('\sigma (10^-^1^6 cm^2)');
title('e+N_2(X^1,v=0) => e+N_2(X^1,v=1)');


%%%   elastic momentum transfer from Itikawa (E=200->1000 from siglo
%%%   database, which is from Phelps and Pitchford)
%%%
Eelm = [0 1e-3 0.0015 0.0018 0.002 0.0025 0.003 0.004 0.005 0.006 0.007 ...
        0.008 0.009 0.01 0.012 0.015 0.018 0.02 0.025 0.03 0.04 0.05 ...
        0.06 0.07 0.08 0.09 0.1 0.12 0.15 0.18 0.2 0.25 0.3:0.1:1 1.5 ...
        1.92 1.98 2.46 2.605 4:1:10 12 15 18 20 25 30:10:100 200 300 ...
        500 700 1000];
Qelm = [1.1 1.357 1.426 1.464 1.490 1.550 1.620 1.718 1.810 1.908 2.000 ...
        2.062 2.131 2.191 2.342 2.550 2.729 2.850 3.12 3.40 3.85 4.33 ...
        4.72 5.10 5.41 5.69 5.95 6.45 7.10 7.59 7.90 8.50 9.00 9.70 ...
        10.16 10.65 10.87 11.00 11.03 11.07 11.12 17.40 18.03 16.65 ...
        12.38 10.90 9.90 9.45 9.29 9.19 9.29 9.45 9.84 9.97 9.07 8.20 ...
        7.25 6.80 6.31 5.60 4.51 3.59 2.94 2.50 2.19 0.8 0.48 0.23 ...
        0.143 0.07]*1e-16;


%%%   effective momentum tranfer from Phelps 1985
%%%   Qeff = Qelm + sum(Qinel)
%%%
Eeff = [0:1e-3:3e-3 5e-3 7e-3 8.5e-3 1e-2 1.5e-2 2e-2 3e-2 4e-2 5e-2 ...
        7e-2 1e-1 1.2e-1 1.5e-1 1.7e-1 2e-1:5e-2:4e-1 5e-1 7e-1 1.0 1.2 ...
        1.3 1.5 1.7 1.9 2.1 2.2 2.5 2.8 3.0 3.3 3.6 4 4.5 5 6 7 8 10 12 ...
        15 17 20 25 30 50 75 100 150 200 300 500 700 1e3 1.5e3 2e3 3e3 ...
        5e3 7e3 1e4];

Qeff = [1.1 1.36 1.49 1.62 1.81 2 2.1 2.19 2.55 2.85 3.4 3.85 4.33 5.1 ...
        5.95 6.45 7.1 7.4 7.9 8.5 9.0 9.4 9.7 9.9 10 10 10.4 11 12 13.8 ...
        19.6 27 28.5 30 28 21.7 17.2 14.7 12.6 11.3 10.9 10.4 10.1 10 ...
        10.4 10.9 11 10.7 10.2 9.5 9.0 8.6 6.6 5.8 4.9 4.2 3.3 2.44 ...
        1.96 1.55 1.12 0.81 0.63 0.4 0.29 0.21]*1e-16; % [cm^2]


    
%%%   ionization cross sections from Itikawa
%
Eizn = [15.6 16:0.5:25 30:5:40 45:5:100 110 120:20:200 225:25:300 ...
            350:50:1e3];
Qizn = [0 0.0211 0.0466 0.0713 0.0985 0.129 0.164 0.199 0.230 0.270 ...
            0.308 0.344 0.380 0.418 0.455 0.492 0.528 0.565 0.603 ...
            0.640 0.929 1.16 1.37 1.52 1.60 1.66 1.72 1.74 1.78 1.80 ...
            1.81 1.82 1.83 1.85 1.85 1.83 1.81 1.78 1.72 1.67 1.61 ...
            1.55 1.48 1.41 1.37 1.28 1.20 1.11 1.05 0.998 0.943 0.880 ...
            0.844 0.796 0.765 0.738 0.719 0.698 0.676]*1e-16; % X2+A2+B2
Qdizn = [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.0325 0.0904 ...
            0.166 0.245 0.319 0.390 0.438 0.482 0.523 0.561 0.587 ...
            0.605 0.632 0.645 0.656 0.660 0.661 0.652 0.633 0.595 ...
            0.566 0.516 0.493 0.458 0.438 0.393 0.351 0.324 0.299 ...
            0.274 0.248 0.234 0.217 0.205 0.200 0.192 0.183 0.176 ...
            0.167]*1e-16;
    
        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if(write_data)
    
    Itikawa_xsecs.EA3 = EA3;   % [eV]
    Itikawa_xsecs.QA3 = QA3;   % [cm^2]
    Itikawa_xsecs.UA3 = 6.17;  % [eV]
    %
    Itikawa_xsecs.EB3 = EB3;  
    Itikawa_xsecs.QB3 = QB3;   
    Itikawa_xsecs.UB3 = 7.353;  
    %
    Itikawa_xsecs.EW3 = EW3;  
    Itikawa_xsecs.QW3 = QW3;   
    Itikawa_xsecs.UW3 = 7.362;  
    %
    Itikawa_xsecs.EBp3 = EBp3;  
    Itikawa_xsecs.QBp3 = QBp3;   
    Itikawa_xsecs.UBp3 = 8.165;  
    %
    Itikawa_xsecs.Eap1 = Eap1;  
    Itikawa_xsecs.Qap1 = Qap1;   
    Itikawa_xsecs.Uap1 = 8.399;  
    %
    Itikawa_xsecs.Ea1 = Ea1;  
    Itikawa_xsecs.Qa1 = Qa1;   
    Itikawa_xsecs.Ua1 = 8.549;  
    %
    Itikawa_xsecs.Ew1 = Ew1;  
    Itikawa_xsecs.Qw1 = Qw1;   
    Itikawa_xsecs.Uw1 = 8.890;  
    %
    Itikawa_xsecs.EC3 = EC3;  
    Itikawa_xsecs.QC3 = QC3;   
    Itikawa_xsecs.UC3 = 11.032;  
    %
    Itikawa_xsecs.EE3 = EE3;  
    Itikawa_xsecs.QE3 = QE3;   
    Itikawa_xsecs.UE3 = 11.875;  
    %
    Itikawa_xsecs.Eapp1 = Eapp1;  
    Itikawa_xsecs.Qapp1 = Qapp1;   
    Itikawa_xsecs.Uapp1 = 12.255;  
    %
    Itikawa_xsecs.ESum = ESum;  
    Itikawa_xsecs.QSum = QSum;   
    Itikawa_xsecs.USum = 13.0;  
    %
    Itikawa_xsecs.Eizn = Eizn;
    Itikawa_xsecs.Qizn = Qizn;
    Itikawa_xsecs.Uizn = 15.6;
    %
    Itikawa_xsecs.Edizn = Eizn;
    Itikawa_xsecs.Qdizn = Qdizn;
    Itikawa_xsecs.Udizn = 25;
    %
    Itikawa_xsecs.Eelm = Eelm;
    Itikawa_xsecs.Qelm = Qelm;
    Itikawa_xsecs.mM = 1.95e-5;
    %
    Itikawa_xsecs.Eeff = Eeff;
    Itikawa_xsecs.Qeff = Qeff;
%
    save('../../Xsecs/Itikawa_xsecs.mat','Itikawa_xsecs');
    
end



