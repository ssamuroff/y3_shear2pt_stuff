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

# adjust these as needed
ymin = -0.5
ymax = 4
yticks = np.linspace(ymin,ymax,5)

ytick_labels = ['%3.1f'%y for y in yticks]

# factor by which to multiply the IA contributions
F=10.

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

markersize=2.5
ytickfontsize=10



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

    xip_ii = np.loadtxt("%s/shear_xi_ii_plus/bin_%d_%d.txt"%(filename,i+1,j+1))
    xim_ii = np.loadtxt("%s/shear_xi_ii_minus/bin_%d_%d.txt"%(filename,i+1,j+1))
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

def get_modifier(x,dxi,target):
    if len(dxi)==0: return 0
    import scipy.interpolate as interp
    interpolator = interp.interp1d(np.log10(x),dxi) 
    return interpolator(np.log10(target))
    

def cornerplot(theory, data, show_cuts=False):

    plt.switch_backend("pdf")
    plt.style.use("y1a1")
    matplotlib.rcParams["ytick.minor.visible"]=False
    matplotlib.rcParams["xtick.minor.visible"]=False
    matplotlib.rcParams["ytick.minor.width"]=0.1
    matplotlib.rcParams["ytick.major.size"]=2.5
    matplotlib.rcParams["xtick.major.size"]=2.5
    matplotlib.rcParams["xtick.minor.size"]=1.8
    ni,nj=4,4
    #ni,nj=np.genfromtxt("%s/shear_xi_plus/values.txt"%theory1[0]).T[2]
    ni = int(ni)
    nj = int(nj)
    if data is not None:
        data = fi.FITS(data)


    rows, cols = ni+1, nj+2

    count = 0

    for i in range(ni):
        for j in range(nj):
            count+=1
            if j>i:
                continue

            print(i,j)
            (xp,xip,dxip),(xm,xim,dxim) = get_real_spectra(i,j,data,error=True)


            posp = positions[(i+1,j+1,"+")]
            ax = plt.subplot(rows,cols,posp)
            ax.annotate("(%d, %d)"%(i+1,j+1), (3.,yticks[-2]), textcoords='data', fontsize=9, )
            ax.yaxis.set_tick_params(which='minor', left='off', right='off')

            plt.ylim(ymin,ymax)
            plt.xscale("log")
            if (posp==19) or (posp==1) or (posp==7) or (posp==13):
                #plt.yticks(visible=True)

                plt.yticks(yticks[:-1],ytick_labels[:-1],fontsize=ytickfontsize,visible=True)
            else:
                plt.yticks(visible=False)

            if (posp==19):
                plt.ylabel(r"$\theta \xi_+ \times 10^{4}$", fontsize=11)
                plt.xlabel(r"$\theta \;\; [ \mathrm{arcmin} ]$", fontsize=10)
            else:
                pass

            if posp in [19,14,9,4]:
                plt.xlabel(r"$\theta \;\; [ \mathrm{arcmin} ]$ ", fontsize=10)

            plt.xlim(2.2,270)
            plt.xticks([10,100],["10", "100"], fontsize=9)
            plt.axhline(0, color='k', ls=':')


            if show_cuts:
                xlower,xupper = lims['+'][(i+1,j+1)]
                plt.axvspan(1e-6, xlower, color='gray',alpha=0.2)
                plt.axvspan(xupper, 500, color='gray',alpha=0.2)

                xlower_opt,xupper_opt = lims_opt['+'][(i+1,j+1)]
                plt.axvspan(1e-6,xlower_opt,color='gray',alpha=0.2)



            linestyles=['-',':','--','-']

            xta,xip_theory,xim_theory, xip_theory_gi,xim_theory_gi, xip_theory_ii,xim_theory_ii = get_theory_spectra(i,j,theory)

            plt.errorbar(xp, xp*xip*1e4, yerr=xp*dxip*1e4, marker='.', linestyle='none', markerfacecolor='k', markeredgecolor='k', ecolor='k',markersize=markersize)
            p1 = plt.plot(xta,xta*xip_theory*1e4,color='darkmagenta',lw=1.5, label='GG+GI+II')
            plt.plot(xta,F*xta*(xip_theory_gi+xip_theory_ii)*1e4,color='steelblue',lw=1., ls='-', label='GI')
            p2 = plt.plot(xta,F*xta*xip_theory_gi*1e4,color='pink',lw=1.5, ls='--', label='GI')
            p3 = plt.plot(xta,F*xta*xip_theory_ii*1e4,color='midnightblue',lw=1.5, ls=':', label='II')


            posm = positions[(i+1,j+1,"-")]
            ax = plt.subplot(rows,cols,posm)
            ax.annotate("(%d, %d)"%(i+1,j+1), (3,yticks[-2]), textcoords='data', fontsize=9)
            ax.yaxis.set_tick_params(which='minor', left='off', right='off')

            plt.ylim(ymin,ymax)
            ax.yaxis.set_ticks_position("right")
            ax.yaxis.set_label_position("right")
            
            if (posm==30) or (posm==12) or (posm==18) or (posm==24):
                #plt.yticks(visible=True)
                ax.yaxis.set_label_position("right")
                plt.yticks(yticks,ytick_labels,fontsize=ytickfontsize,visible=True)

            else:
                plt.yticks(visible=False)

            if (posm==30):
                plt.ylabel(r"$\theta \xi_-\times 10^{4}$", fontsize=11)
                plt.yticks(yticks[:-1],ytick_labels[:-1],fontsize=ytickfontsize)

            else:
                pass

            if posm in [30,29,28,27]:
                plt.xlabel(r"$\theta \;\; [ \mathrm{arcmin} ]$ ", fontsize=10)

            plt.xscale("log")
            plt.xlim(2.2,270)

            plt.xticks([10,100],["10", "100"], fontsize=9)
            plt.yticks(yticks[:-1],ytick_labels[:-1],fontsize=ytickfontsize)
            plt.axhline(0, color='k', ls=':')

            if show_cuts:
                xlower,xupper = lims['-'][(i+1, j+1)]
                plt.axvspan(1e-6, xlower, color='gray',alpha=0.2)
                plt.axvspan(xupper, 500, color='gray',alpha=0.2)

                xlower_opt,xupper_opt = lims_opt['-'][(i+1,j+1)]
                plt.axvspan(1e-6,xlower_opt,color='gray',alpha=0.2)

            plt.errorbar(xm, xm*xim*1e4, yerr=xm*dxim*1e4, marker='.', linestyle='none', markerfacecolor='k', markeredgecolor='k', ecolor='k',markersize=markersize)
            plt.plot(xta,xta*xim_theory*1e4,color='darkmagenta',lw=1.5)
            plt.plot(xta,F*xta*(xim_theory_gi+xim_theory_ii)*1e4,color='steelblue',lw=1., ls='-', label='GI')
            plt.plot(xta,F*xta*xim_theory_gi*1e4,color='pink',lw=1.5, ls='--')
            plt.plot(xta,F*xta*xim_theory_ii*1e4,color='midnightblue',lw=1.5, ls=':')



    plt.legend([p1,p2,p3],title='title', bbox_to_anchor=(1.05, 1), loc='upper right', fontsize=12)

#    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*0.65, box.height])
    legend_x = 4.2
    legend_y = 5.2
    proxies = [plt.Line2D([0,2.5], [0,0], linestyle=ls, linewidth=1.5, color=lc) for ls,lc in [('-','darkmagenta'),('-','steelblue'),('--','pink'),(':','midnightblue')]]
    plt.legend(proxies,["GG+GI+II", r"$10 \times$ GI+II", r"$10 \times$ GI", r'$10 \times$ II'], loc='upper right', bbox_to_anchor=(legend_x, legend_y), fontsize=9)

    plt.subplots_adjust(hspace=0,wspace=0, bottom=0.14,left=0.14, right=0.88)
    plt.savefig("plots/unblinded_datavector_xipm_maglimbf.pdf")
    plt.savefig("plots/unblinded_datavector_xipm_maglimbf.png")






def main(args):
   
    cornerplot(args.theory,
               args.data, show_cuts=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--theory',"-t", type=str, action='store', default='none')
    parser.add_argument('--data',"-d", type=str, action='store')

    args = parser.parse_args()


    main(args)
