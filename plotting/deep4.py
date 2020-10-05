import numpy as np
import os
import pylab as plt
plt.switch_backend('pdf')
plt.style.use('y1a1')

import tools.emcee as mc
from chainconsumer import ChainConsumer

print('Loading chains...')

base = '/Users/hattifattener/Documents/y3cosmicshear/chains/DEEP2/'
c1 = mc.chain(base+'chain_1x2pt_fiducial_test_0.40_CLASS_C1_DEEP2_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm_btatest.txt')
c2 = mc.chain(base+'chain_1x2pt_fiducial_test_0.40_CLASS_C1_DEEP2_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4_nobin44.ini_lcdm.txt')
c3 = mc.chain(base+'chain_1x2pt_fiducial_v0.40_fiducial.fits_scales_1x2pt_v0.40fid_0.5.ini_lcdm.txt')


#c1 = mc.chain('chain_1x2pt_fiducial_test_0.40_CLASS_NLA_C1_GAMA_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')

c1.add_s8()
c2.add_s8()
c3.add_s8()


#'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'

samp1 = np.array([c1.samples['cosmological_parameters--omega_m'], c1.samples['cosmological_parameters--s8'], c1.samples['intrinsic_alignment_parameters--a1'], c1.samples['intrinsic_alignment_parameters--a2'], c1.samples['intrinsic_alignment_parameters--alpha1'], c1.samples['intrinsic_alignment_parameters--alpha2'], c1.samples['intrinsic_alignment_parameters--bias_ta']])
samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8'], c2.samples['intrinsic_alignment_parameters--a1'], c2.samples['intrinsic_alignment_parameters--a2'], c2.samples['intrinsic_alignment_parameters--alpha1'], c2.samples['intrinsic_alignment_parameters--alpha2'], c2.samples['intrinsic_alignment_parameters--bias_ta']])
samp3 = np.array([c3.samples['cosmological_parameters--omega_m'], c3.samples['cosmological_parameters--s8'], c3.samples['intrinsic_alignment_parameters--a1'], c3.samples['intrinsic_alignment_parameters--a2'], c3.samples['intrinsic_alignment_parameters--alpha1'], c3.samples['intrinsic_alignment_parameters--alpha2'], c3.samples['intrinsic_alignment_parameters--bias_ta']])


#import pdb ; pdb.set_trace()
print('Making cornerplot...')
cc = ChainConsumer()

#import pdb ; pdb.set_trace()


names = [r'$\Omega_{\rm m}$','$S_8$','$A_1$', '$A_2$', r'$\eta_1$', r'$\eta_2$', r'$b_{\rm TA}$']


cc.add_chain(samp3.T, parameters=names, weights=c3.weight, kde=True, name=r'Fiducal')
cc.add_chain(samp1.T, parameters=names, weights=c1.weight, kde=True, name=r'DEEP2')
cc.add_chain(samp2.T, parameters=names, weights=c2.weight, kde=True, name=r'DEEP2, no $\xi^{44}_\pm$')



cc.configure(colors=['#000000','#8b008b','#FF94CB', '#FF1493', ],shade=[False,True,True]*3, shade_alpha=[0.25, 0.25, 0.1,0.5], legend_kwargs={"loc": "upper right", "fontsize": 20},label_font_size=12,tick_font_size=14)
#cc.configure(colors=['#800080', '#800080', '#FF1493', '#000000' ],shade=[False,True,True,False], shade_alpha=[0.25,0.25,0.25], max_ticks=4, kde=[6]*5, linestyles=["-", "-", '-.', '--'], legend_kwargs={"loc": "upper right", "fontsize": 14},label_font_size=14,tick_font_size=14) 
plt.close() ; 
fig = cc.plotter.plot(extents={'$S_8$':(0.75,0.95),r'$\Omega_{\rm m}$':(0.15,0.45),'$A_1$':(-0.9,2), '$A_2$':(-3.,1), r'$\eta_1$':(-5,5), r'$\eta_2$':(-5,2), r'$b_{\rm TA}$':(0,2)}, truth=[0.3,0.82355,0.2,-1.36,-1.3,-2.5,1] )


plt.suptitle(r'$\Lambda$CDM $1 \times 2\mathrm{pt}$', fontsize=20)
plt.subplots_adjust(bottom=0.155,left=0.155, hspace=0, wspace=0)

print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/robustness/fiducial_test_0.40_CLASS_C1_DEEP2_v2_nobin44.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/robustness/fiducial_test_0.40_CLASS_C1_DEEP2_v2_nobin44.png')


