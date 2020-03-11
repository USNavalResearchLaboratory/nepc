function [ne] = CoronaModel_Nitrogen(model,Pgas,Jpeak)

model.hist.disable; % makes faster when running lots of iterations
% addpath('~/../../Applicaitons/COMSOL44/');
resultspath = './../parametric_data/';
comsolpath  = './../parametric_programs/';


% Nlos = 2.6868e25;              % Loschmidt's number [1/m^3]
% Nt   = Nlos*Pgas/760*273/Tgas; % particle number density


model.param.set('Pg0',Pgas);
model.param.set('Jpeak0',Jpeak);


%%% write stuff to text file
%
thisname = ['Swarm_vs_Corona_','P=',num2str(Pgas),'Torr_' ...
            'J=',num2str(Jpeak),'kAcm2'];
thisdata  = fullfile(resultspath,[thisname,'.txt']);
thismodel = fullfile(comsolpath,[thisname,'.mph']);

fid=fopen(thisdata,'wt');
fprintf(fid,'*** input parameters for simulation ***\n');
fprintf(fid,['P [Torr]         = ',num2str(Pgas), '\n']);
fprintf(fid,['Jpeak [kA/cm^2]  = ',num2str(Jpeak), '\n']);
fprintf(fid,'*********************************** \n');
%fclose(fid);


%%% obtain time dependent solution
%
model.sol('sol1').run;
mphsave(model,thismodel);


%%% get species densities at last time step (2*Tau_rise = end of pulse)
%
Te = mphglobal(model,'comp2.Te','t',2*Tau*1e-9); % [eV]
ne = mphglobal(model,'comp2.ne','t',2*Tau*1e-9); % [1/m^3]

%fid=fopen(filename,'wt');
fprintf(fid,'*********************************** \n');
fprintf(fid,'*********     Corona     ********** \n');
fprintf(fid,['Te (eV)      = ',num2str(Te), '\n']);
fprintf(fid,['ne (eV)      = ',num2str(ne), '\n']);
fprintf(fid,'*********************************** \n');
fclose(fid);


% save([chipath,'thischi',num2str(EN),'.mat'],'chi');


%
%
%
%
%



end

