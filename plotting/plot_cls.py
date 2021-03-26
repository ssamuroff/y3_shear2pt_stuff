import numpy as np
import sys
import os
import pylab as plt
plt.switch_backend('pdf')
plt.style.use('y1a1')
from astropy.cosmology import Planck15
import fitsio as fi
from scipy.optimize import curve_fit

from matplotlib import rcParams

fillcol='plum'

rcParams['xtick.major.size'] = 3.5
rcParams['xtick.minor.size'] = 1.7
rcParams['ytick.major.size'] = 3.5
rcParams['ytick.minor.size'] = 1.7
rcParams['xtick.direction']='in'
rcParams['ytick.direction']='in'

fontsize=14

base = sys.argv[1]
name = os.path.basename(base)
i,j = 1,1

x = np.loadtxt('%s/shear_cl_gg/ell.txt'%base)
C_GG = np.loadtxt('%s/shear_cl_gg/bin_%d_%d.txt'%(base,i,j))
C_GI = np.loadtxt('%s/shear_cl_gi/bin_%d_%d.txt'%(base,i,j))
C_II = np.loadtxt('%s/shear_cl_ii/bin_%d_%d.txt'%(base,i,j))

#import pdb ; pdb.set_trace()
#plt.subplot(111)


plt.plot(x,x*x*C_GG, color='steelblue', ls='-', label='GG')
plt.plot(x,x*x*C_GI, color='darkmagenta', ls='-', label='GI')
plt.plot(x,-x*x*C_GI, color='darkmagenta', ls='--')
plt.plot(x,x*x*C_II, color='plum', ls='-', label='II')
plt.ylabel(r'$\ell^2 C(\ell)$', fontsize=16)
plt.xlabel(r'$\ell$', fontsize=16)
plt.legend(fontsize=16)
plt.yscale('log')
plt.xscale('log')
plt.ylim(5e-11,8e-4)
plt.xlim(1e0,1e4)

plt.subplots_adjust(bottom=0.14,left=0.14)

plt.savefig('plots/%s_cl_%d_%d.png'%(name,i,j))
plt.close()

from scipy.special import jv
theta = 10 # arcmin
theta *= (np.pi/(180*60))

J0 = jv(0,x*theta)
J4 = jv(4,x*theta)

plt.plot(x,x*J0,color='darkmagenta', label='$J_0$')
plt.plot(x,x*J4,color='pink', label='$J_4$')


plt.xscale('log')
#plt.ylim(5e-11,8e-4)
plt.xlim(1e0,1e4)

plt.legend(fontsize=16)
plt.ylabel(r'$\ell J_\nu(\theta \ell)$', fontsize=16)
plt.xlabel(r'$\ell$', fontsize=16)
plt.ylim(-1500,1500)
plt.subplots_adjust(bottom=0.14,left=0.15)

plt.savefig('plots/hankel_%3.3f.png'%(theta))
