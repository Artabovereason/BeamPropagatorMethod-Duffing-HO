import numpy as np

'''
	omega 		  : the frequency of oscillation of time-dependent potential.
	amplitude	  : amplitude of the cos in V
	Nx, Ny		  : grid points.
	dt			  : evolution step.
	ntp 		  : number of periods.
	tmax 		  : end of propagation.
	xmax 		  : x-window size.
	ymax 		  : y-window size.
	images    	  : number of .png images.
	absorb_coeff  : 0 = periodic boundary
	output_choice : If 1, it plots on the screen but does not save the images.
					If 2, it saves the images but does not plot on the screen.
					If 3, it saves the images and plots on the screen.

	fixmaximum	  : fixes a maximum scale of |psi|**2 for the plots.
				    If 0, it does not fix it.

	psi_0		  : initial wavefunction.
	f 			  : a Gaussian centered at one of the wells
	V			  : a double well potential

'''

omega         = float(input('Enter the value of omega : '))
amplitude	  = 0.1
Nx 			  = 600
Ny 			  = Nx
dt 			  = 0.01
ntp 		  = 3
if omega == 0 :
	tmax 	  = ntp*2*np.pi
else:
	tmax      = ntp*2*np.pi/omega
xmax 	      = 5
ymax 		  = xmax
images 		  = 300
absorb_coeff  = 20
output_choice = 3
fixmaximum	  = 1.25

def psi_0(x,y):
	f = 0.j+np.exp(-((x-1)**2)/2)/np.sqrt(np.sqrt(np.pi))
	return f;

def V(x,y,t,psi,omega,amplitude):
	V = ((x+np.sin(omega*t))**2-1)**2/8 + amplitude*np.sin(omega*t/0.5)
	return V;
