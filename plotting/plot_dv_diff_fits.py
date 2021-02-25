import numpy as np
import scipy, glob, argparse, yaml
import scipy.interpolate as sint
import fitsio as fi
import pylab as plt
import matplotlib
from matplotlib import rcParams
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import os, sys

# adjust these as needed
ymin = -4.
ymax = 1.
yticks = np.linspace(ymin,ymax,5)

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


markersize=2.5
ytickfontsize=10

rcParams['xtick.major.size'] = 1.5
rcParams['xtick.minor.size'] = 0.75
rcParams['ytick.major.size'] = 1.5
rcParams['ytick.minor.size'] = 0.75
rcParams['xtick.direction']='in'
rcParams['ytick.direction']='in'




def get_spectra(i,j,fits,error=True):
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


    

def cornerplot(path1, path2, show_cuts=False):

    plt.switch_backend("pdf")
    plt.style.use("y1a1")
    matplotlib.rcParams["ytick.minor.visible"]=False
    matplotlib.rcParams["xtick.minor.visible"]=False
    matplotlib.rcParams["ytick.minor.width"]=0.1
    matplotlib.rcParams["ytick.major.size"]=2.5
    matplotlib.rcParams["xtick.major.size"]=2.5
    matplotlib.rcParams["xtick.minor.size"]=1.8

    # number of redshift bins
    ni,nj=4,4
    ni = int(ni)
    nj = int(nj)

    rows, cols = ni+1, nj+2

    count = 0

    # open the FITS files once here
    fits1 = fi.FITS(path1)
    fits2 = fi.FITS(path2)

    # loop over all bin pairs
    for i in range(ni):
        for j in range(nj):
            count+=1
            if j>i:
                continue

            print(i,j)

            # work out which subplot to use
            posp = positions[(i+1,j+1,"+")]
            ax = plt.subplot(rows,cols,posp)
            ax.annotate("(%d, %d)"%(i+1,j+1), (3.,(yticks[0]+yticks[1])/2), textcoords='data', fontsize=9, )
            ax.yaxis.set_tick_params(which='minor', left='off', right='off')
            plt.ylim(ymin,ymax)
            
            plt.xscale("log")
            if (posp==19) or (posp==1) or (posp==7) or (posp==13):
                plt.yticks(visible=True)

                plt.yticks(yticks[:-1],fontsize=ytickfontsize)
            else:
                plt.yticks(visible=False)

            if (posp==19):
                plt.ylabel(r"$ \Delta \xi_+/\xi_+$", fontsize=11)
                plt.xlabel(r"$\theta \;\; [ \mathrm{arcmin} ]$", fontsize=10)
            else:
                pass

            if posp in [19,14,9,4]:
                plt.xlabel(r"$\theta \;\; [ \mathrm{arcmin} ]$ ", fontsize=10)

            plt.xlim(2.2,270)
            plt.xticks([10,100],["10", "100"], fontsize=9)
            #plt.yticks([-2,0,2,4,6,8],['-2', '0', '2', '4', '6', '8'])
            plt.axhline(0, color='k', ls=':')


            if show_cuts:
                xlower,xupper = lims['+'][(i+1,j+1)]
                plt.axvspan(1e-6, xlower, color='gray',alpha=0.2)
                plt.axvspan(xupper, 500, color='gray',alpha=0.2)


            # load and cut the data
            (xp_1,xip_1,dxip_1),(xm_1,xim_1,dxim_1) = get_spectra(i,j,fits1)
            (xp_2,xip_2,dxip_2),(xm_2,xim_2,dxim_2) = get_spectra(i,j,fits2)

            # going to assume the theta binning is the same for the two
            plt.plot(xp_1,(xip_1-xip_2)/xip_1,color='darkmagenta',lw=1.5)


            # The same as everything above, but for xim
            posm = positions[(i+1,j+1,"-")]
            ax = plt.subplot(rows,cols,posm)
            ax.annotate("(%d, %d)"%(i+1,j+1), (3,(yticks[0]+yticks[1])/2), textcoords='data', fontsize=9, )
            ax.yaxis.set_tick_params(which='minor', left='off', right='off')

            #import pdb ; pdb.set_trace()

            plt.ylim(ymin,ymax)
            ax.yaxis.set_ticks_position("right")
            ax.yaxis.set_label_position("right")
            
            if (posm==30) or (posm==12) or (posm==18) or (posm==24):
                plt.yticks(visible=True)
                ax.yaxis.set_label_position("right")
                plt.yticks(yticks,fontsize=ytickfontsize)

            else:
                plt.yticks(visible=False)

            if (posm==30):
                plt.ylabel(r"$ \Delta \xi_-/ \xi_-$", fontsize=11)
                plt.yticks(yticks[:-1],fontsize=ytickfontsize)

            else:
                pass

            if posm in [30,29,28,27]:
                plt.xlabel(r"$\theta \;\; [ \mathrm{arcmin} ]$ ", fontsize=10)
            
            plt.xscale("log")
            plt.xlim(2.2,270)

            plt.xticks([10,100],["10", "100"], fontsize=9)

            plt.yticks(yticks[:-1],fontsize=ytickfontsize)
            plt.axhline(0, color='k', ls=':')

            if show_cuts:
                xlower,xupper = lims['-'][(i+1, j+1)]
                plt.axvspan(1e-6, xlower, color='gray',alpha=0.2)
                plt.axvspan(xupper, 500, color='gray',alpha=0.2)

            plt.plot(xm_1,(xim_1-xim_2)/xim_1,color='darkmagenta',lw=1.5)


    #box = ax.get_position()
    #ax.set_position([box.x0, box.y0, box.width*0.65, box.height])
    #legend_x = 4.2
    #legend_y = 5.2
    #proxies = [plt.Line2D([0,2.5], [0,0], linestyle=ls, linewidth=1.5, color=lc) for ls,lc in [('-','darkmagenta'),('-','pink'),('--','pink'),(':','midnightblue')]]
    #plt.legend(proxies,["GG+GI+II", "GI+II"], loc='upper right', bbox_to_anchor=(legend_x, legend_y), fontsize=9)

    plt.subplots_adjust(hspace=0,wspace=0, bottom=0.14,left=0.14, right=0.88)
    os.system('mkdir plots/')
    plt.savefig("plots/unblinded_datavector_xipm_diff.pdf")
    plt.savefig("plots/unblinded_datavector_xipm_diff.png")





cornerplot(sys.argv[1], sys.argv[2], show_cuts=True)


