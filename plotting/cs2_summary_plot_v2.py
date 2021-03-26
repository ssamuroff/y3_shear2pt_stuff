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


plt.xlim(0.45,0.9)
plt.ylim(0.0,1.075)
plt.yticks(visible=False)

plt.xticks([0.4,0.5,0.6,0.7,0.8,0.9], fontsize=fontsize)
plt.xlabel(r'$S_8\equiv \sigma_8 (\Omega_{\rm m}/0.3)^{0.5}$')


inputs = {r'$1.$ \textbf{Fiducial DES Y3}': (0.756178,0.756178+2.37192e-02,0.756178-2.39828e-02,'#000000'),
         r'$2.$ No IAs': (0.773609,0.773609+1.71847e-02,0.773609-1.75473e-02,'#000000'),
         r'$3.$ NLA': (0.772924,0.772924+2.01912e-02,0.772924-2.08258e-02,'#000000'),
         r'$4.$ per-bin NLA': (0.781, 0.024,0,'#000000'),
         r'$5.$ $A_1>0$ prior': (0.768, 0.023,0,'#000000'),
         r'$6.$ Fixed $\nu$' : ( 0.773, 0.024,0,'#000000'),
        # r'Linear Theory' : (0.74,0.06),
         r'$7.$ $w$CDM': (0.72707,0.769725,0.704727,'#000000'),
         r'$8.$ HMCode $P(k)$' : (0.782, 0.027,0,'#000000'),
         #r'$8.$ $\Omega_{\rm b} h^2$ Prior': (0.764, 0.024,'#000000'), 
        # r'$9.$ DES + BAO + SN': (0.769, 0.020,'#191970'),
         r'$9.$ Planck 18 TT+TE+EE': (0.827,0.827+0.016,0.827-0.016,'#8b0000'),
         r'$10.$ Planck 18 TT+TE+EE ($w$CDM)': (0.,0.016,0,'#ffc0cb'),
         r'$11.$ KiDS-1000': (0.759,0.759+0.024,0.759-0.021,'#FA86C9'),
         r'$12.$ HSC Y1':(0.78,0.78+0.030,0.78-0.033,'#228B22'),
         r'$13.$ DES Y1 (NLA) ':(0.787306,0.806457,0.758579,'#191970'),
         r'$14.$ DES Y1 (TATT) ':(0.747195,0.786509,0.703743,'#191970')}
         #r'Low-$z$ External': (0.75,0.015)}

ninputs = len(inputs.keys())
print('%d lines'%ninputs)

y = 1.
dy = 1.05/ninputs

for i,label in enumerate(inputs.keys()):
	X,u,l,colour = inputs[label]
	if colour=='#000000':
		c = 'darkmagenta'
	else:
		c = colour

	#import pdb ; pdb.set_trace()
	
	try: 
		dX = [[X-l],[u-X]]
		#print(dX)
		plt.errorbar([X], [y], xerr=dX, marker='*', markeredgecolor=c, markerfacecolor=c, ecolor=c, linestyle='none')
	except:
		pass

	if i==0:
		plt.axvspan(l,u,color='plum',alpha=0.2)
		plt.axvline(X,color='k',ls=':')

	if label==r'$9.$ Planck 18 TT+TE+EE':
		plt.axhline(y+(dy/2), color='k', ls='--')


	
	plt.annotate(label,xy=(0.415,y-(dy/8)), fontsize=fontsize, color=colour)
	print(label)

	y-=dy

plt.subplots_adjust(wspace=0, hspace=0, bottom=0.14, left=0.13, right=0.97, top=0.98)
plt.savefig('s8_robustness_summary_v2.pdf')
plt.savefig('s8_robustness_summary_v2.png')

plt.close()
exit()






