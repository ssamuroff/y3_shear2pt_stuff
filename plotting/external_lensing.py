 
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

c0 = mc.chain('/Volumes/groke/work/chains/y3/real/final_paper_chains/chain_1x2pt_lcdm_SR_maglim.txt')
	#chain_1x2pt_lcdm.txt')
c1 = np.genfromtxt(base+'/external/lensing/HSC_Y1_LCDM_post_fid.txt',names=True)
c2 = mc.chain('/Volumes/groke/work/chains/y3/real/final_paper_chains/chain_1x2agg_ML.txt')
#mc.chain('/Volumes/groke/work/chains/y1/fiducial/all/out_all-1x2pt-NG.txt')
c3 = mc.chain('/Volumes/groke/work/other_peoples_datasets/kids1000/KiDS1000_Cosebis_output_multinest_C.txt')

base = '/Volumes/groke/work/chains/y3/real/'
c4 = mc.chain(base+'external/chain_p-TTTEEE-lowE_lcdm.txt')



#c1 = mc.chain('chain_1x2pt_fiducial_test_0.40_CLASS_NLA_C1_GAMA_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c0.add_s8()
c2.add_s8()
s8_1 = c1['COSMOLOGICAL_PARAMETERSSIGMA_8'] * np.sqrt(c1['cosmological_parametersomega_m']/0.3) 
c4.add_s8()
c3.add_s8()

samp0 = np.array([c0.samples['cosmological_parameters--omega_m'], c0.samples['cosmological_parameters--s8'], c0.samples['intrinsic_alignment_parameters--a1'] ])
samp1 = np.array([c1['cosmological_parametersomega_m'], s8_1, c1['intrinsic_alignment_parametersa1']])
samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8'], c2.samples['intrinsic_alignment_parameters--a1'] ])
samp3 = np.array([c3.samples['cosmological_parameters--omega_m'], c3.samples['cosmological_parameters--s8'], c3.samples['intrinsic_alignment_parameters--a']])

samp4 = np.array([c4.samples['cosmological_parameters--omega_m'], c4.samples['cosmological_parameters--s8']]) #, (np.random.rand(len(c4.samples['cosmological_parameters--s8']))-0.5)*8. ])


#import pdb ; pdb.set_trace()
print('Making cornerplot...')
cc = ChainConsumer()

#import pdb ; pdb.set_trace()


names = [r'$\Omega_{\rm m}$','$S_8$','$a_1$']
names2 = [r'$\Omega_{\rm m}$','$S_8$','$A_1$', r'$\eta_1$', '$A_2$', r'$\eta_2$', r'$b_{\rm TA}$']

cc.add_chain(samp0.T, parameters=names, weights=c0.weight, kde=2., name=r'DES Y3')
cc.add_chain(samp1.T, parameters=names, weights=c1['weight'], kde=2., name=r'HSC Y1')
cc.add_chain(samp2.T, parameters=names, weights=c2.weight, kde=2., name=r'DES Y3 optimised')
cc.add_chain(samp3.T, parameters=names, weights=c3.weight, kde=2., name=r'KiDS-1000')

cc.add_chain(samp4.T, parameters=names[:-1], weights=c4.weight, kde=2., name=r'Planck 18')

#7223AD
#A4CD64
#3775A1
#DD9EE8

cc.configure(colors=['#FA86C9', '#228B22','#191970', '#ffc0cb','#7223AD', ],diagonal_tick_labels=False,kde=[2.0, 2.0, 3.0,2.0,2.0],shade=[True,False,False,False,True]*3, shade_alpha=[0.7, 0.05, 0.05,0.05,0.65], legend_kwargs={"loc": "upper right", "fontsize": 16},label_font_size=12,tick_font_size=9)
#cc.configure(colors=['#800080', '#800080', '#FF1493', '#000000' ],shade=[False,True,True,False], shade_alpha=[0.25,0.25,0.25], max_ticks=4, kde=[6]*5, linestyles=["-", "-", '-.', '--'], legend_kwargs={"loc": "upper right", "fontsize": 14},label_font_size=14,tick_font_size=14) 
plt.close() ; 
fig = cc.plotter.plot(extents={'$S_8$':(0.62,0.95),r'$\Omega_{\rm m}$':(0.08,0.55),'$A_1$':(-2.5,3), '$A_2$':(-5.,5), r'$\eta_1$':(-5,5), r'$\eta_2$':(-5,2), r'$b_{\rm TA}$':(0,2)}) #, truth=[0.3,0.82355,0.7,-1.7] )


#plt.suptitle(r'$\Lambda$CDM $1 \times 2\mathrm{pt}$, data=TATT', fontsize=16)
plt.subplots_adjust(bottom=0.175,left=0.175, hspace=0, wspace=0)

print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/1x2pt_external_maglim.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/1x2pt_external_maglim.png')

plt.close()
from getdist import plots, MCSamples
import getdist
import matplotlib.pyplot as plt


g = plots.get_subplot_plotter() #(width_inch=6, ratio=1)
g.settings.legend_fontsize = 18
g.settings.fontsize = 18
g.settings.axes_fontsize = 18
g.settings.axes_labelsize = 22
g.settings.axis_tick_max_labels = 15
g.settings.linewidth = 1.5
g.settings.legend_colored_text=True
g.settings.axis_tick_step_groups = [[2.5, 3, 4, 6, 8],[1, 2, 5, 10]]


samples = MCSamples(samples=samp0.T,names=['x1','x2','x3'], labels=names, label='DES Y3', weights=c0.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples2 =MCSamples(samples=samp1.T,names=['x1','x2','x3'], labels=names, label='HSC Y1', weights=c1['weight'], settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples3 = MCSamples(samples=samp2.T,names=['x1','x2','x3'], labels=names, label='DES Y3 optimised', weights=c2.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples4 =MCSamples(samples=samp3.T,names=['x1','x2','x3'], labels=names, label='KiDS-1000', weights=c3.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples5 = MCSamples(samples=samp4.T,names=['x1','x2'], labels=names[:-1], label='Planck 18 TT+TE+EE', weights=c4.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})


#7223AD
#A4CD64
#3775A1
#DD9EE8
g.triangle_plot([samples, samples3, samples2, samples4, samples5],['x1','x2','x3'], diag1d_kwargs={'normalized':True}, contour_args=[{'alpha':0.6},{'alpha':1},{'alpha':1.},{'alpha':1.},{'alpha':0.6}], filled=[True,False,False,False,True], contour_colors=['#7223AD','#FF69B4','#3775A1','#191970','#A4CD64' ], labels=['DES Y3', 'HSC Y1', 'DES Y1', 'KiDS-1000', 'Planck 18'], param_limits={'x1':(0.05,0.48), 'x2':(0.65,0.9), 'x3':(-2,3.5)}) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])
#import pdb ; pdb.set_trace()

s8_ticks = [0.65,0.75,0.85]
omm_ticks = [0.1,0.2,0.3,0.4]
a1_ticks = [-1,0,1,2,3]

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
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/1x2pt_external_getdist_maglim_v2.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/1x2pt_external_getdist_maglim_v2.png')

