import numpy as np
import sys

# load the parameter covariance matrix 
filename = '%s/covmat.txt'%sys.argv[1]
c = np.loadtxt(filename)

# find the indices for the submatrix...
f=open(filename)
hdr = f.read().split('\n')[0].replace('#','')
hdr = hdr.split()

k = [i for i in range(len(hdr)) if 'omega_m' in hdr[i]][0]
l = [i for i in range(len(hdr)) if 's8' in hdr[i]][0]

print(k,l)

C = np.array([[c[k,k],c[k,l]],[c[l,k],c[l,l]]])

# evaluate the FoM
F = 1./np.sqrt(np.linalg.det(C))

print('S8 Omega_m')
print(F)
