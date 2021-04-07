import sys
import os
import numpy as np
import warnings

chain = sys.argv[1]
poly_output_location = sys.argv[2]

print('Postprocessing:',chain)
print('Looking for extra polychord outputs in:',poly_output_location)

################################################
# first, get the cosmosis postprocessing numbers
################################################

for line in open(chain):
	if line[0:11]=='## run_name':
		run_name = line.split()[-1]
		print('RUN_NAME is:',run_name)
		break
		
command = 'postprocess --no-plots --fix-edges --derive=code/derive_s8.py '+chain+' -o '+run_name
os.system(command)

##################################################################
# Now get the maximum posterior from the enhanced polychord output
##################################################################

relevant_poly_output_name = 'poly_'+run_name+'.txt'

poly_output = np.loadtxt(poly_output_location+relevant_poly_output_name) 

#hopefully figured this out correctly bellow
#the ordering of columns in the polychord output is different than the usual cosmosis chains and looks like:
#[weight, -2*likelihood, param1(Om), param2(h0), ..., paramN-1(sigma8), paramN(sigma12), datavector--chi2, prior]
#this output won't include extra derived parameters such as S8, so will do that by hand below
likelihoods = -0.5*poly_output[:,1] 
priors = poly_output[:,-1]
posteriors = likelihoods+priors
MAP = np.amax(posteriors)
poly_best_fit = poly_output[np.where(posteriors==MAP)[0]].flatten()

##########################################################
# now get the final result to be quoted for each parameter 
##########################################################

center = 'means.txt'
best = 'best_fit.txt'
uerr = 'uerr68.txt'
lerr = 'lerr68.txt'

new_output_name = run_name+'/final.txt'
new_output = open(new_output_name,'w')

new_output.write('# parameter postprocess_mean postprocess_best_fit oversampled_polychord_best_fit (uerr68-mean) (mean-lerr68)\n\n')

with open(run_name+'/'+center) as center_file, open(run_name+'/'+best) as best_file, open(run_name+'/'+uerr) as uerr_file, open(run_name+'/'+lerr) as lerr_file:
	linenumber=2
	for center_line, best_line, uerr_line, lerr_line in zip(center_file, best_file, uerr_file, lerr_file):
		if center_line[0]!='#':
			param_name = center_line.split()[0]

			if (linenumber-len(poly_best_fit)) >= 0:
				poly_value=np.nan
			else:	
				poly_value=poly_best_fit[linenumber]
						
			center_value = float(center_line.split()[1])
			best_value = float(best_line.split()[1])
			uerr_value = float(uerr_line.split()[1])
			lerr_value = float(lerr_line.split()[1])

			if center_value>uerr_value or center_value<lerr_value:
				warnings.warn('\nWARNING: The point estimate from '+run_name+'/'+center+' is not contained inside uerr68 and lerr68 for parameter '+param_name)

			output_line = param_name+'			%1.5e		%1.5e		%1.5e		+%1.5e		-%1.5e\n'%(center_value, best_value, poly_value, uerr_value-center_value, center_value-lerr_value)
			new_output.write(output_line)
			linenumber=linenumber+1


#############################################################################################################
# write separately the extra polychord numbers that I couldn't catch in a smart way for every possible chain: 
#############################################################################################################
new_output.write('\n\n#More oversampled polychord best-fit outputs:\n')
new_output.write('#Weight = %1.5e\n'%(poly_best_fit[0]))
new_output.write('#Likelihood = %1.5e\n'%(-0.5*poly_best_fit[1]))
new_output.write('#Maximum posterior = %1.5e\n'%(MAP))
new_output.write('#S8 = %1.5e\n'%( poly_best_fit[-4]*np.sqrt(poly_best_fit[2]/0.3) ))



#########################################################################################
# getting also the FoM for Omega_m x sigma8 and Omega_m x S8 and writing to the same file 
#########################################################################################
def get_figure_of_merit(fullcov, col1, col2):  
    subcov = np.zeros((2,2))
    subcov[0,0] = fullcov[col1,col1]
    subcov[1,0] = fullcov[col1,col2]
    subcov[0,1] = fullcov[col2,col1]
    subcov[1,1] = fullcov[col2,col2]
    return 1.0/np.sqrt(np.linalg.det(subcov))


with open(run_name+'/covmat.txt') as f:
    cov_header = f.readline()

#find the om, sigma8 and S8 columns - surely there's better ways to do this
col=0    
for param in cov_header[1:].split():
	if param=='cosmological_parameters--omega_m':
		om_col=col
	if param=='cosmological_parameters--sigma_8':
		sigma8_col=col
	if param=='cosmological_parameters--s8_0.500':
		S8_col=col
	col=col+1	

cov = np.loadtxt(run_name+'/covmat.txt')

Om_x_sigma8_FoM = get_figure_of_merit(cov, om_col, sigma8_col)
Om_x_S8_FoM = get_figure_of_merit(cov, om_col, S8_col)

new_output.write('\n\n#Om x sigma8 FoM = %1.3f\n'%Om_x_sigma8_FoM)
new_output.write('#Om x S8 FoM = %1.3f\n'%Om_x_S8_FoM)

print('\nOm x sigma8 FoM = %1.3f'%Om_x_sigma8_FoM)
print('Om x S8 FoM = %1.3f'%Om_x_S8_FoM)

########################################################################
# Done
########################################################################
print('\nWriting output with final result to',new_output_name)

new_output.close()





