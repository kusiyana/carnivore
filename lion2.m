 [t,x3] = ode45('exponential2', [0 5000], [100,100]);
 plot(t, x3);
legend('wb', 'lion', 4)
 
 %plot(x3(2), x3(3));