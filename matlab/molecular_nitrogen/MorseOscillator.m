%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    compute morse oscillator potentials for excited states of N2
%%%    and N2+.
%%%    Loftus 1977,  "The Spectrum of Molecular Nitrogen"
%%%    Laher 1991,   "Improved Fits for the Vib. and Rot. Const..."
%%%    Kosarim 2005, "Ionization of excited nitrogen molecules by ..."
%%%
%%%
clear all;

hconst = 6.6261e-27;  % planks const [erg-s]
econst = 4.8032e-10;  % electron charge
cvac   = 2.9979e10;   % speed of light [cm/s]
erg_eV = 1.6022e-12;  % ergs associatd with 1eV
erg_invcm = 1.9864e-16;  % ergs associated with 1/cm
invcm_to_eV = erg_invcm/erg_eV; % eV associated with 1/cm
%
mN = 2.32e-23;       % nitrogen mass [g] 
mur = mN*mN/(mN+mN); % reduced mass [g]

%%%   set N2 neutral and ion data (see Laher 1991 Table 1)
%
State0  = ['X1Sig' 'A3Sig' 'B3Pi' 'C3Pi' ...
           'X2Sig' 'A2Pi'  'B2Sig']; % this line is ions
we0 = [2359    1460.5  1734.4 2047.2 ...
       2207    1904    2420];  % [1/cm]
xe0   = [14.324  13.775  14.558  28.445 ...
         16.3    15.03   23.85]./we0; % unitless
ye0   = [-2.26e-3 -1.175e-2 1.4e-2  2.0883 ...
         -2.67e-3  2.03e-3  -0.3587]./we0; % unitless
ze0   = [-2.4e-4   1.41e-4  -1.13e-3 -5.35e-1 ...
         -2.61e-3  0        -6.192e-2]./we0; % unitless
ae0   = [0        -7.29e-5 0        0 ...
         3.7e-5   0        0]./we0; % unitless
T0    = [0       49755   59307  88978 ...
         125668  134683  151234];   % exc energy from v=0 [1/cm]
Tv0   = we0.*(1/2-xe0/4+ye0/8+ze0/16+ae0/32); % energy at v=0
Te0   = T0-Tv0;   % exc energy from r=r0 [1/cm]
De0    = [78714   28959   38631  8960 ...
          70273   61256   45706];    % diss energy from v=0 [1/cm]
D0     = De0+Tv0; % diss energy from r=r0 [1/cm] (see fig 1 Gilmore 1965)
Be0     = [1.998   1.455   1.638  1.825 ...
           1.932   1.748   2.073];    % Rot Const [1/cm]
%
a  = 2*pi*we0*cvac.*sqrt(mur./(2*D0*erg_invcm)); 
%re = sqrt(hconst./(8*pi*mNr*Be0*cvac)); % ?
r0  = [1.098 1.286 1.213 1.149 ...
       1.116 1.174 1.0777]*1e-8; % mean internuc distance [cm]

%
%
%

v = 0:1:45;              % vib quantum number
r = (0:0.005:4)*max(r0);
Ev = zeros(length(T0),length(v));
rminset = ones(length(T0),length(v)); % flag for setting rmin
rmin = ones(length(T0),length(v)); % initial r where U(r) = T0(i)+Ev(v);
rmax = rmin;                       % final r where   U(r) = T0(i)+Ev(v);
U = zeros(length(T0),length(r));
for i = 1:length(T0)
    U(i,:) = Te0(i) + D0(i)*(1-exp(-a(i)*(r-r0(i)))).^2;
    U(i,:) = U(i,:)*invcm_to_eV;
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


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%        plot some potential energy curves for neutral N2
%%%

close(figure(1)); figure(1); plot(r/1e-8,U);
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
hold on; plot(r(rmin(4,1):rmax(4,1))/1e-8,Ev(4,rmin(4,1):rmax(4,1),1),'color',[0 0.75 0.75]);
hold on; plot(r(rmin(4,2):rmax(4,2))/1e-8,Ev(4,rmin(4,2):rmax(4,2),2),'color',[0 0.75 0.75]);
hold on; plot(r(rmin(4,3):rmax(4,3))/1e-8,Ev(4,rmin(4,3):rmax(4,3),3),'color',[0 0.75 0.75]);
%
axis([0.9 2 0 13]);
xlabel('r[angstroms]'); ylabel('U [eV]');
title('potential energy curves for neutral molecular nitrogen');
legend('X^1\Sigma','A^3\Sigma','B^3\Pi','C^3\Pi','location','SE');
 
%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%        plot some potential energy curves for neutral N2
%%%

close(figure(2)); figure(2); plot(r/1e-8,U(1,:));
hold on; plot(r/1e-8,U(5,:),'color',[0 0.5 0]);
%
hold on; plot(r(rmin(1,1):rmax(1,1))/1e-8,Ev(1,rmin(1,1):rmax(1,1),1));
hold on; plot(r(rmin(1,5):rmax(1,5))/1e-8,Ev(1,rmin(1,5):rmax(1,5),5));
hold on; plot(r(rmin(1,9):rmax(1,9))/1e-8,Ev(1,rmin(1,9):rmax(1,9),9));
%
for k = 1:11
hold on; plot(r(rmin(5,k):rmax(5,k))/1e-8,Ev(5,rmin(5,k):rmax(5,k),k),'color',[0 0.5 0]);
end
%
axis([0.9 2 0 20]);
xlabel('r[angstroms]'); ylabel('U [eV]');
set(gca,'Xtick',[r(rmin(1,9)),r(rmin(1,5)),r(rmin(1,1)), ...
                 r(rmax(1,1)),r(rmax(1,5)),r(rmax(1,9))]/1e-8);
%title('potential energy curves for neutral molecular nitrogen');
legend('X^1\Sigma','X^2\Sigma','location','SE'); grid on;
 
%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

