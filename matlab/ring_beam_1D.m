%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%  Solve for axial electric and azimuthal magnetic field as function
%%%  of radius due to ring beam inside transport cell with perfectly
%%%  conducting boundaries
%%%
%%%  Assume that current density is uniform over beam area
%%%
%%%
clear all;
cvac = 3e10;   % speed of light in vacuum [cm/s]

%%% set system parameters
%
rw  = 15;                   % wall radius [cm]
rb  = 10;                   % beam radius [cm]
drb = 1;                    % beam thickness [cm]
r1  = rb - drb/2;           % inner beam radius [cm]
r2  = rb + drb/2;           % outer beam radius [cm]
I0  = 8e5*3e9;              % peak beam current [statA]
J0  = I0/(pi*(r2^2-r1^2));  % peak beam current density [statA/cm^2]


%%% set time profile of current pulse
%
t = 0:1:100;   % time [ns]
tau = 50;      % pulse rise time [ns]
It  = (1+sin(pi*t/tau-pi/2))/2;           % J profile in time [unitless]
Itdot = pi/(tau*1e-9)*cos(pi*t/tau-pi/2); % dIt/dt [1/s] 


%%%  Define Jz, Bth, and Ez profiles (neglecting displacement current)
%
r = 0:0.1:rw;  % r [cm]
Jz  = zeros(length(r),length(t));  % [statA/cm^2]
Bth = zeros(length(r),length(t));  % [statV/cm]
Ez  = zeros(length(r),length(t));  % [statV/cm]
for i = 1:length(r)
    if(r(i)<=r1)
        Jz(i,:)  = 0;
        Bth(i,:) = 0;
        Ez(i,:)  = -2/cvac^2*I0*Itdot*(0.5-r1^2/(r2^2-r1^2)*log(r2/r1) ...
                                     + log(rw/r2));
    elseif(r1<r(i) && r(i)<r2)
        Jz(i,:) = J0*It;
        Bth(i,:) = 2*I0*It/cvac/r(i)*(r(i)^2-r1^2)/(r2^2-r1^2);
        Ez(i,:)  = -2/cvac^2*I0*Itdot*((0.5*(r2^2-r(i)^2)-r1^2*log(r2/r(i)))/(r2^2-r1^2) ...
                                     +  log(rw/r2));
    else
        Jz(i,:) = 0;
        Bth(i,:) = 2*I0*It/cvac/r(i);
        Ez(i,:)  = -2/cvac^2*I0*Itdot*log(rw/r(i));
    end
end


%%% compute displacement current and justify neglecting it
%
Ezdot = -pi/(tau*1e-9)*Ez;
Jd = Ezdot/4/pi;


%%% convert Ez from statV/cm to kV/cm
%
Ez_kVcm = Ez*3e4;            % [V/m]
Ez_kVcm = Ez_kVcm/1e3*1e-2;  % [kV/cm]


%%% plot Ez at r=0
%
close(figure(1));
figure(1);
plot(t,Ez_kVcm(1,:));
xlabel('t [ns]');
ylabel('E_z [kV/cm]');
title('Electric Field on Axis');




