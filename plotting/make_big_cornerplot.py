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
#c1 = mc.chain(base+'fiducial/chain_1x2pt_hyperrank_2pt_NG_BLINDED_v0.40cov_xcorrGGL_27072020_SOMPZWZsamples_pit.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c1 = mc.chain(base+'maglim/unblinding/chain_1x2pt_lcdm_SR_maglim.txt')

c2 = mc.chain('chains/chain_prior.txt')
#c2 = mc.chain(base+'external/chain_p-TTTEEE-lowE_lcdm.txt')



#c1 = mc.chain('chain_1x2pt_fiducial_test_0.40_CLASS_NLA_C1_GAMA_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')

c1.add_s8()
c2.add_s8()



#'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'

#import pdb ; pdb.set_trace()
exclude = ['like', 'cosmological_parameters--sigma_12', 'data_vector--2pt_chi2']
names=[n for n in c1.samples.dtype.names if ('--' in n) and (n not in exclude)]
names2=[n for n in c2.samples.dtype.names if ('--' in n) and (n not in exclude)]
samp1 = np.array([c1.samples[n] for n in names ])
samp2 = np.array([c2.samples[n] for n in names2 ])
#samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8'], c2.samples['cosmological_parameters--sigma_8']])
#import pdb ; pdb.set_trace()
#samp2[np.isnan(samp2)] = 0.
samp2 = np.array([s for s in samp2.T if (sum(np.isnan(s))==0)]).T


names_dict = {'cosmological_parameters--omega_m': r'$\Omega_{\rm m}$', 
    'cosmological_parameters--h0' : '$h$', 
    'cosmological_parameters--omega_b': r'$\Omega_{\rm b}$', 
    'cosmological_parameters--n_s' : r'$n_{\rm s}$', 
    'cosmological_parameters--a_s' : r'$A_{\rm s}$', 
    'cosmological_parameters--omnuh2' : r'$\Omega_{\nu} h^2$', 
    'shear_calibration_parameters--m1' : r'$m_1$', 
    'shear_calibration_parameters--m2': r'$m_2$', 
    'shear_calibration_parameters--m3': r'$m_3$', 
    'shear_calibration_parameters--m4': r'$m_4$', 
    'wl_photoz_errors--bias_1' : r'$\Delta z^1$', 
    'wl_photoz_errors--bias_2' : r'$\Delta z^2$', 
    'wl_photoz_errors--bias_3' : r'$\Delta z^3$', 
    'wl_photoz_errors--bias_4' : r'$\Delta z^4$', 
    'lens_photoz_errors--bias_1' : r'$\Delta z^1_{l}$',
    'lens_photoz_errors--bias_2' : r'$\Delta z^2_{l}$', 
    'lens_photoz_errors--bias_3' : r'$\Delta z^3_{l}$', 
    'lens_photoz_errors--width_1' : r'$\delta^1_{l}$',
    'lens_photoz_errors--width_2' : r'$\delta^2_{l}$', 
    'lens_photoz_errors--width_3' : r'$\delta^3_{l}$', 
    'bias_lens--b1' : r'$b_1$', 
    'bias_lens--b2' : r'$b_2$', 
    'bias_lens--b3' : r'$b_3$', 
    'intrinsic_alignment_parameters--a1' : r'$A_1$', 
    'intrinsic_alignment_parameters--a2' : r'$A_2$', 
    'intrinsic_alignment_parameters--alpha1' : r'$\eta_1$', 
    'intrinsic_alignment_parameters--alpha2' : r'$\eta_2$', 
    'intrinsic_alignment_parameters--bias_ta' : r'$b_{\rm TA}$', 
    'cosmological_parameters--sigma_8':r'$\sigma_8$', 
    'cosmological_parameters--s8' : r'$S_8$'}


names_list = [names_dict[n] for n in names ]
names_list2 = [names_dict[n] for n in names2 ]

nparam = len(samp1)
print('%d parameters'%nparam)
plt.close()
from getdist import plots, MCSamples
import getdist
import matplotlib.pyplot as plt


g = plots.get_subplot_plotter() #(width_inch=6, ratio=1)
g.settings.legend_fontsize = 40
g.settings.fontsize = 18
g.settings.axes_fontsize = 18
g.settings.axes_labelsize = 22
g.settings.axis_tick_max_labels = 15
g.settings.linewidth = 1.5
g.settings.legend_colored_text=True
g.settings.axis_tick_step_groups = [[2.5, 3, 4, 6, 8],[1, 2, 5, 10]]


samples = MCSamples(samples=samp1.T,names=['x%d'%(i+1) for i in range(nparam)], labels=names_list, label='Posterior', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})

samples2 = MCSamples(samples=samp2.T,names=['x%d'%(i+1) for i in range(len(samp2))], labels=names_list2, label='Prior', weights=np.ones_like(samp2[0]),  settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})

#import pdb ; pdb.set_trace()
g.triangle_plot([samples],['x%d'%(i+1) for i in range(nparam)], upper_kwargs={'show_1d':False},  filled=[True,False], contour_colors=['#FA86C9','#7223AD' ], labels=['Posterior', 'Prior']) #, param_limits={'x1':(0.18,0.45), 'x2':(0.69,0.9), 'x3':(0.6,1.05)}) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])
#import pdb ; pdb.set_trace()

#s8_ticks = [0.7,0.75,0.8,0.85]
#omm_ticks = [0.2,0.3,0.4]
#sig8_ticks = [0.7,0.8,0.9,1.]
#
## ticks...
#g.subplots[0][0].set_xticks(omm_ticks)
#g.subplots[1][0].set_xticks(omm_ticks)
#g.subplots[1][0].set_yticks(s8_ticks)
#g.subplots[1][1].set_xticks(s8_ticks)
#g.subplots[2][0].set_yticks(sig8_ticks)
#g.subplots[2][0].set_xticks(omm_ticks)
#g.subplots[2][1].set_yticks(sig8_ticks)
#g.subplots[2][1].set_xticks(s8_ticks)
#g.subplots[2][2].set_xticks(sig8_ticks)

#g.add_legend(['DES Y3','HSC Y1'])
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/giant_cornerplot_nprior_maglim.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/giant_cornerplot_nprior_maglim.png')