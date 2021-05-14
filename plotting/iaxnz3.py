import numpy as np
import os
import pylab as plt
plt.switch_backend('pdf')
plt.style.use('y1a1')
from matplotlib import rcParams

import tools.emcee as mc
from chainconsumer import ChainConsumer

rcParams['xtick.major.size'] = 1.5
rcParams['xtick.minor.size'] = 0.85
rcParams['ytick.major.size'] = 1.5
rcParams['ytick.minor.size'] = 0.85
rcParams['xtick.direction']='in'
rcParams['ytick.direction']='in'
#rcParams['text.usetex']=False

print('Loading chains...')

base = '/Users/hattifattener/Documents/y3cosmicshear/chains/cs2/iaxnz_test/'
#c1 = mc.chain(base+'fiducial/chain_1x2pt_hyperrank_2pt_NG_BLINDED_v0.40cov_xcorrGGL_27072020_SOMPZWZsamples_pit.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c1 = mc.chain(base+'chain_1x2pt_fiducial_sim_2pt_NG_BLINDED_v0.40cov_xcorrGGL27072020_1000samples_055ramp_all_2609_meanzisreal10.fits_sim_noiseless.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c2 = mc.chain(base+'chain_1x2pt_fiducial_v0.40_noiseless_104.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c3 = mc.chain(base+'chain_1x2pt_fiducial_v0.40_noiseless_788.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c4 = mc.chain(base+'chain_1x2pt_fiducial_v0.40_noiseless_328.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')


c1.add_s8()
c2.add_s8()
c3.add_s8()
c4.add_s8()



#'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'

samp1 = np.array([c1.samples['cosmological_parameters--omega_m'], c1.samples['cosmological_parameters--s8'], c1.samples['intrinsic_alignment_parameters--a1'], c1.samples['intrinsic_alignment_parameters--a2'],c1.samples['intrinsic_alignment_parameters--alpha1'],c1.samples['intrinsic_alignment_parameters--alpha2'],c1.samples['intrinsic_alignment_parameters--bias_ta']])
samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8'], c2.samples['intrinsic_alignment_parameters--a1'], c2.samples['intrinsic_alignment_parameters--a2'],c2.samples['intrinsic_alignment_parameters--alpha1'],c2.samples['intrinsic_alignment_parameters--alpha2'],c2.samples['intrinsic_alignment_parameters--bias_ta']])
samp3 = np.array([c3.samples['cosmological_parameters--omega_m'], c3.samples['cosmological_parameters--s8'], c3.samples['intrinsic_alignment_parameters--a1'], c3.samples['intrinsic_alignment_parameters--a2'],c3.samples['intrinsic_alignment_parameters--alpha1'],c3.samples['intrinsic_alignment_parameters--alpha2'],c3.samples['intrinsic_alignment_parameters--bias_ta']])
samp4 = np.array([c4.samples['cosmological_parameters--omega_m'], c4.samples['cosmological_parameters--s8'], c4.samples['intrinsic_alignment_parameters--a1'], c4.samples['intrinsic_alignment_parameters--a2'],c4.samples['intrinsic_alignment_parameters--alpha1'],c4.samples['intrinsic_alignment_parameters--alpha2'],c4.samples['intrinsic_alignment_parameters--bias_ta']])




#import pdb ; pdb.set_trace()
print('Making cornerplot...')
cc = ChainConsumer()

#import pdb ; pdb.set_trace()


names = [r'$\Omega_{\rm m}$','$S_8$', r'$a_1$', r'$a_2$', r'$\eta_1$', r'$\eta_2$', r'$b_{\rm TA}$']


cc.add_chain(samp1.T, parameters=names, weights=c1.weight, kde=True, name=r'True $n(z)$, $\Delta \chi^2 = 0.0$')
cc.add_chain(samp2.T, parameters=names, weights=c2.weight, kde=True, name=r'wrong $n(z)$, $\Delta \chi^2 = 3.0$ ')
cc.add_chain(samp3.T, parameters=names, weights=c3.weight, kde=True, name=r'wrong $n(z)$, $\Delta \chi^2 = 7.0$')
cc.add_chain(samp4.T, parameters=names, weights=c4.weight, kde=True, name=r'wrong $n(z)$, $\Delta \chi^2 = 14$')

cc.configure(colors=['#DDA0DD', '#FA86C9','#000000','#4682b4'],shade=[True,False,False,False]*3, shade_alpha=[0.65, 0.55, 0.5,0.5], kde=[2]*4,legend_kwargs={"loc": "upper right", "fontsize": 22},label_font_size=22,tick_font_size=14)
#cc.configure(colors=['#800080', '#800080', '#FF1493', '#000000' ],shade=[False,True,True,False], shade_alpha=[0.25,0.25,0.25], max_ticks=4, kde=[6]*5, linestyles=["-", "-", '-.', '--'], legend_kwargs={"loc": "upper right", "fontsize": 14},label_font_size=14,tick_font_size=14) 
plt.close() ; 
fig = cc.plotter.plot(extents={'$S_8$':(0.75,0.92),r'$\sigma_8$':(0.6,0.95),r'$\Omega_{\rm m}$':(0.18,0.45),'$A_1$':(-1.,1.8), '$A_2$':(-4.,0.5), r'$\eta_1$':(-5,5), r'$\eta_2$':(-5,5), r'$b_{\rm TA}$':(0,2)}) #, truth=[0.3,0.82355,0.7,-1.7] )


plt.suptitle(r'$\Lambda$CDM $1 \times 2\mathrm{pt}$, model=TATT, data=TATT', fontsize=16)
plt.subplots_adjust(bottom=0.155,left=0.155, top=0.98,right=0.98,hspace=0, wspace=0)

print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/y3_tatt_iaxnz_v2.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/y3_tatt_iaxnz_v2.png')







plt.close()
from getdist import plots, MCSamples
import getdist

samples1 = MCSamples(samples=samp1.T,names=['x1','x2','x3','x4','x5','x6','x7'], labels=names, label=r'True $n(z)$, $\Delta \chi^2 = 0.0$', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples2 = MCSamples(samples=samp2.T,names=['x1','x2','x3','x4','x5','x6','x7'], labels=names, label=r'wrong $n(z)$, $\Delta \chi^2 = 3.0$ ', weights=c2.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples3 = MCSamples(samples=samp3.T,names=['x1','x2','x3','x4','x5','x6','x7'], labels=names, label=r'wrong $n(z)$, $\Delta \chi^2 = 7.0$', weights=c3.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples4 = MCSamples(samples=samp4.T,names=['x1','x2','x3','x4','x5','x6','x7'], labels=names, label=r'wrong $n(z)$, $\Delta \chi^2 = 14$', weights=c4.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})

gd = plots.get_single_plotter(width_inch=6, ratio=1)
gd.settings.legend_fontsize = 16
gd.settings.fontsize = 18
gd.settings.axes_fontsize = 16
gd.settings.axes_labelsize = 20
gd.settings.axis_tick_max_labels = 15
gd.settings.linewidth = 1.5
gd.settings.legend_colored_text=True
gd.settings.axis_tick_step_groups = [[2.5, 3, 4, 6, 8],[1, 2, 5, 10]]


col0 = ['#DDA0DD', '#FA86C9','#000000','#4682b4']
#['#8B0000','#8b008b','#191970','#FF69B4','#000000']
gd.triangle_plot([samples1, samples2, samples3, samples4],['x1','x2','x3','x4','x5','x6','x7'], filled=[True,False,False,False,False,False], contour_args=[{'alpha':0.6},{'alpha':1.},{'alpha':1.},{'alpha':1.}, {'alpha':1}, {'alpha':1}],contour_colors=['#7223AD','#3775A1','#A4CD64','#FF69B4','#A4CD64']) #, param_limits={'x1':(-2.5,5), 'x2':(-5,5), 'x3':(-5,5)})
#gd.plot_2d([samples1, samples2,samples3,samples4,samples5],['x1','x2'], filled=[True,True,True,True,False], colors=['#8B0000','#8b008b','#4682b4','#FF69B4','#000000' ], lims=[-1.5,4.5,-5.5,4])
#gd.add_legend(['redMaGiC high-$z$','redMaGiC low-$z$','eBOSS ELGs','eBOSS LRGs','DES Y3'], legend_loc='lower right');
a1_ticks = [-2,0,2,4]
a2_ticks = [-4,-2,0,2,4]
bta_ticks = [-4,-2,0,2,4]
#
## ticks...
#gd.subplots[0][0].set_xticks(a1_ticks)
#gd.subplots[1][0].set_xticks(a1_ticks)
#gd.subplots[1][0].set_yticks(a2_ticks)
#gd.subplots[2][0].set_xticks(a1_ticks)
#gd.subplots[2][0].set_yticks(bta_ticks)
#gd.subplots[2][1].set_xticks(a2_ticks)
#gd.subplots[2][1].set_yticks(bta_ticks)
#gd.subplots[2][2].set_xticks(bta_ticks)

#cc.add_chain(samp_rh.T, parameters=names2, weights=rh.weight, kde=True, name='redMaGiC high-$z$')
#cc.add_chain(samp_rl.T, parameters=names2, weights=rl.weight, kde=True, name='redMaGiC low-$z$')
#cc.add_chain(samp_ee.T, parameters=names2, weights=ee.weight, kde=True, name='eBOSS ELGs')
#cc.add_chain(samp_el.T, parameters=names2, weights=el.weight, kde=True, name='eBOSS LRGs')


#cc.configure(colors=['#8B0000','#8b008b','#4682b4','#FF69B4','#ffc0cb' ],shade=[True]*4, shade_alpha=[0.75, 0.5,0.5,0.2], legend_kwargs={"loc": "upper right", "fontsize": 12},label_font_size=12,tick_font_size=12)
#cc.configure(colors=['#800080', '#800080', '#FF1493', '#000000' ],shade=[False,True,True,False], shade_alpha=[0.25,0.25,0.25], max_ticks=4, kde=[6]*5, linestyles=["-", "-", '-.', '--'], legend_kwargs={"loc": "upper right", "fontsize": 14},label_font_size=14,tick_font_size=14) 
#plt.close() ; 
#fig = cc.plotter.plot(extents={'$A_1$':(-2,3.5), '$A_2$':(-5,6), '$b_g$':(1.2,2.), r'$b_{\rm TA}$':(-2.,3.5)} )


#fig.suptitle('TATT', fontsize=16)
#plt.suptitle(r'$\Lambda$CDM $1 \times 2\mathrm{pt}$, model=TATT, data=TATT', fontsize=16)
plt.subplots_adjust(bottom=0.155,left=0.155, hspace=0, wspace=0,top=0.88)
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/y3_tatt_iaxnz_v3_getdist.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/y3_tatt_iaxnz_v3_getdist.png')
