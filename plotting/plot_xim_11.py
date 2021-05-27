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

lims_opt={}
lims_opt["+"]={}
lims_opt["-"]={}
lims_opt["+"][(1,1)] = [2.475, 250.0]
lims_opt["+"][(2,1)] = [2.475, 250.0]
lims_opt["+"][(3,1)] = [3.116, 250.0]
lims_opt["+"][(4,1)] = [2.475, 250.0]
lims_opt["+"][(2,2)] = [3.923, 250.0]
lims_opt["+"][(3,2)] = [4.938, 250.0]
lims_opt["+"][(4,2)] = [4.938, 250.0]
lims_opt["+"][(3,3)] = [3.923, 250.0]
lims_opt["+"][(4,3)] = [4.938, 250.0]
lims_opt["+"][(4,4)] = [3.923, 250.0]
lims_opt["+"][(1,2)] = [2.475, 250.0]
lims_opt["+"][(1,3)] = [3.116, 250.0]
lims_opt["+"][(1,4)] = [2.475, 250.0]
lims_opt["+"][(2,3)] = [4.938, 250.0]
lims_opt["+"][(2,4)] = [4.938, 250.0]
lims_opt["+"][(3,4)] = [4.938, 250.0]

lims_opt["-"][(1,1)] = [24.75, 250.0]
lims_opt["-"][(2,1)] = [19.660, 250.0]
lims_opt["-"][(3,1)] = [24.750, 250.0]
lims_opt["-"][(4,1)] = [19.660, 250.0]
lims_opt["-"][(2,2)] = [31.158, 250.0]
lims_opt["-"][(3,2)] = [39.226, 250.0]
lims_opt["-"][(4,2)] = [39.226, 250.0]
lims_opt["-"][(3,3)] = [49.383, 250.0]
lims_opt["-"][(3,4)] = [49.383, 250.0]
lims_opt["-"][(4,4)] = [39.226, 250.0]
lims_opt["-"][(1,2)] = [19.660, 250.0]
lims_opt["-"][(1,3)] = [24.750, 250.0]
lims_opt["-"][(1,4)] = [19.660, 250.0]
lims_opt["-"][(2,3)] = [39.226, 250.0]
lims_opt["-"][(2,4)] = [39.226, 250.0]
lims_opt["-"][(4,3)] = [49.383, 250.0]



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

F=1.

rcParams['xtick.major.size'] = 1.5
rcParams['xtick.minor.size'] = 0.75
rcParams['ytick.major.size'] = 1.5
rcParams['ytick.minor.size'] = 0.75
rcParams['xtick.direction']='in'
rcParams['ytick.direction']='in'




def get_theory_spectra(i,j,filename):
    theta = np.loadtxt("%s/shear_xi_plus/theta.txt"%filename)
    theta = theta * 60. * 180. / np.pi
    xip = np.loadtxt("%s/shear_xi_plus/bin_%d_%d.txt"%(filename,i+1,j+1))
    xim = np.loadtxt("%s/shear_xi_minus/bin_%d_%d.txt"%(filename,i+1,j+1))

    xip_gi = np.loadtxt("%s/shear_xi_gi_plus/bin_%d_%d.txt"%(filename,i+1,j+1))
    xim_gi = np.loadtxt("%s/shear_xi_gi_minus/bin_%d_%d.txt"%(filename,i+1,j+1))

    xip_ii = np.loadtxt("%s/shear_xi_plus_ii/bin_%d_%d.txt"%(filename,i+1,j+1))
    xim_ii = np.loadtxt("%s/shear_xi_minus_ii/bin_%d_%d.txt"%(filename,i+1,j+1))
    return theta, xip, xim, xip_gi, xim_gi, xip_ii, xim_ii

def get_real_spectra(i,j,fits,error=True):
    if fits is None:
        return [],[],[]
    else:
        selectp = (fits["xip"]["BIN1"][:]==j+1) & (fits["xip"]["BIN2"][:]==i+1)
        selectm = (fits["xim"]["BIN1"][:]==j+1) & (fits["xim"]["BIN2"][:]==i+1)

        xp = fits["xip"]["ANG"][:][selectp]
        xm = fits["xim"]["ANG"][:][selectm]

        xip = fits["xip"]["VALUE"][:][selectp]
        xim = fits["xim"]["VALUE"][:][selectm]

        if error:
            cov = fits["COVMAT"][:,:]
            startp,endp = fits["covmat"].read_header()["STRT_0"], fits["covmat"].read_header()["STRT_1"]
            dx = endp - startp
            startm = endp
            endm = startm + dx

            nx = xp.size

            covp = cov[startp:endp,startp:endp]
            covm = cov[startm:endm,startm:endm]

            i0 = nx*(i + j)
            errp = np.diag(covp[i0:(i0+nx),i0:(i0+nx)])
            errp = np.sqrt(errp)
            errm = np.diag(covm[i0:(i0+nx),i0:(i0+nx)])
            errm = np.sqrt(errm)
            if len(errp)==0:
                import pdb ; pdb.set_trace()

        else:
            errp = None
            errm = None

        return (xp,xip,errp), (xm,xim,errm)

i,j=3,3
data = fi.FITS('/Users/hattifattener/Documents/y3-3x2pt/data/des-y3/2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits')
xta,xip_theory,xim_theory, xip_theory_gi,xim_theory_gi, xip_theory_ii,xim_theory_ii = get_theory_spectra(i,j,'data/fid_1x2pt_maglim/')
(xp,xip,dxip),(xm,xim,dxim) = get_real_spectra(i,j,data,error=True)


plt.subplot(111)
plt.xlim(2.2,270)
plt.xscale('log')
plt.yscale('log')
plt.ylabel(r"$\theta \xi_- \times 10^{4}$", fontsize=16)
plt.xlabel(r"$\theta \;\; [ \mathrm{arcmin} ]$", fontsize=16)

#scale cuts
xlower,xupper = lims['-'][(i+1,j+1)]
plt.axvspan(1e-6, xlower, color='gray',alpha=0.2)
plt.axvspan(xupper, 500, color='gray',alpha=0.2)
xlower_opt,xupper_opt = lims_opt['-'][(i+1,j+1)]
plt.axvspan(1e-6,xlower_opt,color='gray',alpha=0.2)

plt.axhline(0,color='k',ls=':')
plt.annotate("(%d, %d)"%(i+1,j+1), (2.7,2.9), textcoords='data', fontsize=16 )

plt.errorbar(xm, xm*xim*1e4, yerr=xm*dxim*1e4, marker='.', linestyle='none', markerfacecolor='k', markeredgecolor='k', ecolor='k',markersize=markersize)
plt.plot(xta,xta*xim_theory*1e4,color='darkmagenta',lw=1.5, label='GG+GI+II')
plt.plot(xta,F*xta*(xim_theory_gi+xim_theory_ii)*1e4,color='#016E51',lw=1.5, ls='-', label='GI+II')
plt.plot(xta,F*xta*xim_theory_gi*1e4,color='midnightblue',lw=1.5, ls='--',label='GI')
plt.plot(xta,F*xta*xim_theory_ii*1e4,color='#FFA500',lw=1.5, ls='-.',label='II')
plt.legend(fontsize=14, loc='lower right')

plt.subplots_adjust(bottom=0.15,left=0.15)
plt.savefig('xim_%d%d_seminar_log.png'%(i,j))
plt.close()



plt.subplot(111)
plt.xlim(2.2,270)
plt.xscale('log')
plt.yscale('log')
plt.ylabel(r"$\theta \xi_+ \times 10^{4}$", fontsize=16)
plt.xlabel(r"$\theta \;\; [ \mathrm{arcmin} ]$", fontsize=16)

#scale cuts
xlower,xupper = lims['+'][(i+1,j+1)]
plt.axvspan(1e-6, xlower, color='gray',alpha=0.2)
plt.axvspan(xupper, 500, color='gray',alpha=0.2)
xlower_opt,xupper_opt = lims_opt['+'][(i+1,j+1)]
plt.axvspan(1e-6,xlower_opt,color='gray',alpha=0.2)

plt.axhline(0,color='k',ls=':')
plt.annotate("(%d, %d)"%(i+1,j+1), (150,3.), textcoords='data', fontsize=16 )

plt.errorbar(xm, xm*xip*1e4, yerr=xm*dxim*1e4, marker='.', linestyle='none', markerfacecolor='k', markeredgecolor='k', ecolor='k',markersize=markersize)
plt.plot(xta,xta*xip_theory*1e4,color='darkmagenta',lw=1.5, label='GG+GI+II')
plt.plot(xta,F*xta*(xip_theory_gi+xip_theory_ii)*1e4,color='#016E51',lw=1.5, ls='-', label='GI+II')
plt.plot(xta,F*xta*xip_theory_gi*1e4,color='midnightblue',lw=1.5, ls='--',label='GI')
plt.plot(xta,F*xta*xip_theory_ii*1e4,color='#FFA500',lw=1.5, ls='-.',label='II')
plt.legend(fontsize=14, loc='lower left')

plt.subplots_adjust(bottom=0.15,left=0.15)
plt.savefig('xip_%d%d_seminar_log.png'%(i,j))

