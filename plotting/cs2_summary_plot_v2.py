import numpy as np
import sys
import pylab as plt
plt.switch_backend('pdf')
plt.style.use('y1a1')
from matplotlib import rcParams


rcParams['xtick.major.size'] = 3.5
rcParams['xtick.minor.size'] = 1.7
rcParams['ytick.major.size'] = 3.5
rcParams['ytick.minor.size'] = 1.7
rcParams['xtick.direction']='in'
rcParams['ytick.direction']='in'

fontsize=12

plt.xlim(0.45,0.9)
plt.ylim(-0.015,1.075)
plt.yticks(visible=False)

plt.xticks([0.4,0.5,0.6,0.7,0.8,0.9], fontsize=fontsize)
plt.xlabel(r'$S_8\equiv \sigma_8 (\Omega_{\rm m}/0.3)^{0.5}$')

# name, posterior mean, uerr, lerr, colour
inputs = {r'$1.$ \textbf{Fiducial DES Y3 cosmic shear }': (0.759282,0.0246493,0.0234257,'#8b008b'),
         r'$2.$ DES Y3 optimized':(0.7723844, 0.0174336,0.016969,'#8b008b'),
         r'$3.$ No IAs': (0.773609,0.0171847,0.0175473,'#8b008b'),
         r'$4.$ NLA': (0.772924,0.0201912,0.0208258,'#8b008b'),
         r'$5.$ NLA, free $a_1$ per $z-$bin': (0.789564, 0.0224087,0.0197953,'#8b008b'),
         r'$6.$ $a_1>0$ prior': (0.754651, 0.0220130, 0.0223430,'#8b008b'),
         r'$7.$ Fixed $\nu$' : (0.772078, 0.0231110, 0.0234010,'#8b008b'),
         r'$8.$ $w$CDM': (0.735182,0.0231179,0.0413201,'#8b008b'),
         r'$9.$ Baryon $P(k)$ (HMCode)' : (0.772318, 0.0261294, 0.0265586,'#8b008b'),
         r'$10.$ Planck 18 TT+TE+EE+lowE': (0.827, 0.016, 0.016,'#A4CD64'),
         r'$11.$ Planck 18 TT+TE+EE+lowE ($w$CDM)': (0.795826, 0.0265606, 0.0281404,'#A4CD64'),
         r'$12.$ Planck 18 Lensing': (0.8663937, 0.0631783, 0.0608757,'#8b008b'),
         r'$13.$ KiDS-1000': (0.759, 0.024, 0.021,'#FA86C9'),
         r'$14.$ HSC Y1 $C_\ell$':(0.78, 0.030, 0.033,'#3775A1'),
         r'$15.$ HSC Y1 $\xi_\pm$':(0.804, 0.032, 0.029,'#3775A1'),
         r'$16.$ DES Y1 (NLA) ':(0.7799136, 0.0265434, 0.0213346,'#DD9EE8'),
         r'$17.$ DES Y1 (TATT) ':(0.7307221, 0.0557869, 0.0269791,'#DD9EE8')}


ninputs = len(inputs.keys())
print('%d lines'%ninputs)

y = 1.
dy = 1.05/ninputs

for i,label in enumerate(inputs.keys()):
	X,u,l,colour = inputs[label]

	try: 
		dX = [[l],[u]]
		plt.errorbar([X], [y], xerr=dX, marker='*', markeredgecolor=colour, markerfacecolor=colour, ecolor=colour, linestyle='none')		
	except:
		pass

	# vertical error band
	if i==0:
		plt.axvspan(X-l,X+u,color='plum',alpha=0.2)
		plt.axvline(X,color='k',ls=':')

	# draw in the DES/external line
	if label==r'$10.$ Planck 18 TT+TE+EE+lowE':
		plt.axhline(y+(dy*2/3), color='darkmagenta', ls='--')

	# do the ones above the line in black
	if colour=='#8b008b' and i<9:
		textcolour='#000000'
	else:
		textcolour=colour
	
	plt.annotate(label,xy=(0.415,y-(dy/8)), fontsize=fontsize, color=textcolour)
	print(label)

	y-=dy

plt.subplots_adjust(wspace=0, hspace=0, bottom=0.14, left=0.13, right=0.97, top=0.98)
plt.savefig('s8_robustness_summary_v2.pdf')
plt.savefig('s8_robustness_summary_v2.png')

plt.close()
exit()






