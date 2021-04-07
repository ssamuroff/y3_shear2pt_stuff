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

best_fits=True

plt.xlim(0.45,0.9)
plt.ylim(0.0,1.075)
plt.yticks(visible=False)

plt.xticks([0.4,0.5,0.6,0.7,0.8,0.9], fontsize=fontsize)
plt.xlabel(r'$S_8\equiv \sigma_8 (\Omega_{\rm m}/0.3)^{0.5}$')


inputs = {r'$1.$ \textbf{Fiducial DES Y3}': (0.759282,0.759282+2.46493e-02,0.759282-2.34257e-02,7.54768e-01,'#000000'),
         r'$2.$ DES Y3 optimised':(0.7723844, 0.789818,0.755415, 0,'#000000'),
         r'$3.$ No IAs': (0.773609,0.773609+0.0171847,0.773609-0.0175473,7.59853e-01,'#000000'),
         r'$4.$ NLA': (0.772924,0.772924+0.0201912,0.772924-0.0208258,7.72708e-01,'#000000'),
         r'$5.$ per-bin NLA': (0.781, 0.024,0,0.,'#000000'),
         r'$6.$ $A_1>0$ prior': (0.754651, 0.754651+0.0220130,0.754651-0.0223430,7.26813e-01,'#000000'),
         r'$7.$ Fixed $\nu$' : (0.772078, 0.772078+2.31110e-02,0.772078-2.34010e-02,7.53457e-01,'#000000'),
        # r'Linear Theory' : (0.74,0.06),
         r'$8.$ $w$CDM': (0.735182,0.735182+2.31179e-02,0.735182-4.13201e-02,6.98546e-01,'#000000'),
         r'$9.$ HMCode $P(k)$' : (0.782, 0.027,0,0.,'#000000'),
         #r'$8.$ $\Omega_{\rm b} h^2$ Prior': (0.764, 0.024,'#000000'), 
        # r'$9.$ DES + BAO + SN': (0.769, 0.020,'#191970'),
         r'$10.$ Planck 18 TT+TE+EE': (0.827,0.827+0.016,0.827-0.016,0.,'#A4CD64'),
         r'$11.$ Planck 18 TT+TE+EE ($w$CDM)': (0.,0.016,0,0.,'#ffc0cb'),
         r'$12.$ KiDS-1000': (0.759,0.759+0.024,0.759-0.021,0.,'#FA86C9'),
         r'$13.$ HSC Y1 Hikage et al':(0.78,0.78+0.030,0.78-0.033,0.,'#3775A1'),
         r'$14.$ HSC Y1 Hamana et al':(0.804,0.804+0.032,0.804-0.029,0.,'#3775A1'),
         r'$15.$ DES Y1 (NLA) ':(0.7799136,0.806457,0.758579,0.,'#DD9EE8'),
         r'$16.$ DES Y1 (TATT) ':( 0.7307221,0.786509,0.703743,0.,'#DD9EE8')}
         #r'Low-$z$ External': (0.75,0.015)}



ninputs = len(inputs.keys())
print('%d lines'%ninputs)

y = 1.
dy = 1.05/ninputs

for i,label in enumerate(inputs.keys()):
	X,u,l,BF,colour = inputs[label]
	if colour=='#000000':
		c = 'darkmagenta'
	else:
		c = colour
	
	try: 
		dX = [[X-l],[u-X]]
		#print(dX)
		if best_fits: 
			#import pdb ; pdb.set_trace()
			plt.errorbar([X], [y+dy/8], xerr=dX, marker='*', markeredgecolor=c, markerfacecolor=c, ecolor=c, linestyle='none')
			plt.errorbar([BF], [y-dy/8], xerr=dX, marker='.', markeredgecolor=c, markerfacecolor='w', ecolor=c, linestyle='none')
		else:
			plt.errorbar([X], [y], xerr=dX, marker='*', markeredgecolor=c, markerfacecolor=c, ecolor=c, linestyle='none')
		
	except:
		pass

	if i==0:
		plt.axvspan(l,u,color='plum',alpha=0.2)
		plt.axvline(X,color='k',ls=':')

	if label==r'$10.$ Planck 18 TT+TE+EE':
		plt.axhline(y+(dy*2/3), color='darkmagenta', ls='--')


	
	plt.annotate(label,xy=(0.415,y-(dy/8)), fontsize=fontsize, color=colour)
	print(label)

	y-=dy

plt.subplots_adjust(wspace=0, hspace=0, bottom=0.14, left=0.13, right=0.97, top=0.98)
plt.savefig('s8_robustness_summary_v2.pdf')
plt.savefig('s8_robustness_summary_v2.png')

plt.close()
exit()






