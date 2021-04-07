 
import numpy as np
import os
import pylab as plt
plt.switch_backend('pdf')
plt.style.use('y1a1')

import tools.emcee as mc
from chainconsumer import ChainConsumer

from matplotlib import rcParams
rcParams['xtick.major.size'] = 3.5
rcParams['xtick.minor.size'] = 1.7
rcParams['ytick.major.size'] = 3.5
rcParams['ytick.minor.size'] = 1.7
rcParams['xtick.direction']='in'
rcParams['ytick.direction']='in'
print('Loading chains...')

base = '/Users/hattifattener/Documents/y3cosmicshear/chains/'

c0 = mc.chain('/Volumes/groke/work/chains/y3/real/maglim/unblinding/chain_1x2pt_lcdm_SR_maglim.txt')
c1 = mc.chain('/Volumes/groke/work/chains/y3/real/final_paper_chains/tests_1x2pt/maglim/chain_noia_1x2pt_lcdm_maglim.txt')
c2 = mc.chain('/Volumes/groke/work/chains/y3/real/final_paper_chains/tests_1x2pt/maglim/chain_NLA_noz_1x2pt_lcdm_maglim.txt')
c3 = mc.chain('/Volumes/groke/work/chains/y3/real/final_paper_chains/tests_1x2pt/maglim/chain_NLA_1x2pt_lcdm_maglim.txt')


#c1 = mc.chain('chain_1x2pt_fiducial_test_0.40_CLASS_NLA_C1_GAMA_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c0.add_s8()
c1.add_s8()
c2.add_s8()
c3.add_s8()


samp0 = np.array([c0.samples['cosmological_parameters--omega_m'], c0.samples['cosmological_parameters--s8'], c0.samples['intrinsic_alignment_parameters--a1'] ])
samp1 = np.array([c1.samples['cosmological_parameters--omega_m'], c1.samples['cosmological_parameters--s8'] ])
samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8'], c2.samples['intrinsic_alignment_parameters--a1'] ])
samp3 = np.array([c3.samples['cosmological_parameters--omega_m'], c3.samples['cosmological_parameters--s8'], c3.samples['intrinsic_alignment_parameters--a1'] ])


#import pdb ; pdb.set_trace()
print('Making cornerplot...')

plt.close()
from getdist import plots, MCSamples
import getdist
import matplotlib.pyplot as plt


g = plots.get_subplot_plotter() #(width_inch=6, ratio=1)
g.settings.legend_fontsize = 22
g.settings.fontsize = 18
g.settings.axes_fontsize = 18
g.settings.axes_labelsize = 22
g.settings.axis_tick_max_labels = 15
g.settings.linewidth = 1.5
g.settings.legend_colored_text=True
g.settings.axis_tick_step_groups = [[2.5, 3, 4, 6, 8],[1, 2, 5, 10]]

names = [r'$\Omega_{\rm m}$','$S_8$','$A_1$']
samples = MCSamples(samples=samp0.T,names=['x1','x2','x3'], labels=names, label='Fiducial', weights=c0.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples1 = MCSamples(samples=samp1.T,names=['x1','x2'], labels=names[:-1], label='No IAs', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples2 = MCSamples(samples=samp2.T,names=['x1','x2','x3'], labels=names, label='NLA no $z$', weights=c2.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples3 = MCSamples(samples=samp3.T,names=['x1','x2','x3'], labels=names, label='NLA', weights=c3.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})




#7223AD
#A4CD64
#3775A1
#DD9EE8
g.triangle_plot([samples,samples1,samples2,samples3],['x1','x2','x3'], diag1d_kwargs={'normalized':True}, contour_args=[{'alpha':0.6},{'alpha':1},{'alpha':1.},{'alpha':1.},{'alpha':0.6}], filled=[True,False,False,False], contour_colors=['#7223AD','#DD9EE8','#FFC0CB','hotpink','#A4CD64' ], labels=['DES Y3', 'HSC Y1', 'DES Y1', 'KiDS-1000', 'Planck 18'], param_limits={'x1':(0.05,0.48), 'x2':(0.65,0.9), 'x3':(-2,1.5)}) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])
#import pdb ; pdb.set_trace()

s8_ticks = [0.65,0.75,0.85]
omm_ticks = [0.1,0.2,0.3,0.4]
a1_ticks = [-1,0,1]

# ticks...
g.subplots[0][0].set_xticks(omm_ticks)
g.subplots[1][0].set_xticks(omm_ticks)
g.subplots[1][0].set_yticks(s8_ticks)
g.subplots[1][1].set_xticks(s8_ticks)
g.subplots[2][0].set_yticks(a1_ticks)
g.subplots[2][0].set_xticks(omm_ticks)
g.subplots[2][1].set_yticks(a1_ticks)
g.subplots[2][1].set_xticks(s8_ticks)
g.subplots[2][2].set_xticks(a1_ticks)

#g.add_legend(['DES Y3','HSC Y1'])
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/1x2pt_ias_all_getdist_maglim_v2.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/1x2pt_ias_all_getdist_maglim_v2.png')

