%function [A,E,kstart,kend,Q] = Phy4Entry_eVib_xsecs
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   See Phy4Entry_eVib_xsecs.m for full shabang
%%%   this script loads e+N2(X1,v) = e+N2(X1,v') xsecs from
%%%   Laporta Plasma Sources Sci. Tech. 23 (2014) and saves them.
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
write_data = 0; % 0 for do not write and 1 for do write
load_data = 1;


%%% set potential energy for transition from the ground state 0->0:58
%
Uvib = [0.000 0.288 0.573 0.855 1.133 1.408 1.679 1.947 2.211 2.471 2.728 ...
        2.982 3.232 3.478 3.270 3.959 4.195 4.426 4.654 4.878 5.099 5.315 ...
        5.528 5.737 5.942 6.143 6.339 6.532 6.721 6.905 7.084 7.260 7.430 ...
        7.596 7.757 7.913 8.064 8.210 8.350 8.485 8.614 8.737 8.853 8.963 ...
        9.067 9.163 9.252 9.335 9.409 9.476 9.535 9.587 9.631 9.667 9.696 ...
        9.717 9.732 9.742 9.748]; % [eV]

   
%%%   import text file data set and get the energy domain
%
if(load_data)
    % delims = 2;
    % A = importdata('../../Xsecs/Phy4Entry_eV_crossSections/data_Cshort.txt', ...
    %                '\t',delims);
    delims = 1;
    A = importdata('../../Xsecs/Phy4Entry_eV_crossSections/data_C_j=0.txt', ...
                   '\t',delims);
    lengthE = 1;
    Eindex = 5;
    while (A.data(1+lengthE,Eindex) ~= 0)
        lengthE = lengthE+1;
    end
    lengthE = lengthE-1; % data file erroneously contains last Energy term twice 
    E = A.data(1:lengthE,Eindex); % energy grid 0->15 eV
end


%%%   loop over v=0:58 and vp=v:58
%
numVib = 59;                 % there are 59 (0-58) vib states
Q = zeros(numVib,numVib,lengthE);
%lengthk = (numVib*(numVib+1)/2); % 59+58+57+...+1
kendlimit = length(A.data(:,1));
kend = 0; kstart =1;
for i = 1:numVib
    for j = i:numVib
        kend = kstart;
        thisv = i-1;
        while (A.data(kend,3) <= j-1 && A.data(kend,1)==thisv)
            kend = kend+1;
            if(kend==kendlimit+1)
                break;
            end
        end
        kend = kend-1;      % index where data for this j starts

        lengthQ = kend-kstart; % length of current data -1 (see error above)
        for k=kstart:kend-1 % minus 1 due to error above
            Q(i,j,k-kstart+lengthE-lengthQ+1) = A.data(k,6)';
        end      
        kstart = kend+1;  % index where data for this j ends
        
        if(j>i)
            gi = 1; gj = 1;
            Qinterp = interp1(E,squeeze(Q(i,j,:)),E+(Uvib(j)-Uvib(i)),'pchirp');
            Qinterp = max(Qinterp,0);
          %  Qinterp(1) = 0;
            Q(j,i,:) = gi/gj*(E+(Uvib(j)-Uvib(i)))./E.*Qinterp;
            Q(j,i,1) = interp1(E(2:10),squeeze(Q(j,i,2:10)),E(1),'pchirp');
        end
    end
end
close(figure(1)); f1 = figure(1);
semilogy(E,squeeze(Q(1,1:10,:)));
xlabel('energy [eV]'); ylabel('\sigma [cm^2]');
title('e+N_2(X^1,v=0)=>e+N_2(X^1,v=0:10)');

%  Qexc(i,j,:) = InterpForbidden(thisE,thisQ,E,thisU);
 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %%%
% %%%    Interp forbidden xsecs (~1/E^3 at high energy)
% %%%
% 
% function [Q1] = InterpForbidden(E0,Q0,E1,U)
% 
%     Emax = E0(length(E0));
%     Qmax = Q0(length(Q0));
%     Q1 = interp1(E0,Q0,E1,'pchirp');
%     for Ei = 1:length(E1)
%         if(E1(Ei)<=U)
%             Q1(Ei) = 0;
%         end
%         if(E1(Ei)>Emax)
%             Q1(Ei) = Qmax*(Emax./E1(Ei))^3;
%         end
%     end
%     
% end
% 
% %%%
% %%%
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%                     write date to file
%%%

if(write_data)
    
    Laporta_xsecs.Uvib = Uvib;
    Laporta_xsecs.E = E;
    Laporta_xsecs.Q = Q;
    save('Laporta_xsecs.mat','Laporta_xsecs');
    
end
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
% 
% end