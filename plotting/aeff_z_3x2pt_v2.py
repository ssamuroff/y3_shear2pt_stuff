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

fontsize=14
x = np.array([0.38,0.52,0.74,0.96])
A1_mid = np.array([1.223792e-01,9.282708e-02,7.006017e-02,5.471900e-02])
A1_lower = np.array([-0.161886,-0.135667,-0.134867,-0.186587])
A1_upper = np.array([0.44319,0.666418,1.03425,1.46844])

A2_mid = np.array([-2.955918e-02,-5.090510e-02,-7.807510e-02,-1.060926e-01])
A2_lower = np.array([-0.448084,-0.589549,-0.742754,-0.956489])
A2_upper = np.array([0.142344,0.209118,0.341095,0.527137])




A1_mid_rm = np.array([2.210842e-01,3.349795e-01,5.263790e-01,7.555621e-01])
A1_lower_rm = np.array([0.138966,-0.167535,0.421392,0.558036])
A1_upper_rm = np.array([0.44319,0.666418,1.03425,1.46844])

A2_mid_rm = np.array([-5.543460e-02,-1.033747e-02,8.564863e-02,2.208198e-01])
A2_lower_rm = np.array([-0.677319,-0.926016,-1.35369,-1.86078])
A2_upper_rm = np.array([0.142344,0.209118,0.341095,0.527137])


x_lens_rm = np.array([0.27301636434170573,0.43229516007171964,0.58204045796512,0.7261471754257801,0.8482244486492069])
x_lens_ml = np.array([0.3006574937282265,0.45685765541541273,0.6205625326451203,0.768904251235295])
b_rm_mid = np.array([1.742793,1.824858,1.922334,2.152928,2.316451])
b_rm_lower = np.array([1.61497,1.7142,1.79918,2.02545,2.17597])
b_rm_upper = np.array([1.84393,1.92989,2.02784,2.26782,2.44338])

b_ml_mid = np.array([1.487848,1.685931,1.908615,1.792744])
b_ml_lower = np.array([1.3943,1.56807,1.79325,1.67338])
b_ml_upper = np.array([1.58784,1.79275,2.03183,1.90153])

   
colours = ['#7223AD','#A4CD64','#DD9EE8','#3775A1']

#plt.subplot(121,aspect=0.11594202898550725)
plt.subplot(211)
plt.minorticks_on()
plt.xlim(0.2,1.05)
plt.ylim(1.3,2.5)
plt.axhline(1,color='k',ls=':')
plt.ylabel('Galaxy bias $b_g$',fontsize=fontsize)
plt.xticks([0.2,0.4,0.6,0.8,1.],visible=False)


plt.errorbar(x_lens_ml,b_ml_mid, yerr=[b_ml_mid-b_ml_lower,b_ml_upper-b_ml_mid] ,label=r'Maglim ($b_1$)', linestyle='none', marker='o', markeredgecolor=colours[0], markerfacecolor=colours[0], ecolor=colours[0], markersize=3.5)
plt.errorbar(x_lens_rm,b_rm_mid, yerr=[b_rm_mid-b_rm_lower,b_rm_upper-b_rm_mid] ,label=r'redMaGiC ($b_1$)', linestyle='none', marker='o', markerfacecolor=colours[2], markeredgecolor=colours[2], ecolor=colours[2], markersize=3.5)
plt.legend(loc='upper left',fontsize=8)


plt.subplot(212)
plt.minorticks_on()
plt.errorbar(x-0.02,A1_mid, yerr=[A1_mid-A1_lower,A1_upper-A1_mid] ,label=r'Maglim ($a_1$)', linestyle='none', marker='o', markeredgecolor=colours[0], markerfacecolor=colours[0], ecolor=colours[0], markersize=3.5)
plt.errorbar(x+0.02,A2_mid, yerr=[A2_mid-A2_lower,A2_upper-A2_mid] ,label=r'Maglim ($a_2$)', linestyle='none', marker='v', markeredgecolor=colours[0], markerfacecolor=colours[0], ecolor=colours[0])

plt.errorbar(x-0.01,A1_mid_rm, yerr=[A1_mid_rm-A1_lower_rm,A1_upper_rm-A1_mid_rm] ,label=r'redMaGiC ($a_1$)', linestyle='none', marker='o', markerfacecolor='w', markeredgecolor=colours[2], ecolor=colours[2], markersize=3.5)
plt.errorbar(x+0.01,A2_mid_rm, yerr=[A2_mid_rm-A2_lower_rm,A2_upper_rm-A2_mid_rm] ,label=r'redMaGiC ($a_2$)', linestyle='none', marker='v', markerfacecolor='w', markeredgecolor=colours[2], ecolor=colours[2])

plt.ylim(-1.9,1.6)
plt.xlim(0.2,1.05)
plt.axhline(0,color='k',ls=':')
plt.xticks([0.2,0.4,0.6,0.8,1.],fontsize=fontsize)
plt.yticks([-1,0,1],fontsize=fontsize)
plt.xlabel('Redshift $z$',fontsize=fontsize)
plt.ylabel('Effective $a_i$',fontsize=fontsize)
plt.legend(loc='lower left',fontsize=8)





plt.subplots_adjust(bottom=0.155,left=0.155, top=0.98,right=0.75,hspace=0, wspace=0)
print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/iaeff_z_maglim_redmagic_3x2pt.png')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/iaeff_z_maglim_redmagic_3x2pt.pdf')
