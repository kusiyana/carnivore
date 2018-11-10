% exponential.m
%
% Implements the function dx/dt = x
%
% Inputs:
%   t - Time variable: not used here because our equation
%       is independent of time, or 'autonomous'.
%   x - Independent variable: this is our population
% Output:
%   dx - First derivative: the rate of change of the
%        population, given the population
function dx = exponential(t, x)
dx = zeros(3,1);

%     a is the natural growth rate of buffalo in the absence of predation,
%     c is the natural death rate of lion in the absence of food (buffalo),
%     b is the death rate per encounter of buffalo due to predation,
%     e is the efficiency of turning predated buffalo into lions. 
    
    a = 0.03;
    b = 0.0371;
    c = 0.85;
    e = 0.27 ;
    
    
    
    %gaussian behaviour
    gb = 200; % point of maximum cooperation
    gc = 400; % grow and die rate
    g = 0.1+ 17 * exp(-1*((x(3)-gb)^2)/(2*gc^2));
g;
    timecycle = 200;
    summerfactor = 0.5;
     
     if (t > timecycle) summerfactor = 0.45;
     end
     if (t > timecycle*2) summerfactor = 0.88;
     end
     
dx(1) = 0; %0.01*x(1) - 0.1*x(2);

dx(2) = summerfactor * a*x(2) - 0.01*x(2) - b*x(3);
dx(3) = (g*e * b * x(2) * (x(3))) - (c * x(3))^1.5;
x(3);
end
