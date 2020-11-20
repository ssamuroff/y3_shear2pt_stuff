import numpy as np
import tools.emcee as mc
from chainconsumer import ChainConsumer
import sys

make_plot = False
nla_only =True
#zmean = [0.38,0.52,0.74,0.96]

zmean = [0.33743060204439729,0.52566351194711403,0.74482301410314122,0.93292117984817646]

def derive_eff_A(chain,z0,suffix):
    alpha = chain.samples['intrinsic_alignment_parameters--alpha%d'%suffix]
    A0 = chain.samples['intrinsic_alignment_parameters--a%d'%suffix]
    A = A0 * ((z0+1)/(1.62))**alpha
    return A

input_name = sys.argv[1]
chain = mc.chain(input_name)

for i,z0 in enumerate(zmean):
	print(i,z0)
	A1 = derive_eff_A(chain,z0,1)
	if not nla_only:
		A2 = derive_eff_A(chain,z0,2)

	chain.add_external_column(A1,'aeff1_%d'%(i+1), cosmosis_section='intrinsic_alignment_parameters')
	if not nla_only:
		chain.add_external_column(A2,'aeff2_%d'%(i+1), cosmosis_section='intrinsic_alignment_parameters')


output_name = input_name.replace('.txt','_IAeff.txt')
chain.write_columns(output_name)



if not make_plot:
	exit()

import pylab as plt
plt.switch_backend('pdf')
plt.style.use('y1a1')

from matplotlib import rcParams
rcParams['xtick.major.size'] = 3.5
rcParams['xtick.minor.size'] = 1.7
rcParams['ytick.major.size'] = 3.5
rcParams['ytick.minor.size'] = 1.7
rcParams['xtick.direction']='in'
rcParams['ytick.direction']='in'

names = [r'$A^1_{1}$',r'$A^2_{1}$',r'$A^3_{1}$',r'$A^4_{1}$', r'$A^1_{2}$',r'$A^2_{2}$',r'$A^3_{2}$',r'$A^4_{2}$']
samp1 = np.array([ chain.samples['intrinsic_alignment_parameters--aeff1_1'],chain.samples['intrinsic_alignment_parameters--aeff1_2'],chain.samples['intrinsic_alignment_parameters--aeff1_3'],chain.samples['intrinsic_alignment_parameters--aeff1_4'], chain.samples['intrinsic_alignment_parameters--aeff2_1'],chain.samples['intrinsic_alignment_parameters--aeff2_2'],chain.samples['intrinsic_alignment_parameters--aeff2_3'],chain.samples['intrinsic_alignment_parameters--aeff2_4']])
#import pdb ; pdb.set_trace()
print('Making cornerplot...')
cc = ChainConsumer()


cc.add_chain(samp1.T, parameters=names, weights=chain.weight, kde=True)

cc.configure(colors=['#DDA0DD', '#FA86C9','#7223AD',],shade=[True,True,True]*3, shade_alpha=[0.65, 0.55, 0.1,0.5], kde=[2]*3,legend_kwargs={"loc": "upper right", "fontsize": 12},label_font_size=12,tick_font_size=12)
plt.close() ; 
fig = cc.plotter.plot(extents={r'$A^1_{1}$':(-3.,3.), r'$A^2_{1}$':(-3.,3.), r'$A^3_{1}$':(-3.,3.), r'$A^4_{1}$':(-3.,3.), r'$A^1_{2}$':(-5.,0.), r'$A^2_{2}$':(-5.,0.), r'$A^3_{2}$':(-5.,0.), r'$A^4_{2}$':(-5.,0.)}) #, truth=[0.3,0.82355,0.7,-1.7] )

plt.subplots_adjust(bottom=0.155,left=0.155, top=0.98,right=0.98,hspace=0, wspace=0)

print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/cs2/iaeff_test.png')

  