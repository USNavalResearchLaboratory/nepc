function N2_dissociation
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%          this script compares different data sets 
%%%          for dissociation of molecular nitrogen (N2)
%%%          
%%%          It also extrapolates to high energy using
%%%          the functional form in Eq. 4 of Taylor 1988
%%%          and creates xsecs for diss. from N2(A)
%%%
%%%          See Zipf 1980, Taylor 1988, and Itikawa 2005
%%%
writedata = 0;
plot_Bacri   = 0;
plot_Itikawa = 1;
plot_Zipf    = 1;
plot_compare = 0;
plot_from_excited = 0;
scrsz = get(0,'ScreenSize');


%%% set some needed constants
%
R = 13.6;       % hydrogen ionization potential [eV]
mc2 = 0.511e6;  % electron rest mass energy [eV]
a0  = 5.29e-9;  % bohr radius [cm]
%
E = [0 10.^(0:0.02:7)];   % kinetic energy grid (eV)
gamma = E/(mc2)+1;
beta = sqrt(1-1./gamma.^2);
ET = 0.5*mc2*beta.^2;     % 1/2mv^2 (E used in Taylor 1988)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%     dissociation of N2(X3Sigam, A3Sigma, B3Pi, a'1Sigma,
%%%                        a1Pi, C3Pi, E3Sigma) from Bacri 1982
%%%

x = [1.5:0.5:11.5 13:1:27 35:5:50];  % electron energy [eV]
%
sigdX0 = [0 0 0 0 0 0 0  0 0 0 0 0 0 0 0 0 0 0.003 0.023 0.048 0.068 ...
          0.184 0.347 0.509 0.682 0.852 0.979 1.063 1.131 1.193 1.254 ...
          1.307 1.344 1.377 1.407 1.429 1.501 1.468 1.419 1.337]*1e-16; % [cm^2]
%
sigdA0 = [0 0 0 0 0 0 0 0 0.011 60.643 106.59 116.46 123.45 128.39 131.79 134.30 135.70 ...
           136.38 136.49 136.17 135.51 132.13 129.20 125.99 122.66 119.29 ...
           115.95 112.69 109.52 106.46 103.51 100.69 97.980 95.391 93.102 ...
           90.701 76.420 69.045 62.957 57.860]*1e-16; % [cm^2]
%
sigdB0 = [0 0 0 0 0 0 0 0 4.732 17.491 25.493 29.119 31.761 33.709 35.138 36.170 36.890 ...
          37.366 37.648 37.775 37.779 37.273 36.662 35.926 35.118 34.272 ...
          33.413 32.555 31.710 30.884 30.082 29.306 28.558 27.838 27.147 ...
          26.483 22.061 19.944 18.193 16.724]*1e-16; % [cm^2]
%
sigdap0= [0 0 0 0 0 0 0 0 0 0 0.239 0.536 0.699 0.818 0.908 0.978 1.033 1.076 1.109 ...
          1.135 1.154 1.182 1.184 1.178 1.166 1.150 1.131 1.111 1.090 ...
          1.068 1.046 1.024 1.002 0.980 0.959 0.939 0.796 0.724 0.664 0.613]*1e-16; % [cm^2]
%
sigda0 = [0 0 0 0 0 0 0 0 0 0.199 1.454 2.779 4.033 6.435 6.103 7.462 8.014 8.441 8.774 ...
          9.417 9.708 10.435 10.668 10.747 10.745 10.687 10.588 10.461 10.315 ...
          10.155 9.986 9.811 9.635 9.457 9.280 9.105 7.832 7.169 6.599 6.103]*1e-16; % [cm^2]
%
sigdC0 = [0.003 8.660 176.39 203.81 213.65 214.79 211.46 205.86 199.17 192.06 ...
          184.89 177.89 171.15 164.73 158.65 152.92 147.52 142.45 137.68 ...
          133.19 129.97 117.70 111.20 105.37 100.11 95.362 91.045 87.108 ...
          83.503 80.192 77.139 74.316 71.699 69.265 66.997 64.877 51.887 ...
          46.192 41.667 37.982]*1e-16; % [cm^2]
%
[sigdX_B,sigdX_B_fit] = TaylorExtrap(x,sigdX0,9.75,2);
[sigdA_B,sigdA_B_fit] = TaylorExtrap(x,sigdA0,9.75-6.2+2.4,2);
%
if(plot_Bacri==1)
    close(figure(1));
    figure(1);
    loglog(x,sigdX0,'b*');
    %hold on; loglog(E,sigdX_B,'black','linewidth',2);
    hold on; loglog(x,sigdA0,'g*');
    hold on; loglog(x,sigdB0,'r*');
    hold on; loglog(x,sigdC0,'cyan*');
    %hold on; plot(E,sigdA_B/10,'magenta','linewidth',2);
    xlabel('electron energy [eV]');
    ylabel('\sigma [cm^2]');
    legend('e+N_2(X)=>e+2N','extrapolated','e+N_2(A)=>e+2N','extrapolated', ...
           'location','SE');
    title('Dissociation from Bacri 1982');
    axis([0 1e3 1e-19 3e-15]);
    annotation('textarrow', [0.26 0.24], [0.78 0.84], ...
               'string','\sigma_m_d_x/10');
end

%%%       
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%     dissociation of N2(X1Sigam, A3Sigma, B3Pi, W3Delta, B'3Sigma,
%%%                        a'1Sigma, a1Pi, w1Delta, 
%%%                        C3Pi) from Annaloro 2014
%%%

U  = [0     6.17  7.35  7.36  8.17  8.40 8.55 8.89 11.0];
re = [1.098 1.286 1.213 1.27  1.27  1.28 1.23 1.27 1.149]*1e-8; % mean internuc distance [cm]
Ud = [9.75  9.75  12.13 12.13 13.33 14.5 14.5 14.5 12.13];
Eann = 1:1:100;  % electron energy [eV]
for j = 1:length(re)
    for i = 1:length(Eann)
        if(Eann(i)<=Ud(j)-U(j))
            Qd_ann(j,i) = 0;
        else
            Qd_ann(j,i) = pi*re(j)^2*(Ud(j)-U(j))/Eann(i);
        end
    end
end

plot_ann = 0;
if(plot_ann==1)
    close(figure(11));
    figure(11);
    loglog(Eann,Qd_ann(1,:),'black*');
    %hold on; loglog(E,sigdX_B,'black','linewidth',2);
    hold on; loglog(Eann,Qd_ann(2,:),'r*');
    hold on; loglog(Eann,Qd_ann(3,:),'g*');
    hold on; loglog(Eann,Qd_ann(9,:),'b*');
    %hold on; plot(E,sigdA_B/10,'magenta','linewidth',2);
    xlabel('electron energy [eV]');
    ylabel('\sigma [cm^2]');
  %  legend('e+N_2(X)=>e+2N','extrapolated','e+N_2(A)=>e+2N','extrapolated', ...
  %         'location','SE');
    title('Dissociation from Annaloro 2014');
    axis([0 1e3 1e-19 3e-15]);
end

%%%       
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%     dissociation and dissociative ionization of N2(X) 
%%%     from itikawa 2005
%%%

x1 = [10:2:20 25 30:10:60 80 100 125 150 175 200];  % electron energy [eV]
%
sigdn0 = [0 0.01 0.04 0.20 0.36 0.52 0.87 1.04 1.15 1.23 1.23 1.20 1.16 ...
         1.10 1.04 0.99 0.95]*1e-16; % [cm^2]
%
x2 = [10:2:20 25:5:100 110 120:20:200 225:25:300 350:50:1000];
sigdiX0 = [0 0 0 0 0 0 0 0.0325 0.0904 0.166 0.245 0.319 0.390 0.438 0.482 ...
          0.523 0.561 0.587 0.605 0.632 0.645 0.656 0.660 0.661 0.652 0.633 ...
          0.595 0.566 0.516 0.493 0.458 0.438 0.393 0.351 0.324 0.299 0.274 ...
          0.248 0.234 0.217 0.205 0.200 0.192 0.183 0.176 0.167]*1e-16; % [cm^2]     
%
[sigdn_I, sigdn_I_fit]  = TaylorExtrap(x1,sigdn0,9.75,0.7);
[sigdiX_I,sigdiX_I_fit] = TaylorExtrap(x2,sigdiX0,25,1);
%
if(plot_Itikawa==1)
    close(figure(2));
    figure(2);
    loglog(x1,sigdn0,'black*');
  %  hold on; loglog(E,sigdn_I,'black','linewidth',2);
   % hold on; loglog(E,sigdn_I_fit,'blacko','linewidth',2);
    hold on; loglog(x2,sigdiX0,'r*');
   % hold on; plot(E,sigdiX_I,'r','linewidth',2);
   % hold on; loglog(E,sigdiX_I_fit,'ro','linewidth',2);
    xlabel('electron energy [eV]');
    ylabel('\sigma [cm^2]');
    title('Dissociation from Itikawa 2006');
    axis([5 1e3 5e-19 2e-16]);
    annotation('textarrow', [0.71 0.655], [0.84 0.69], ...
               'string','dissociation to neutral products');
 %   legend('e+N_2(X)=>e+N+N','extrapolated','fit',...
 %          'e+N_2(X)=>e+N+N^+','extrapolated','fit', ...
 %          'location','SE');
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%     dissociation and dissociative ionization of N2(X) 
%%%     from Zipf 1980 and 1978
%%%

x3 = [9.75 10.0 10.5 11.0 12.0 13.0:0.5:16.0 17:1:20 22:2:30 33:3:45 50:5:60 ...
      70:10:100 120:20:200 250:50:400];  % electron energy [eV]
%
%
%    e+N2(X) => e + 2N
%
sig_tot0 = [0.0 0.0127 0.0187 0.0249 0.0492 0.112 0.160 0.243 0.285 0.358 0.400 ...
         0.475 0.565 0.682 0.782 0.856 1.05 1.20 1.36 1.47 1.58 1.67 1.75 ...
         1.82 1.88 1.94 2.03 2.10 2.16 2.24 2.27 2.27 2.24 2.16 2.05 1.94 ...
         1.86 1.76 1.55 1.39 1.25 1.14]*1e-16; % [cm^2]
%
%    e+N2(X) => e + N(4S,2D) + N(2D)
%
sig_2D0 = 1/1.15*[0.0 0.0 0.0 0.0 0.0 0.0 0.04 0.086 0.125 0.167 0.204 0.242 ...
          0.312 0.375 0.437 0.491 0.585 0.667 0.735 0.782 0.823 ...
          0.873 0.912 0.942 0.970 0.990 1.02 1.03 1.04 1.06 1.08 1.07 1.05 ...
          1.01 0.960 0.910 0.865 .823 .725 .650 .585 .532]*1e-16; % [cm^2]
%
%    e+N2(X) => e + N(4S) + N(2D)
%
sig_4S2D0 = 0.85*sig_2D0;
%
%    e+N2(X) => e + N(2D) + N(2D)
%
sig_2D2D0 = 0.15*sig_2D0;
%
%    e+N2(X) => e + N(4S) + N(2P)
%
sig_4S2P0 = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.022 0.035 0.054 0.080 0.127 ...
          0.183 0.238 0.290 0.392 0.478 0.556 0.622 0.675 0.722 0.757 ...
          0.777 0.790 0.800 0.810 0.807 0.805 0.795 0.770 0.742 0.717 ...
          0.663 0.622 0.585 0.553 0.525 0.470 0.430 0.395 0.370]*1e-16; % [cm^2]
%
%    e+N2(X) => e + N+ + N(2D)
%
sig_i2D0 = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 ...
          0.0 0.0 0.0 0.00975 0.0205 0.0375 0.0540 0.0785 0.0960 0.135 ...
          0.170 0.195 0.235 0.265 0.290 0.305 0.315 0.310 0.303 0.292 ...
          0.280 0.248 0.222 0.198 0.183]*1e-16; % [cm^2]
%
%
%    e+N2(X) => e + N+ + N(4S)
%
sig_i4S0 = sig_i2D0; % [cm^2]
%
sig_ditot0 = sig_i2D0+sig_i4S0; % total dissociative ionization xsec
%
sig_dntot0 = sig_tot0 - sig_ditot0;
sig_4S4S0 = sig_dntot0 - sig_4S2P0 - sig_4S2D0 - sig_2D2D0;
%sigdX = sig_tot0 - sig_ditot0;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%       take xsecs and extrapolate using Taylor, then 
%%%       use Taylor fit for entire energy range and replace  
%%%       deltaE with deltaE-Eexc to create approximate cross  
%%%       sections for dissocation from excited state with energy Eexc
%%%

[sig_dntotX,sig_dntotX_fit,sig_dntotA] = TaylorExtrap2(x3,sig_tot0-sig_ditot0, ...
                                                       9.75,9.75-6.2,0.8);
[sig_4S2DX,sig_4S2DX_fit,sig_4S2DA,Aconst_4S2D] = TaylorExtrap2(x3,sig_4S2D0, ...
                                                    9.75+2.4,9.75+2.4-6.2,1);
[sig_4S2PX,sig_4S2PX_fit,sig_4S2PA,Aconst_4S2P] = TaylorExtrap2(x3,sig_4S2P0, ...
                                                    9.75+3.6,9.75+3.6-6.2,1);
[sig_2D2DX,sig_2D2DX_fit,sig_2D2DA,Aconst_2D2D] = TaylorExtrap2(x3,sig_2D2D0, ...
                                                    9.75+2*2.4,9.75+2*2.4-6.2,1.2);
[sig_i4SX,sig_i4SX_fit,sig_i4SA,Aconst_i4S]  = TaylorExtrap2(x3,sig_i4S0,9.75+14.5, ...
                                                  9.75+14.5-6.2,0.8);  % 15.6 or 14.5?
[sig_i2DX,sig_i2DX_fit,sig_i2DA,Aconst_i2D]  = TaylorExtrap2(x3,sig_i2D0,9.75+14.5+2.4, ...
                                                  9.75+14.5+2.4-6.2,0.8);  % 15.6 or 14.5?
%
%figure(100); loglog(sig_dntotX_fit);
%
[Aconst_4S2D,Aconst_4S2P,Aconst_2D2D,Aconst_i4S,Aconst_i2D]; % needed in lsp
%
sig_4S4SX = sig_dntotX-(sig_4S2DX+sig_4S2PX+sig_2D2DX);
sig_4S4SX = max(sig_4S4SX,0);
sig_4S4SA = sig_dntotA-(sig_4S2DA+sig_4S2PA+sig_2D2DA);
sig_4S4SA = max(sig_4S4SA,0);
for iA=1:length(E)
    if(E(iA)>=100)
        sig_4S4SA(iA) = 0;
    end
end

if(plot_from_excited==1)
    close(figure(7));
    f7=figure(7);
    loglog(E,sig_dntotX,'black');
    hold on; loglog(E,sig_4S2DX,'g');
    hold on; loglog(E,sig_4S2PX,'r');
    hold on; loglog(E,sig_2D2DX,'b');
    hold on; loglog(E,sig_dntotA,'black*');
    hold on; loglog(E,sig_4S2DA,'g*');
    hold on; loglog(E,sig_4S2PA,'r*');
    hold on; loglog(E,sig_2D2DA,'b*');
    hold on; loglog(E,sig_4S4SX,'magenta');
    hold on; loglog(E,sig_4S4SA,'magenta*');
    title('Dissociative to neutral products from N2(X) and N2(A)');
    ylabel('\sigma [cm^2]');
    xlabel('\epsilon [eV]');
    axis([4 1e5 1e-19 2e-15]);
end

%%%%%%%%%%%%%%%%%%%%
%%%
%%%

if(plot_Zipf==1)
close(figure(33));
figure(33);
loglog(E,sig_4S4SX,'black','linewidth',2);
hold on ;loglog(E,sig_4S2DX,'g','linewidth',2);
hold on; loglog(E,sig_4S2PX,'r','linewidth',2);
hold on; loglog(E,sig_2D2DX,'b','linewidth',2);
% hold on; loglog(x3,sig_i2DX,'g','linewidth',2);
% hold on; loglog(x3,sig_4S4SX,'g','linewidth',2);
axis([10 1e4 1e-19 1e-16]);
xlabel('electron energy [eV]');
ylabel('\sigma [cm^2]');
title('Dissociation Channels in Nitrogen from Zipf 1978');
legend('e+N_2(X) => e+2N(^4S)','e+N_2(X) => e+N(^4S)+N(^2D)', ...
       'e+N_2(X) => e+N(^4S)+N(^2P)','e+N_2(X) => e+2N(^2D)', ...
       'location','best');
end  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    compare total cross sections from different models
%%%

if(plot_compare==1)
    close(figure(4));
    figure(4);
    loglog(x,sigdX0,'black','linewidth',2);
    hold on; loglog(x1,sigdn0,'b','linewidth',2);
    hold on; loglog(x3,sigdX,'r','linewidth',2);
    legend('Bacri','Itikawa','Zipf','location','SE');
    hold on; loglog(x2,sigdiX0,'b*');
    hold on; loglog(x3,sig_ditot0,'r*');
    axis([10 1e3 1e-18 2e-16]);
    annotation('textarrow', [0.558 .518], [0.515 0.719], ...
               'string','dissociation ionization');
    xlabel('electron energy [eV]');
    ylabel('\sigma [cm^2]');
    title('Total dissocation cross sections from different models');
end

%%% write data to files
%
if(writedata == 1)
    path = '../Boltzmann/xsecs_extrapolated/';
    %
    %  xsecs for dissocation from N2(X)
    %
    fileID = fopen([path,'N2X_dn_4S4S.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E; sig_4S4SX*1e-4]);
    %
    fileID = fopen([path,'N2X_dn_4S2D.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E; sig_4S2DX*1e-4]);
    %
    fileID = fopen([path,'N2X_dn_4S2P.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E; sig_4S2PX*1e-4]);
    %
    fileID = fopen([path,'N2X_dn_2D2D.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E; sig_2D2DX*1e-4]);
    %
    fileID = fopen([path,'N2X_di_i4S.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E; sig_i4SX*1e-4]);
    %
    fileID = fopen([path,'N2X_di_i2D.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E; sig_i2DX*1e-4]);
    %
    %  xsecs for dissocation from N2(A)
    %
    fileID = fopen([path,'N2A_dn_4S4S.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E; sig_4S4SA*1e-4]);
    %
    fileID = fopen([path,'N2A_dn_4S2D.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E; sig_4S2DA*1e-4]);
    %
    fileID = fopen([path,'N2A_dn_4S2P.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E; sig_4S2PA*1e-4]);
    %
    fileID = fopen([path,'N2A_dn_2D2D.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E; sig_2D2DA*1e-4]);
    %
    fileID = fopen([path,'N2A_di_i4S.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E; sig_i4SA*1e-4]);
    %
    fileID = fopen([path,'N2A_di_i2D.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E; sig_i2DA*1e-4]);
    
    N2_diss_xsecs.E = E;
    %
    N2_diss_xsecs.N2X_dn_4S4S = sig_4S4SX*1e-4;
    N2_diss_xsecs.N2X_dn_4S2D = sig_4S2DX*1e-4;
    N2_diss_xsecs.N2X_dn_4S2P = sig_4S2PX*1e-4;
    N2_diss_xsecs.N2X_dn_2D2D = sig_2D2DX*1e-4;
    %
    N2_diss_xsecs.N2X_di_i4S = sig_i4SX*1e-4;
    N2_diss_xsecs.N2X_di_i2D = sig_i2DX*1e-4;
    %
    N2_diss_xsecs.N2A_dn_4S4S = sig_4S4SA*1e-4;
    N2_diss_xsecs.N2A_dn_4S2D = sig_4S2DA*1e-4;
    N2_diss_xsecs.N2A_dn_4S2P = sig_4S2PA*1e-4;
    N2_diss_xsecs.N2A_dn_2D2D = sig_2D2DA*1e-4;
    %
    N2_diss_xsecs.N2A_di_i4S = sig_i4SA*1e-4;
    N2_diss_xsecs.N2A_di_i2D = sig_i2DA*1e-4;
    %
    save('N2_dissociation_xsecs.mat','N2_diss_xsecs');
    
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   extrapolate xsecs using expression from Eq. 4 in Taylor 1988
%%%

function [xsec,xsec_fit] = TaylorExtrap(E0,xsec0,deltaE,C)

    fEt = (ET/deltaE-1)./ET.^2.*(log(C*ET/deltaE.*gamma.^2)-beta.^2);    
    %
    for Ei = 1:length(E)
        if(E(Ei)<=deltaE)
            xsec(Ei) = 0;
        elseif(E(Ei)<=max(E0))
            xsec(Ei) = interp1(E0,xsec0,E(Ei));
            xsec_maxE0 = xsec(Ei);
            Emaxi = Ei;
        else
            xsec(Ei) = xsec_maxE0*fEt(Ei)/fEt(Emaxi);
        end
    end
    %
    for Ei = 1:length(E)
        if(E(Ei)<=deltaE)
            xsec_fit(Ei) = 0;
        else
            xsec_fit(Ei) = xsec_maxE0*fEt(Ei)/fEt(Emaxi);
        end
    end
    
end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   extrapolate xsecs using expression from Eq. 4 in Taylor 1988
%%%   then make a fit to data with taylor expression
%%%   then replace deltaE with deltaEA for excited
%%%

function [xsec,xsec_fit,xsecA,Aconst] = TaylorExtrap2(E0,xsec0,deltaE,deltaEA,C)

   % fEt = (ET/deltaE-1)./ET.^2.*(log(C*ET/deltaE.*gamma.^2)-beta.^2); 
    fEt = (1-deltaE./ET).*(deltaE./ET);
    %
    for Ei = 1:length(E)
        if(E(Ei)<=deltaE)
            xsec(Ei) = 0;
        elseif(E(Ei)<=max(E0))
            xsec(Ei) = interp1(E0,xsec0,E(Ei));
            xsec_maxE0 = xsec(Ei);
            Emaxi = Ei;
        else
            xsec(Ei) = xsec_maxE0*fEt(Ei)/fEt(Emaxi);
        end
    end
    %
    for Ei = 1:length(E)
        if(E(Ei)<=deltaE)
            xsec_fit(Ei) = 0;
        else
            xsec_fit(Ei) = xsec_maxE0*fEt(Ei)/fEt(Emaxi);
        end
    end
    %
    fEtA = (ET/deltaEA-1)./ET.^2.*(log(C*ET/deltaEA.*gamma.^2)-beta.^2); 
    for Ei = 1:length(E)
        if(E(Ei)<=deltaEA)
            xsecA(Ei) = 0;
        else
            xsecA(Ei) = xsec_maxE0*fEtA(Ei)/fEt(Emaxi);
        end
    end
            xsecA = max(xsecA,0);
    Aconst = xsec_maxE0/fEt(Emaxi)/(4*pi*R^2*a0^2);
end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   create xsecs using expression from Eq. 4 in Taylor 1988
%%%

function [xsec] = TaylorCreate(deltaE,C,A)

    fET = (ET/deltaE-1)./ET.^2.*(log(C*ET/deltaE.*gamma.^2)-beta.^2);
    %
    xsec = A*4*pi*a0^2*R^2*fET;
    for iE = 1:length(E)
        if(E(iE)<=deltaE)
            xsec(iE) = 0;
        end
    end

end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

end


       