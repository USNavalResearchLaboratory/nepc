%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   Add the three vibrational resolved excitation xsecs
%%%   for N2(A3) together and write to file.
%%%
%%%
writedata = 1;
%
f1 = importdata('../Boltzmann/A3_1.txt',' ',0);
f2 = importdata('../Boltzmann/A3_2.txt',' ',0);
f3 = importdata('../Boltzmann/A3_3.txt',' ',0);
%
E1 = f1(:,1);
xsec1 = f1(:,2);
E2 = f2(:,1);
xsec2 = f2(:,2);
E3 = f3(:,1);
xsec3 = f3(:,2);
%
xsec_net = xsec1 + interp1(E2,xsec2,E1) + interp1(E3,xsec3,E1);


%%%
%
close(figure(1));
figure(1);
loglog(E1,xsec1,'b');
hold on; loglog(E2,xsec2,'r');
hold on; loglog(E3,xsec3,'g');
hold on; loglog(E1,xsec_net,'black*');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%% write data to files
%
if(writedata == 1)
    path = '../Boltzmann/xsecs_extrapolated/';
    fileID = fopen([path,'N2X_Anet.txt'],'w');
    fprintf(fileID,'%e    %e\n',[E1'; xsec_net']);
end
