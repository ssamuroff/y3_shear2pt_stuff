 
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
c7 = np.genfromtxt(base+'/external/lensing/HSC_hamana2020_fiducial/hsc_hamana2020_fiducial.txt').T

c2 = mc.chain('/Volumes/groke/work/chains/y3/real/final_paper_chains/chain_1x2agg_ML.txt')
c5 = mc.chain('/Volumes/groke/work/chains/y1/fiducial/all/out_all-1x2pt-NG.txt')
c3 = mc.chain('/Volumes/groke/work/other_peoples_datasets/kids1000/KiDS1000_Cosebis_output_multinest_C.txt')
base = '/Volumes/groke/work/chains/y3/real/'
c4 = mc.chain(base+'external/chain_p-TTTEEE-lowE_lcdm.txt')

c6 = mc.chain('/Volumes/groke/work/chains/y3/real/final_paper_chains/tests_1x2pt/maglim/chain_NLA_1x2pt_lcdm_maglim.txt')




#c1 = mc.chain('chain_1x2pt_fiducial_test_0.40_CLASS_NLA_C1_GAMA_twopoint_new.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c0.add_s8()
c2.add_s8()
s8_1 = c1['COSMOLOGICAL_PARAMETERSSIGMA_8'] * np.sqrt(c1['cosmological_parametersomega_m']/0.3) 
c4.add_s8()
c3.add_s8()
c5.add_s8()
c6.add_s8()
s8_7 = c7[18]

c5 = mc.chain('/Volumes/groke/work/chains/y3/real/final_paper_chains/chain_1x2pt_lcdm_noSR_maglim_optimized.txt')
c5.add_s8()

samp0 = np.array([c0.samples['cosmological_parameters--omega_m'], c0.samples['cosmological_parameters--s8'] ])
samp1 = np.array([c1['cosmological_parametersomega_m'], s8_1])
samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8'] ])
samp3 = np.array([c3.samples['cosmological_parameters--omega_m'], c3.samples['cosmological_parameters--s8']])

samp4 = np.array([c4.samples['cosmological_parameters--omega_m'], c4.samples['cosmological_parameters--s8']]) #, (np.random.rand(len(c4.samples['cosmological_parameters--s8']))-0.5)*8. ])

samp5 = np.array([c5.samples['cosmological_parameters--omega_m'], c5.samples['cosmological_parameters--s8']])
samp7 = np.array([c7[16],s8_7])

#import pdb ; pdb.set_trace()
print('Making cornerplot...')

#import pdb ; pdb.set_trace()

names0 = [r'$\Omega_{\rm m}$','$S_8$']
names = [r'$S_8$','$a_1$']
names2 = [r'$\Omega_{\rm m}$','$S_8$','$A_1$', r'$\eta_1$', '$A_2$', r'$\eta_2$', r'$b_{\rm TA}$']


plt.close()
from getdist import plots, MCSamples
import getdist
import matplotlib.pyplot as plt


#g = plots.get_subplot_plotter() #(width_inch=6, ratio=1)
g = plots.get_single_plotter(width_inch=6, ratio=0.8)
g.settings.legend_fontsize = 9
g.settings.fontsize = 16
g.settings.axes_fontsize = 16
g.settings.axes_labelsize = 16
g.settings.axis_tick_max_labels = 16
g.settings.linewidth = 1.5
g.settings.legend_colored_text=False
g.settings.axis_tick_step_groups = [[2.5, 3, 4, 6, 8],[1, 2, 5, 10]]


samples = MCSamples(samples=samp0.T,names=['x1','x2'], labels=names0, label='DES Y3', weights=c0.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples2 =MCSamples(samples=samp1.T,names=['x1','x2'], labels=names0, label='HSC (Hikage et al))', weights=c1['weight'], settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples3 = MCSamples(samples=samp2.T,names=['x1','x2'], labels=names0, label='DES Y3 optimized', weights=c2.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples4 =MCSamples(samples=samp3.T,names=['x1','x2'], labels=names0, label='KiDS-1000', weights=c3.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples5 = MCSamples(samples=samp4.T,names=['x1','x2'], labels=names0, label='Planck 18 TT+TE+EE+lowE', weights=c4.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples6 = MCSamples(samples=samp5.T,names=['x1','x2'], labels=names0, label='DES Y3', weights=c5.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})

samples7 = MCSamples(samples=samp7.T,names=['x1','x2'], labels=names0, label='HSC (Hamana et al)', weights=c7[0], settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})

hsc_colour = '#3775A1'

#7223AD
#A4CD64
#3775A1
#DD9EE8
#g.triangle_plot([samples, samples3, samples2, samples4, samples5],['x1','x2'], diag1d_kwargs={'normalized':True}, contour_args=[{'alpha':0.6},{'alpha':1,'ls':'--'},{'alpha':1.},{'alpha':1.},{'alpha':0.6}], filled=[True,False,False,False,True], contour_colors=['#7223AD','#000000','#3775A1','#FF69B4','#A4CD64' ], labels=['DES Y3', 'HSC Y1', 'DES Y1', 'KiDS-1000', 'Planck 18'], param_limits={'x1':(0.05,0.48), 'x2':(0.65,0.9), 'x3':(-2,3.5)}) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])

g.plot_2d([samples, samples3, samples6,samples2, samples7, samples4, samples5],['x1','x2'], diag1d_kwargs={'normalized':True}, alphas=[0.6,1,1.,1,1.,0.6], ls=['-','--','-','-.',':','-','-'],lws=[1.5]*8,filled=[True,False,False,False,False,False,True], colors=['#7223AD','#000000','darkmagenta','#3775A1',hsc_colour,'#FF69B4','#A4CD64' ], labels=['DES Y3', 'HSC Y1', 'DES Y1', 'KiDS-1000', 'Planck 18'], lims=[0.05,0.65,0.66,0.93]) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])
#import pdb ; pdb.set_trace()

s8_ticks = [0.65,0.75,0.85]
omm_ticks = [0.1,0.2,0.3,0.4]
a1_ticks = [-1,0,1,2,3]

# ticks...
#g.subplots[0][0].set_xticks(omm_ticks)
#g.subplots[1][0].set_xticks(omm_ticks)
#g.subplots[1][0].set_yticks(s8_ticks)
#g.subplots[1][1].set_xticks(s8_ticks)

g.add_legend(['DES Y3','DES Y3 optimized','DES Y3 optimized, no SR',r'HSC $C_\ell$',r'HSC $\xi_\pm$','KiDS-1000','Planck 18 TT+TE+EE+lowE'])
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/1x2pt_external_getdist_maglim_v2_s8omm_withhamana.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/1x2pt_external_getdist_maglim_v2_s8omm_withhamana.png')

c5 = mc.chain('/Volumes/groke/work/chains/y3/real/final_paper_chains/chain_1x2pt_lcdm_noSR_maglim_optimized.txt')
c5.add_s8()

samp0 = np.array([c0.samples['cosmological_parameters--s8'], c0.samples['intrinsic_alignment_parameters--a1'] ])
samp1 = np.array([s8_1, c1['intrinsic_alignment_parametersa1']])
samp2 = np.array([c2.samples['cosmological_parameters--s8'], c2.samples['intrinsic_alignment_parameters--a1'] ])
samp3 = np.array([c3.samples['cosmological_parameters--s8'], c3.samples['intrinsic_alignment_parameters--a']])

samp5 = np.array([c5.samples['cosmological_parameters--s8'], c5.samples['intrinsic_alignment_parameters--a1']])

samp6 = np.array([c6.samples['cosmological_parameters--s8'], c6.samples['intrinsic_alignment_parameters--a1']])

samp4 = np.array([c4.samples['cosmological_parameters--s8']]) #, (np.random.rand(len(c4.samples['cosmological_parameters--s8']))-0.5)*8. ])

samp7 = np.array([s8_7,c7[7]])

plt.close()
from getdist import plots, MCSamples
import getdist
import matplotlib.pyplot as plt


#g = plots.get_subplot_plotter() #(width_inch=6, ratio=1)
g = plots.get_single_plotter(width_inch=6, ratio=0.8)
g.settings.legend_fontsize = 9
g.settings.fontsize = 16
g.settings.axes_fontsize = 16
g.settings.axes_labelsize = 16
g.settings.axis_tick_max_labels = 16
g.settings.linewidth = 1.5
g.settings.legend_colored_text=False
g.settings.axis_tick_step_groups = [[2.5, 3, 4, 6, 8],[1, 2, 5, 10]]


samples = MCSamples(samples=samp0.T,names=['x1','x2'], labels=names, label='DES Y3', weights=c0.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples2 =MCSamples(samples=samp1.T,names=['x1','x2'], labels=names, label='HSC (Hikage et al))', weights=c1['weight'], settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples3 = MCSamples(samples=samp2.T,names=['x1','x2'], labels=names, label='DES Y3 optimized', weights=c2.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples4 =MCSamples(samples=samp3.T,names=['x1','x2'], labels=names, label='KiDS-1000', weights=c3.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples5 = MCSamples(samples=samp5.T,names=['x1','x2'], labels=names, label='DES Y1 (NLA)', weights=c5.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples6 = MCSamples(samples=samp6.T,names=['x1','x2'], labels=names, label='DES Y3 (NLA)', weights=c6.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples7 = MCSamples(samples=samp7.T,names=['x1','x2'], labels=names, label='HSC (Hamana et al)', weights=c7[0], settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})


#7223AD
#A4CD64
#3775A1
#DD9EE8
#g.triangle_plot([samples, samples3, samples2, samples4, samples5],['x1','x2'], diag1d_kwargs={'normalized':True}, contour_args=[{'alpha':0.6},{'alpha':1,'ls':'--'},{'alpha':1.},{'alpha':1.},{'alpha':0.6}], filled=[True,False,False,False,True], contour_colors=['#7223AD','#000000','#3775A1','#FF69B4','#A4CD64' ], labels=['DES Y3', 'HSC Y1', 'DES Y1', 'KiDS-1000', 'Planck 18'], param_limits={'x1':(0.05,0.48), 'x2':(0.65,0.9), 'x3':(-2,3.5)}) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])

g.plot_2d([samples, samples3, samples5, samples6, samples2, samples7, samples4],['x1','x2'], diag1d_kwargs={'normalized':True}, alphas=[0.6,1,1.,1,1.,1.,1.], ls=['-','--','-','-','-.',':','-'],lws=[1.5]*8,filled=[True,False,False,False,False,False,False], colors=['#7223AD','#000000','darkmagenta','pink','#3775A1','#3775A1','#FF69B4' ], labels=['DES Y3', 'HSC Y1', 'DES Y1', 'KiDS-1000', 'Planck 18'], lims=[0.62,0.87,-2,2.6,]) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])
#import pdb ; pdb.set_trace()

s8_ticks = [0.65,0.75,0.85]
omm_ticks = [0.1,0.2,0.3,0.4]
a1_ticks = [-1,0,1,2,3]

# ticks...
#g.subplots[0][0].set_xticks(omm_ticks)
#g.subplots[1][0].set_xticks(omm_ticks)
#g.subplots[1][0].set_yticks(s8_ticks)
#g.subplots[1][1].set_xticks(s8_ticks)

g.add_legend(['DES Y3 (TATT)','DES Y3 optimized (TATT)','DES Y3 optimized, no SR (TATT)','DES Y3 (NLA)',r'HSC $C_\ell$ (NLA)', r'HSC $\xi_\pm$ (NLA)', 'KiDS-1000 (NLA no-$z$)'],legend_loc='upper left')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/1x2pt_external_getdist_maglim_v2_a1s8_withhamana.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/1x2pt_external_getdist_maglim_v2_a1s8_withhamana.png')
