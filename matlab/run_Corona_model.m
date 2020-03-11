%%% script to run comsol with matlab function
%%%
%%%
%
%clear all;


%%% set path and filename for source program
%
filepath = '../';
filename = '0D_Swarm_vs_Corona_v02';


%%% set path to save stuff
%
% resultspath = './../parametric_data/';
resultspath = './../parametric_data_new/';
% resultspath = './../parametric_data_noPar/';
comsolpath  = './../parametric_programs/';


%%% set input parameters
%
Tau   = 50;   % beam rise time [ns]
rB    = 1;    % beam radius [cm]
Epeak = 1;    % beam energy [MeV]
% Pgas  = 20;   % initial gas pressure [Torr]
Tgas  = 300;  % initial gas temperature [K]
% Jpeak = 20;   % peak current density [kA/cm^2]

Pgas = [0.5,1,2,5,10,20];
%Jpeak = [1:1:10,20:10:100,200:100:500]; % peak current density [kA/cm^2]
Jpeak = 50:100:950;
neS = zeros(size(Jpeak));
neC = zeros(size(Jpeak));
for j=1:length(Pgas);
  for i=1:length(Jpeak)

    %%% define model and open it
    %
    model = mphload([filepath,filename]);
    model.hist.disable; % makes faster when running lots of iterations
    model.param.set('Pg',[num2str(Pgas(j)),'[torr]']);
    model.param.set('Tg',[num2str(Tgas),'[K]']);
    model.param.set('Jpeak',[num2str(Jpeak(i)),'[kA/cm^2]']);
    model.param.set('Tau_rise',[num2str(Tau),'[ns]']);
    model.param.set('rB',[num2str(rB),'[cm]']);
    model.param.set('KEB0',[num2str(Epeak),'[MV]']);

    %%% write stuff to text file
    %
    thisname = ['Swarm_vs_Corona_','P=',num2str(Pgas(j)),'Torr_' ...
                'J=',num2str(Jpeak(i)),'kAcm2'];
    thisdata  = fullfile(resultspath,[thisname,'.txt']);
    thismodel = fullfile(comsolpath,[thisname,'.mph']);


    %%% obtain time dependent solution
    %
    model.sol('sol1').run;
    mphsave(model,thismodel);


    %%% get Swarm stuff at last time step (2*Tau = end of pulse)
    %
    Te_S = mphglobal(model,'comp1.Te','t',2*Tau*1e-9); % [eV]
    ne_S = mphglobal(model,'comp1.ne','t',2*Tau*1e-9,'unit','1/cm^3'); % [1/cm^3]
    neS(i) = ne_S;
    N20_S= mphglobal(model,'comp1.N20','t',2*Tau*1e-9,'unit','1/cm^3'); % [1/cm^3]


    %%% get Corona stuff at last time step
    %
    Te_C = mphglobal(model,'comp2.Te','t',2*Tau*1e-9); % [eV]
    Th_C = mphglobal(model,'comp2.Th','t',2*Tau*1e-9); % [eV]
    %
    Zbar = mphglobal(model,'comp2.Zbar','t',2*Tau*1e-9); % sum_i(NiZi^2)/ne
    %
    ne_C = mphglobal(model,'comp2.ne','t',2*Tau*1e-9,'unit','1/cm^3'); % [1/cm^3]
    neC(i) = ne_C;
    %
    N20_C= mphglobal(model,'comp2.N20','t',2*Tau*1e-9,'unit','1/cm^3'); % [1/cm^3]
    N2x_C= mphglobal(model,'comp2.N2x','t',2*Tau*1e-9,'unit','1/cm^3'); % [1/cm^3]
    N2p_C= mphglobal(model,'comp2.N2p','t',2*Tau*1e-9,'unit','1/cm^3'); % [1/cm^3]
    %
    N0_C= mphglobal(model,'comp2.N0','t',2*Tau*1e-9,'unit','1/cm^3'); % [1/cm^3]
    Nx_C= mphglobal(model,'comp2.Nx','t',2*Tau*1e-9,'unit','1/cm^3'); % [1/cm^3]
    N1_C= mphglobal(model,'comp2.Np','t',2*Tau*1e-9,'unit','1/cm^3'); % [1/cm^3]
    N2_C= mphglobal(model,'comp2.Np2','t',2*Tau*1e-9,'unit','1/cm^3'); % [1/cm^3]
    N3_C= mphglobal(model,'comp2.Np3','t',2*Tau*1e-9,'unit','1/cm^3'); % [1/cm^3]
    N4_C= mphglobal(model,'comp2.Np4','t',2*Tau*1e-9,'unit','1/cm^3'); % [1/cm^3]
    N5_C= mphglobal(model,'comp2.Np5','t',2*Tau*1e-9,'unit','1/cm^3'); % [1/cm^3]
    N6_C= mphglobal(model,'comp2.Np6','t',2*Tau*1e-9,'unit','1/cm^3'); % [1/cm^3]
    N7_C= mphglobal(model,'comp2.Np7','t',2*Tau*1e-9,'unit','1/cm^3'); % [1/cm^3]



    %%% write data to text file
    %
    formatSpec ='%10.3e\n';
    fid=fopen(thisdata,'wt');
    fprintf(fid,'*** input parameters for simulation ***\n');
    fprintf(fid,['Pg [Torr]        = ',num2str(Pgas(j)), '\n']);
    fprintf(fid,['Tg [K]           = ',num2str(Tgas), '\n']);
    fprintf(fid,['Ebeam [MeV]      = ',num2str(Epeak), '\n']);
    fprintf(fid,['Tau_rise [ns]    = ',num2str(Tau), '\n']);
    fprintf(fid,['rbeam [cm]       = ',num2str(rB), '\n']);
    fprintf(fid,['Jbeam [kA/cm^2]  = ',num2str(Jpeak(i)), '\n']);
    fprintf(fid,'***************************************\n');
    fprintf(fid,'****   Swarm at t=2Tau_rise    ********\n');
    fprintf(fid,'***************************************\n');
    fprintf(fid,['Te (eV)      = ',num2str(Te_S), '\n']);
    fprintf(fid,['ne  (1/cc)   = ',num2str(ne_S,formatSpec), '\n']);
    fprintf(fid,['N20 (1/cc)   = ',num2str(N20_S,formatSpec), '\n']);
    fprintf(fid,'***************************************\n');
    fprintf(fid,'****   Corona at t=2Tau_rise   ********\n');
    fprintf(fid,'***************************************\n');
    fprintf(fid,['Te (eV)      = ',num2str(Te_C), '\n']);
    fprintf(fid,['Th (eV)      = ',num2str(Th_C), '\n']);
    fprintf(fid,['Zbar         = ',num2str(Zbar), '\n']);
    fprintf(fid,['ne  (1/cc)   = ',num2str(ne_C,formatSpec), '\n']);
    fprintf(fid,['N20 (1/cc)   = ',num2str(N20_C,formatSpec), '\n']);
    fprintf(fid,['N2x (1/cc)   = ',num2str(N2x_C,formatSpec), '\n']);
    fprintf(fid,['N2p (1/cc)   = ',num2str(N2p_C,formatSpec), '\n']);
    fprintf(fid,['N0  (1/cc)   = ',num2str(N0_C,formatSpec), '\n']);
    fprintf(fid,['Nx  (1/cc)   = ',num2str(Nx_C,formatSpec), '\n']);
    fprintf(fid,['N1  (1/cc)   = ',num2str(N1_C,formatSpec), '\n']);
    fprintf(fid,['N2  (1/cc)   = ',num2str(N2_C,formatSpec), '\n']);
    fprintf(fid,['N3  (1/cc)   = ',num2str(N3_C,formatSpec), '\n']);
    fprintf(fid,['N4  (1/cc)   = ',num2str(N4_C,formatSpec), '\n']);
    fprintf(fid,['N5  (1/cc)   = ',num2str(N5_C,formatSpec), '\n']);
    fprintf(fid,['N6  (1/cc)   = ',num2str(N6_C,formatSpec), '\n']);
    fprintf(fid,['N7  (1/cc)   = ',num2str(N7_C,formatSpec), '\n']);
    fprintf(fid,'***************************************\n');
    fclose(fid);
i
  end
  j
end


%%% plot electron density vs current density
%
% close(figure(7));
figure(7); 
loglog(Jpeak,neC,'g','Linewidth',2);
% title(['Pgas = ',num2str(Pgas),' torr']);
% set(gca,'fontsize',14);
% legend('Swarm','Corona');

%
%
%
%
%
%

