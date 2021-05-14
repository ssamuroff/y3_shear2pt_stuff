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
c1 = mc.chain(base+'/final_paper_chains/chain_3x2pt_lcdm_SR_maglim_IAeff.txt')


c1.add_s8(alpha=0.5)


#'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'

samp1 = np.array([c1.samples['intrinsic_alignment_parameters--aeff1_1'], c1.samples['intrinsic_alignment_parameters--aeff2_1']])
samp2 = np.array([c1.samples['intrinsic_alignment_parameters--aeff1_2'], c1.samples['intrinsic_alignment_parameters--aeff2_2']])
samp3 = np.array([c1.samples['intrinsic_alignment_parameters--aeff1_3'], c1.samples['intrinsic_alignment_parameters--aeff2_3']])
samp4 = np.array([c1.samples['intrinsic_alignment_parameters--aeff1_4'], c1.samples['intrinsic_alignment_parameters--aeff2_4']])


names = [r'$A_1$', r'$A_2$']




plt.close()
from getdist import plots, MCSamples
import getdist
import matplotlib.pyplot as plt


g = plots.get_single_plotter(width_inch=6, ratio=0.8)
g.settings.legend_fontsize = 12
g.settings.fontsize = 18
g.settings.axes_fontsize = 18
g.settings.axes_labelsize = 22
g.settings.axis_tick_max_labels = 15
g.settings.linewidth = 1.5
g.settings.legend_colored_text=True
g.settings.axis_tick_step_groups = [[2.5, 3, 4, 6, 8],[1, 2, 5, 10]]


samples1 = MCSamples(samples=samp1.T,names=['x1','x2'], labels=names, label='bin 1', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples2 = MCSamples(samples=samp2.T,names=['x1','x2'], labels=names, label='bin 2', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples3 = MCSamples(samples=samp3.T,names=['x1','x2'], labels=names, label='bin 3', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples4 = MCSamples(samples=samp4.T,names=['x1','x2'], labels=names, label='bin 4', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})


#DD9EE8
#g.triangle_plot([samples, samples2, samples5],['x1','x2','x3'], filled=[True,False,True,False,False,True], contour_args=[{'alpha':0.6},{'alpha':1.,'ls':'--'},{'alpha':0.6},{'alpha':1.}], diag1d_kwargs={'normalized':True}, contour_colors=['#7223AD','#000000','#A4CD64'], labels=['DES Y3', 'Planck 2018'], param_limits={'x1':(0.18,0.51), 'x2':(0.69,0.9), 'x3':(0.6,1.05)}) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])
#import pdb ; pdb.set_trace()

g.plot_2d([samples1, samples2, samples3, samples4],['x1','x2'], diag1d_kwargs={'normalized':True}, alphas=[0.6,0.6,0.6,0.6], ls=['-','-','-','-','-','-'],lws=[1.5]*5,filled=[False,False,False,True], colors=['#8b008b','steelblue','#ffc0cb', '#FF69B4'], lims=[-2.5,2,-4.,5.] ) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])

s8_ticks = [0.7,0.75,0.8,0.85]
omm_ticks = [0.2,0.3,0.4]
sig8_ticks = [0.7,0.8,0.9,1.]

# ticks...
#g.subplots[0][0].set_xticks(omm_ticks)
#g.subplots[0][0].set_yticks(s8_ticks)


plt.axhline(0,color='hotpink',ls=':')
plt.axvline(0,color='hotpink',ls=':')
g.add_legend(['bin 1','bin 2','bin 3', 'bin 4'])
#plt.title(r'$3\times2$pt')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/3x2pt_ias_zbins_maglim.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/3x2pt_ias_zbins_maglim.png')

plt.close()

c1 = mc.chain(base+'/final_paper_chains/chain_1x2pt_lcdm_SR_maglim_IAeff.txt')


c1.add_s8(alpha=0.5)


#'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'

samp1 = np.array([c1.samples['intrinsic_alignment_parameters--aeff1_1'], c1.samples['intrinsic_alignment_parameters--aeff2_1']])
samp2 = np.array([c1.samples['intrinsic_alignment_parameters--aeff1_2'], c1.samples['intrinsic_alignment_parameters--aeff2_2']])
samp3 = np.array([c1.samples['intrinsic_alignment_parameters--aeff1_3'], c1.samples['intrinsic_alignment_parameters--aeff2_3']])
samp4 = np.array([c1.samples['intrinsic_alignment_parameters--aeff1_4'], c1.samples['intrinsic_alignment_parameters--aeff2_4']])


names = [r'$A_1$', r'$A_2$']




plt.close()
from getdist import plots, MCSamples
import getdist
import matplotlib.pyplot as plt


g = plots.get_single_plotter(width_inch=6, ratio=0.8)
g.settings.legend_fontsize = 12
g.settings.fontsize = 18
g.settings.axes_fontsize = 18
g.settings.axes_labelsize = 22
g.settings.axis_tick_max_labels = 15
g.settings.linewidth = 1.5
g.settings.legend_colored_text=True
g.settings.axis_tick_step_groups = [[2.5, 3, 4, 6, 8],[1, 2, 5, 10]]


samples1 = MCSamples(samples=samp1.T,names=['x1','x2'], labels=names, label='bin 1', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples2 = MCSamples(samples=samp2.T,names=['x1','x2'], labels=names, label='bin 2', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples3 = MCSamples(samples=samp3.T,names=['x1','x2'], labels=names, label='bin 3', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples4 = MCSamples(samples=samp4.T,names=['x1','x2'], labels=names, label='bin 4', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})


#DD9EE8
#g.triangle_plot([samples, samples2, samples5],['x1','x2','x3'], filled=[True,False,True,False,False,True], contour_args=[{'alpha':0.6},{'alpha':1.,'ls':'--'},{'alpha':0.6},{'alpha':1.}], diag1d_kwargs={'normalized':True}, contour_colors=['#7223AD','#000000','#A4CD64'], labels=['DES Y3', 'Planck 2018'], param_limits={'x1':(0.18,0.51), 'x2':(0.69,0.9), 'x3':(0.6,1.05)}) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])
#import pdb ; pdb.set_trace()

g.plot_2d([samples1, samples2, samples3, samples4],['x1','x2'], diag1d_kwargs={'normalized':True}, alphas=[0.6,0.6,0.6,0.6], ls=['-','-','-','-','-','-'],lws=[1.5]*5,filled=[False,False,False,True], colors=['#8b008b','steelblue','#ffc0cb', '#FF69B4'], lims=[-2.5,2,-4.,5.]  ) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])

s8_ticks = [0.7,0.75,0.8,0.85]
omm_ticks = [0.2,0.3,0.4]
sig8_ticks = [0.7,0.8,0.9,1.]

# ticks...
#g.subplots[0][0].set_xticks(omm_ticks)
#g.subplots[0][0].set_yticks(s8_ticks)

plt.axhline(0,color='hotpink',ls=':')
plt.axvline(0,color='hotpink',ls=':')
g.add_legend(['bin 1','bin 2','bin 3', 'bin 4'])
#plt.title(r'$3\times2$pt')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/1x2pt_ias_zbins_maglim.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/1x2pt_ias_zbins_maglim.png')

