 [t,x3] = ode45('exponential', [0 2700], [0,10000,100]);
 plot(t, x3);
% legend('grass', 'buffalo', 'lion', 4)
 
 %plot(x3(2), x3(3));