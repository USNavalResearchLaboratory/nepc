function momentum_xsecs
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   this script computes the total momentum transfer xsecs for atomic
%%%   nitrogen species and corresponding rate constants
%%%
%%%   Qmom = Qelm + Qexc + Qizn
%%%
%%%   - superlastic included in Qexc
%%%   - Qelastic used for Qelm for j>4S,2D,2P
%%%   - Qizn for j>4S,2D,2P from Lotz
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
write_data = 0;
%addpath('../'); % path to MaxMobilityRateConst.m

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   load cross sections from YangWang 2014
%
YW = load('./YangWang_xsecs.mat');
YW = YW.YangWang_xsecs;
E = YW.E;        % energy [eV]
Qexc = YW.Qexc;  % excitation cross sections
Qelm = YW.Qelm;  
Qizn = YW.Qizn;


%%%   set Qelm
%
Qelm = zeros(27,length(E));
Qelm(1:3,:) = YW.Qelm;
for i = 4:27
    Qelm(i,:) = squeeze(YW.Qexc(i,i,:));
end

%%%   set Qexc
%
Qexc = squeeze(sum(YW.Qexc,2));
for i = 1:27
    Qexc(i,:) = Qexc(i,:)-squeeze(YW.Qexc(i,i,:))'; % subtract off elastic part
end
%Qexc = max(Qexc,0);

%%%   set Qizn
%
Qizn = zeros(27,length(E));
Qizn(1:3,:) = YW.Qizn;

a = [3.2 4.0]; b = [0.83 0.7]; c = [0.22 0.5]; q = [3 2]; P = [14.5 20.3];
% QLotz   = LotzIonization(E,a,b,c,q,P);
% QLotz2D = LotzIonization(E,a,b,c,q,P-2.4);
% QLotz2P = LotzIonization(E,a,b,c,q,P-3.6);
% figure(1); plot(E,Qizn(1,:),'b',E,sum(QLotz),'bx');
% legend('Wang','Lotz','location','best');
% figure(2); plot(E,Qizn(2,:),'r',E,sum(QLotz2D),'rx');
% legend('Wang','Lotz','location','best');
% figure(3); plot(E,Qizn(3,:),'g',E,sum(QLotz2P),'gx');
% legend('Wang','Lotz','location','best');
 
for i = 4:27
    Qizn(i,:) = sum(LotzIonization(E,a,b,c,q,P-YW.UeV(i)));
end

Qmom = Qelm+Qexc+Qizn;


%%%   now plot stuff
%

plot_total_momentum=1;
thisi = 1;
if(plot_total_momentum)
    close(figure(1));
    f1=figure(1); set(f1,'position',[10 100 1000 800]);
    %
    subplot(2,2,1);
    loglog(E,Qmom(thisi,:)*1e16,'black');
    hold on; plot(E, Qelm(thisi,:)*1e16,'r*');
    hold on; plot(E, Qexc(thisi,:)*1e16,'b*');
    hold on; plot(E, Qizn(thisi,:)*1e16,'g*');
    xlabel('electron energy [eV]'); 
    ylabel('cross section [1\times 10^-^1^6cm^2]');
    title('total momentum exchange with N(^4S)');
    axis([1e-3 1e3 1e-1 1e4]); 
%     set(gca,'XTick',0:10:50);
%     set(gca,'YTick',0:3:15);
    legend('tot','elm','exc','izn','location','NE');
%     %
    subplot(2,2,2);
    loglog(E,Qmom(thisi+1,:)*1e16,'black');
    hold on; plot(E, Qelm(thisi+1,:)*1e16,'r*');
    hold on; plot(E, Qexc(thisi+1,:)*1e16,'b*');
    hold on; plot(E, Qizn(thisi+1,:)*1e16,'g*');
    xlabel('electron energy [eV]'); 
    ylabel('cross section [1\times 10^-^1^6cm^2]');
    title('total momentum exchange with N(^2D)');
    axis([1e-3 1e3 1e-1 1e4]); 
%     set(gca,'XTick',0:10:50);
%     set(gca,'YTick',0:3:15);
    legend('tot','elm','exc','izn','location','NE');
%     %
    subplot(2,2,3);
    loglog(E,Qmom(thisi+2,:)*1e16,'black');
    hold on; plot(E, Qelm(thisi+2,:)*1e16,'r*');
    hold on; plot(E, Qexc(thisi+2,:)*1e16,'b*');
    hold on; plot(E, Qizn(thisi+2,:)*1e16,'g*');
    xlabel('electron energy [eV]'); 
    ylabel('cross section [1\times 10^-^1^6cm^2]');
    title('total momentum exchange with N(^2P)');
    axis([1e-3 1e3 1e-1 1e4]); 
%     set(gca,'XTick',0:10:50);
%     set(gca,'YTick',0:3:15);
    legend('tot','elm','exc','izn','location','NE');
%     %
    subplot(2,2,4);
    loglog(E,Qmom(thisi+3,:)*1e16,'black');
    hold on; plot(E, Qelm(thisi+3,:)*1e16,'r*');
    hold on; plot(E, Qexc(thisi+3,:)*1e16,'b*');
    hold on; plot(E, Qizn(thisi+3,:)*1e16,'g*');
    xlabel('electron energy [eV]'); 
    ylabel('cross section [1\times 10^-^1^6cm^2]');
    title('total momentum exchange with N(3s^4P)');
    axis([1e-3 1e3 1e-1 1e4]); 
%     set(gca,'XTick',0:10:50);
%     set(gca,'YTick',0:3:15);
    legend('tot','elm','exc','izn','location','NE');
%     %
end


%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
% if(write_total_momentum)
%     momentum.N4S.E = EmomS; % [eV]
%     momentum.N4S.Q = QmomS; % total momentum [cm^2]
%     momentum.N4S.Qelm = QelmS;
%     momentum.N4S.Qexc = QexcS;
%     momentum.N4S.Qizn = QiznS;
%     %
%     momentum.N2D.E = EmomD; % [eV]
%     momentum.N2D.Q = QmomD; % total momentum [cm^2]
%     momentum.N2D.Qelm = QelmD;
%     momentum.N2D.Qexc = QexcD;
%     momentum.N2D.Qizn = QiznD;
%     %
%     momentum.N2P.E = EmomP; % [eV]
%     momentum.N2P.Q = QmomP; % total momentum [cm^2]
%     momentum.N2P.Qelm = QelmP;
%     momentum.N2P.Qexc = QexcP;
%     momentum.N2P.Qizn = QiznP;
% 
%     save('momentum.mat','momentum');
% end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   create xsecs using expression from Lotz 1968
%%%   for ionization of atomic nitrogen
%%%

function [xsec] = LotzIonization(thisE,a,b,c,q,P)
    mc2 = 0.511e6;
    gamma = thisE/(mc2)+1;
    beta = sqrt(1-1./gamma.^2);
    ET = 0.5*mc2*beta.^2;
    for k = 1:length(a)
        for j = 1:length(ET)
            if(ET(j)<=P(k))
                xsec(k,j) = 0;
            else
                xsec(k,j) = 1e-14*a(k)*q(k).*log(ET(j)/P(k))/(ET(j)*P(k)) ...
                          .* (1-b(k)*exp(-c(k)*(ET(j)/P(k)-1)));
            end
        end
    end
end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%                     write date to file
%%%

if(write_data)
    
    total_xsecs.E = E;
    %
    total_xsecs.Qexc = Qexc;
    total_xsecs.Qelm = Qelm;
    total_xsecs.Qizn = Qizn;
    total_xsecs.Qmom = Qmom;
    
    save('total_xsecs.mat','total_xsecs');
    
end
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

end

