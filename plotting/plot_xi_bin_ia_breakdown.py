import numpy as np
import scipy, glob, argparse, yaml
import scipy.interpolate as sint
import fitsio as fi
import pylab as plt
import matplotlib
from matplotlib import rcParams
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import os
from tools.cosmosis import cosmosis_tools as ct
import tools.emcee as mc
from string import Template as Tm

lims={}
lims["+"]={}
lims["-"]={}
lims["+"][(1,1)] = [2.475, 250.0]
lims["+"][(2,1)] = [6.21691892, 250.0]
lims["+"][(3,1)] = [6.21691892, 250.0]
lims["+"][(4,1)] = [4.93827423, 250.0]
lims["+"][(2,2)] = [6.21691892, 250.0]
lims["+"][(3,2)] = [6.21691892, 250.0]
lims["+"][(4,2)] = [6.21691892, 250.0]
lims["+"][(3,3)] = [6.21691892, 250.0]
lims["+"][(4,3)] = [6.21691892, 250.0]
lims["+"][(4,4)] = [4.93827423, 250.0]
lims["+"][(1,2)] = [6.21691892, 250.0]
lims["+"][(1,3)] = [6.21691892, 250.0]
lims["+"][(1,4)] = [4.93827423, 250.0]
lims["+"][(2,3)] = [6.21691892, 250.0]
lims["+"][(2,4)] = [6.21691892, 250.0]
lims["+"][(3,4)] = [6.21691892, 250.0]
lims["-"][(1,1)] = [24.75, 250.0]
lims["-"][(2,1)] = [62.16918918, 250.0]
lims["-"][(3,1)] = [62.16918918, 250.0]
lims["-"][(4,1)] = [49.3827423, 250.0]
lims["-"][(2,2)] = [62.16918918, 250.0]
lims["-"][(3,2)] = [78.26637209, 250.0]
lims["-"][(4,2)] = [78.26637209, 250.0]
lims["-"][(3,3)] = [78.26637209, 250.0]
lims["-"][(3,4)] = [78.26637209, 250.0]
lims["-"][(4,4)] = [62.16918918, 250.0]
lims["-"][(1,2)] = [62.16918918, 250.0]
lims["-"][(1,3)] = [62.16918918, 250.0]
lims["-"][(1,4)] = [49.3827423, 250.0]
lims["-"][(2,3)] = [78.26637209, 250.0]
lims["-"][(2,4)] = [78.26637209, 250.0]
lims["-"][(4,3)] = [78.26637209, 250.0]


positions={
    (1,1,"+"):4,
    (1,1,"-"):12,
    (2,1,"+"):3,
    (2,1,"-"):18,
    (3,1,"+"):2,
    (3,1,"-"):24,
    (4,1,"+"):1,
    (4,1,"-"):30,
    (2,2,"+"):9,
    (2,2,"-"):17,
    (3,2,"+"):8,
    (3,2,"-"):23,
    (4,2,"+"):7,
    (4,2,"-"):29,
    (3,3,"+"):14,
    (3,3,"-"):22,
    (4,3,"+"):13,
    (4,3,"-"):28,
    (4,4,"+"):19,
    (4,4,"-"):27}

ymin=0.05
markersize=2.5
ytickfontsize=10

F=10.

rcParams['xtick.major.size'] = 1.5
rcParams['xtick.minor.size'] = 0.75
rcParams['ytick.major.size'] = 1.5
rcParams['ytick.minor.size'] = 0.75
rcParams['xtick.direction']='in'
rcParams['ytick.direction']='in'

i,j = 4,1

base = '/Users/hattifattener/Documents/y3cosmicshear/data/'

x =  np.loadtxt(base+'fid_1x2pt/shear_xi_gi_plus/theta.txt') * 60. * 180. / np.pi
GI_all = np.loadtxt(base+'fid_1x2pt/shear_xi_gi_plus/bin_%d_%d.txt'%(i,j))
GI_noA2 = np.loadtxt(base+'fid_1x2pt_noA2/shear_xi_gi_plus/bin_%d_%d.txt'%(i,j))
GI_nobTA = np.loadtxt(base+'fid_1x2pt_nobTA/shear_xi_gi_plus/bin_%d_%d.txt'%(i,j))
GI_A1 = np.loadtxt(base+'fid_1x2pt_noA2_nobTA/shear_xi_gi_plus/bin_%d_%d.txt'%(i,j))

GI_A2 = GI_all- GI_noA2
GI_bTA = GI_all- GI_nobTA



plt.plot(x,1e4*x*GI_all,color='darkmagenta', lw=1.5, label=r'Total')
plt.plot(x,1e4*x*GI_A1,color='pink', lw=1.5, label=r'$A_1$')
plt.plot(x,1e4*x*GI_A2,color='plum', lw=1.5, label=r'$A_2$')
plt.plot(x,1e4*x*GI_bTA,color='hotpink', lw=1.5, label=r'$b_{\rm TA}$')
plt.axhline(0,color='k',ls=':')

GI_cross = GI_all-(GI_A1+GI_A2+GI_bTA)

#plt.plot(x,1e4*x*(GI_cross),color='k', lw=1.5,ls=':', label='Cross terms')

#ax = plt.subplot(1,1,1)
plt.annotate("(%d, %d)"%(i,j), (3.,0.075), textcoords='data', fontsize=19)
plt.ylim(-0.1,0.1)
plt.xlabel(r"$\theta \;\; [ \mathrm{arcmin} ]$ ", fontsize=18)
plt.ylabel(r"$\theta \xi^{\rm GI}_+$ ", fontsize=18)
plt.xscale("log")
plt.xlim(2.2,270)
plt.xticks([10,100],["10", "100"], fontsize=18)
plt.axhline(0, color='k', ls=':')

xlower,xupper = lims['-'][(i, j)]
plt.axvspan(1e-6, xlower, color='gray',alpha=0.2)
plt.axvspan(xupper, 500, color='gray',alpha=0.2)
plt.subplots_adjust(hspace=0,wspace=0, bottom=0.14,left=0.14, right=0.88)

plt.legend(fontsize=16)
plt.subplots_adjust(hspace=0,wspace=0, bottom=0.14,left=0.185, right=0.95)
plt.savefig("plots/xipm_ia_breakdown.pdf")
plt.savefig("plots/xipm_ia_breakdown.png")




