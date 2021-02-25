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

base = '/Volumes/groke/work/chains/y3/real/external/'
#c1 = mc.chain(base+'fiducial/chain_1x2pt_hyperrank_2pt_NG_BLINDED_v0.40cov_xcorrGGL_27072020_SOMPZWZsamples_pit.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt')
c1 = mc.chain(base+'chain_s_b_wcdm.txt')
c2 = mc.chain(base+'chain_p-lensing_wcdm.txt')
c3 = mc.chain(base+'../chain_1x2pt_wcdm.txt')
#c4 = mc.chain(base+'')



c1.add_s8()
c2.add_s8()
c3.add_s8()
#c4.add_s8()



#'out_redmagic_high_mock_baseline-gp1-gg1-pp1-multinest-fidcov-ta-y3fid-6rpmin_200rpmax-rsd1-lens0-mag0-phot1.txt'

samp1 = np.array([c1.samples['cosmological_parameters--w'],c1.samples['cosmological_parameters--omega_m'], c1.samples['cosmological_parameters--s8'], (np.random.rand(len(c1.samples['cosmological_parameters--s8'])) - 0.5) * 10.5, (np.random.rand(len(c1.samples['cosmological_parameters--s8'])) - 0.5) * 10.5])
samp2 = np.array([c2.samples['cosmological_parameters--w'],c2.samples['cosmological_parameters--omega_m'], c2.samples['cosmological_parameters--s8'], (np.random.rand(len(c2.samples['cosmological_parameters--s8'])) - 0.5) * 10.5, (np.random.rand(len(c2.samples['cosmological_parameters--s8'])) - 0.5) * 10.5])
samp3 = np.array([c3.samples['cosmological_parameters--w'],c3.samples['cosmological_parameters--omega_m'], c3.samples['cosmological_parameters--s8'], c3.samples['intrinsic_alignment_parameters--a1'], c3.samples['intrinsic_alignment_parameters--a2']])
#samp4 = np.array([c4.samples['cosmological_parameters--w0'],c4.samples['cosmological_parameters--omega_m'], c4.samples['cosmological_parameters--s8'], c4.samples['intrinsic_alignment_parameters--a1'], c4.samples['intrinsic_alignment_parameters--a2']])




#import pdb ; pdb.set_trace()
print('Making cornerplot...')
cc = ChainConsumer()

#import pdb ; pdb.set_trace()


names = ['$w$',r'$\Omega_{\rm m}$','$S_8$', r'$A_1$', r'$A_2$']


cc.add_chain(samp1.T, parameters=names, weights=c1.weight, kde=True, name=r'Low-z (Pantheon SN + eBOSS BAO)')
#cc.add_chain(samp2.T, parameters=names, weights=c2.weight, kde=True, name=r'Planck 15')
cc.add_chain(samp3.T, parameters=names, weights=c3.weight, kde=True, name=r'DES Y3 $1 \times 2$pt')
#cc.add_chain(samp4.T, parameters=names, weights=c4.weight, kde=True, name=r'')

cc.configure(colors=['#5C1F84', '#F9ACCC','#000000','#4682b4'],shade=[True,True,True,False]*3, shade_alpha=[0.65, 0.65, 0.5,0.5], kde=[2]*4,legend_kwargs={"loc": "upper right", "fontsize": 16},label_font_size=16,tick_font_size=14)
#cc.configure(colors=['#800080', '#800080', '#FF1493', '#000000' ],shade=[False,True,True,False], shade_alpha=[0.25,0.25,0.25], max_ticks=4, kde=[6]*5, linestyles=["-", "-", '-.', '--'], legend_kwargs={"loc": "upper right", "fontsize": 14},label_font_size=14,tick_font_size=14) 
plt.close() ; 
fig = cc.plotter.plot(extents={'$S_8$':(0.65,0.84),r'$\sigma_8$':(0.6,0.95),r'$\Omega_{\rm m}$':(0.18,0.45),'$A_1$':(-1.5,1.8), '$A_2$':(-4.,5), r'$\eta_1$':(-5,5), r'$\eta_2$':(-5,5), r'$b_{\rm TA}$':(0,2)}) #, truth=[0.3,0.82355,0.7,-1.7] )


#plt.suptitle(r'$\Lambda$CDM $1 \times 2\mathrm{pt}$, model=TATT, data=TATT', fontsize=16)
plt.subplots_adjust(bottom=0.155,left=0.155, top=0.98,right=0.98,hspace=0, wspace=0)

print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/external_wcdm.pdf')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/external_wcdm.png')

