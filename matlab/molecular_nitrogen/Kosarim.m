%%%%%%%%%%
%%%
%%%  cross sections for ionization of nitrogen molecules using
%%%  model by A.V. Kosarim Chem. Phys. Lett. 414 (2005) 215-221
%%%
%%%  also see potential_energy_curves.m for computing J1 and J2
%%%
%%%  Considering ionizing into states X2, A2, B2. I think higher states
%%%  are for dissociative ionization process (they dissociate)
%%%
%%%  Note that must renormalize total from ground state to itikawa
%%%  (1.9e-16). This factor changes if include more final ion states
%%%
clear all;
write_data = 1;

load('./Jvvp_and_Jvvpp.mat');
Jvps = Jvvp_and_Jvvpp; % see potential_energy_curves.m

econst = 4.8032e-10; % electron charge
eV_erg = 1.6022e-12; % energy in ergs associatd with 1eV
Aconst = pi*econst^4/eV_erg^2/2;
%
E = 15:1:1e3; % electron energy grid [eV]
%
Ematch = 100; % energy where xsec matches itikawa
[~,thisEi]=min(abs(E-Ematch)); % where sum data is


%%%   ionization cross sections from Itikawa
%
EItikawa = [15.6 16:0.5:25 30:5:40 45:5:100 110 120:20:200 225:25:300 ...
            350:50:1e3];
[~,thisEi_Itikawa] = min(abs(EItikawa-Ematch));
Qizn_Itikawa = [0 0.0211 0.0466 0.0713 0.0985 0.129 0.164 0.199 0.230 0.270 ...
            0.308 0.344 0.380 0.418 0.455 0.492 0.528 0.565 0.603 ...
            0.640 0.929 1.16 1.37 1.52 1.60 1.66 1.72 1.74 1.78 1.80 ...
            1.81 1.82 1.83 1.85 1.85 1.83 1.81 1.78 1.72 1.67 1.61 ...
            1.55 1.48 1.41 1.37 1.28 1.20 1.11 1.05 0.998 0.943 0.880 ...
            0.844 0.796 0.765 0.738 0.719 0.698 0.676]*1e-16; % X2+A2+B2
Qdizn_Itikawa = [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.0325 0.0904 ...
            0.166 0.245 0.319 0.390 0.438 0.482 0.523 0.561 0.587 ...
            0.605 0.632 0.645 0.656 0.660 0.661 0.652 0.633 0.595 ...
            0.566 0.516 0.493 0.458 0.438 0.393 0.351 0.324 0.299 ...
            0.274 0.248 0.234 0.217 0.205 0.200 0.192 0.183 0.176 ...
            0.167]*1e-16;

        
%%%   values below are from tables in reference above
%
% E1 = [20 30 50];
% Q1 = [0.82 2.1 3.4]*1e-17;
% E2 = [20 30 50];
% Q2 = [0.79 2.9 5.2]*1e-17;
% E3 = [20 30 50];
% Q3 = [0.13 1.0 2.0]*1e-17;
% 
% figure(1); hold on; plot(E1,Q1,'b*');
% hold on; plot(E2,Q2,'r*');
% hold on; plot(E3,Q3,'g*');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%      compute cross sections from N2(X1Sigma)
%%%

%%%  e+ N2(X1Sigma) -> 2e + N2(X2Sigma,A2Pi,B2Sigma,C2Sigma)
%
n = [2 4 2 2];
for i = 1:3   % not going into C2Sigma (see Slinker 1990)
    J1 = Jvps.J1_X1(i,1);
    J2 = Jvps.J2_X1(i,1);
    x1 = E/J1;
    x2 = E/J2;
    f1 = max(0,(x1-1)./(pi*(x1+2).*(x1+10)));
    f2 = max(0,(x2-1)./(pi*(x2+2).*(x2+10)));
    QX1(i,:) = n(i)*Aconst*(f1/J1^2 +f2/J2^2);
    UX1(i) = min(J1,J2);
end
%scaleFactors = [8.69 8.79 1.92]*1e-17; % from Doering for X2 A2 B2 at 100eV
%scaleFactors = [6.05 10.11 2.74]*1e-17; % from Van Zyl for X2 A2 B2 at 100eV
scale = [7.03 8.71 2.36]*1e-17; % from itikawa for X2 A2 B2 at 100eV
for i = 1:3
    QX1(i,:) = QX1(i,:)/QX1(i,thisEi)*scale(i);
end
%Qtot = sum(QX1,1);
%scale = Qizn_Itikawa(thisEi_Itikawa)/Qtot(thisEi);
%QX1 = scale*QX1;


close(figure(1)); f1=figure(1);
set(f1,'position',[0 50 800 800]);
subplot(2,2,1);
plot(E,QX1);
hold on; plot(E,sum(QX1),'black');
hold on; plot(EItikawa,Qizn_Itikawa,'black--');
hold on; plot(EItikawa,Qdizn_Itikawa,'magenta--');
legend('X^2\Sigma','A^2\Pi','B^2\Sigma','total','Itikawa','location','best');
xlabel('electron energy [eV]');
ylabel('\sigma [cm^2]');
title('ionization from N2(X^1\Sigma)');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%      compute cross sections from N2(A3Sigma)
%%%

%%%  e+ N2(A3Sigma) -> 2e + N2(X2Sigma,A2Pi,B2Sigma)
%
n = [0 1 2 2];
for i = 1:3
    J1 = Jvps.J1_A3(i,1); % 9.41;
    J2 = Jvps.J2_A3(i,1); % 11.21;
    x1 = E/J1;
    x2 = E/J2;
    f1 = max(0,scale(i)*(x1-1)./(pi*(x1+2).*(x1+10)));
    f2 = max(0,scale(i)*(x2-1)./(pi*(x2+2).*(x2+10)));
    QA3(i,:) = n(i)*Aconst*(f1/J1^2 +f2/J2^2);
    UA3(i) = min(J1,J2);
end


subplot(2,2,2);
plot(E,QA3);
hold on; plot(E,sum(QA3),'black');
legend('X^2\Sigma','A^2\Pi','B^2\Sigma','total','location','best');
xlabel('electron energy [eV]');
ylabel('\sigma [cm^2]');
title('ionization from N2(A^3\Sigma)');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%      compute cross sections from N2(B3Sigma)
%%%

%%%  e+ N2(B3Pi) -> 2e + N2(X2Sigma,A2Pi,B2Sigma)
%
n = [1 0 4 4];
for i = 1:3
    J1 = Jvps.J1_B3(i,1); % 9.41;
    J2 = Jvps.J2_B3(i,1); % 11.21;
    x1 = E/J1;
    x2 = E/J2;
    f1 = max(0,scale(i)*(x1-1)./(pi*(x1+2).*(x1+10)));
    f2 = max(0,scale(i)*(x2-1)./(pi*(x2+2).*(x2+10)));
    QB3(i,:) = n(i)*Aconst*(f1/J1^2 +f2/J2^2);
    UB3(i) = min(J1,J2);
end


subplot(2,2,3);
plot(E,QB3);
hold on; plot(E,sum(QB3),'black');
legend('X^2\Sigma','A^2\Pi','B^2\Sigma','total','location','best');
xlabel('electron energy [eV]');
ylabel('\sigma [cm^2]');
title('ionization from N2(B^3\Pi)');


%%%  e+ N2(W3Delta) -> 2e + N2(X2Sigma,A2Pi,B2Sigma)
%
n = [0 1 2 2];
for i = 1:3
    J1 = Jvps.J1_W3(i,1); % 9.41;
    J2 = Jvps.J2_W3(i,1); % 11.21;
    x1 = E/J1;
    x2 = E/J2;
    f1 = max(0,scale(i)*(x1-1)./(pi*(x1+2).*(x1+10)));
    f2 = max(0,scale(i)*(x2-1)./(pi*(x2+2).*(x2+10)));
    QW3(i,:) = n(i)*Aconst*(f1/J1^2 +f2/J2^2);
    UW3(i) = min(J1,J2);
end


subplot(2,2,4);
plot(E,QW3);
hold on; plot(E,sum(QW3),'black');
legend('X^2\Sigma','A^2\Pi','B^2\Sigma','total','location','best');
xlabel('electron energy [eV]');
ylabel('\sigma [cm^2]');
title('ionization from N2(W^3\Delta)');


%%%  e+ N2(B3pSigma) -> 2e + N2(X2Sigma,A2Pi,B2Sigma,C2Sigma)
%
n = [0 1 2 2];
for i = 1:3
    J1 = Jvps.J1_Bp3(i,1); % 9.41;
    J2 = Jvps.J2_Bp3(i,1); % 11.21;
    x1 = E/J1;
    x2 = E/J2;
    f1 = max(0,scale(i)*(x1-1)./(pi*(x1+2).*(x1+10)));
    f2 = max(0,scale(i)*(x2-1)./(pi*(x2+2).*(x2+10)));
    QBp3(i,:) = n(i)*Aconst*(f1/J1^2 +f2/J2^2);
    UBp3(i) = min(J1,J2);
end


close(figure(2)); f2=figure(2);
set(f2,'position',[500 50 800 800]);
subplot(2,2,1);
plot(E,QBp3);
hold on; plot(E,sum(QBp3),'black');
legend('X^2\Sigma','A^2\Pi','B^2\Sigma','total','location','best');
xlabel('electron energy [eV]');
ylabel('\sigma [cm^2]');
title('ionization from N2(B^3\Sigma)');


%%%  e+ N2(a'1Sigma) -> 2e + N2(X2Sigma,A2Pi,B2Sigma,C2Sigma)
%
n = [0 1 2 2];
for i = 1:3
    J1 = Jvps.J1_ap1(i,1); % 9.41;
    J2 = Jvps.J2_ap1(i,1); % 11.21;
    x1 = E/J1;
    x2 = E/J2;
    f1 = max(0,scale(i)*(x1-1)./(pi*(x1+2).*(x1+10)));
    f2 = max(0,scale(i)*(x2-1)./(pi*(x2+2).*(x2+10)));
    Qap1(i,:) = n(i)*Aconst*(f1/J1^2 +f2/J2^2);
    Uap1(i) = min(J1,J2);
end


subplot(2,2,2);
plot(E,Qap1);
hold on; plot(E,sum(Qap1),'black');
legend('X^2\Sigma','A^2\Pi','B^2\Sigma','total','location','best');
xlabel('electron energy [eV]');
ylabel('\sigma [cm^2]');
title('ionization from N2(a^1\Sigma)');


%%%  e+ N2(a1Pi) -> 2e + N2(X2Sigma,A2Pi,B2Sigma)
%
n = [1 0 4 4];
for i = 1:3
    J1 = Jvps.J1_a1(i,1); % 9.41;
    J2 = Jvps.J2_a1(i,1); % 11.21;
    x1 = E/J1;
    x2 = E/J2;
    f1 = max(0,scale(i)*(x1-1)./(pi*(x1+2).*(x1+10)));
    f2 = max(0,scale(i)*(x2-1)./(pi*(x2+2).*(x2+10)));
    Qa1(i,:) = n(i)*Aconst*(f1/J1^2 +f2/J2^2);
    Ua1(i) = min(J1,J2);
end


subplot(2,2,3);
plot(E,Qa1);
hold on; plot(E,sum(Qa1),'black');
legend('X^2\Sigma','A^2\Pi','B^2\Sigma','total','location','best');
xlabel('electron energy [eV]');
ylabel('\sigma [cm^2]');
title('ionization from N2(a^1\Pi)');

%%%  e+ N2(w1Delta) -> 2e + N2(X2Sigma,A2Pi,B2Sigma)
%
n = [0 1 2 2];
for i = 1:3
    J1 = Jvps.J1_w1(i,1); % 9.41;
    J2 = Jvps.J2_w1(i,1); % 11.21;
    x1 = E/J1;
    x2 = E/J2;
    f1 = max(0,scale(i)*(x1-1)./(pi*(x1+2).*(x1+10)));
    f2 = max(0,scale(i)*(x2-1)./(pi*(x2+2).*(x2+10)));
    Qw1(i,:) = n(i)*Aconst*(f1/J1^2 +f2/J2^2);
    Uw1(i) = min(J1,J2);
end


subplot(2,2,4);
plot(E,Qw1);
hold on; plot(E,sum(Qw1),'black');
legend('X^2\Sigma','A^2\Pi','B^2\Sigma','total','location','best');
xlabel('electron energy [eV]');
ylabel('\sigma [cm^2]');
title('ionization from N2(w^1\Delta)');


%%%  e+ N2(C3Pi) -> 2e + N2(X2Sigma,A2Pi,B2Sigma,C2Sigma)
%
n = [0 0 1 1];
for i = 1:3
    J1 = Jvps.J1_C3(i,1); % 9.41;
    J2 = Jvps.J2_C3(i,1); % 11.21;
    x1 = E/J1;
    x2 = E/J2;
    f1 = max(0,scale(i)*(x1-1)./(pi*(x1+2).*(x1+10)));
    f2 = max(0,scale(i)*(x2-1)./(pi*(x2+2).*(x2+10)));
    QC3(i,:) = n(i)*Aconst*(f1/J1^2 +f2/J2^2);
    UC3(i) = min(J1,J2);
end


close(figure(3)); f3=figure(3);
%set(f2,'position',[500 50 800 800]);
%subplot(2,2,1);
plot(E,QC3);
hold on; plot(E,sum(QC3),'black');
legend('X^2\Sigma','A^2\Pi','B^2\Sigma','total','location','best');
xlabel('electron energy [eV]');
ylabel('\sigma [cm^2]');
title('ionization from N2(C^3\Pi)');


paperPlot=1;
if(paperPlot)
    close(figure(111)); f111=figure(111);
    set(f111,'position',[0 600 800 300]);
    subplot(1,2,1);
    loglog(E,sum(QX1)/1e-16,'black'); axis([10 1e3 1e-3 10]); axis('square');
    hold on; plot(E,QX1/1e-16);
    hold on; plot(EItikawa,Qizn_Itikawa/1e-16,'black--');
 %   hold on; plot(EItikawa,Qdizn_Itikawa/1e-16,'magenta--');
    lg1=legend('total','X^2\Sigma','A^2\Pi','B^2\Sigma','Itikawa','location','best');
    xlabel('electron energy [eV]');
    ylabel('\sigma [10^-^1^6cm^2]');
    set(gca,'xtick',10.^(0:1:3));
    %
    subplot(1,2,2);
    plot(E,sum(QX1)/1e-16,'black'); axis([0 1e3 0 2]); axis('square');
    hold on; plot(E,QX1/1e-16);
    hold on; plot(EItikawa,Qizn_Itikawa/1e-16,'black--');
 %   hold on; plot(EItikawa,Qdizn_Itikawa/1e-16,'magenta--');
    lg2=legend('total','X^2\Sigma','A^2\Pi','B^2\Sigma','Itikawa','location','best');
    xlabel('electron energy [eV]');
    ylabel('\sigma [10^-^1^6cm^2]');
    set(gca,'xtick',0:200:1e3);
    set(gca,'ytick',0:0.5:2);
    hold on; plot(thisEi,scale/1e-16,'Marker','*');
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    write data to file
%%% 
if(write_data)
    
    Kosarim_xsecs.E = E; % [eV]
    Kosarim_xsecs.QX1  = QX1; % [cm^2]
    Kosarim_xsecs.UX1  = UX1; % [eV]
    Kosarim_xsecs.QA3  = QA3;
    Kosarim_xsecs.UA3  = UA3; % [eV]
    Kosarim_xsecs.QB3  = QB3;    
    Kosarim_xsecs.UB3  = UB3; % [eV]
    Kosarim_xsecs.QW3  = QW3;  
    Kosarim_xsecs.UW3  = UW3; % [eV]
    Kosarim_xsecs.QBp3 = QBp3;
    Kosarim_xsecs.UBp3 = UBp3; % [eV]
    Kosarim_xsecs.Qap1 = Qap1;   
    Kosarim_xsecs.Uap1 = Uap1; % [eV]
    Kosarim_xsecs.Qa1  = Qa1;  
    Kosarim_xsecs.Ua1  = Ua1; % [eV]
    Kosarim_xsecs.Qw1  = Qw1;
    Kosarim_xsecs.Uw1  = Uw1; % [eV]
    Kosarim_xsecs.QC3  = QC3;
    Kosarim_xsecs.UC3  = UC3; % [eV]
    Kosarim_xsecs.readme = ['cross sections for ionization of molecular ', ...
    'nitrogen excited states (v=0) calculated using model from Kosarim 2005'];
    save('../../Xsecs/Kosarim_xsecs.mat','Kosarim_xsecs');
    
end




