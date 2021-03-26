import numpy as np
import os
import sys
import astropy.table as tb
import pylab as plt
plt.switch_backend('pdf')
plt.style.use('y1a1')
from matplotlib import rcParams

import tools.emcee as mc


class chain:
	def __init__(self, filename):
		self.samples=tb.Table.read(filename, format="ascii")

		self.post = self.samples["post"]
		self.samples.remove_column("post")

		self.weight = self.samples["weight"]
		self.samples.remove_column("weight")
		self.has_wt=True

		sep = "END_OF_PRIORS_INI\n"
		text = open(filename).read()
		self.header = text.split(sep)[0]+sep
		self.npar = int(self.header.split("n_varied=")[1].split("\n")[0])

		for name in self.samples.dtype.names:  
			if name.lower()!=name:
				self.samples.rename_column(name,name.lower())

	def add_s8(self, alpha=0.5):
		newcol = self.samples['cosmological_parameters--sigma_8']*((self.samples['cosmological_parameters--omega_m']/0.3)**alpha)
		newcol = tb.Column(newcol, name="cosmological_parameters--s8")

		self.samples = tb.Table(self.samples)
		self.samples.add_column(newcol, index=len(self.samples.dtype))

		cosmosis_section = 'cosmological_parameters'
		name = 's8'

		self.header = self.header.replace("\tpost", "\t%s--%s\tpost"%(cosmosis_section, name))

		self.header = self.header.replace("n_varied=%d"%self.npar, "n_varied=%d"%(self.npar+1))
		self.npar+=1

c = chain(sys.argv[-1])
c.add_s8(alpha=0.59)

X = np.sum(c.samples['cosmological_parameters--s8']*c.weight)/np.sum(c.weight)
dX = np.sqrt(np.sum((c.samples['cosmological_parameters--s8']-X)**2*c.weight)/np.sum(c.weight))

print('S8 = %3.3f +- %3.3f'%(X,dX))
