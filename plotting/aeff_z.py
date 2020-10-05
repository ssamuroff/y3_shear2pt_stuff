import numpy as np
import tools.emcee as mc
from chainconsumer import ChainConsumer
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

fontsize=16
x = np.array([0.38,0.52,0.74,0.96])
A1_mid = np.array([5.488826e-01,6.917138e-01,9.836143e-01,1.374445])
A1_lower = np.array([0.471694, 0.584965, 0.757438, 0.940599])
A1_upper = np.array([0.620481,0.804017,1.1926,1.69758])

A2_mid = np.array([-1.951333,-2.301541,-2.909604,-3.588715])
A2_lower = np.array([-2.09421,-2.50611,-3.23011,-4.05454])
A2_upper = np.array([-1.78769,-2.07409,-2.56197,-3.06636])


Anla_mid = np.array([8.930814e-01,7.542483e-01,5.994304e-01,4.927354e-01])
Anla_lower = np.array([0.854662,0.716393,0.548117,0.43002])
Anla_upper = np.array([0.928075,0.792705,0.644769,0.541609])




plt.subplot(111,aspect=0.07)
plt.errorbar(x,A1_mid, yerr=[A1_lower,A1_upper] ,label='Fiducial Y3 ($A_1$)', linestyle='none', marker='*', markeredgecolor='darkmagenta', markerfacecolor='darkmagenta', ecolor='darkmagenta')
plt.errorbar(x+0.01,A2_mid, yerr=[A2_lower,A2_upper] ,label='Fiducial Y3 ($A_2$)', linestyle='none', marker='v', markeredgecolor='midnightblue', markerfacecolor='midnightblue', ecolor='midnightblue')
plt.errorbar(x-0.01,Anla_mid, yerr=[Anla_lower,Anla_upper] ,label='NLA', linestyle='none', marker='x', markeredgecolor='hotpink', markerfacecolor='hotpink', ecolor='hotpink')


plt.ylim(-6,4.5)
plt.xlim(0.3,1.1)
plt.axhline(0,color='k',ls=':')
plt.xticks([0.4,0.6,0.8,1.],fontsize=fontsize)
plt.yticks([-6,-4,-2,0,2,4],fontsize=fontsize)
plt.xlabel('$z$',fontsize=fontsize)
plt.ylabel('Effective $A_i$',fontsize=fontsize)
plt.legend(loc='upper left',fontsize=fontsize)
plt.subplots_adjust(bottom=0.155,left=0.155, top=0.98,right=0.98,hspace=0, wspace=0)
print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/iaeff_z.png')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/iaeff_z.pdf')
