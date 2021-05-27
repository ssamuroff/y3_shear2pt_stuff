import numpy as np
import tools.emcee as mc
from chainconsumer import ChainConsumer
import sys
import pylab as plt
plt.switch_backend('pdf')
plt.style.use('y1a1')

from matplotlib import rcParams
rcParams['xtick.major.size'] = 3.5
rcParams['xtick.minor.size'] = 1.8
rcParams['ytick.major.size'] = 3.5
rcParams['ytick.minor.size'] = 1.8
rcParams['xtick.direction']='in'
rcParams['ytick.direction']='in'

fontsize=18
x = np.array([0.38,0.52,0.74,0.96])
A1_mid = np.array([-1.504193e-01,-2.915737e-01,-5.367945e-01,-8.405973e-01])
A1_lower = np.array([-0.492065,-0.740945,-1.11384,-1.58536])
A1_upper = np.array([-0.0260135,-0.0716774,0.207471,0.295096])

A2_mid = np.array([5.222886e-01,7.005400e-01,9.804462e-01,1.289521e+00])
A2_lower = np.array([-0.602222,0.189556,0.0611762,-0.0517204])
A2_upper = np.array([1.43255,2.09538,3.12841,4.31565])


Anla_mid = np.array([-3.162944e-02, -7.022266e-02, -1.283421e-01, -1.958317e-01])
Anla_lower = np.array([-0.175702,-0.207582,-0.274731,-0.372243])
Anla_upper = np.array([0.0680387,0.0954747,0.130383,0.138064])
   

Anlapb_mid = np.array([-4.59804e-02,2.69611e-02,5.29374e-01,1.76122])
Anlapb_lower = Anlapb_mid - np.array([1.58199e-01,1.71558e-01,3.74310e-01,1.73082e+00])
Anlapb_upper = np.array([1.66593e-01,1.86135e-01,3.65583e-01,1.67571e+00]) + Anlapb_mid


colours = ['#016E51','#12239E','#E13102','#FFA500']

plt.subplot(111,aspect=0.11594202898550725)
plt.minorticks_on()
plt.errorbar(x,A1_mid, yerr=[A1_mid-A1_lower,A1_upper-A1_mid] ,label='TATT ($a_1$)', linestyle='none', marker='*', markeredgecolor=colours[0], markerfacecolor=colours[0], ecolor=colours[0])
plt.errorbar(x+0.01,A2_mid, yerr=[A2_mid-A2_lower,A2_upper-A2_mid] ,label='TATT ($a_2$)', linestyle='none', marker='v', markeredgecolor=colours[1], markerfacecolor=colours[1], ecolor=colours[1])
plt.errorbar(x-0.01,Anla_mid, yerr=[Anla_mid-Anla_lower,Anla_upper-Anla_mid] ,label='NLA', linestyle='none', marker='x', markeredgecolor=colours[2], markerfacecolor=colours[2], ecolor=colours[2])
#plt.errorbar(x-0.025,Anlapb_mid, yerr=[Anlapb_lower,Anlapb_upper] ,label='NLA (per bin)', linestyle='none', marker='D',markersize=3.5, markeredgecolor='forestgreen', markerfacecolor='forestgreen', ecolor='forestgreen')
plt.errorbar(x-0.025,Anlapb_mid, yerr=[Anlapb_mid-Anlapb_lower,Anlapb_upper-Anlapb_mid] ,label='NLA, free $a_1$ per $z-$bin', linestyle='none', marker='D',markersize=3.5, markeredgecolor=colours[3], markerfacecolor=colours[3], ecolor=colours[3])
   

plt.ylim(-1.9,5.)
plt.xlim(0.3,1.1)
plt.axhline(0,color='k',ls=':')
plt.xticks([0.4,0.6,0.8,1.],fontsize=fontsize)
plt.yticks([-1,0,1,2,3,4,5],fontsize=fontsize)
plt.xlabel('Redshift $z$',fontsize=fontsize)
plt.ylabel('Effective $a_i$',fontsize=fontsize)
plt.legend(loc='upper left',fontsize=14)
plt.subplots_adjust(bottom=0.155,left=0.155, top=0.98,right=0.98,hspace=0, wspace=0)
print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/iaeff_z_maglim_final.png')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/iaeff_z_maglim_final.pdf')
