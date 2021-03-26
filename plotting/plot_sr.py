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
c2 = mc.chain(base+'maglim/unblinding/chain_1x2pt_lcdm_noSR_maglim.txt')



#c1 = mc.chain('chain_1x2pt_fiducial_test_0.40_CLASS_NLA_C1_GAMA_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')

c1.add_s8(alpha=0.5)
c2.add_s8(alpha=0.5)


#'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'

samp1 = np.array([c1.samples['intrinsic_alignment_parameters--a1'], c1.samples['intrinsic_alignment_parameters--a2'], c1.samples['intrinsic_alignment_parameters--alpha1'], c1.samples['intrinsic_alignment_parameters--alpha2'], c1.samples['intrinsic_alignment_parameters--bias_ta'],c1.samples['wl_photoz_errors--bias_1'],c1.samples['wl_photoz_errors--bias_2'],c1.samples['wl_photoz_errors--bias_3'],c1.samples['wl_photoz_errors--bias_4'], c1.samples['bias_lens--b1'],c1.samples['bias_lens--b2'],c1.samples['bias_lens--b3']])
samp2 = np.array([c2.samples['intrinsic_alignment_parameters--a1'], c2.samples['intrinsic_alignment_parameters--a2'], c2.samples['intrinsic_alignment_parameters--alpha1'], c2.samples['intrinsic_alignment_parameters--alpha2'], c2.samples['intrinsic_alignment_parameters--bias_ta'],c2.samples['wl_photoz_errors--bias_1'],c2.samples['wl_photoz_errors--bias_2'],c2.samples['wl_photoz_errors--bias_3'],c2.samples['wl_photoz_errors--bias_4']])




#import pdb ; pdb.set_trace()
print('Making cornerplot...')
cc = ChainConsumer()

#import pdb ; pdb.set_trace()


names_IA = [r'$A_1$', r'$A_2$', r'$\eta_1$', r'$\eta_2$', r'$b_{\rm TA}$', r'$\delta z_s^1$',r'$\delta z_s^2$', r'$\delta z_s^3$', r'$\delta z_s^4$']
names_lens = ['$b_1$', '$b_2$', '$b_3$']

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


samples = MCSamples(samples=samp1.T,names=['x%d'%(i+1) for i in range(len(names_IA+names_lens))], labels=names_IA+names_lens, label=r'$1\times2$pt + SR', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples2 = MCSamples(samples=samp2.T,names=['x%d'%(i+1) for i in range(len(names_IA))], labels=names_IA, label=r'$1\times2$pt', weights=c2.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})

g.triangle_plot([samples, samples2],['x%d'%(i+1) for i in range(len(names_IA+names_lens))], filled=[True,True,False,False,True], contour_args={'alpha':0.6}, diag1d_kwargs={'normalized':True}, contour_colors=['#9A32A3','#FFC0CB','#DD9EE8'], labels=[r'$1\times2$pt + SR', r'$1\times2$pt'] , param_limits={'x1':(-3,2),'x2':(-3.5,3.5), 'x3':(-5,5), 'x4':(-5,5), 'x5':(0.,2), 'x6':(-0.05,0.05), 'x7':(-0.05,0.05), 'x8':(-0.05,0.05), 'x9':(-0.05,0.05), 'x10':(0.8,3), 'x11':(0.8,3), 'x12':(0.8,3) }) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])
#import pdb ; pdb.set_trace()

s8_ticks = [0.7,0.75,0.8,0.85]
omm_ticks = [0.2,0.3,0.4]
sig8_ticks = [0.7,0.8,0.9,1.]

# ticks...
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
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/ias_lens_sr.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/ias_lens_sr.png')