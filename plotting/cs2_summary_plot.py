import numpy as np
import sys
import pylab as plt
plt.switch_backend('pdf')
plt.style.use('y1a1')
from astropy.cosmology import Planck15
import fitsio as fi
from scipy.optimize import curve_fit

from matplotlib import rcParams

fillcol='plum'

rcParams['xtick.major.size'] = 3.5
rcParams['xtick.minor.size'] = 1.7
rcParams['ytick.major.size'] = 3.5
rcParams['ytick.minor.size'] = 1.7
rcParams['xtick.direction']='in'
rcParams['ytick.direction']='in'

fontsize=14

plt.subplot(111)


plt.xlim(0.45,0.95)
plt.ylim(0.0,1.1)
plt.yticks(visible=False)

plt.xticks([0.4,0.5,0.6,0.7,0.8,0.9], fontsize=fontsize)
plt.xlabel(r'$S_8\equiv \sigma_8 (\Omega_{\rm m}/0.3)^{0.5}$')

inputs = {r'$1.$ \textbf{Fiducial DES Y3}': (0.766,0.023,'#000000'),
         r'$2.$ No IAs': (0.769,0.019,'#000000'),
         r'$3.$ NLA': (0.778,0.019,'#000000'),
         r'$4.$ per-bin NLA': (0.781, 0.024,'#000000'),
         r'$5.$ Fixed $\nu$' : ( 0.773, 0.024,'#000000'),
        # r'Linear Theory' : (0.74,0.06),
         r'$6.$ $w$CDM': (0.738,0.035,'#000000'),
         r'$7.$ HMCode $P(k)$' : (0.76,0.05,'#000000'),
         r'$8.$ $\Omega_{\rm b} h^2$ Prior': (0.73,0.06,'#000000'), 
         r'$9.$ External BAO+SN': (0.74,0.07,'#191970'),
         r'$10.$ Planck 18 TT+TE+EE': (0.827,0.016,'#8b0000'),
         r'$11.$ Planck 18 TT+TE+EE ($w$CDM)': (0.,0.016,'#ffc0cb'),
         r'$12.$ KiDS-1000': (0.759,0.024,'#FA86C9'),
         r'$13.$ HSC Y1':(0.804,0.032,'#228B22')}
         #r'Low-$z$ External': (0.75,0.015)}

ninputs = len(inputs.keys())
print('%d lines'%ninputs)

y = 1.
dy = 1.05/ninputs

for i,label in enumerate(inputs.keys()):
	X,dX,colour = inputs[label]
	if colour=='#000000':
		c = 'darkmagenta'
	else:
		c = colour
	
	plt.errorbar([X], [y], xerr=dX, marker='*', markeredgecolor=c, markerfacecolor=c, ecolor=c, linestyle='none')

	if i==0:
		plt.axvspan(X-dX,X+dX,color='plum',alpha=0.2)
		plt.axvline(X,color='k',ls=':')

	if label==r'$9.$ External BAO+SN':
		plt.axhline(y+(dy/2), color='k', ls='--')


	
	plt.annotate(label,xy=(0.42,y-(dy/8)), fontsize=fontsize, color=colour)
	print(label)

	y-=dy

plt.subplots_adjust(wspace=0, hspace=0, bottom=0.14, left=0.13, right=0.97, top=0.98)
plt.savefig('s8_robustness_summary.pdf')
plt.savefig('s8_robustness_summary.png')

plt.close()


plt.subplot(111)


plt.xlim(0.45,0.95)
plt.ylim(0.0,1.1)
plt.yticks(visible=False)

plt.xticks([0.4,0.5,0.6,0.7,0.8,0.9], fontsize=fontsize)
plt.xlabel(r'$S_8\equiv \sigma_8 (\Omega_{\rm m}/0.3)^{0.5}$')

inputs = {r'$1.$ \textbf{Fiducial DES Y3}': (0.766,0.023,'#000000'),
         r'$2.$ No IAs': (0.769,0.019,'#000000'),
         r'$3.$ NLA': (0.778,0.019,'#000000'),
         r'$4.$ per-bin TATT': (0.,0.05,'#000000')}
         #r'Low-$z$ External': (0.75,0.015)}

ninputs = len(inputs.keys())
print('%d lines'%ninputs)

y = 1.
dy = 1.05/ninputs

for i,label in enumerate(inputs.keys()):
	X,dX,colour = inputs[label]
	if colour=='#000000':
		c = 'darkmagenta'
	else:
		c = colour
	
	plt.errorbar([X], [y], xerr=dX, marker='*', markeredgecolor=c, markerfacecolor=c, ecolor=c, linestyle='none')

	if i==0:
		plt.axvspan(X-dX,X+dX,color='plum',alpha=0.2)
		plt.axvline(X,color='k',ls=':')

	if label==r'$9.$ External BAO+SN':
		plt.axhline(y+(dy/2), color='k', ls='--')


	
	plt.annotate(label,xy=(0.42,y-(dy/8)), fontsize=fontsize, color=colour)
	print(label)

	y-=dy

plt.subplots_adjust(wspace=0, hspace=0, bottom=0.14, left=0.13, right=0.97, top=0.98)
plt.savefig('s8_robustness_summary_ias.pdf')
plt.savefig('s8_robustness_summary_ias.png')
