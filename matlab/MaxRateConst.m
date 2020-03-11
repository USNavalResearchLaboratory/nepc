function [k] = MaxRateConst(U,EQ,Q,Te,forbidden)

    % k [cm^3/s] is rate constant for Maswellian EEDF
    % U [eV] is potential energy for reaction
    % EQ [eV] is energy grid that cross section Q [cm^2] is on
    % 1 for forbidden and 0 for allowed
    
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
    if(forbidden)
        Qinterp = InterpForbidden(EQ,Q,E,U);
    else
        Qinterp = InterpAllowed(EQ,Q,E,U);
    end
%     close(figure(2));
%     figure(2); loglog(E,Qinterp,'r*',EQ,Q,'b');
    
    gamma = sqrt(2*1.7588e11); % sqrt(2*e/me)
    k = gamma*trapz(E,E.*Qinterp.*FM)*100; % [cm^3/s]

end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    Interp allowed xsecs (~ln(E)/E at high energy)
%%%

function [Q1] = InterpAllowed(E0,Q0,E1,U)

    Emax = E0(length(E0));
    Qmax = Q0(length(Q0));
    Q1 = interp1(E0,Q0,E1,'spline');
    for Ei = 1:length(E1)
        if(E1(Ei)<=U)
            Q1(Ei) = 0;
        end
        if(E1(Ei)>Emax)
            Q1(Ei) = Qmax*log(E1(Ei))./E1(Ei) ...
                   / (log(Emax)/Emax);
        end
    end
    
end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%    Interp forbidden xsecs (~1/E^3 at high energy)
%%%

function [Q1] = InterpForbidden(E0,Q0,E1,U)

    Emax = E0(length(E0));
    Qmax = Q0(length(Q0));
    Q1 = interp1(E0,Q0,E1,'pchirp');
    for Ei = 1:length(E1)
        if(E1(Ei)<=U)
            Q1(Ei) = 0;
        end
        if(E1(Ei)>Emax)
            Q1(Ei) = Qmax*(Emax./E1(Ei))^3;
        end
    end
    
end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
