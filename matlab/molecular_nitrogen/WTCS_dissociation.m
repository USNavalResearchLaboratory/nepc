%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    compute Weighted Total Cross Sections (WTCS) for electron-
%%%    impact dissociation of excited states of N2 and N2+.
%%%    
%%%    See P. Teulet 1999 and Bacri 1980
%%%
clear all;

hconst = 6.6261e-27;  % planks const [erg-s]
econst = 4.8032e-10;  % electron charge
Navo   = 6.0221e23;   % Avogadro's number [1/mol]
a0     = 5.28e-9;     % Bohr Radius [cm]
amu    = 1.6605e-24;     % atomic mass unit [g]
cvac   = 2.9979e10;   % speed of light [cm/s]
erg_eV = 1.6022e-12;  % ergs associatd with 1eV
erg_invcm = 1.9864e-16;  % ergs associated with 1/cm
invcm_to_eV = erg_invcm/erg_eV; % eV associated with 1/cm
%
mN = 2.32e-23;       % nitrogen mass [g] 
mur = mN*mN/(mN+mN); % reduced mass [g]
mua = mur/amu;       % reduced mass in atomic mass units


State0  = ['X1Sig'   'A3Sig'   'B3Pi'   'W3Delta' ...
           'B3Sigma' 'a1Sigma' 'a1Pi'   'w1Delta' 'C3Pi' ...
           'X2Sig'   'A2Pi'    'B2Sig'  'C3Sigma']; % last 4 are ions
we0 = [2359      1460      1734      1507 ...
       1517      1530      1694      1560    2047  ...  
       2207      1904      2421      2072]; % [1/cm]
xe0 = [14.32    13.78    14.56    12.58 ...
       12.18    12.08    13.95    12.01  28.45 ...    
       16.30    15.03    23.85    9.29]./we0;
ye0 = [-2.26e-3 -1.18e-2  1.40e-2   3.09e-2 ...
        4.19e-2  4.13e-2  7.94e-3   4.54-2  2.09  ...  
       -2.67e-3  2.03e-3  -0.359   -0.43]./we0;
ze0 = [-2.4e-4   1.41e-4  -1.13e-3  -7.1e-4 ...
       -7.3e-4  -2.9e-4    2.9e-4    0   -5.35e-1  ...
       -2.61e-3  0        -6.19e-2   0]./we0;
ae0 = [0      -7.29e-5   0         0 ...
       0       0         0         0   0 ...      
       3.7e-5  0         0         0]./we0;
T0  = [0       49755   59307   59380 ...
       65851   67739   68951   71698   88978  ...
       125668  134683  151234  190210]; % [1/cm]
Be  = [1.998  1.455  1.638  1.470 ...
       1.473  1.480  1.617  1.496 1.825 ... 
       1.932  1.744  2.085  1.511];       % [1/cm]

%%%   set N2 neutral and ion data (see Laher 1991 Table 1)
%
% State0  = ['X1Sig' 'A3Sig' 'B3Pi' 'C3Pi' ...
%            'X2Sig' 'A2Pi'  'B2Sig']; % this line is ions
% we0 = [2359    1460.5  1734.4 2047.2 ...
%        2207    1904    2420];  % [1/cm]
% xe0   = [14.324  13.775  14.558  28.445 ...
%          16.3    15.03   23.85]./we0; % unitless
% ye0   = [-2.26e-3 -1.175e-2 1.4e-2  2.0883 ...
%          -2.67e-3  2.03e-3  -0.3587]./we0; % unitless
% ze0   = [-2.4e-4   1.41e-4  -1.13e-3 -5.35e-1 ...
%          -2.61e-3  0        -6.192e-2]./we0; % unitless
% ae0   = [0        -7.29e-5 0        0 ...
%          3.7e-5   0        0]./we0; % unitless
% T0    = [0       49755   59307  88978 ...
%          125668  134683  151234];   % exc energy from v=0 [1/cm]
Tv0   = we0.*(1/2-xe0/4+ye0/8+ze0/16+ae0/32); % energy at v=0
Te0   = T0-Tv0;   % exc energy from r=r0 [1/cm]
% De0    = [78714   28959   38631  8960 ...
%           70273   61256   45706];    % diss energy from v=0 [1/cm]
De0    = [78714   28959   38631  38716  41862 ...
          49686   48476   45733  8960 ...
          70273   61256   45706  24843];    % diss energy from v=0 [1/cm]
D0     = De0+Tv0; % diss energy from r=r0 [1/cm] (see fig 1 Gilmore 1965)
% Be0     = [1.998   1.455   1.638  1.825 ...
%            1.932   1.748   2.073];    % Rot Const [1/cm]
%
a  = 2*pi*we0*cvac.*sqrt(mur./(2*D0*erg_invcm)); 
%re = sqrt(hconst./(8*pi*mNr*Be0*cvac)); % ?
r0  = [1.098 1.286 1.213 1.290 1.270 ...
       1.280 1.230 1.280 1.149 ...
       1.116 1.174 1.078 1.26]*1e-8; % mean internuc distance [cm]
JL  = [264   190   205   218  223 ...  
       244   232   235   117 ...
       253   249   202   186]; % lost rotational state with potential well (v=0)
%


v = 0:1:45;  % vib quantum number
J = 0; %JL(5);      % rot quantum number
r = (0.05:0.005:4)*max(r0);
Ev = zeros(length(T0),length(v));
rminset = ones(length(T0),length(v)); % flag for setting rmin
rmin = ones(length(T0),length(v)); % initial r where U(r) = T0(i)+Ev(v);
rmax = rmin;                       % final r where   U(r) = T0(i)+Ev(v);
U = zeros(length(T0),length(r));
for i = 1:length(T0)
    U(i,:) = Te0(i) + D0(i)*(1-exp(-a(i)*(r-r0(i)))).^2 ...
           + hconst/8/pi^2/mur/cvac*J*(J+1)./r.^2;
    U(i,:) = U(i,:)*invcm_to_eV;
    UL(i,:) = Te0(i) + D0(i)*(1-exp(-a(i)*(r-r0(i)))).^2 ...
            + hconst/8/pi^2/mur/cvac*JL(i)*(JL(i)+1)./r.^2;
    UL(i,:) = UL(i,:)*invcm_to_eV;
    for j = 1:length(r)
        for k=1:length(v)
            Ev(i,j,k) = Te0(i) + we0(i)* ( (v(k)+1/2) ...
                              -    xe0(i)*(v(k)+1/2).^2 ...
                              +    ye0(i)*(v(k)+1/2).^3 ...
                              +    ze0(i)*(v(k)+1/2).^4 ...
                              +    ae0(i)*(v(k)+1/2).^5 );
            Ev(i,j,k) = Ev(i,j,k)*invcm_to_eV; % [eV]
            if(Ev(i,j,k)<U(i,j))
                Ev(i,j,k) = 0;
                if(rminset(i,k))
                    rmin(i,k) = j+1;
                end
            else
                rmax(i,k) = j;
                rminset(i,k) = 0;
            end
        end
    end
end
%figure(111); plot(r/1e-8,U(13,:)); axis([0.6 3 20 50]);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%        plot some potential energy curves for neutral N2
%%%

close(figure(1)); figure(1); plot(r/1e-8,U(1:3,:));
hold on; plot(r/1e-8,U(9,:),'color',[0 0.75 0.75]);
hold on; plot(r(rmin(1,1):rmax(1,1))/1e-8,Ev(1,rmin(1,1):rmax(1,1),1));
hold on; plot(r(rmin(1,2):rmax(1,2))/1e-8,Ev(1,rmin(1,2):rmax(1,2),2));
hold on; plot(r(rmin(1,3):rmax(1,3))/1e-8,Ev(1,rmin(1,3):rmax(1,3),3));
%
hold on; plot(r(rmin(2,1):rmax(2,1))/1e-8,Ev(2,rmin(2,1):rmax(2,1),1),'color',[0 0.5 0]);
hold on; plot(r(rmin(2,2):rmax(2,2))/1e-8,Ev(2,rmin(2,2):rmax(2,2),2),'color',[0 0.5 0]);
hold on; plot(r(rmin(2,3):rmax(2,3))/1e-8,Ev(2,rmin(2,3):rmax(2,3),3),'color',[0 0.5 0]);
%
hold on; plot(r(rmin(3,1):rmax(3,1))/1e-8,Ev(3,rmin(3,1):rmax(3,1),1),'r');
hold on; plot(r(rmin(3,2):rmax(3,2))/1e-8,Ev(3,rmin(3,2):rmax(3,2),2),'r');
hold on; plot(r(rmin(3,3):rmax(3,3))/1e-8,Ev(3,rmin(3,3):rmax(3,3),3),'r');
%
hold on; plot(r(rmin(9,1):rmax(9,1))/1e-8,Ev(9,rmin(9,1):rmax(9,1),1),'color',[0 0.75 0.75]);
hold on; plot(r(rmin(9,2):rmax(9,2))/1e-8,Ev(9,rmin(9,2):rmax(9,2),2),'color',[0 0.75 0.75]);
hold on; plot(r(rmin(9,3):rmax(9,3))/1e-8,Ev(9,rmin(9,3):rmax(9,3),3),'color',[0 0.75 0.75]);
%
axis([0.9 2 0 13]);
xlabel('r[angstroms]'); ylabel('U [eV]');
title('potential energy curves for neutral molecular nitrogen');
legend('X^1\Sigma','A^3\Sigma','B^3\Pi','C^3\Pi','location','SE');
hold on; plot(r/1e-8,U(4:8,:));
 
%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%        plot some potential energy curves for neutral N2
%%%

close(figure(2)); figure(2); plot(r/1e-8,U(1,:));
hold on; plot(r/1e-8,U(10,:),'color',[0 0.5 0]);
%
hold on; plot(r(rmin(1,1):rmax(1,1))/1e-8,Ev(1,rmin(1,1):rmax(1,1),1));
hold on; plot(r(rmin(1,5):rmax(1,5))/1e-8,Ev(1,rmin(1,5):rmax(1,5),5));
hold on; plot(r(rmin(1,9):rmax(1,9))/1e-8,Ev(1,rmin(1,9):rmax(1,9),9));
%
for k = 1:11
hold on; plot(r(rmin(10,k):rmax(10,k))/1e-8,Ev(10,rmin(10,k):rmax(10,k),k),'color',[0 0.5 0]);
end
%
axis([0.9 2 0 20]);
xlabel('r[angstroms]'); ylabel('U [eV]');
%set(gca,'Xtick',[r(rmin(1,7)),r(rmin(1,5)),r(rmin(1,1)), ...
%                 r(rmax(1,1)),r(rmax(1,5)),r(rmax(1,7))]/1e-8);
%title('potential energy curves for neutral molecular nitrogen');
legend('X^1\Sigma','X^2\Sigma','location','SE'); grid on;
 
%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

compute_diss_xsecs = 1;
if(compute_diss_xsecs==1)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%  Now that we have potential curves, go about computing Xsecs
%%%


%%%   compute probability of electron being at (r-r0)
%
k0 = 4*pi^2*cvac^2/Navo*mua*we0.^2;
alpha = 2*pi/hconst*sqrt(mur*k0);
for k = 1:length(alpha)
    P0(k,:) = sqrt(alpha(k)/pi).*exp(-alpha(k)*(r-r0(k)).^2);
end
%figure(20); plot(r,P0);


%%%   compute cross section using Gryzinkis formulat
%
dr = r(2)-r(1);
eta = [2 1 1 1 1 1 1 1 1];
E = [0:0.5:100 150:50:1e3]; % electron enegy [eV]
for j = 1:9
    DE(j,:) = UL(j,:)- U(j,:);
    EL(j,:) = U(10,:) - U(j,:);
    for k = 1:length(r)
        u = E/DE(j,k);
        v = EL(j,k)/DE(j,k);
        gu0(j,k,:) = eta(j)./u.*(1-1./u).^(1+v/(1+v)).*(u./(u+v)).^1.5 ...
                  .*(1+2*v/3*(1-0.5./u).*log(2.718+sqrt((u-1)/v)));
        for i = 1:length(E)
            if(u(i)<=1 || v<=0) % v can be negative at small r due to Morse approx
                gu0(j,k,i) = 0;
            end
        end
        QD(j,k,:) = 4*pi*a0^2*(13.5./DE(j,k))^2*gu0(j,k,:);
        PQ(j,k,:) = P0(j,k)*QD(j,k,:);
    end
end
QD_WTCS = squeeze(sum(PQ*dr,2));
figure(77); loglog(E,QD_WTCS(1:3,:)); axis([0 1e3 1e-18 1e-14]);
hold on; loglog(E,QD_WTCS(9,:),'color',[0 0.75 0.75]);
xlabel('electron energy [eV]'); ylabel('\sigma [cm^2]');
title('e+N_2(*) => e+N+N');
legend('X^1\Sigma','A^3\Sigma','B^3\Pi','C^3\Pi');


WTCS_diss.E = E;
WTCS_diss.Q = QD_WTCS;
WTCS_diss.U = 9.76 + [0 0    2.38 2.38 3.58 4.76 4.76 4.76 2.38] ...
                   - [0 6.17 7.35 7.36 8.17 8.40 8.55 8.89 11.0];
save('WTCS_diss.mat','WTCS_diss');

%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

end