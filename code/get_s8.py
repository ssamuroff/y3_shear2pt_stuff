import numpy as np
import os
import sys
import pylab as plt
plt.switch_backend('pdf')
plt.style.use('y1a1')
from matplotlib import rcParams

import tools.emcee as mc

c = mc.chain(sys.argv[-1])
c.add_s8()

X = np.sum(c.samples['cosmological_parameters--s8']*c.weight)/np.sum(c.weight)
dX = np.sqrt(np.sum((c.samples['cosmological_parameters--s8']-X)**2*c.weight)/np.sum(c.weight))

print('S8 = %3.3f +- %3.3f'%(X,dX))