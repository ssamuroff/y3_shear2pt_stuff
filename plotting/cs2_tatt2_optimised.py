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
c1 = mc.chain(base+'/final_paper_chains/chain_1x2pt_lcdm_noSR_maglim_optimized.txt')
c2 = mc.chain(base+'/final_paper_chains/chain_1x2pt_nla_lcdm_noSR_maglim_optimized.txt')


c1.add_s8()
c2.add_s8()



#'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'

samp1 = np.array([c1.samples['cosmological_parameters--omega_m'], c1.samples['cosmological_parameters--s8'], c1.samples['intrinsic_alignment_parameters--a1'], c1.samples['intrinsic_alignment_parameters--a2']])
samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8'], c2.samples['intrinsic_alignment_parameters--a1']])

#import pdb ; pdb.set_trace()
print('Making cornerplot...')
cc = ChainConsumer()

#import pdb ; pdb.set_trace()


names = [r'$\Omega_{\rm m}$','$S_8$', r'$a_1$', r'$a_2$']
names2 = [r'$\Omega_{\rm m}$','$S_8$', r'$A_1$']


cc.add_chain(samp1.T, parameters=names, weights=c1.weight, kde=2., name=r'TATT')
cc.add_chain(samp2.T, parameters=names2, weights=c2.weight, kde=2., name=r'NLA')


cc.configure(colors=['#DDA0DD','#191970', '#FA86C9','#7223AD',],shade=[True,False,False]*3, shade_alpha=[0.65, 0.55, 0.1,0.5],legend_kwargs={"loc": "upper right", "fontsize": 25},label_font_size=18,tick_font_size=14)
#cc.configure(colors=['#800080', '#800080', '#FF1493', '#000000' ],shade=[False,True,True,False], shade_alpha=[0.25,0.25,0.25], max_ticks=4, kde=[6]*5, linestyles=["-", "-", '-.', '--'], legend_kwargs={"loc": "upper right", "fontsize": 14},label_font_size=14,tick_font_size=14) 
plt.close() ; 
fig = cc.plotter.plot(extents={'$S_8$':(0.69,0.85),r'$\sigma_8$':(0.6,0.95),r'$\Omega_{\rm m}$':(0.14,0.5),'$A_1$':(-1.4,2), '$A_2$':(-2.,4), r'$\eta_1$':(-5,5), r'$\eta_2$':(-5,5), r'$b_{\rm TA}$':(0,2)}) #, truth=[0.3,0.82355,0.7,-1.7] )


plt.suptitle(r'$\Lambda$CDM', fontsize=22)
plt.subplots_adjust(bottom=0.155,left=0.155, top=0.98,right=0.98,hspace=0, wspace=0)

print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/unblinded_y3cs_tatt_v2_optimised.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/unblinded_y3cs_tatt_v2_optimised.png')


#exit()

#
#base = '/Volumes/groke/work/chains/y3/real/'
##c1 = mc.chain(base+'fiducial/chain_1x2pt_hyperrank_2pt_NG_BLINDED_v0.40cov_xcorrGGL_27072020_SOMPZWZsamples_pit.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
#c1 = mc.chain(base+'chain_3x2pt_lcdm.txt')
#c2 = mc.chain(base+'robustnesstests/chain_3x2pt_nla.txt')
##mc.chain('/Volumes/groke/work/chains/y1/blazek/eta/TATT/all/out_all-1x2pt-NG-TATT-alpha-v3.txt')
#
#
#c1.add_s8()
#c2.add_s8()
#
#
#
##'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'
#
#samp1 = np.array([c1.samples['cosmological_parameters--omega_m'], c1.samples['cosmological_parameters--s8'], c1.samples['intrinsic_alignment_parameters--a1'], c1.samples['intrinsic_alignment_parameters--a2']])
#samp2 = np.array([c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8'], c2.samples['intrinsic_alignment_parameters--a1']])
#
#
#
##import pdb ; pdb.set_trace()
#print('Making cornerplot...')
#cc = ChainConsumer()
#
##import pdb ; pdb.set_trace()
#
#
#names = [r'$\Omega_{\rm m}$','$S_8$', r'$A_1$', r'$A_2$']
#names2 = [r'$\Omega_{\rm m}$','$S_8$', r'$A_1$']
#
#
#cc.add_chain(samp1.T, parameters=names, weights=c1.weight, kde=2., name=r'TATT')
#cc.add_chain(samp2.T, parameters=names2, weights=c2.weight, kde=2., name=r'NLA')
#
#cc.configure(colors=['#DDA0DD','#191970', '#FA86C9','#7223AD',],shade=[True,False,True]*3, shade_alpha=[0.65, 0.55, 0.1,0.5], kde=[2]*3,legend_kwargs={"loc": "upper right", "fontsize": 28},label_font_size=22,tick_font_size=14)
##cc.configure(colors=['#800080', '#800080', '#FF1493', '#000000' ],shade=[False,True,True,False], shade_alpha=[0.25,0.25,0.25], max_ticks=4, kde=[6]*5, linestyles=["-", "-", '-.', '--'], legend_kwargs={"loc": "upper right", "fontsize": 14},label_font_size=14,tick_font_size=14) 
#plt.close() ; 
#fig = cc.plotter.plot(extents={'$S_8$':(0.69,0.85),r'$\sigma_8$':(0.6,0.95),r'$\Omega_{\rm m}$':(0.14,0.5),'$A_1$':(-1.4,2), '$A_2$':(-2.,4), r'$\eta_1$':(-5,5), r'$\eta_2$':(-5,5), r'$b_{\rm TA}$':(0,2)}) #, truth=[0.3,0.82355,0.7,-1.7] )
#
#
#plt.suptitle(r'$\Lambda$CDM', fontsize=22)
#plt.subplots_adjust(bottom=0.155,left=0.155, top=0.98,right=0.98,hspace=0, wspace=0)
#
#print('Saving...')
#plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/unblinded_y33x2pt_tatt_v2.pdf')
#plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/unblinded_y33x2pt_tatt_v2.png')
#
#


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

#7223AD
#A4CD64
#3775A1
#DD9EE8
colours = ['#7223AD','#000000','#FFC0CB','#3775A1','#A4CD64','#3775A1']


samples = MCSamples(samples=samp1.T,names=['x1','x2','x3','x4'], labels=names, label='TATT', weights=c1.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})
samples2 = MCSamples(samples=samp2.T,names=['x1','x2','x3'], labels=names[:-1], label='NLA', weights=c2.weight, settings={'boundary_correction_order':0, 'mult_bias_correction_order':1})



g.triangle_plot([samples, samples2],['x1','x2','x3','x4'], filled=[True,False,True,False,False,True], contour_args=[{'alpha':0.6},{'alpha':1.,'ls':'--'},{'alpha':0.6},{'alpha':1.}], diag1d_kwargs={'normalized':True}, contour_colors=colours, labels=['TATT', 'NLA', 'NLA (no $z$)'], param_limits={'x1':(0.18,0.51), 'x2':(0.69,0.85), 'x3':(-1.8,2),'x4':(-2.5,4.5)}) #, markers=[[0.15,0.3,0.45], [0.6,0.7,0.8,0.9], [-2,-1,0,1,2,3]])
#import pdb ; pdb.set_trace()

s8_ticks = [0.7,0.75,0.8,0.85]
omm_ticks = [0.2,0.3,0.4]
a1_ticks = [-0.8,0,0.8,1.6]
a2_ticks = [-1.5,0.,1.5,3.]

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

g.subplots[3][0].set_xticks(omm_ticks)
g.subplots[3][0].set_yticks(a2_ticks)
g.subplots[3][1].set_xticks(s8_ticks)
g.subplots[3][1].set_yticks(a2_ticks)
g.subplots[3][2].set_xticks(a1_ticks)
g.subplots[3][2].set_yticks(a2_ticks)
g.subplots[3][3].set_xticks(a2_ticks)

#plt.suptitle(r'redMaGiC SR', fontsize=22)
#g.add_legend(['DES Y3','HSC Y1'])
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/unblinded_y3_1x2pt_tatt_v2_getdist_optimised.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/unblinded_y3_1x2pt_tatt_v2_getdist_optimised.png')


