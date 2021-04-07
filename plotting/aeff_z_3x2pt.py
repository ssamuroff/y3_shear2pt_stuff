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

fontsize=18
x = np.array([0.38,0.52,0.74,0.96])
A1_mid = np.array([7.975471e-02,1.102145e-01,1.641993e-01,2.303808e-01])
A1_lower = np.array([-0.0690587,-0.0787695,-0.0986,-0.139074])
A1_upper = np.array([0.210907,0.300952,0.432006,0.592155])

A2_mid = np.array([2.465375e-02,3.434589e-02,6.220786e-02,1.032715e-01])
A2_lower = np.array([-0.348632,-0.498742,-0.751087,-0.993141])
A2_upper = np.array([0.347368,0.408864,0.518273,0.685324])





A1_mid_1x2pt = np.array([-1.984938e-01, -3.621645e-01, -6.468443e-01, -9.992728e-01])
A1_lower_1x2pt = np.array([-0.486423,-0.838705,-1.21343,-1.70101])
A1_upper_1x2pt = np.array([-0.0619944,0.185991,-0.319283,0.222796])

A2_mid_1x2pt = np.array([ 6.224822e-01, 8.698588e-01, 1.255058e+00, 1.682571e+00])
A2_lower_1x2pt = np.array([0.421932,0.46693,0.413339,0.248971])
A2_upper_1x2pt = np.array([1.48475,2.19802,3.29567,4.51947])

        
colours = ['#7223AD','#A4CD64','#DD9EE8','#3775A1']

plt.subplot(111,aspect=0.11594202898550725)
plt.errorbar(x,A1_mid_1x2pt, yerr=[A1_mid_1x2pt-A1_lower_1x2pt,A1_upper_1x2pt-A1_mid_1x2pt] ,label=r'$\xi_\pm$ ($A_1$)', linestyle='none', marker='o', markeredgecolor=colours[0], markerfacecolor='w', ecolor=colours[0], markersize=3.5)
plt.errorbar(x+0.01,A2_mid_1x2pt, yerr=[A2_mid_1x2pt-A2_lower_1x2pt,A2_upper_1x2pt-A2_mid_1x2pt] ,label=r'$\xi_\pm$ ($A_2$)', linestyle='none', marker='v', markeredgecolor=colours[0], markerfacecolor='w', ecolor=colours[0])
plt.errorbar(x-0.02,A1_mid, yerr=[A1_mid-A1_lower,A1_upper-A1_mid] ,label=r'$\xi_\pm + \gamma_t + w$ ($A_1$)', linestyle='none', marker='o', markeredgecolor=colours[2], markerfacecolor=colours[2], ecolor=colours[2], markersize=3.5)
plt.errorbar(x+0.02,A2_mid, yerr=[A2_mid-A2_lower,A2_upper-A2_mid] ,label=r'$\xi_\pm + \gamma_t + w$ ($A_2$)', linestyle='none', marker='v', markeredgecolor=colours[2], markerfacecolor=colours[2], ecolor=colours[2])

plt.ylim(-1.9,5.)
plt.xlim(0.3,1.1)
plt.axhline(0,color='k',ls=':')
plt.xticks([0.4,0.6,0.8,1.],fontsize=fontsize)
plt.yticks([-1,0,1,2,3,4,5],fontsize=fontsize)
plt.xlabel('Redshift $z$',fontsize=fontsize)
plt.ylabel('Effective $a_i$',fontsize=fontsize)
plt.legend(loc='upper left',fontsize=13)
plt.subplots_adjust(bottom=0.155,left=0.155, top=0.98,right=0.98,hspace=0, wspace=0)
print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/iaeff_z_maglim_3x2pt.png')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/iaeff_z_maglim_3x2pt.pdf')
