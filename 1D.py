import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import cm
import shutil
import platform
import imageio

''''
	grid         : define a grid.
	L            : builds the Laplacian in Fourier space.
	absorb       : introduces an absorbing shell at the border of the computational window.
	savepsi      : saves the data of abs(psi)**2 at different values of t.
	V            : a double well potential.
	output       : defines graphic output: |psi|^2 is depicted.
	final_output : some operations after the computation is finished: save the
				   final value of psi, generate videos and builds the final
				   plot: a contour map of the y=0 cut as a function of x and t.
	movie        : generates video from the saved figures.
				   This function is called by final_output.
'''

omega         = float(input('Enter the value of omega : '))
amplitude	  = 0.1
filename 	  = []

def grid(Nx,Ny,xmax,ymax):
	x = np.linspace(-xmax, xmax-2*xmax/Nx, Nx)    						 	     # x variable
	y = 0                													     # not used, but a value must be given
	return x,y;

def L(Nx,Ny,xmax,ymax):
	kx = np.linspace(-Nx/4/xmax, Nx/4/xmax-1/2/xmax, Nx)     				     # x variable
	return (2*np.pi*1.j*kx)**2

def absorb(x,y,xmax,ymax,dt,absorb_coeff):
	wx = xmax/20
	return np.exp(-absorb_coeff*(2-np.tanh((x+xmax)/wx)+np.tanh((x-xmax)/wx))*dt);

def savepsi(Ny,psi):
	return abs(psi)**2

def V(x,y,t,psi,omega,amplitude):										  		 # A double well potential
	V = ((x+np.sin(omega*t))**2-1)**2/8 + amplitude*np.sin(omega*t/0.5)
	return V;

def output(x,y,psi,n,t,folder,output_choice,fixmaximum):
	if (output_choice==2) or (output_choice==3):
		num =str(int(n))
		if n < 100:
			num ='0'+str(int(n))
		if n < 10:
			num ='00'+str(int(n))
	fig = plt.figure("1D plot")													 # figure
	plt.clf()                       											 # clears the figure
	plt.plot(x, abs(psi)**2 , color='red')  									 # makes the plot
	plt.plot(x, V(x,0,t,psi,omega,amplitude) , color='blue' )
	plt.xlabel('$x$')           												 # format LaTeX if installed (choose axes labels,
	plt.ylabel('$|\psi|^2$')    												 # title of the plot and axes range
	plt.title('$t=$ %f'%(t))    												 # title of the plot
	plt.axis([min(x),max(x),-0.5,2.5])
    # Saves figure
	if (output_choice==2) or (output_choice==3):
		figname = folder+'/fig'+num+'.png'
		plt.savefig(figname)
		filename.append(figname)
	# Displays on screen
	if (output_choice==1) or (output_choice==3):
		plt.show(block=False)
		fig.canvas.flush_events()
	return;

def final_output(folder,x,Deltat,psi,savepsi,output_choice,images,fixmaximum):
	np.save(folder,psi)															 # saves final wavefunction
	if (output_choice==2) or (output_choice==3):
		movie(folder)	                        								 # creates video
	# 																			 # Now we make a plot of the evolution depicting the 1D cut at y=0
	tvec=np.linspace(0,Deltat*images,images+1)
	tt,xx=np.meshgrid(tvec,x)
	figtx = plt.figure("Evolution of |psi(x)|^2")            				     # figure
	plt.clf()                													 # clears the figure
	figtx.set_size_inches(8,6)
    # Generates the plot
	toplot=savepsi
	if fixmaximum>0:
		toplot[toplot>fixmaximum]=fixmaximum
	plt.contourf(xx, tt, toplot, 100, cmap=cm.jet, linewidth=0, antialiased=False)
	cbar=plt.colorbar()              											 # colorbar
	plt.xlabel('$x$')                 											 # axes labels, title, plot and axes range
	plt.ylabel('$t$')
	cbar.set_label('$|\psi|^2$',fontsize=14)
	figname = folder+'/sectx.png'
	plt.savefig(figname)    											  		 # Saves the figure
	plt.show()      															 # Displays figure on screen

def movie(folder):
	with imageio.get_writer('mygif.gif', mode='I') as writer:
	    for figname in filename[1:]:
	        image = imageio.imread(figname)
	        writer.append_data(image)

	for figname in set(filename):
	    os.remove(figname)
