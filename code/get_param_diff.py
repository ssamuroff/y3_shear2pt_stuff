# lots of stuff to import
import sys, os
from getdist import plots, MCSamples
from getdist.gaussian_mixtures import GaussianND
import getdist
getdist.chains.print_load_details = False
import scipy
import matplotlib.pyplot as plt
import numpy as np
from getdist.gaussian_mixtures import GaussianND
# import tension tools utilities:
from tensiometer import utilities
from tensiometer import cosmosis_interface
from tensiometer import mcmc_tension
from tensiometer import gaussian_tension

do_full=False

# Define the chains we want to use. This is the only bit that should be modified.
chain1_name = sys.argv[1]
chain2_name = sys.argv[2]

print(chain1_name,chain2_name)

# we need to define the labels mapping since cosmosis does not ship them...
parameter_labels_dict = {'cosmological_parameters--omega_m': '\\Omega_m',
                         'cosmological_parameters--h0': 'h_0',
                         'cosmological_parameters--omega_b': '\\Omega_b',
                         'cosmological_parameters--n_s': 'n_s',
                         'cosmological_parameters--a_s': 'A_s',
                         'cosmological_parameters--omnuh2': '\\Omega_\\nu h^2',
                         'COSMOLOGICAL_PARAMETERS--SIGMA_8': '\\sigma_8'}
# getdist settings:
settings = {'smooth_scale_1D': 0.2, 'smooth_scale_2D': 0.2,
            'boundary_correction_order': 1, 'mult_bias_correction_order': 1}
# latex rendering because it's cool:
plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
plt.rc('text', usetex=True)
# seed randoms to get reproducible results:
np.random.seed(0)
# parameters to use in the following:
selected_params = ['cosmological_parameters--omega_m', 'COSMOLOGICAL_PARAMETERS--SIGMA_8']
full_params = ['cosmological_parameters--omega_m',
               'cosmological_parameters--h0',
               'cosmological_parameters--omega_b',
               'cosmological_parameters--n_s',
               'cosmological_parameters--omnuh2',
               'COSMOLOGICAL_PARAMETERS--SIGMA_8',]

# chain 1:
chain_1 = cosmosis_interface.MCSamplesFromCosmosis(chain1_name, param_label_dict=parameter_labels_dict, settings=settings)
# chain 2:
chain_2 = cosmosis_interface.MCSamplesFromCosmosis(chain2_name, param_label_dict=parameter_labels_dict, settings=settings)
chain_1.name_tag = 'chain 1'
chain_2.name_tag = 'chain 2'

print('Number of samples chain 1 =', len(chain_1.weights), ', number of effective samples =', np.round(np.sum(chain_1.weights)**2./np.sum(chain_1.weights**2)))
print('Number of samples chain 2 =', len(chain_2.weights), ', number of effective samples =', np.round(np.sum(chain_2.weights)**2./np.sum(chain_2.weights**2)))



# calculate the parameter difference distribution for the tension calculation
ch_1 = utilities.bernoulli_thin(chain_1.copy())
ch_2 = utilities.bernoulli_thin(chain_2.copy(), num_repeats=2)

diff_chain = mcmc_tension.parameter_diff_chain(ch_1, ch_2)
print('Number of samples diff chain', len(diff_chain.weights), np.round(np.sum(diff_chain.weights)**2./np.sum(diff_chain.weights**2)))
diff_chain.name_tag = 'Planck vs DES'
diff_chain.updateSettings(settings);
diff_chain.updateBaseStatistics();


# the parameter names in the difference chain are a little different:
delta_param_names = ['delta_'+name for name in selected_params]
delta_param_names_full = ['delta_'+name for name in full_params]

#plot out the difference chain
#g = plots.get_single_plotter()
#g.triangle_plot(diff_chain, delta_param_names, filled=True, markers={name:0. for name in delta_param_names}, contour_args={'alpha':0.6}, contour_colors=['darkmagenta'])
#plt.savefig('plots/param_diff_distribution.png')
#plt.close()


# now work out the shift in terms of sigma
exact_shift_P_1, exact_shift_low_1, exact_shift_hi_1 = mcmc_tension.exact_parameter_shift(diff_chain, param_names=delta_param_names, feedback=3)
print(f'Shift probability considering selected parameters = {exact_shift_P_1:.5f} +{exact_shift_hi_1-exact_shift_P_1:.5f} -{exact_shift_P_1-exact_shift_low_1:.5f}')
print(f'n_sigma = {utilities.from_confidence_to_sigma(exact_shift_P_1):.3f}')

if do_full:
	# and the fuller calculation...
	exact_shift_P_1, exact_shift_low_1, exact_shift_hi_1 = mcmc_tension.exact_parameter_shift(diff_chain, param_names=delta_param_names_full, scale=0.2, feedback=3, chunk_size=200, smallest_improvement=1.e-3, method='nearest_elimination')
	print(f'Shift probability considering full = {exact_shift_P_1:.5f} +{exact_shift_hi_1-exact_shift_P_1:.5f} -{exact_shift_P_1-exact_shift_low_1:.5f}')
	print(f'    n_sigma = {utilities.from_confidence_to_sigma(exact_shift_P_1):.3f}')


print('Done')