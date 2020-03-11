function [kmom] = MaxMobilityRateConst(EQ,Q,Te)

    % kmom [cm^3/s] is the mobility rate constant for Maxwellian EEDF
    % EQ [eV] is energy grid that cross section Q [cm^2] is on
    % Q [cm^2] is effective momentum xsec (Qelm + sum(Qinel))
    
    Q = Q*1e-4; % convert from cm^2 to m^2
    E = 0:Te/2e3:20*Te;     % electron kinetic energy [eV]
    FM = 2/sqrt(pi)/Te^(3/2)*exp(-E/Te);  % Maxwellian EEDF
    
    %%% check to make sure grid is refined enough using 0th 
    %%% and 2nd moments
    %
    test0 = trapz(E,FM.*E.^(1/2));   % should be one
    error0 = 100*abs(1-test0);
    if(error0>=1)
        warning('0th velocity moment not converged');
    end
    %
    ebar = trapz(E,FM.*E.^(3/2));    % should be 3*Te/2;
    error2 = 100*abs(ebar-3*Te/2)/(3*Te/2);
    if(error2>=1)
        warning('2nd velocity moment not converged');
    end
    
    
    %%% interpolate Q to energy grid and integrate
    %
    Qinterp = InterpAllowed(EQ,Q,E);
%     close(figure(100));
%     figure(100); loglog(E,Qinterp,'r*',EQ,Q,'b');
%     Qinterp(1)
    
    econst  = 1.6022e-19;
    meconst = 9.1094e-31;
    gamma = sqrt(2*econst/meconst); % sqrt(2*e/me)
    mueN = gamma/3/Te*trapz(E,E./Qinterp.*FM); % [m^3/s]
    
 
    kmom = econst/meconst/mueN*1e6; % [cm^3/s]

end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    Interp allowed xsecs (~ln(E)/E at high energy)
%%%

function [Q1] = InterpAllowed(E0,Q0,E1)

    Emax = E0(length(E0));
    Qmax = Q0(length(Q0));
    Q1 = interp1(E0,Q0,E1,'spline');
    for Ei = 1:length(E1)
        if(E1(Ei)>Emax)
            Q1(Ei) = Qmax*log(E1(Ei))./E1(Ei) ...
                   / (log(Emax)/Emax);
        end
    end
    
end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
