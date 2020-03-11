%%% testing
%


clear all;

Te = 0.1:0.1:10;
alpha = log10(Te);

Rx1 = 8.36e-11*Te.^8.079.*exp(-3.899+0.765*alpha).*alpha.^2;
Rx3 = 7.64e-12*Te.^9.977.*exp(-5.171+1.112*alpha).*alpha.^2;
Rd  = 2.44e-12*Te.^11.576.*exp(-5.856+1.312*alpha).*alpha.^2;
Ri  = 7.68e-09*Te.^18.645.*exp(-7.555+1.106*alpha).*alpha.^2;
Rv  = 8.55e-09*Te.^1.402.*exp(-1.729+0.056*alpha).*alpha.^2;
Ru1 = 7.68e-09*Te.^1.805.*exp(-0.853+0.394*alpha).*alpha.^2;


close(figure(1));
figure(1); loglog(Te,Rx1+Rx3,'r');
hold on; loglog(Te,Rv,'b');
hold on; loglog(Te,Ri+Rd,'g');
hold on; loglog(Te,Ru1,'black');