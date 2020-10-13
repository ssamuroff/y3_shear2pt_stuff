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

fontsize=15

plt.subplot(111)


plt.xlim(0.45,0.95)
plt.ylim(0.0,1.1)
plt.yticks(visible=False)

plt.xticks([0.4,0.5,0.6,0.7,0.8,0.9], fontsize=fontsize)
plt.xlabel(r'$S_8\equiv \sigma_8 (\Omega_{\rm m}/0.3)^{0.5}$')

inputs = {r'Fiducial': (0.75,0.05),
         r'No IAs': (0.8,0.05),
         r'NLA IAs': (0.77,0.05),
         r'per-bin IAs': (0.7,0.05),
         r'Fixed $\nu$' : (0.77,0.04),
         r'Linear Theory' : (0.74,0.06),
         r'Baryonic $P(k)$' : (0.76,0.05),
         r'$\Omega_{\rm b} h^2$ Prior': (0.73,0.06), 
         r'Low-$z$ External': (0.74,0.07),
         r'Planck': (0.82,0.02),
         r'DES Y3 + Low-$z$ External': (0.75,0.015)}

ninputs = len(inputs.keys())
print('%d lines'%ninputs)

y = 1.
dy = 1.05/ninputs

for i,label in enumerate(inputs.keys()):
	X,dX = inputs[label]
	plt.errorbar([X], [y], xerr=dX, marker='*', markeredgecolor='darkmagenta', markerfacecolor='darkmagenta', ecolor='darkmagenta', linestyle='none')

	if i==0:
		plt.axvspan(X-dX,X+dX,color='plum',alpha=0.2)
		plt.axvline(X,color='k',ls=':')

	if label==r'Low-$z$ External':
		plt.axhline(y+(dy/2), color='k', ls='--')


	
	plt.annotate(label,xy=(0.42,y-(dy/8)), fontsize=fontsize)
	print(label)

	y-=dy

plt.subplots_adjust(wspace=0, hspace=0, bottom=0.14, left=0.13, right=0.97, top=0.98)
plt.savefig('s8_robustness_summary.pdf')
plt.savefig('s8_robustness_summary.png')
