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
function dx = exponential2(t, x)
dx = zeros(2,1);

%     a is the natural growth rate of buffalo in the absence of predation,
%     c is the natural death rate of lion in the absence of food (buffalo),
%     b is the death rate per encounter of buffalo due to predation,
%     e is the efficiency of turning predated buffalo into lions. 
    
rmax = 0.002884;
theta = 5.946;
K = 49.6;
h1 = 0.045; % time to kill prey
h2 = 1.422; % time to eat prey
G = 1; %group effect
a = 0.5; % wildebeest density
eps = 0.01; % 
d = 0.03; % lion death rate


dx(1) = rmax * x(1) * (1- (x(1)/K)^theta - a*x(1)/(G+ a*(G*h1 + h2)*x(2)));
dx(2) = a*x(1)/(G+ a*(G*h1 + h2)*x(1)) * eps * x(2) - d * x(2);

end
