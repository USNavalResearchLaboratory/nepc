%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   Compare cross sections for ionization of singly ionized atomic
%%%   nitrogen from Lotz 1968 and Drawin 1969. Also see Taylor 1988.
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
E = [29:1:100 110:10:200 250:50:1e4];


%%% Lotz 1968
%
a = [3.9 4.4]*1e-14; b = [0.46 0.4]; c = [0.62 0.6]; q = [2 2]; P = [29.6 36.7];
%
QLotz = zeros(length(a),length(E));
for i = 1:length(a)
    for j = 1:length(E)
        if(E(j)>=P(i))
            QLotz(i,j) = a(i)*q(i).*log(E(j)/P(i))/(E(j)*P(i)) ...
                      .* (1-b(i)*exp(-c(i)*(E(j)/P(i)-1)));
        end
    end
end


%%% plot and compare
%
close(figure(1));
figure(1);
loglog(E,sum(QLotz),'black');
xlabel('E [eV]'); ylabel('\sigma  [cm^2]');
%title('rate constants for e+N(^4S)=>e+N^+');
%legend('Lotz','Corona','FLYCHK','location','SE');
%axis([0.3 10 1e-14 1e-7]);



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%% Taylor 1988 (see Taylor 1987 and Drawin 1969)
%
a0 = 5.29e-9; Ry = 13.5;
f = 0.74; eta = 2.7; U = 29.6; Z = 2;
QDrawin = max(0,f*eta*4*pi*a0^2*Ry^2./E.^2.*(E/U-1).*log(1.25*(1+(Z-1)/(Z+2))*E/U));


figure(1); 
hold on; plot(E,QDrawin,'r--');
axis([10 1e4 1e-18 1e-16]);
title('e+N^+ => 2e+N^+^+');
legend('Lotz','Drawin','location','best');



