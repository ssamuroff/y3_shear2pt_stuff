 
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

base = '/Users/hattifattener/Documents/y3cosmicshear'

# 0: NLA, 1: TATT
D1M0=mc.chain(base+"/chains/ias_fid/final/mnla_dtatt/chain_1x2pt_nla_sim_2pt_NG_BLINDED_v0.40cov_xcorrGGL27072020_1000samples_055ramp_all_2609_meanzisreal10.fits_sim_noiseless.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt")
D1M1=mc.chain(base+"/chains/ias_fid/final/mtatt_dtatt/chain_1x2pt_fiducial_sim_2pt_NG_BLINDED_v0.40cov_xcorrGGL27072020_1000samples_055ramp_all_2609_meanzisreal10.fits_sim_noiseless.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt")
D0M0=mc.chain(base+"/chains/ias_fid/final/mnla_dnla/chain_1x2pt_nla_sim_2pt_NG_BLINDED_v0.40cov_xcorrGGL27072020_1000samples_055ramp_all_2609_meanzisreal10.fits_sim_noiseless_nla.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt")
D0M1=mc.chain(base+"/chains/ias_fid/final/mtatt_dnla/chain_1x2pt_fiducial_sim_2pt_NG_BLINDED_v0.40cov_xcorrGGL27072020_1000samples_055ramp_all_2609_meanzisreal10.fits_sim_noiseless_nla.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt")


D1M0.add_s8()
D1M1.add_s8()
D0M0.add_s8()
D0M1.add_s8()


samp0 = np.array([D1M0.samples['cosmological_parameters--omega_m'], D1M0.samples['cosmological_parameters--s8'] ])
samp1 = np.array([D1M1.samples['cosmological_parameters--omega_m'], D1M1.samples['cosmological_parameters--s8'] ])
samp2 = np.array([D0M0.samples['cosmological_parameters--omega_m'], D0M0.samples['cosmological_parameters--s8'] ])
samp3 = np.array([D0M1.samples['cosmological_parameters--omega_m'], D0M1.samples['cosmological_parameters--s8'] ])


#import pdb ; pdb.set_trace()
print('Making cornerplot...')

#import pdb ; pdb.set_trace()

names = [r'$\Omega_{\rm m}$','$S_8$']


plt.close()
from getdist import plots, MCSamples
import getdist
import matplotlib.pyplot as plt


#g = plots.get_subplot_plotter() #(width_inch=6, ratio=1)
g = plots.get_single_plotter(width_inch=6, ratio=0.8)
g.settings.legend_fontsize = 14
g.settings.fontsize = 16
g.settings.axes_fontsize = 16
g.settings.axes_labelsize = 16
g.settings.axis_tick_max_labels = 16
g.settings.linewidth = 1.5
g.settings.legend_colored_text=True
g.settings.axis_tick_step_groups = [[2.5, 3, 4, 6, 8],[1, 2, 5, 10]]


samples0 = MCSamples(samples=samp0.T,names=['x1','x2'], labels=names, label='data=TATT, model=NLA', weights=D1M0.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples1 =MCSamples(samples=samp1.T,names=['x1','x2'], labels=names, label='data=TATT, model=TATT', weights=D1M1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples2 = MCSamples(samples=samp2.T,names=['x1','x2'], labels=names, label='data=NLA, model=NLA', weights=D0M0.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples3 =MCSamples(samples=samp3.T,names=['x1','x2'], labels=names, label='data=NLA, model=TATT', weights=D0M1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})


#7223AD
#A4CD64
#3775A1
#DD9EE8
#g.triangle_plot([samples, samples3, samples2, samples4, samples5],['x1','x2'], diag1d_kwargs={'normalized':True}, contour_args=[{'alpha':0.6},{'alpha':1,'ls':'--'},{'alpha':1.},{'alpha':1.},{'alpha':0.6}], filled=[True,False,False,False,True], contour_colors=['#7223AD','#000000','#3775A1','#FF69B4','#A4CD64' ], labels=['DES Y3', 'HSC Y1', 'DES Y1', 'KiDS-1000', 'Planck 18'], param_limits={'x1':(0.05,0.48), 'x2':(0.65,0.9), 'x3':(-2,3.5)}) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])

g.plot_2d([samples0, samples1, samples2, samples3, ],['x1','x2'], diag1d_kwargs={'normalized':True}, alphas=[0.6,0.6,1.,1.,0.6], ls=['-','-','-','-','-','-'],lws=[1.5]*5,filled=[True,True,False,False,True], colors=['#191970','#8b008b','#FF69B4','#228B22' ], labels=['DES Y3', 'HSC Y1', 'DES Y1', 'KiDS-1000', 'Planck 18'], lims=[0.15,0.48,0.7,0.9]) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])
#import pdb ; pdb.set_trace()

s8_ticks = [0.65,0.75,0.85]
omm_ticks = [0.1,0.2,0.3,0.4]
a1_ticks = [-1,0,1,2,3]

# ticks...
#g.subplots[0][0].set_xticks(omm_ticks)
#g.subplots[1][0].set_xticks(omm_ticks)
#g.subplots[1][0].set_yticks(s8_ticks)
#g.subplots[1][1].set_xticks(s8_ticks)

plt.title(r'\textbf{simulated Y3 cosmic shear}', fontsize=14) #, xy=(0.24,0.901))
plt.plot([0.3], [0.8259369942966649*np.sqrt(0.3/0.3)], markersize=8., marker='x', color='k', linestyle='none' )
g.add_legend(['data=TATT, model=NLA','data=TATT, model=TATT','data=NLA, model=NLA','data=NLA, model=TATT'], legend_loc='lower left')
#plt.subplots_adjust(top=0.94)
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/1x2pt_iatest_tatt_nla_s8omm.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/1x2pt_iatest_tatt_nla_s8omm.png')
