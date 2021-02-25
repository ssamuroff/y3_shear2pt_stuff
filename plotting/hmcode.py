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

base = '/Volumes/groke/work/chains/y3/real/'
c1 = mc.chain(base+'ia_testing/chain_hmcode_1x2pt_lcdm.txt')
c0 = mc.chain(base+'chain_1x2pt_lcdm.txt')



#c1 = mc.chain('chain_1x2pt_fiducial_test_0.40_CLASS_NLA_C1_GAMA_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')

c0.add_s8()
c1.add_s8()


#'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'

samp0 = np.array([c0.samples['cosmological_parameters--omega_m'], c0.samples['cosmological_parameters--s8']])
samp1 = np.array([c1.samples['cosmological_parameters--omega_m'], c1.samples['cosmological_parameters--s8'], c1.samples['halo_model_parameters--a'], c1.samples['halo_model_parameters--eta_0']])
        

#import pdb ; pdb.set_trace()
print('Making cornerplot...')
cc = ChainConsumer()

#import pdb ; pdb.set_trace()


names = [r'$\Omega_{\rm m}$','$S_8$']
names2 = [r'$\Omega_{\rm m}$','$S_8$','$A$',r'$\eta_0$']


cc.add_chain(samp0.T, parameters=names, weights=c0.weight, kde=True, name=r'Fiducial')
cc.add_chain(samp1.T, parameters=names2, weights=c1.weight, kde=True, name=r'hmcode')


cc.configure(colors=['#121F90','#8b008b','#FF94CB', '#FF1493', ],shade=[False,True,True]*3, shade_alpha=[0.25, 0.25, 0.1,0.5], legend_kwargs={"loc": "upper right", "fontsize": 16},label_font_size=12,tick_font_size=14)
#cc.configure(colors=['#800080', '#800080', '#FF1493', '#000000' ],shade=[False,True,True,False], shade_alpha=[0.25,0.25,0.25], max_ticks=4, kde=[6]*5, linestyles=["-", "-", '-.', '--'], legend_kwargs={"loc": "upper right", "fontsize": 14},label_font_size=14,tick_font_size=14) 
plt.close() ; 
fig = cc.plotter.plot(extents={'$S_8$':(0.5,0.95),r'$\Omega_{\rm m}$':(0.15,0.45),'$A_1$':(-5.,5), '$A_2$':(-5.,5), r'$\eta_1$':(-5,5), r'$\eta_2$':(-5,2), r'$b_{\rm TA}$':(0,2)}) #, truth=[0.3,0.82355,0.7,-1.7] )


plt.suptitle(r'$w$CDM $1 \times 2\mathrm{pt}$', fontsize=16)
plt.subplots_adjust(bottom=0.155,left=0.155, hspace=0, wspace=0, top=0.92)

print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/hmcode_1x2pt.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/hmcode_1x2pt.png')

