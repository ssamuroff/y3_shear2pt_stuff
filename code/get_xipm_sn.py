import numpy as np
import sys

M = np.loadtxt(sys.argv[1]+'/data_vector/2pt_theory.txt')
D = np.loadtxt(sys.argv[1]+'/data_vector/2pt_data.txt')
C0 = np.loadtxt(sys.argv[1]+'/data_vector/2pt_inverse_covariance.txt')

S0 = np.sqrt(np.dot(D,np.dot(C0,D)))
print('S/N wrong: %3.3f'%S0)

S1 = np.dot(np.dot(D,C0),M)/np.sqrt(np.dot(np.dot(M,C0),M))
print('S/N right: %3.3f'%S1)

print(len(D))