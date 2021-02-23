import numpy as np
import os
import sys
import astropy.table as tb
import pylab as plt
plt.switch_backend('pdf')
plt.style.use('y1a1')
from matplotlib import rcParams

import tools.emcee as mc

base="/Volumes//groke/work/chains/y3/real/ia_testing/"

models = {}

def get_bic(chain):
	chi2 = chain.samples['data_vector--2pt_chi2'].min() # min chi2
	k = chain.npar # no of free parameters
	npts = 227 # apparently
#	import pdb ; pdb.set_trace()

	return k * np.log10(npts) + chi2


def show_result(name,m):
	print('%s: %3.3f - %3.3f = %3.3f'%(name,m['TATT'],m[name],m['TATT']-m[name]))


models['noIA'] = get_bic(mc.chain(base+'/../chain_noia_1x2pt_lcdm.txt'))
models['NLA_noz'] = get_bic(mc.chain(base+'/chain_NLA_noz_1x2pt_lcdm.txt'))
models['NLA'] = get_bic(mc.chain(base+'/chain_NLA_1x2pt_lcdm.txt'))
models['TA'] = get_bic(mc.chain(base+'/chain_TA_1x2pt_lcdm.txt'))
models['TATT_noz'] = get_bic(mc.chain(base+'/chain_TATT_noz_1x2pt_lcdm.txt'))
models['TATT'] = get_bic(mc.chain(base+'../chain_1x2pt_lcdm.txt'))


show_result('noIA',models)
show_result('NLA_noz',models)
show_result('NLA',models)
show_result('TA',models)
show_result('TATT_noz',models)
