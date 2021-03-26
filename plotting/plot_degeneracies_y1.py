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

base = '/Volumes/groke/work/chains/y1/'
#c1 = mc.chain(base+'fiducial/chain_1x2pt_hyperrank_2pt_NG_BLINDED_v0.40cov_xcorrGGL_27072020_SOMPZWZsamples_pit.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c1 = mc.chain(base+'blazek/eta/TATT/all/out_all-1x2pt-NG-TATT-alpha-v3.txt')
c2 = mc.chain(base+'fiducial/all/out_all-1x2pt-NG.txt')



#c1 = mc.chain('chain_1x2pt_fiducial_test_0.40_CLASS_NLA_C1_GAMA_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')

c1.add_s8(alpha=0.5)
c2.add_s8(alpha=0.5)


#'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'

omegam_1 = np.sum(c1.samples['cosmological_parameters--omega_m'] * c1.weight)/np.sum(c1.weight)
sigma8_1 = np.sum(c1.samples['cosmological_parameters--sigma_8'] * c1.weight)/np.sum(c1.weight)
s8_1 = np.sum(c1.samples['cosmological_parameters--s8'] * c1.weight)/np.sum(c1.weight)

omegam_2 = np.sum(c2.samples['cosmological_parameters--omega_m'] * c2.weight)/np.sum(c2.weight)
sigma8_2 = np.sum(c2.samples['cosmological_parameters--sigma_8'] * c2.weight)/np.sum(c2.weight)
s8_2 = np.sum(c2.samples['cosmological_parameters--s8'] * c2.weight)/np.sum(c2.weight)


samp1 = np.array([c1.samples['cosmological_parameters--omega_m']-omegam_1, c1.samples['cosmological_parameters--s8']-s8_1, c1.samples['cosmological_parameters--sigma_8']-sigma8_1])
samp2 = np.array([c2.samples['cosmological_parameters--omega_m']-omegam_2, c2.samples['cosmological_parameters--s8']-s8_2, c2.samples['cosmological_parameters--sigma_8']-sigma8_2])



#import pdb ; pdb.set_trace()
print('Making cornerplot...')
cc = ChainConsumer()

#import pdb ; pdb.set_trace()


names = [r'$\Omega_{\rm m}$','$S_8$', r'$\sigma_8$']




plt.close()
from getdist import plots, MCSamples
import getdist
import matplotlib.pyplot as plt


g = plots.get_subplot_plotter() #(width_inch=6, ratio=1)
g.settings.legend_fontsize = 22
g.settings.fontsize = 18
g.settings.axes_fontsize = 16
g.settings.axes_labelsize = 22
g.settings.axis_tick_max_labels = 15
g.settings.linewidth = 1.5
g.settings.legend_colored_text=True
g.settings.axis_tick_step_groups = [[2.5, 3, 4, 6, 8],[1, 2, 5, 10]]


samples = MCSamples(samples=samp1.T,names=['x1','x2','x3'], labels=names, label='TATT', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples5 = MCSamples(samples=samp2.T,names=['x1','x2','x3'], labels=names, label='NLA', weights=c2.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})

g.triangle_plot([samples, samples5],['x1','x2','x3'], filled=[False,True,False,False,True], diag1d_kwargs={'normalized':True}, contour_args={'alpha':0.4},contour_colors=['#FA86C9','#7223AD' ], labels=['TATT', 'NLA']) #, param_limits={'x1':(0.18,0.45), 'x2':(0.69,0.9), 'x3':(0.6,1.05)}) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])
#import pdb ; pdb.set_trace()

s8_ticks = [-0.2,-0.1,0,0.1]
omm_ticks = [-0.1,0,0.1,0.2]
sig8_ticks = [-0.15,0,0.15]

# ticks...
g.subplots[0][0].set_xticks(omm_ticks)
g.subplots[1][0].set_xticks(omm_ticks)
g.subplots[1][0].set_yticks(s8_ticks)
g.subplots[1][1].set_xticks(s8_ticks)
g.subplots[2][0].set_yticks(sig8_ticks)
g.subplots[2][0].set_xticks(omm_ticks)
g.subplots[2][1].set_yticks(sig8_ticks)
g.subplots[2][1].set_xticks(s8_ticks)
g.subplots[2][2].set_xticks(sig8_ticks)

#g.add_legend(['DES Y3','HSC Y1'])
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/blinded_y1cs_degeneracies.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/blinded_y1cs_degeneracies.png')