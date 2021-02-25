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

base = '/Users/hattifattener/Documents/y3cosmicshear/'
c1 = mc.chain(base+'/chains/ias_fid/final/mnla_dtatt/chain_1x2pt_nla_sim_2pt_NG_BLINDED_v0.40cov_xcorrGGL27072020_1000samples_055ramp_all_2609_meanzisreal10.fits_sim_noiseless.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c2 = mc.chain(base+'/chains/ias_fid/final/mtatt_dtatt/chain_1x2pt_fiducial_sim_2pt_NG_BLINDED_v0.40cov_xcorrGGL27072020_1000samples_055ramp_all_2609_meanzisreal10.fits_sim_noiseless.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c3 = mc.chain(base+'/chains/ias_fid/final/mnla_dnla/chain_1x2pt_nla_sim_2pt_NG_BLINDED_v0.40cov_xcorrGGL27072020_1000samples_055ramp_all_2609_meanzisreal10.fits_sim_noiseless_nla.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c4 = mc.chain(base+'chains/ias_fid/final/mtatt_dnla/chain_1x2pt_fiducial_sim_2pt_NG_BLINDED_v0.40cov_xcorrGGL27072020_1000samples_055ramp_all_2609_meanzisreal10.fits_sim_noiseless_nla.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')


#c1 = mc.chain('chain_1x2pt_fiducial_test_0.40_CLASS_NLA_C1_GAMA_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')

c1.add_s8()
c2.add_s8()
c3.add_s8()
c4.add_s8()


#'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'

samp1 = np.array([c1.samples['cosmological_parameters--omega_m'], c1.samples['cosmological_parameters--s8'], c1.samples['intrinsic_alignment_parameters--a1'], c1.samples['intrinsic_alignment_parameters--alpha1']])
samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8'], c2.samples['intrinsic_alignment_parameters--a1'], c2.samples['intrinsic_alignment_parameters--alpha1'], c2.samples['intrinsic_alignment_parameters--a2'], c2.samples['intrinsic_alignment_parameters--alpha2'], c2.samples['intrinsic_alignment_parameters--bias_ta']])
samp3 = np.array([c3.samples['cosmological_parameters--omega_m'], c3.samples['cosmological_parameters--s8'], c3.samples['intrinsic_alignment_parameters--a1'], c3.samples['intrinsic_alignment_parameters--alpha1']])


#import pdb ; pdb.set_trace()
print('Making cornerplot...')
cc = ChainConsumer()

#import pdb ; pdb.set_trace()


names = [r'$\Omega_{\rm m}$','$S_8$','$A_1$', r'$\eta_1$']
names2 = [r'$\Omega_{\rm m}$','$S_8$','$A_1$', r'$\eta_1$', '$A_2$', r'$\eta_2$', r'$b_{\rm TA}$']


cc.add_chain(samp1.T, parameters=names, weights=c1.weight, kde=True, name=r'model=NLA, data=TATT')
cc.add_chain(samp2.T, parameters=names2, weights=c2.weight, kde=True, name=r'model=TATT, data=TATT')
cc.add_chain(samp3.T, parameters=names, weights=c3.weight, kde=True, name=r'model=NLA, data=NLA')



cc.configure(colors=['#121F90','#8b008b','#FF94CB', '#FF1493', ],shade=[False,True,True]*3, shade_alpha=[0.25, 0.25, 0.1,0.5], legend_kwargs={"loc": "upper right", "fontsize": 16},label_font_size=12,tick_font_size=14)
#cc.configure(colors=['#800080', '#800080', '#FF1493', '#000000' ],shade=[False,True,True,False], shade_alpha=[0.25,0.25,0.25], max_ticks=4, kde=[6]*5, linestyles=["-", "-", '-.', '--'], legend_kwargs={"loc": "upper right", "fontsize": 14},label_font_size=14,tick_font_size=14) 
plt.close() ; 
fig = cc.plotter.plot(extents={'$S_8$':(0.5,0.95),r'$\Omega_{\rm m}$':(0.15,0.45),'$A_1$':(-5.,5), '$A_2$':(-5.,5), r'$\eta_1$':(-5,5), r'$\eta_2$':(-5,2), r'$b_{\rm TA}$':(0,2)}) #, truth=[0.3,0.82355,0.7,-1.7] )


#plt.suptitle(r'$\Lambda$CDM $1 \times 2\mathrm{pt}$, data=TATT', fontsize=16)
plt.subplots_adjust(bottom=0.155,left=0.155, hspace=0, wspace=0)

print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/sim_ia_1x2pt.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/sim_ia_1x2pt.png')









samp1 = np.array([c1.samples['cosmological_parameters--omega_m'], c1.samples['cosmological_parameters--s8']])
samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8']])
samp3 = np.array([c3.samples['cosmological_parameters--omega_m'], c3.samples['cosmological_parameters--s8']])
samp4 = np.array([c4.samples['cosmological_parameters--omega_m'], c4.samples['cosmological_parameters--s8']])


#import pdb ; pdb.set_trace()
print('Making cornerplot...')
cc = ChainConsumer()

#import pdb ; pdb.set_trace()


names = [r'$\Omega_{\rm m}$','$S_8$']
names2 = [r'$\Omega_{\rm m}$','$S_8$']


cc.add_chain(samp1.T, parameters=names, weights=c1.weight, kde=True, name=r'model=NLA, data=TATT')
cc.add_chain(samp2.T, parameters=names2, weights=c2.weight, kde=True, name=r'model=TATT, data=TATT')
cc.add_chain(samp3.T, parameters=names, weights=c3.weight, kde=True, name=r'model=NLA, data=NLA')
cc.add_chain(samp4.T, parameters=names, weights=c4.weight, kde=True, name=r'model=TATT, data=NLA')


cc.configure(colors=['#121F90','#8b008b','#FF94CB', '#4682b4','#FF1493', ],shade=[True,True,False,False]*3, shade_alpha=[0.25, 0.25, 0.1,0.5], legend_kwargs={"loc": "lower right", "fontsize": 8},label_font_size=10,tick_font_size=8)
#cc.configure(colors=['#800080', '#800080', '#FF1493', '#000000' ],shade=[False,True,True,False], shade_alpha=[0.25,0.25,0.25], max_ticks=4, kde=[6]*5, linestyles=["-", "-", '-.', '--'], legend_kwargs={"loc": "upper right", "fontsize": 14},label_font_size=14,tick_font_size=14) 
plt.close() ; 
fig = cc.plotter.plot(extents={'$S_8$':(0.66,0.9),r'$\Omega_{\rm m}$':(0.15,0.5),'$A_1$':(-5.,5), '$A_2$':(-5.,5), r'$\eta_1$':(-5,5), r'$\eta_2$':(-5,2), r'$b_{\rm TA}$':(0,2)}) #, truth=[0.3,0.82355,0.7,-1.7] )


#plt.suptitle(r'$\Lambda$CDM $1 \times 2\mathrm{pt}$, data=TATT', fontsize=16)
plt.subplots_adjust(bottom=0.2,left=0.22, top=0.98,right=0.98, hspace=0, wspace=0)

print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/sim_ia_1x2pt_1panel.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/sim_ia_1x2pt_1panel.png')


plt.close()
from getdist import plots, MCSamples
import getdist

samples1 = MCSamples(samples=samp1.T,names=['x1','x2'], labels=names, weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples2 = MCSamples(samples=samp2.T,names=['x1','x2'], labels=names, weights=c2.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples3 = MCSamples(samples=samp3.T,names=['x1','x2'], labels=names, weights=c3.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples4 = MCSamples(samples=samp4.T,names=['x1','x2'], labels=names, weights=c4.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})


gd = plots.get_single_plotter(width_inch=6, ratio=1)
gd.settings.legend_fontsize = 12
#import pdb ; pdb.set_trace()
gd.plot_2d([samples1, samples2,samples3,samples4],['x1','x2'], filled=[True,True,False,False], colors=['#121F90','#8b008b','#FF94CB', '#4682b4','#FF1493', ], lims=[0.15,0.5,0.66,0.9])
gd.add_legend(['model=NLA, data=TATT ', 'model=TATT, data=TATT','model=NLA, data=NLA','model=TATT, data=NLA'], legend_loc='lower right');
plt.subplots_adjust(bottom=0.2,left=0.22, top=0.98,right=0.98, hspace=0, wspace=0)

print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/sim_ia_1x2pt_1panel_getdist.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/sim_ia_1x2pt_1panel_getdist.png')





