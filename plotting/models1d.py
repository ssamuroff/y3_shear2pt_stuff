import numpy as np
import tools.emcee as mc
from chainconsumer import ChainConsumer
import sys
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

fontsize=14


plt.subplot(211)#,aspect=0.145)
plt.xlim(0.5,6.5)

x = np.arange(1,7,1)
chi2 = np.array([209.3,208.31,209.81,207.95, 210.6,205.89])
dof = np.array([206,205,204,204,203,202]) 
plt.plot(x,chi2/dof,color='darkmagenta',lw=1.5)
plt.axhline(1,color='k',ls=':')
plt.yticks([1,1.01,1.02,1.03,1.04],fontsize=fontsize)
plt.ylabel(r'$\chi^2 / N_\mathrm{dof}$',fontsize=fontsize)

plt.subplot(212)

R = np.array([3.34,4.81,2.24,0.32,0.3,1])
dR = np.array([0.85,1.222,0.58,0.08,0.08,0])

R0 = np.array([-1, 1.44,0.46,0.15,0.92,3.31])
dR0 = np.array([0, 0.28,0.09,0.03,0.2,0.87])

plt.errorbar(x,R,yerr=dR,markerfacecolor='pink',markeredgecolor='pink',ecolor='pink',linestyle='none', marker='o', markersize=4.5, label='Relative to TATT')
plt.errorbar(x,R0,yerr=dR0,markerfacecolor='plum',markeredgecolor='plum',ecolor='plum',linestyle='none', marker='D', markersize=4.5, label='Relative to previous step')

plt.yticks([0,2,4,6],fontsize=fontsize)
plt.ylabel(r'$R$',fontsize=fontsize)
plt.ylim(-0.4,6.5)

plt.xlim(0.5,6.5)

plt.axhline(0,color='k',ls=':')
plt.xticks([1,2,3,4,5,6],['NLA, \n no $z$', 'NLA', 'TA', 'TATT, \n no $z$', 'TATT, \nno $A_2$ $z$', 'TATT'],fontsize=12)
#plt.xlabel('$z$',fontsize=fontsize)
#plt.ylabel('Effective $A_i$',fontsize=fontsize)
plt.legend(loc='upper right',fontsize=12)
plt.subplots_adjust(bottom=0.155,left=0.155, top=0.98,right=0.98,hspace=0, wspace=0)
print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/ia_model_ladder.png')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/ia_model_ladder.pdf')












plt.close()

plt.subplot(311)
plt.xlim(0.5,6.5)

x = np.arange(1,7,1)
S = np.array([0.782, 0.782, 0.781, 0.779, 0.766, 0.766])
dS = np.array([0.020, 0.020, 0.019, 0.022, 0.023, 0.023]) 
plt.errorbar(x,S,yerr=dS,markerfacecolor='steelblue',markeredgecolor='steelblue',ecolor='steelblue',linestyle='none', marker='o', markersize=4.5, label='$S_8$')

plt.ylim(0.69,0.85)
plt.yticks([0.7,0.75,0.8,0.85],fontsize=fontsize)

#plt.plot(x,chi2/dof,color='darkmagenta',lw=1.5)
plt.axhline(0.766,color='k',ls=':')
plt.axhspan(0.766-0.023,0.766+0.023, color='steelblue', alpha=0.2)
#plt.yticks([1,1.01,1.02,1.03,1.04],fontsize=fontsize)
plt.ylabel(r'$S_8$',fontsize=fontsize)
 


plt.subplot(312)#,aspect=0.145)
plt.xlim(0.5,6.5)

x = np.arange(1,7,1)
chi2 = np.array([209.3,208.31,209.81,207.95, 210.6,205.89])
dof = np.array([206,205,204,204,203,202]) 
plt.plot(x,chi2/dof,color='darkmagenta',lw=1.5)
plt.axhline(1,color='k',ls=':')
plt.yticks([1,1.01,1.02,1.03],fontsize=fontsize)
plt.ylabel(r'$\chi^2 / N_\mathrm{dof}$',fontsize=fontsize)

plt.subplot(313)

R = np.array([3.34,4.81,2.24,0.32,0.3,1])
dR = np.array([0.85,1.222,0.58,0.08,0.08,0])

R0 = np.array([-1, 1.44,0.46,0.15,0.92,3.31])
dR0 = np.array([0, 0.28,0.09,0.03,0.2,0.87])

plt.errorbar(x,R,yerr=dR,markerfacecolor='pink',markeredgecolor='pink',ecolor='pink',linestyle='none', marker='o', markersize=4.5, label='Relative to TATT')
plt.errorbar(x,R0,yerr=dR0,markerfacecolor='plum',markeredgecolor='plum',ecolor='plum',linestyle='none', marker='D', markersize=4.5, label='Relative to previous step')

plt.yticks([0,2,4,6],fontsize=fontsize)
plt.ylabel(r'$R$',fontsize=fontsize)
plt.ylim(-0.4,6.9)

plt.xlim(0.5,6.5)

plt.axhline(0,color='k',ls=':')
plt.xticks([1,2,3,4,5,6],['NLA, \n no $z$', 'NLA', 'TA', 'TATT, \n no $z$', 'TATT, \nno $A_2$ $z$', 'TATT'],fontsize=12)
#plt.xlabel('$z$',fontsize=fontsize)
#plt.ylabel('Effective $A_i$',fontsize=fontsize)
plt.legend(loc='upper right',fontsize=12)
plt.subplots_adjust(bottom=0.155,left=0.155, top=0.98,right=0.98,hspace=0, wspace=0)
print('Saving...')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/ia_model_ladder_withs8.png')
plt.savefig('/Users/hattifattener/Documents/y3cosmicshear/plots/ia_model_ladder_withs8.pdf')
