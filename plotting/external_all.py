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
c1 = mc.chain(base+'/final_paper_chains/chain_1x2pt_lcdm_SR_maglim.txt')
c5 = mc.chain(base+'/final_paper_chains/chain_1x2agg_ML.txt')
	#final_paper_chains/chain_1x2_0321.txt')
c2 = mc.chain(base+'external/chain_p-TTTEEE-lowE_lcdm.txt')
c3 = mc.chain(base+'final_paper_chains/tests_1x2pt/maglim/chain_NLA_1x2pt_lcdm_maglim.txt')
c4 = mc.chain(base+'external/chain_s_b_lcdm.txt')

#c1 = mc.chain('chain_1x2pt_fiducial_test_0.40_CLASS_NLA_C1_GAMA_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')

c1.add_s8(alpha=0.5)
c2.add_s8(alpha=0.5)
c3.add_s8(alpha=0.5)
c4.add_s8(alpha=0.5)
c5.add_s8(alpha=0.5)

#'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'

samp1 = np.array([c1.samples['cosmological_parameters--omega_m'], c1.samples['cosmological_parameters--s8']])
samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8']])
samp3 = np.array([c3.samples['cosmological_parameters--omega_m'], c3.samples['cosmological_parameters--s8']])
samp4 = np.array([c4.samples['cosmological_parameters--omega_m'], c4.samples['cosmological_parameters--s8']])
samp5 = np.array([c5.samples['cosmological_parameters--omega_m'], c5.samples['cosmological_parameters--s8']])

names = [r"$\Omega_{\rm m}$", "$S_8$"]
#import pdb ; pdb.set_trace()
print('Making cornerplot...')



plt.close()
from getdist import plots, MCSamples
import getdist
import matplotlib.pyplot as plt


g = plots.get_subplot_plotter() #(width_inch=6, ratio=1)
g.settings.legend_fontsize = 13
g.settings.fontsize = 14
g.settings.axes_fontsize = 14
g.settings.axes_labelsize = 14
g.settings.axis_tick_max_labels = 15
g.settings.linewidth = 1.5
g.settings.legend_colored_text=True
g.settings.axis_tick_step_groups = [[2.5, 3, 4, 6, 8],[1, 2, 5, 10]]

samples4 = MCSamples(samples=samp4.T,names=['x1','x2'], labels=names, label='BAO+SN', weights=c4.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples = MCSamples(samples=samp1.T,names=['x1','x2'], labels=names, label='DES Y3', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples5 = MCSamples(samples=samp5.T,names=['x1','x2'], labels=names, label='DES Y3 optimised', weights=c5.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples3 = MCSamples(samples=samp3.T,names=['x1','x2'], labels=names, label='DES Y3 (NLA)', weights=c3.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples2 = MCSamples(samples=samp2.T,names=['x1','x2'], labels=names, label='Planck 18 TT+TE+EE', weights=c2.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})

g.triangle_plot([samples4,samples, samples5, samples3, samples2],['x1','x2'], filled=[True,True,False,True,True,True], contour_args={'alpha':0.6}, diag1d_kwargs={'normalized':True}, contour_colors=['#3775A1','#7223AD','#FF69B4','#FFC0CB','#A4CD64'], labels=['DES Y3', 'Planck 2018'], param_limits={'x1':(0.18,0.51), 'x2':(0.6,1.0)}) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])
#import pdb ; pdb.set_trace()

s8_ticks = [0.7,0.8,0.9,1.]
omm_ticks = [0.2,0.3,0.4,0.5]
#sig8_ticks = [0.7,0.8,0.9,1.]
#
## ticks...
g.subplots[0][0].set_xticks(omm_ticks)
g.subplots[1][0].set_xticks(omm_ticks)
g.subplots[1][0].set_yticks(s8_ticks)
g.subplots[1][1].set_xticks(s8_ticks)
#g.subplots[2][0].set_yticks(sig8_ticks)
#g.subplots[2][0].set_xticks(omm_ticks)
#g.subplots[2][1].set_yticks(sig8_ticks)
#g.subplots[2][1].set_xticks(s8_ticks)
#g.subplots[2][2].set_xticks(sig8_ticks)

#g.add_legend(['DES Y3','HSC Y1'])
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/TATT_NLA_vs_ext_2_maglim.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/TATT_NLA_vs_ext_2_maglim.png')