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


c1 = mc.chain('/Volumes/groke/work/chains/y3/real/chain_1x2pt_lcdm.txt')
c2 = mc.chain('/Volumes/groke/work/chains/y3/real/external/chain_s_b_lcdm.txt')
c3 = mc.chain('/Volumes/groke/work/chains/y3/real/external/chain_1x2pt_s_b_lcdm.txt')



#c1 = mc.chain('chain_1x2pt_fiducial_test_0.40_CLASS_NLA_C1_GAMA_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')

c1.add_s8()
c2.add_s8()
c3.add_s8()

c3.samples['cosmological_parameters--omega_m']+=0.15
c3.samples['cosmological_parameters--sigma_8']+=0.15

#'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'

samp1 = np.array([c1.samples['cosmological_parameters--omega_m'], c1.samples['cosmological_parameters--s8'], c1.samples['cosmological_parameters--sigma_8']])
samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8'], c2.samples['cosmological_parameters--sigma_8']])
samp3 = np.array([c3.samples['cosmological_parameters--omega_m'], c3.samples['cosmological_parameters--s8'], c3.samples['cosmological_parameters--sigma_8']])

#import pdb ; pdb.set_trace()
print('Making cornerplot...')


#import pdb ; pdb.set_trace()

names0 = [r'$\Omega_{\rm m}$','$S_8$',r'$\sigma_8$']
names = ['$A_1$', '$A_2$', r'$b_{\rm TA}$']
names2 = [r'$\Omega_{\rm m}$','$S_8$','$A_1$', '$A_2$', r'$b_{\rm TA}$']


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


samples = MCSamples(samples=samp1.T,names=['x1','x2','x3'], labels=names0, label=r'$1\times2$pt', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples2 =MCSamples(samples=samp2.T,names=['x1','x2','x3'], labels=names0, label=r'Low$-z$', weights=c2.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples3 = MCSamples(samples=samp3.T,names=['x1','x2','x3'], labels=names0, label=r'$1\times2$pt + Low$-z$', weights=c3.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})

g.triangle_plot([samples, samples2, samples3],['x1','x2','x3'], filled=[True,True,True,True,True], contour_args={'alpha':0.7},contour_colors=['#FA86C9','#191970','#4E1B68','#BD8AD8','#7223AD' ], param_limits={'x1':(0.15,0.48), 'x2':(0.68,0.85),'x3':(0.5,1.2) })
#import pdb ; pdb.set_trace()
##
#s8_ticks = [0.65,0.7,0.75]
#omm_ticks = [0.2,0.3,0.4]
#a1_ticks = [-2,-1,0,1]
#a2_ticks = [-4,-2,0,2]
#bta_ticks = [0,0.5,1,1.5,2]
##
### ticks...
#g.subplots[0][0].set_xticks(omm_ticks)
#g.subplots[1][0].set_xticks(omm_ticks)
#g.subplots[1][0].set_yticks(s8_ticks)
#g.subplots[1][1].set_xticks(s8_ticks)
#g.subplots[2][0].set_yticks(a1_ticks)
#g.subplots[2][0].set_xticks(omm_ticks)
#g.subplots[2][1].set_yticks(a1_ticks)
#g.subplots[2][1].set_xticks(s8_ticks)
#g.subplots[2][2].set_xticks(a1_ticks)
#
#
#g.subplots[3][0].set_yticks(a2_ticks)
#g.subplots[3][0].set_xticks(omm_ticks)
#g.subplots[3][1].set_yticks(a2_ticks)
#g.subplots[3][1].set_xticks(s8_ticks)
#g.subplots[3][2].set_xticks(a1_ticks)
#g.subplots[3][2].set_yticks(a2_ticks)
#g.subplots[3][3].set_xticks(a2_ticks)


#
#g.subplots[4][0].set_yticks(bta_ticks)
#g.subplots[4][0].set_xticks(omm_ticks)
#g.subplots[4][1].set_yticks(bta_ticks)
#g.subplots[4][1].set_xticks(s8_ticks)
#g.subplots[4][2].set_xticks(a1_ticks)
#g.subplots[4][2].set_yticks(bta_ticks)
#g.subplots[4][3].set_xticks(a2_ticks)
#g.subplots[4][4].set_xticks(bta_ticks)
#

#g.add_legend(['DES Y3','HSC Y1'])
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/external_lcdm.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/external_lcdm.png')

