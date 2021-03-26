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

base = '/Users/hattifattener/Documents/y3cosmicshear/chains/mice/'
c1 = mc.chain(base+'baseline/chain_1x2pt_fiducial_sim_MICE_baseline_Sep8th.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c2 = mc.chain('/Volumes/groke/work/chains/y3/simulated/mice/chain_1x2pt_fiducial_sim_MICE_wIA_2021.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c3 = mc.chain('/Volumes/groke/work/chains/y3/simulated/mice/chain_1x2pt_nla_sim_MICE_wIA_2021.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')

c4 = mc.chain('/Volumes/groke/work/chains/y3/simulated/mice/chain_1x2pt_iasonly_MICE_wIA_2021.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')

#c1 = mc.chain('chain_1x2pt_fiducial_test_0.40_CLASS_NLA_C1_GAMA_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')

c1.add_s8()
c2.add_s8()
c3.add_s8()




#'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'

samp1 = np.array([c1.samples['cosmological_parameters--omega_m'], c1.samples['cosmological_parameters--s8'], c1.samples['intrinsic_alignment_parameters--a1'], c1.samples['intrinsic_alignment_parameters--a2'], c1.samples['intrinsic_alignment_parameters--bias_ta']])
samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8'], c2.samples['intrinsic_alignment_parameters--a1'], c2.samples['intrinsic_alignment_parameters--a2'], c2.samples['intrinsic_alignment_parameters--bias_ta']])
samp3 = np.array([c3.samples['cosmological_parameters--omega_m'], c3.samples['cosmological_parameters--s8'], c3.samples['intrinsic_alignment_parameters--a1']])
samp4 = np.array([c4.samples['intrinsic_alignment_parameters--a1'], c4.samples['intrinsic_alignment_parameters--a2'], c4.samples['intrinsic_alignment_parameters--bias_ta']])

#import pdb ; pdb.set_trace()
print('Making cornerplot...')
cc = ChainConsumer()

#import pdb ; pdb.set_trace()

names0 = [r'$\Omega_{\rm m}$','$S_8$','$A_1$']
names = ['$A_1$', '$A_2$', r'$b_{\rm TA}$']
names2 = [r'$\Omega_{\rm m}$','$S_8$','$A_1$', '$A_2$', r'$b_{\rm TA}$']


cc.add_chain(samp1.T, parameters=names2, weights=c1.weight, kde=True, name=r'MICE Baseline')
cc.add_chain(samp2.T, parameters=names2, weights=c2.weight, kde=True, name=r'MICE IAs (TATT)')
cc.add_chain(samp3.T, parameters=names0, weights=c3.weight, kde=True, name=r'MICE IAs (NLA)')



cc.configure(colors=['#2e8b57','#002366','#808080', '#FF1493', ],shade=[True,True,False]*3, shade_alpha=[0.5, 0.5, 0.1,0.5], legend_kwargs={"loc": "upper right", "fontsize": 20},label_font_size=22,tick_font_size=14)
#cc.configure(colors=['#800080', '#800080', '#FF1493', '#000000' ],shade=[False,True,True,False], shade_alpha=[0.25,0.25,0.25], max_ticks=4, kde=[6]*5, linestyles=["-", "-", '-.', '--'], legend_kwargs={"loc": "upper right", "fontsize": 14},label_font_size=14,tick_font_size=14) 
plt.close() ; 
fig = cc.plotter.plot(extents={'$S_8$':(0.59,0.8),r'$\Omega_{\rm m}$':(0.15,0.4),'$A_1$':(-4.,2), '$A_2$':(-3.5,3.5), r'$\eta_1$':(-5,5), r'$\eta_2$':(-5,5), r'$b_{\rm TA}$':(0,2)}, truth=[0.25,0.7302967433402215] )


#plt.suptitle(r'$\Lambda$CDM $1 \times 2\mathrm{pt}$, data=TATT', fontsize=16)
plt.subplots_adjust(bottom=0.155,left=0.155, hspace=0, wspace=0)

print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/mice_ia_1x2pt_v2.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/mice_ia_1x2pt_v2.png')

# #4682b4 steel blue
# #002366 royal blue











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


samples = MCSamples(samples=samp1.T,names=['x1','x2','x3','x4','x5'], labels=names2, label='Baseline (TATT)', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples2 =MCSamples(samples=samp2.T,names=['x1','x2','x3','x4','x5'], labels=names2, label='with IAs (TATT)', weights=c2.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples3 = MCSamples(samples=samp3.T,names=['x1','x2','x3'], labels=names0, label='with IAs (NLA)', weights=c3.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples4 = MCSamples(samples=samp4.T,names=['x3','x4','x5'], labels=names, label='with IAs (TATT, fixed cosmology)', weights=c4.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})

g.triangle_plot([samples, samples2, samples3,samples4],['x1','x2','x3','x4','x5'], diag1d_kwargs={'normalized':True}, filled=[True,False,False,True,True], contour_args={'alpha':0.6},contour_colors=['#191970','#4E1B68','#228B22','#BD8AD8','#7223AD' ], labels=['Baseline (TATT)', 'with IAs (TATT)', 'with IAs (NLA)'], param_limits={'x1':(0.15,0.48), 'x2':(0.6,0.79), 'x3':(-2.5,1.1),'x5':(0,2.2)}, markers={'x1':0.25,'x2':0.7302967433402215}, marker_args={'color':'hotpink', 'lw':1.})
#import pdb ; pdb.set_trace()
#
s8_ticks = [0.65,0.7,0.75]
omm_ticks = [0.2,0.3,0.4]
a1_ticks = [-2,-1,0,1]
a2_ticks = [-4,-2,0,2]
bta_ticks = [0,0.5,1,1.5,2]
#
## ticks...
g.subplots[0][0].set_xticks(omm_ticks)
g.subplots[1][0].set_xticks(omm_ticks)
g.subplots[1][0].set_yticks(s8_ticks)
g.subplots[1][1].set_xticks(s8_ticks)
g.subplots[2][0].set_yticks(a1_ticks)
g.subplots[2][0].set_xticks(omm_ticks)
g.subplots[2][1].set_yticks(a1_ticks)
g.subplots[2][1].set_xticks(s8_ticks)
g.subplots[2][2].set_xticks(a1_ticks)


g.subplots[3][0].set_yticks(a2_ticks)
g.subplots[3][0].set_xticks(omm_ticks)
g.subplots[3][1].set_yticks(a2_ticks)
g.subplots[3][1].set_xticks(s8_ticks)
g.subplots[3][2].set_xticks(a1_ticks)
g.subplots[3][2].set_yticks(a2_ticks)
g.subplots[3][3].set_xticks(a2_ticks)



g.subplots[4][0].set_yticks(bta_ticks)
g.subplots[4][0].set_xticks(omm_ticks)
g.subplots[4][1].set_yticks(bta_ticks)
g.subplots[4][1].set_xticks(s8_ticks)
g.subplots[4][2].set_xticks(a1_ticks)
g.subplots[4][2].set_yticks(bta_ticks)
g.subplots[4][3].set_xticks(a2_ticks)
g.subplots[4][4].set_xticks(bta_ticks)


#g.add_legend(['DES Y3','HSC Y1'])
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/mice_ia_1x2pt_v2_getdist.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/mice_ia_1x2pt_v2_getdist.png')




exit()



samp1 = np.array([c1.samples['cosmological_parameters--omega_m'], c1.samples['cosmological_parameters--s8']])
samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8']])
#samp3 = np.array([c3.samples['cosmological_parameters--omega_m'], c3.samples['cosmological_parameters--s8']])


#import pdb ; pdb.set_trace()
print('Making cornerplot...')
cc = ChainConsumer()

#import pdb ; pdb.set_trace()


names = [r'$\Omega_{\rm m}$','$S_8$']
names2 = [r'$\Omega_{\rm m}$','$S_8$']


cc.add_chain(samp1.T, parameters=names, weights=c1.weight, kde=True, name=r'MICE No Shape Noise, No IAs')
cc.add_chain(samp2.T, parameters=names2, weights=c2.weight, kde=True, name=r'MICE IAs')
#cc.add_chain(samp3.T, parameters=names, weights=c3.weight, kde=True, name=r'MICE IAs (reduced)')



cc.configure(colors=['#121F90','#8b008b','#000000', '#FF1493', ],shade=[False,True,True]*3, shade_alpha=[0.25, 0.25, 0.1,0.5], legend_kwargs={"loc": "lower right", "fontsize": 8},label_font_size=10,tick_font_size=8)
#cc.configure(colors=['#800080', '#800080', '#FF1493', '#000000' ],shade=[False,True,True,False], shade_alpha=[0.25,0.25,0.25], max_ticks=4, kde=[6]*5, linestyles=["-", "-", '-.', '--'], legend_kwargs={"loc": "upper right", "fontsize": 14},label_font_size=14,tick_font_size=14) 
plt.close() ; 
fig = cc.plotter.plot(extents={'$S_8$':(0.65,0.95),r'$\Omega_{\rm m}$':(0.15,0.47),'$A_1$':(-5.,5), '$A_2$':(-5.,5), r'$\eta_1$':(-5,5), r'$\eta_2$':(-5,2), r'$b_{\rm TA}$':(0,2)}) #, truth=[0.3,0.82355,0.7,-1.7] )


#plt.suptitle(r'$\Lambda$CDM $1 \times 2\mathrm{pt}$, data=TATT', fontsize=16)
plt.subplots_adjust(bottom=0.2,left=0.22, top=0.98,right=0.98, hspace=0, wspace=0)

print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/mice_ia_1x2pt_1panel.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/mice_ia_1x2pt_1panel.png')


