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

fontsize=20
x = np.array([0.38,0.52,0.74,0.96])
A1_mid = np.array([-6.076555e-02,-7.048947e-02,-8.907613e-02,-1.118457e-01])
A1_lower = np.array([-0.187001,-0.23118,-0.321237,-0.437003])
A1_upper = np.array([-0.0266776,-0.0281887,-0.029717,-0.0274099])

A2_mid = np.array([6.284241e-01,8.935907e-01,1.483301,2.343928])
A2_lower = np.array([0.533484,0.754714,1.12342,1.62395])
A2_upper = np.array([0.988349,1.42715,2.38936,3.75763])


Anla_mid = np.array([2.330456e-01,3.091803e-01,4.441479e-01,6.086719e-01])
Anla_lower = np.array([0.179162,0.229137,0.268122,0.314099])
Anla_upper = np.array([0.281541,0.382819,0.568512,0.784596])
   

Anlapb_mid = np.array([ 0.144392,0.419248,0.927698,0.644873])
Anlapb_lower = np.array([0.00693158,0.357998,0.456882,-0.204823])
Anlapb_upper = np.array([0.166369,0.543666,1.00964,1.11375])



plt.subplot(111,aspect=0.145)
plt.errorbar(x,[-6.076555e-02,-7.048947e-02,-8.907613e-02,-1.118457e-01], yerr=[2.574949e-01,3.433505e-01,5.422800e-01,8.424319e-01] ,label='TATT ($A_1$)', linestyle='none', marker='*', markeredgecolor='darkmagenta', markerfacecolor='darkmagenta', ecolor='darkmagenta')
plt.errorbar(x+0.01,[6.284241e-01,8.935907e-01,1.483301e+00,2.343928e+00], yerr=[6.539511e-01,9.131919e-01,1.504510e+00,2.393313e+00] ,label='TATT ($A_2$)', linestyle='none', marker='v', markeredgecolor='midnightblue', markerfacecolor='midnightblue', ecolor='midnightblue')
plt.errorbar(x-0.01,[2.330456e-01,3.091803e-01,4.441479e-01,6.086719e-01], yerr=[1.147800e-01,1.586962e-01,2.835736e-01,4.568873e-01] ,label='NLA', linestyle='none', marker='x', markeredgecolor='hotpink', markerfacecolor='hotpink', ecolor='hotpink')
#plt.errorbar(x-0.025,Anlapb_mid, yerr=[Anlapb_lower,Anlapb_upper] ,label='NLA (per bin)', linestyle='none', marker='D',markersize=3.5, markeredgecolor='forestgreen', markerfacecolor='forestgreen', ecolor='forestgreen')
plt.errorbar(x-0.025,[8.919087e-02,4.570875e-01,7.478942e-01,5.344187e-01], yerr=[1.699039e-01,1.969002e-01,5.777228e-01,1.419922e+00] ,label='NLA per bin', linestyle='none', marker='D',markersize=3.5, markeredgecolor='forestgreen', markerfacecolor='forestgreen', ecolor='forestgreen')
   

plt.ylim(-1,4.5)
plt.xlim(0.3,1.1)
plt.axhline(0,color='k',ls=':')
plt.xticks([0.4,0.6,0.8,1.],fontsize=fontsize)
plt.yticks([-1,0,1,2,3,4],fontsize=fontsize)
plt.xlabel('$z$',fontsize=fontsize)
plt.ylabel('Effective $A_i$',fontsize=fontsize)
plt.legend(loc='upper left',fontsize=16)
plt.subplots_adjust(bottom=0.155,left=0.155, top=0.98,right=0.98,hspace=0, wspace=0)
print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/iaeff_z.png')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/iaeff_z.pdf')
