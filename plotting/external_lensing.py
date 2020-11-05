import numpy as np
import os
import pylab as plt
plt.switch_backend('pdf')
plt.style.use('y1a1')

import tools.emcee as mc
from chainconsumer import ChainConsumer

print('Loading chains...')

base = '/Users/hattifattener/Documents/y3cosmicshear/chains/'

c0 = mc.chain(base+'ias_fid/fidm/mtatt_dnla/chain_1x2pt_hyperrank_2pt_SOMPZWZsamples_pit_goodlowz_shifted_1000samples_ramped.055_PITfix_sim_noiseless_GCharSmail_SIMULATED_NLA.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c1 = np.genfromtxt(base+'/external/lensing/HSC_Y1_LCDM_post_fid.txt',names=True)
c2 = mc.chain('/Volumes/groke/work/chains/y1/fiducial/all/out_all-1x2pt-NG.txt')
c3 = np.genfromtxt('/Volumes/groke/work/other_peoples_datasets/kids450/KV450_fiducial.txt',names=True)

#c1 = mc.chain('chain_1x2pt_fiducial_test_0.40_CLASS_NLA_C1_GAMA_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c0.add_s8()
c2.add_s8()
s8_1 = c1['COSMOLOGICAL_PARAMETERSSIGMA_8'] * np.sqrt(c1['cosmological_parametersomega_m']/0.3) 



samp0 = np.array([c0.samples['cosmological_parameters--omega_m'], c0.samples['cosmological_parameters--s8'], c0.samples['intrinsic_alignment_parameters--a1'], c0.samples['intrinsic_alignment_parameters--alpha1']])
samp1 = np.array([c1['cosmological_parametersomega_m'], s8_1, c1['intrinsic_alignment_parametersa1'], c1['intrinsic_alignment_parametersalpha1']])
samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8'], c2.samples['intrinsic_alignment_parameters--a'], c2.samples['intrinsic_alignment_parameters--alpha']])
samp3 = np.array([c3['Omega_m'], c3['S8'], c3['A_IA']])

#import pdb ; pdb.set_trace()
print('Making cornerplot...')
cc = ChainConsumer()

#import pdb ; pdb.set_trace()


names = [r'$\Omega_{\rm m}$','$S_8$','$A_1$', r'$\eta_1$']
names2 = [r'$\Omega_{\rm m}$','$S_8$','$A_1$', r'$\eta_1$', '$A_2$', r'$\eta_2$', r'$b_{\rm TA}$']

cc.add_chain(samp0.T, parameters=names, weights=c0.weight, kde=True, name=r'DES Y3')
cc.add_chain(samp1.T, parameters=names, weights=c1['weight'], kde=True, name=r'HSC Y1')
cc.add_chain(samp2.T, parameters=names, weights=c2.weight, kde=True, name=r'DES Y1')
cc.add_chain(samp3.T, parameters=names[:-1], weights=c3['weights'], kde=True, name=r'KiDS-450')



cc.configure(colors=['#8b008b', '#121F90','#FF94CB', '#FF1493','#000000', ],shade=[True,True,True]*3, shade_alpha=[0.4, 0.25, 0.25,0.1], legend_kwargs={"loc": "upper right", "fontsize": 16},label_font_size=12,tick_font_size=14)
#cc.configure(colors=['#800080', '#800080', '#FF1493', '#000000' ],shade=[False,True,True,False], shade_alpha=[0.25,0.25,0.25], max_ticks=4, kde=[6]*5, linestyles=["-", "-", '-.', '--'], legend_kwargs={"loc": "upper right", "fontsize": 14},label_font_size=14,tick_font_size=14) 
plt.close() ; 
fig = cc.plotter.plot(extents={'$S_8$':(0.65,0.95),r'$\Omega_{\rm m}$':(0.08,0.55),'$A_1$':(-5.,5), '$A_2$':(-5.,5), r'$\eta_1$':(-5,5), r'$\eta_2$':(-5,2), r'$b_{\rm TA}$':(0,2)}) #, truth=[0.3,0.82355,0.7,-1.7] )


#plt.suptitle(r'$\Lambda$CDM $1 \times 2\mathrm{pt}$, data=TATT', fontsize=16)
plt.subplots_adjust(bottom=0.155,left=0.155, hspace=0, wspace=0)

print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/1x2pt_external.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/1x2pt_external.png')




