import numpy as np
import scipy, glob, argparse, yaml
import fitsio as fi
import pylab as plt
import matplotlib
import os
from tools.cosmosis import cosmosis_tools as ct
import tools.emcee as mc
from string import Template as Tm


lims={}

lims[(1,1)] = [64.0, 250.0]
lims[(2,1)] = [40.0, 250.0]
lims[(3,1)] = [30.0, 250.0]
lims[(4,1)] = [24.0, 250.0]
lims[(2,2)] = [40.0, 250.0]
lims[(3,2)] = [30.0, 250.0]
lims[(4,2)] = [24.0, 250.0]
lims[(3,3)] = [30.0, 250.0]
lims[(4,3)] = [24.0, 250.0]
lims[(4,4)] = [24.0, 250.0]
lims[(1,2)] = [64.0, 250.0]
lims[(1,3)] = [64.0, 250.0]
lims[(1,4)] = [64.0, 250.0]
lims[(2,3)] = [40.0, 250.0]
lims[(2,4)] = [40.0, 250.0]
lims[(3,4)] = [30.0, 250.0]

lims[(1,5)] = [5.715196, 250.0]
lims[(2,5)] = [7.195005, 250.0]
lims[(3,5)] = [7.195005, 250.0]
lims[(4,5)] = [7.195005, 250.0]

lims[(5,1)] = [21.0, 250.0]
lims[(5,2)] = [21.0, 250.0]
lims[(5,3)] = [21.0, 250.0]
lims[(5,4)] = [21.0, 250.0]


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

from matplotlib import rcParams
rcParams['xtick.major.size'] = 1.5
rcParams['xtick.minor.size'] = 0.75
rcParams['ytick.major.size'] = 1.5
rcParams['ytick.minor.size'] = 0.75
rcParams['xtick.direction']='in'
rcParams['ytick.direction']='in'



def get_theory_spectra(i,j,filename):
    theta = np.loadtxt("%s/galaxy_shear_xi/theta.txt"%filename)
    theta = theta * 60. * 180. / np.pi
    gammat = np.loadtxt("%s/galaxy_shear_xi/bin_%d_%d.txt"%(filename,j+1,i+1))
    gammat_gi = np.loadtxt("%s/galaxy_intrinsic_xi/bin_%d_%d.txt"%(filename,j+1,i+1))
    return theta, gammat, gammat_gi

def get_real_spectra(i,j,fits,error=True):
    if fits is None:
        return [],[],[]
    else:
        selectp = (fits["gammat"]["BIN1"][:]==j+1) & (fits["gammat"]["BIN2"][:]==i+1)

        xp = fits["gammat"]["ANG"][:][selectp]

        y = fits["gammat"]["VALUE"][:][selectp]

        if error:
            cov = fits["COVMAT"][:,:]
            start,end = fits["covmat"].read_header()["STRT_2"], fits["covmat"].read_header()["STRT_3"]
            dx = end - start

            nx = xp.size

            covp = cov[start:end,start:end]

            i0 = nx*(i + j)
            err = np.diag(covp[i0:(i0+nx),i0:(i0+nx)])
            err = np.sqrt(err)

        else:
            err = None

        return (xp,y,err)

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
    #ni,nj=np.genfromtxt("%s/galaxy_shear_xi/values.txt"%theory).T[2]
    #ni = int(ni)
    #nj = int(nj)
    nj,ni=4,5
    if data is not None:
        data = fi.FITS(data)


    fig = plt.figure(0)

    rows, cols = nj, ni

    count = 0


    for i in range(nj):
        for j in range(ni):
            count+=1

            print(i,j)
            xta, gammat_theory_a, gammat_theory_gi = get_theory_spectra(i,j,theory)
            xa, gammat_a,dgammat_a  = get_real_spectra(i,j,data)
            #print (dgammat_a)


            ax = plt.subplot(rows,cols, count)
            ax.annotate("(%d, %d)"%(j+1,i+1), (3.8,1.1e-2), textcoords='data', fontsize=11, )
            ax.yaxis.set_tick_params(which='minor', left='off', right='off')

            plt.ylim(1e-5,1e-1)
            plt.yscale("log")
            plt.xscale("log")
            if (j==0):
                pass
                #fig.text(0.07,0.5, r"$\theta \gamma_t \times 10^{2}$", ha='center', va='center', rotation='vertical', fontsize=12)
            if (i==nj-1):
                plt.xlabel(r"$\theta$ / arcmin", fontsize=12)
            plt.yticks(fontsize=10)

            if not (j==0):
                plt.yticks(visible=False)
            plt.xlim(2.2,270)
            plt.xticks([10,100],["10", "100"], fontsize=10)
            plt.yticks([1e-5,1e-4,1e-3,1e-2])
            plt.axhline(0, color='k',ls=':')
            if j in [0,6,11,17]:
                plt.ylabel(r"$\theta \gamma_t$", fontsize=11)


            if show_cuts:
                xlower,xupper = lims[(j+1,i+1)]
                plt.axvspan(1e-6, xlower, color='gray',alpha=0.2)
                plt.axvspan(xupper, 500, color='gray',alpha=0.2)

            if (j==1) & (i==0): import pdb ; pdb.set_trace()
           
            plt.errorbar(xa, xa*gammat_a, yerr=xa*dgammat_a, ls="none", marker=".", markersize=2,  ecolor="k", markeredgecolor="k", markerfacecolor="k")
            

            plt.plot(xta, xta*gammat_theory_a,color="darkmagenta", ls='-',lw=1.5)
            plt.plot(xta, -xta*gammat_theory_gi,color="pink", ls='--',lw=1.5)
           # plt.plot(xtb, 1e2*xtb*gammat_theory_b,color="k")


    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*0.65, box.height])
    legend_x = 4.2
    legend_y = 5.2
    proxies = [plt.Line2D([0,2.5], [0,0], linestyle=ls, linewidth=1.5, color=lc) for ls,lc in [('-','darkmagenta'),('--','pink')]]
    plt.legend(proxies,["GG+GI", "GI"], loc='upper right', bbox_to_anchor=(legend_x, legend_y), fontsize=10)


    plt.subplots_adjust(hspace=0,wspace=0)
    plt.savefig("plots/unblinded_datavector_gammat_log.pdf")
    plt.savefig("plots/unblinded_datavector_gammat_log.png")



def parse_values(filename, args, blind=False):
    mean_vals = np.genfromtxt("%s/means.txt"%filename, dtype=[("name", "S100"),("mean", float), ("std", float)])

    params = {
    "cosmological_parameters":
        {
        "omega_m" :  0.295,
        "h0"       :  0.6881,
        "omega_b"  :  0.0468,
        "n_s"        :  0.9676,
        "A_s"        :  2.260574e-9,
        "omnuh2"     :  0.0006,
        "w"         : -1.0,
        "massive_nu" :  1,
        "massless_nu":  2.046,
        "omega_k"    :  0.0,
        "tau"        :  0.08,
        "wa"         :  0.0},
    "shear_calibration_parameters":
        {
        "m1" : 0.0,
        "m2" : 0.0,
        "m3" : 0.0,
        "m4" : 0.0},
    "intrinsic_alignment_parameters":
        {
        "a"     : 0.0,
        "alpha" : 0.0,
        "z0"    : 0.62},
    "wl_photoz_errors":
        {
        "bias_1" : 0.0,
        "bias_2" : 0.0,
        "bias_3" : 0.0,
        "bias_4" : 0.0},
    "lens_photoz_errors":
        {
        "bias_1" : 0.0,
        "bias_2" : 0.0,
        "bias_3" : 0.0,
        "bias_4" : 0.0},
    "bias_parameters":
        {
        "b_1" : 0.0,
        "b_2" : 0.0,
        "b_3" : 0.0,
        "b_4" : 0.0}}

    for i, name in enumerate(mean_vals["name"]):
        if (name=="post") or (name=="weight"):
            continue
        section, param = name.split("--")
        print (section, param,)
        value = mean_vals["mean"][i]
        params[section][param] = value
        if blind:
            print("XXX")
        else:
            print(value)

    return params

def export_values(mean_values_dict, export_to='output/values.ini'):
    vals = Tm(open("/home/samuroff/local/python/lib/python2.7/site-packages/tools/cosmosis/values_template-3x2pt").read())
    vals_all = {}
    for name1 in mean_values_dict.keys():
        for  name2 in mean_values_dict[name1].keys():
            vals_all[name2] = mean_values_dict[name1][name2]

    values_txt = vals.substitute(vals_all)

    outfile = open(export_to, "wa")
    outfile.write(values_txt)
    outfile.close()


def main(args):
    cornerplot(args.theory, args.data, show_cuts=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--theory',"-t", type=str, action='store', default='none')
    parser.add_argument('--data',"-d", type=str, action='store')

    args = parser.parse_args()

    main(args)
