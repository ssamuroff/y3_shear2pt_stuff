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
#rcParams['text.usetex']=False

print('Loading chains...')

base = '/Volumes/groke/work/chains/y3/real/'
#c1 = mc.chain(base+'fiducial/chain_1x2pt_hyperrank_2pt_NG_BLINDED_v0.40cov_xcorrGGL_27072020_SOMPZWZsamples_pit.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c1 = mc.chain(base+'/final_paper_chains/chain_1x2pt_lcdm_SR_maglim.txt')
c2 = mc.chain(base+'/final_paper_chains/tests_1x2pt/maglim/chain_TATT_1x2pt_fixednu_lcdm_maglim.txt')
c3 = mc.chain(base+'/final_paper_chains/tests_1x2pt/maglim/chain_TATT_1x2pt_fixednu_lcdm_maglim.txt')
#c4 = mc.chain(base+'')



c1.add_s8()
c2.add_s8()
c3.add_s8()
#c4.add_s8()



#'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'

samp1 = np.array([c1.samples['cosmological_parameters--omega_m'], c1.samples['cosmological_parameters--s8']])
samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8']])
samp3 = np.array([c3.samples['cosmological_parameters--omega_m'], c3.samples['cosmological_parameters--s8']])
#samp4 = np.array([c4.samples['cosmological_parameters--w0'],c4.samples['cosmological_parameters--omega_m'], c4.samples['cosmological_parameters--s8'], c4.samples['intrinsic_alignment_parameters--a1'], c4.samples['intrinsic_alignment_parameters--a2']])




#import pdb ; pdb.set_trace()
print('Making cornerplot...')
cc = ChainConsumer()

#import pdb ; pdb.set_trace()


names = [r'$\Omega_{\rm m}$','$S_8$']

plt.close()
from getdist import plots, MCSamples
import getdist
import matplotlib.pyplot as plt


g = plots.get_subplot_plotter() #(width_inch=6, ratio=1)
g.settings.legend_fontsize = 13
g.settings.fontsize = 16
g.settings.axes_fontsize = 16
g.settings.axes_labelsize = 16
g.settings.axis_tick_max_labels = 15
g.settings.linewidth = 1.5
g.settings.legend_colored_text=True
g.settings.axis_tick_step_groups = [[2.5, 3, 4, 6, 8],[1, 2, 5, 10]]


samples = MCSamples(samples=samp1.T,names=['x1','x2'], labels=names, label='DES Y3 Fiducial', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples2 = MCSamples(samples=samp3.T,names=['x1','x2'], labels=names, label=r'Fixed $\sum m_\nu = 0.06 \mathrm{eV}$', weights=c3.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples3 = MCSamples(samples=samp2.T,names=['x1','x2'], labels=names, label='HMCode $P(k)$', weights=c2.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})

g.triangle_plot([samples, samples2, samples3],['x1','x2'], filled=[True,False,False,False,False,True], contour_args=[{'alpha':0.6},{'alpha':1.},{'alpha':1},{'alpha':1.}], diag1d_kwargs={'normalized':True}, contour_colors=['#7223AD','#DD9EE8','#A4CD64'], labels=['DES Y3', 'Planck 2018'], param_limits={'x1':(0.16,0.5), 'x2':(0.69,0.87), 'x3':(0.6,1.05)}) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])
#import pdb ; pdb.set_trace()

s8_ticks = [0.7,0.75,0.8,0.85]
omm_ticks = [0.2,0.3,0.4]
sig8_ticks = [0.7,0.8,0.9,1.]

# ticks...
g.subplots[0][0].set_xticks(omm_ticks)
g.subplots[1][0].set_xticks(omm_ticks)
g.subplots[1][0].set_yticks(s8_ticks)
g.subplots[1][1].set_xticks(s8_ticks)


#g.add_legend(['DES Y3','HSC Y1'])
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/nu_hm_maglim.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/nu_hm_maglim.png')