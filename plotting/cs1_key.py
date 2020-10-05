import numpy as np
import os
import pylab as plt
plt.switch_backend('pdf')
plt.style.use('y1a1')
from matplotlib import rcParams

import tools.emcee as mc
from chainconsumer import ChainConsumer

rcParams['xtick.major.size'] = 3.5
rcParams['xtick.minor.size'] = 1.7
rcParams['ytick.major.size'] = 3.5
rcParams['ytick.minor.size'] = 1.7
rcParams['xtick.direction']='in'
rcParams['ytick.direction']='in'

print('Loading chains...')

base = '/Users/hattifattener/Documents/y3cosmicshear/chains/cs2/'
c1 = mc.chain(base+'../DEEP2/chain_1x2pt_fiducial_test_0.40_CLASS_C1_DEEP2_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4_nobin11.ini_lcdm.txt')
c2 = mc.chain(base+'external/out_planck15_TTTEEE-mnu-multinest.txt')



#c1 = mc.chain('chain_1x2pt_fiducial_test_0.40_CLASS_NLA_C1_GAMA_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')

c1.add_s8()
c2.add_s8()


#'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'

samp1 = np.array([c1.samples['cosmological_parameters--omega_m'], c1.samples['cosmological_parameters--s8'], c1.samples['cosmological_parameters--sigma_8']])
samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8'], c2.samples['cosmological_parameters--sigma_8']])



#import pdb ; pdb.set_trace()
print('Making cornerplot...')
cc = ChainConsumer()

#import pdb ; pdb.set_trace()


names = [r'$\Omega_{\rm m}$','$S_8$', r'$\sigma_8$']


cc.add_chain(samp1.T, parameters=names, weights=c1.weight, kde=True, name=r'DES Y3 (Fiducial)')
cc.add_chain(samp2.T, parameters=names, weights=c2.weight, kde=True, name=r'Planck 2015')



cc.configure(colors=[ '#FA86C9','#7223AD','#DDA0DD'],shade=[True,True,True]*3, shade_alpha=[0.65, 0.55, 0.1,0.5], kde=[2]*3,legend_kwargs={"loc": "upper right", "fontsize": 12},label_font_size=12,tick_font_size=12)
#cc.configure(colors=['#800080', '#800080', '#FF1493', '#000000' ],shade=[False,True,True,False], shade_alpha=[0.25,0.25,0.25], max_ticks=4, kde=[6]*5, linestyles=["-", "-", '-.', '--'], legend_kwargs={"loc": "upper right", "fontsize": 14},label_font_size=14,tick_font_size=14) 
plt.close() ; 
fig = cc.plotter.plot(extents={'$S_8$':(0.75,0.92),r'$\sigma_8$':(0.6,1.05),r'$\Omega_{\rm m}$':(0.16,0.45),'$A_1$':(0.,1.2), '$A_2$':(-4.,1), r'$\eta_1$':(-4,0), r'$\eta_2$':(-5,2), r'$b_{\rm TA}$':(0,2)}) #, truth=[0.3,0.82355,0.7,-1.7] )


#plt.suptitle(r'$\Lambda$CDM $3 \times 2\mathrm{pt}$', fontsize=16)
plt.subplots_adjust(bottom=0.15,left=0.15, top=0.98,right=0.98,hspace=0, wspace=0)

print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/y3cs_keyplot.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/y3cs_keyplot.png')


