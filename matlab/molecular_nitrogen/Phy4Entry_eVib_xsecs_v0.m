function [A,E,kstart,kend,Q] = Phy4Entry_eVib_xsecs_v0
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   only loads cross sections for collisions with ground state !!!
%%%   See Phy4Entry_eVib_xsecs.m for full shabang
%%%   this script loads e+N2(X1,v) = e+N2(X1,v') xsecs from
%%%   Laporta Plasma Sources Sci. Tech. 23 (2014)
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

write_data = 0; % 0 for do not write and 1 for do write
write_txtFile = 0; % for writing to text file for two-term simulations

%%% set potential energy for transition from the ground state 0->0:58
%
Uvib = [0.000 0.288 0.573 0.855 1.133 1.408 1.679 1.947 2.211 2.471 ...
        2.728 2.982 3.232 3.478 3.270 3.959 4.195 4.426 4.654 4.878 ...
        5.099 5.315 5.528 5.737 5.942 6.143 6.339 6.532 6.721 6.905 ...
        7.084 7.260 7.430 7.596 7.757 7.913 8.064 8.210 8.350 8.485 ...
        8.614 8.737 8.853 8.963 9.067 9.163 9.252 9.335 9.409 9.476 ...
        9.535 9.587 9.631 9.667 9.696 9.717 9.732 9.742 9.748]; % [eV]

   
%%%   import text file data set
%
delims = 2;
A = importdata('../../Xsecs/Phy4Entry_eV_crossSections/data_Cshort.txt' ...
               ,'\t',delims);

lengthE = 1;
Eindex = 5;
while (A.data(1+lengthE,Eindex) ~= 0)
    lengthE = lengthE+1;
end
lengthE = lengthE-1; % data file erroneously contains last Energy term twice 
E = A.data(1:lengthE,Eindex); % energy grid 0->15 eV

numVib = 59;                 % there are 59 (0-58) vib states
Q = zeros(numVib,lengthE);
kstart = zeros(1,numVib); kstart(1) = 1;
kend   = zeros(1,numVib); kendlimit = length(A.data(:,1));
for j = 1:numVib
    
    kend(j) = kstart(j);
    while (A.data(kend(j),3) <= j-1)
        kend(j) = kend(j)+1;
        if(kend(j)==kendlimit+1)
            break;
        end
    end
    kend(j) = kend(j)-1;      % index where data for this j starts
    if (j<length(kstart))
        kstart(j+1) = kend(j)+1;  % index where data for this j ends
    end
    
    lengthQ = kend(j)-kstart(j); % length of current data -1 (see error above)
    
    for k=kstart(j):kend(j)-1 % minus 1 due to error above
        Q(j,k-kstart(j)+lengthE-lengthQ+1) = A.data(k,6)';
    end
end

close(figure(11));
figure(11);
semilogy(E,Q(2:11,:)/1e-16); axis([0 15 1e-10 1e1]);
set(gca,'ytick',10.^(-10:2:0));
set(gca,'xtick',0:3:15);
xlabel('energy [eV]'); ylabel('\sigma [10^-^1^6 cm^2]');
title('e+N_2(X^1,v=0)=>e+N_2(X^1,v=1:10)'); axis('square');
lg = legend('v1','v2','v3','v4','v5','v6','v7','v8','v9','v10');



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%                     write date to file
%%%

if(write_data)
    
    Laporta_xsecs.Uvib = Uvib;
    Laporta_xsecs.E = E;
    
    save('Laporta_xsecs.mat','Laporta_xsecs');
    
end


if(write_txtFile)
    fout = fopen('./vibTesting.txt','wt');
    for m=2:11 % v=0 => v=1:10
        fprintf(fout, '%s\n', 'EXCITATION');
        fprintf(fout, '%s\n', ['e+N2X1=>e+N2X1v',num2str(m-1)]);
        fprintf(fout, '%4.3f %4.0f %4.0f\n', Uvib(m), 0, 1);
        fprintf(fout, '%s\n', '1.   1.');
        fprintf(fout, '%s\n', '-----------------------------');
        for k=1:length(E)
            fprintf(fout, '%4.3f    %10.4e\n', E(k), 1e-4*Q(m,k));
        end
        fprintf(fout, '%s\n\n\n', '-----------------------------');
    end
    fclose(fout);
end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

end

