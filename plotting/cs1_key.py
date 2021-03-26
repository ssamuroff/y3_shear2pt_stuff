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
c1 = mc.chain(base+'maglim/unblinding/trimmed_chains/chain_1x2pt_lcdm_SR_maglim.txt')
	#final_paper_chains/chain_1x2_0321.txt')
c2 = mc.chain(base+'external/chain_p-TTTEEE-lowE_lcdm.txt')



#c1 = mc.chain('chain_1x2pt_fiducial_test_0.40_CLASS_NLA_C1_GAMA_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')

c1.add_s8(alpha=0.5)
c2.add_s8(alpha=0.5)


#'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'

samp1 = np.array([c1.samples['cosmological_parameters--omega_m'], c1.samples['cosmological_parameters--s8'], c1.samples['cosmological_parameters--sigma_8']])
samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8'], c2.samples['cosmological_parameters--sigma_8']])



#import pdb ; pdb.set_trace()
print('Making cornerplot...')
cc = ChainConsumer()

#import pdb ; pdb.set_trace()


names = [r'$\Omega_{\rm m}$','$S_8$', r'$\sigma_8$']


cc.add_chain(samp1.T, parameters=names, weights=c1.weight, kde=True, name=r'DES Y3 (Fiducial)')
cc.add_chain(samp2.T, parameters=names, weights=c2.weight, kde=True, name=r'Planck 2018 TT+TE+EE')



#7223AD
#4682B4
#228B22
#191970

# '#FA86C9','#7223AD','#DDA0DD'

cc.configure(colors=[ '#7223AD','#191970'],shade=[True,True,True]*3, shade_alpha=[0.65, 0.55, 0.1,0.5], kde=[2]*3,legend_kwargs={"loc": "upper right", "fontsize": 12},label_font_size=12,tick_font_size=12)
#cc.configure(colors=['#800080', '#800080', '#FF1493', '#000000' ],shade=[False,True,True,False], shade_alpha=[0.25,0.25,0.25], max_ticks=4, kde=[6]*5, linestyles=["-", "-", '-.', '--'], legend_kwargs={"loc": "upper right", "fontsize": 14},label_font_size=14,tick_font_size=14) 
plt.close() ; 
fig = cc.plotter.plot(extents={'$S_8$':(0.65,0.89),r'$\sigma_8$':(0.6,1.05),r'$\Omega_{\rm m}$':(0.16,0.45),'$A_1$':(0.,1.2), '$A_2$':(-4.,1), r'$\eta_1$':(-4,0), r'$\eta_2$':(-5,2), r'$b_{\rm TA}$':(0,2)}) #, truth=[0.3,0.82355,0.7,-1.7] )


#plt.suptitle(r'$\Lambda$CDM $3 \times 2\mathrm{pt}$', fontsize=16)
plt.subplots_adjust(bottom=0.15,left=0.15, top=0.98,right=0.98,hspace=0, wspace=0)

print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/unblinded_y3cs_keyplot_v2_maglim.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/unblinded_y3cs_keyplot_v2_maglim.png')



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


samples = MCSamples(samples=samp1.T,names=['x1','x2','x3'], labels=names, label='DES Y3', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples5 = MCSamples(samples=samp2.T,names=['x1','x2','x3'], labels=names, label='Planck 2018', weights=c2.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})

g.triangle_plot([samples, samples5],['x1','x2','x3'], filled=[True,True,False,False,True], contour_args={'alpha':0.6}, diag1d_kwargs={'normalized':True}, contour_colors=['#7223AD','#A4CD64'], labels=['DES Y3', 'Planck 2018'], param_limits={'x1':(0.18,0.51), 'x2':(0.69,0.9), 'x3':(0.6,1.05)}) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])
#import pdb ; pdb.set_trace()

s8_ticks = [0.7,0.75,0.8,0.85]
omm_ticks = [0.2,0.3,0.4]
sig8_ticks = [0.7,0.8,0.9,1.]

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
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/unblinded_y3cs_keyplot_getdist_v2_maglim_newcolourscheme3.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/unblinded_y3cs_keyplot_getdist_v2_maglim_newcolourscheme3.png')