##########################################################
# Starting script to the module 'SIR models of HIV epidemic'
##########################################################
# implements the basic SIR model, and plots simulation results

# LOAD LIBRARIES
library(odesolve)


###################################
# FUNCTION DEFINITIONS
###################################
# SIR <- function(t, x, parms)
# Use: calculates the derivatives for the SIR model

SIR <- function(t, x, parms){
	with(as.list(c(parms,x)),{
		dN = popGrowth * dF/50
		dF = -3*dF
 		der <- c(dN, dF) #, dD_m, dD_fh, dD_fu
		list(der)
	}) # end of 'with'
}  # end of function definition



	### INITIALIZE PARAMETER SETTINGS
# set the parameters of the model
	cond_factor = 0 #proportion using condoms
parms <- c(
	popGrowth		= 0.025 # pop growth rate
	)		

# set the initial values

dt    <- seq(0,1,0.002)
simulation <- list(); integral <- list(); prev <- list(); prevC <- list()

inits <- c(
dN = 1,     #D_m = 0
dF = 1
)	

simulation[[1]] <- as.data.frame(lsoda(inits, dt, SIR, parms=parms)) # this way our set 'parms' will be used as default
attach(simulation[[1]]) # attach command allows you to refer to the columns of the data frame directly.
plot(simulation[[1]][,1], simulation[[1]][,2], type="l", col="red")

