function atomicN_excitation_allowed
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   Computes the excitation rate constant for optically allowed
%%%   transitions for some atomic nitrogen species for Maxwellian
%%%   electrons. The formula for the rate constant is
%%%   
%%%   kmn = 1.6e-5*fnm*gnm/(Unm*sqrt(Te))*exp(-Unm/Te)
%%%
%%%   See NRL formulary pg 52 eq. (4)
%%%   See Taylor 1988 CR
%%%   See J. Phys. Chem. Ref. Data, Vol. 36, No. 4, 2007
%%%   See FLYCHCK manual pg 25
%%%


writedata = 0;


%%%    create electron temperature grid
%
Te = 0.1:0.1:50;   % [eV]
   
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%           Define data for 4S transitions (29 total)
%%%

%%%   4S -> 4P3s (has 3 different spin states)
%
J = [1/2     3/2     5/2];
U = [10.326  10.330  10.336];   % [eV]
A = [4.00e0  4.03e0  4.07e0]*1e8;   % Einstein coefficient [Hz]
f = [4.32e-2 8.69e-2 1.32e-1];  % oscillator strength
%
k_1 = opt_allowed_Maxwell(Te,U(1),f(1));
k_2 = opt_allowed_Maxwell(Te,U(2),f(2));
k_3 = opt_allowed_Maxwell(Te,U(3),f(3));

k_4S_4P3s = k_1 + k_2 + k_3;
kE_4S_4P3s = U(1)*k_1 + U(2)*k_2 + U(3)*k_3;
kE4S4P3S_2 = 10.3319*opt_allowed_Maxwell(Te,10.3319,2.62e-1);
k_4Stot  = k_4S_4P3s;
kE_4Stot = kE_4S_4P3s;

%%%   4S -> 2P3s (has 2 different spin states)
%
J = [1/2     3/2];
U = [10.680  10.690];   % [eV]
A = [2.72e-4 4.94e-4]*1e8;   % Einstein coefficient [Hz]
f = [2.75e-6 9.96e-6];  % oscillator strength
%
k_1 = opt_allowed_Maxwell(Te,U(1),f(1));
k_2 = opt_allowed_Maxwell(Te,U(2),f(2));

k_4S_2P3s = k_1 + k_2;
kE_4S_2P3s = U(1)*k_1 + U(2)*k_2;
k_4Stot  = k_4Stot  + k_4S_2P3s;
kE_4Stot = kE_4Stot + kE_4S_2P3s;

%%%   4S -> 4P2p4 (has 3 different spin states)
%
J = [1/2     3/2     5/2];
U = [10.932  10.929  10.924];   % [eV]
A = [1.51e00 1.49e00 1.44e00]*1e8;   % Einstein coefficient [Hz]
f = [1.46e-2 2.87e-2 4.16e-2];  % oscillator strength
%
k_1 = opt_allowed_Maxwell(Te,U(1),f(1));
k_2 = opt_allowed_Maxwell(Te,U(2),f(2));
k_3 = opt_allowed_Maxwell(Te,U(3),f(3));

k_4S_4Pp4 = k_1 + k_2 + k_3;
kE_4S_4Pp4 = U(1)*k_1 + U(2)*k_2 + U(3)*k_3;
kE4S4Pp4_2 = 10.92*opt_allowed_Maxwell(Te,10.92,8.49e-2);
k_4Stot  = k_4Stot  + k_4S_4Pp4;
kE_4Stot = kE_4Stot + kE_4S_4Pp4;


%%%   4S -> 2D3s (has 2 different spin states)
%
J = [3/2     5/2];
U = [12.357  12.357];   % [eV]
A = [1.86e-6 8.40e-6]*1e8;   % Einstein coefficient [Hz]
f = [2.81e-8 1.90e-7];  % oscillator strength
%
k_1 = opt_allowed_Maxwell(Te,U(1),f(1));
k_2 = opt_allowed_Maxwell(Te,U(2),f(2));

k_4S_2D3s = k_1 + k_2;
kE_4S_2D3s = U(1)*k_1 + U(2)*k_2;
k_4Stot  = k_4Stot  + k_4S_2D3s;
kE_4Stot = kE_4Stot + kE_4S_2D3s;


%%%   4S -> 4P4s (has 3 different spin states)
%
J = [1/2     3/2     5/2];
U = [12.848  12.853  12.862];   % [eV]
A = [5.52e-1 5.66e-1 5.94e-1]*1e8;   % Einstein coefficient [Hz]
f = [3.86e-3 7.90e-3 1.24e-2];  % oscillator strength
%
k_1 = opt_allowed_Maxwell(Te,U(1),f(1));
k_2 = opt_allowed_Maxwell(Te,U(2),f(2));
k_3 = opt_allowed_Maxwell(Te,U(3),f(3));

k_4S_4P4s  = k_1 + k_2 + k_3;
kE_4S_4P4s = U(1)*k_1 + U(2)*k_2 + U(3)*k_3;
k_4Stot  = k_4Stot  + k_4S_4P4s;
kE_4Stot = kE_4Stot + kE_4S_4P4s;


%%%   4S -> 2P4s (has 2 different spin states)
%
J = [1/2     3/2];
U = [12.912  12.922];   % [eV]
A = [1.69e-3 3.75e-3]*1e8;   % Einstein coefficient [Hz]
f = [1.16e-5 5.18e-5];  % oscillator strength
%
k_1 = opt_allowed_Maxwell(Te,U(1),f(1));
k_2 = opt_allowed_Maxwell(Te,U(2),f(2));

k_4S_2P4s = k_1 + k_2;
kE_4S_2P4s = U(1)*k_1 + U(2)*k_2;
k_4Stot  = k_4Stot  + k_4S_2P4s;
kE_4Stot = kE_4Stot + kE_4S_2P4s;


%%%   4S -> 2P3d (has 2 different spin states)
%
J = [1/2     3/2];
U = [12.975  12.971];   % [eV]
A = [2.63e-3 4.29e-3]*1e8;   % Einstein coefficient [Hz]
f = [1.80e-5 5.88e-5];  % oscillator strength
%
k_1 = opt_allowed_Maxwell(Te,U(1),f(1));
k_2 = opt_allowed_Maxwell(Te,U(2),f(2));

k_4S_2P3d = k_1 + k_2;
kE_4S_2P3d = U(1)*k_1 + U(2)*k_2;
k_4Stot  = k_4Stot  + k_4S_2P3d;
kE_4Stot = kE_4Stot + kE_4S_2P3d;


%%%   4S -> 4F3d (has 2 different spin states)
%
J = [3/2     5/2];
U = [12.977  12.979];   % [eV]
A = [1.40e-4 3.37e-3]*1e8;   % Einstein coefficient [Hz]
f = [1.91e-6 6.92e-5];  % oscillator strength
%
k_1 = opt_allowed_Maxwell(Te,U(1),f(1));
k_2 = opt_allowed_Maxwell(Te,U(2),f(2));

k_4S_4F3d = k_1 + k_2;
kE_4S_4F3d = U(1)*k_1 + U(2)*k_2;
k_4Stot  = k_4Stot  + k_4S_4F3d;
kE_4Stot = kE_4Stot + kE_4S_4F3d;


%%%   4S -> 2F3d (has 1 spin state)
%
J = 5/2;
U = 12.995;   % [eV]
A = 1.95e-1*1e8;   % Einsten coefficient [Hz]
f = 4.00e-3;  % oscillator strength
%
k_4S_2F3d = opt_allowed_Maxwell(Te,U,f);
kE_4S_2F3d = U*k_4S_2F3d;
k_4Stot  = k_4Stot  + k_4S_2F3d;
kE_4Stot = kE_4Stot + kE_4S_2F3d;


%%%   4S -> 4P3d (has 3 different spin states)
%
J = [1/2     3/2     5/2];
U = [13.004  13.001  12.997];   % [eV]
A = [1.90e00 1.81e00 1.62e00]*1e8;   % Einstein coefficient [Hz]
f = [1.29e-2 2.47e-2 3.31e-2];  % oscillator strength
%
k_1 = opt_allowed_Maxwell(Te,U(1),f(1));
k_2 = opt_allowed_Maxwell(Te,U(2),f(2));
k_3 = opt_allowed_Maxwell(Te,U(3),f(3));

k_4S_4P3d  = k_1 + k_2 + k_3;
kE_4S_4P3d = U(1)*k_1 + U(2)*k_2 + U(3)*k_3;
k_4Stot  = k_4Stot  + k_4S_4P3d;
kE_4Stot = kE_4Stot + kE_4S_4P3d;


%%%   4S -> 4D3d (has 3 different spin states)
%
J = [1/2     3/2     5/2];
U = [13.016  13.018  13.019];   % [eV]
A = [7.62e-2 1.45e-1 1.12e-1]*1e8;   % Einstein coefficient [Hz]
f = [5.18e-4 1.97e-3 2.29e-3];  % oscillator strength
%
k_1 = opt_allowed_Maxwell(Te,U(1),f(1));
k_2 = opt_allowed_Maxwell(Te,U(2),f(2));
k_3 = opt_allowed_Maxwell(Te,U(3),f(3));

k_4S_4D3d  = k_1 + k_2 + k_3;
kE_4S_4D3d = U(1)*k_1 + U(2)*k_2 + U(3)*k_3;
k_4Stot  = k_4Stot  + k_4S_4D3d;
kE_4Stot = kE_4Stot + kE_4S_4D3d;


%%%   4S -> 2D3d (has 2 different spin states)
%
J = [3/2     5/2];
U = [13.033  13.036];   % [eV]
A = [7.62e-2 1.45e-1]*1e8;   % Einstein coefficient [Hz]
f = [2.32e-5 1.69e-4];  % oscillator strength
%
k_1 = opt_allowed_Maxwell(Te,U(1),f(1));
k_2 = opt_allowed_Maxwell(Te,U(2),f(2));

k_4S_2D3d = k_1 + k_2;
kE_4S_2D3d = U(1)*k_1 + U(2)*k_2;
k_4Stot  = k_4Stot  + k_4S_2D3d;
kE_4Stot = kE_4Stot + kE_4S_2D3d;


close(figure(2));
f2=figure(2); set(f2,'position', [50 100 1000 400]);
%
subplot(1,2,1);
loglog(Te,k_4S_4P3s);                % dominant energy contribution
hold on; plot(Te,k_4S_2P3s,'g');    
hold on; plot(Te,k_4S_4Pp4,'r');    % dominant energy contribution
hold on; plot(Te,k_4S_2D3s,'y');
hold on; plot(Te,k_4S_4P4s,'b--');  % dominant energy contribution
hold on; plot(Te,k_4S_2P4s,'magenta');
hold on; plot(Te,k_4S_2P3d,'magenta--');
hold on; plot(Te,k_4S_4F3d,'cyan--');
hold on; plot(Te,k_4S_2F3d,'y--');
hold on; plot(Te,k_4S_4P3d,'r--');  % dominant energy contribution
hold on; plot(Te,k_4S_4D3d,'g--');
hold on; plot(Te,k_4S_2D3d,'cyan');
hold on; plot(Te,k_4Stot,'black');  % total
hold on; plot(Te,k_4S_4P3s+k_4S_4Pp4+k_4S_4P4s+k_4S_4P3d,'r*');
axis([1e-1 50 1e-25 1e-5]); xlabel('T_e [eV]'); ylabel('k [cm^3/s]');
title('N(^4S) Optically allowed ks');
%
subplot(1,2,2);
loglog(Te,kE_4S_4P3s);                % dominant energy contribution
hold on; plot(Te,kE_4S_2P3s,'g');    
hold on; plot(Te,kE_4S_4Pp4,'r');     % dominant energy contribution
hold on; plot(Te,kE_4S_2D3s,'y');
hold on; plot(Te,kE_4S_4P4s,'b--');   % dominant energy contribution
hold on; plot(Te,kE_4S_2P4s,'magenta');
hold on; plot(Te,kE_4S_2P3d,'magenta--');
hold on; plot(Te,kE_4S_4F3d,'cyan--');
hold on; plot(Te,kE_4S_2F3d,'y--');
hold on; plot(Te,kE_4S_4P3d,'r--');  % dominant energy contribution
hold on; plot(Te,kE_4S_4D3d,'g--');
hold on; plot(Te,kE_4S_2D3d,'cyan');
hold on; plot(Te,kE_4Stot,'black');  % total
hold on; plot(Te,kE_4S_4P3s+kE_4S_4Pp4+kE_4S_4P4s+kE_4S_4P3d,'r*');
axis([1e-1 50 1e-25 1e-5]); xlabel('T_e [eV]'); ylabel('kE [eV-cm^3/s]');
title('N(^4S) Optically allowed kEs');

%%%
%%%
%%%

close(figure(4));
figure(4); 
subplot(1,2,1);
plot(Te,kE_4S_4P3s,'b'); 
hold on; plot(Te,kE4S4P3S_2,'r--');
%
hold on; plot(Te,kE_4S_4Pp4,'g');
hold on; plot(Te,kE4S4Pp4_2,'g*');
%axis([0.1 40 1e-25 1e-6]);
%
subplot(1,2,2);
plot(log10(Te),log10(kE_4S_4P3s),'b'); 
hold on; plot(log10(Te),log10(kE4S4P3S_2),'r--'); 
%axis([0.1 40 1e-25 1e-6]);

%%%
%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%%   create maxwellian avaraged rate constant for optically
%%%   allowed transitions
%%%
function kconst = opt_allowed_Maxwell(Te,U,f)

    Gaunt = 0.15+0.28*exp(U./Te).*expint(U./Te);
    kconst = 1.578e-5./sqrt(Te).*Gaunt.*exp(-U./Te)*f/U;

end

%%%
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



end


       