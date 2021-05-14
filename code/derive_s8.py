import numpy as np

# Uncomment the function below to compute statistics on w_pivot
# Will only work if you're using a chain with w0,wa free and if 
# postprocess has been run once already 
# (as it takes the parameter covariance as input)
'''
def derive_wp(chain):
    w0 = chain['cosmological_parameters--w']
    wa = chain['cosmological_parameters--wa']
    cov = np.loadtxt('covmat.txt')[6:8,6:8]
   
    cov_w0w0 = cov[0,0]
    cov_wawa = cov[1,1]
    cov_w0wa = cov[0,1]
    one_minus_ap = - cov_w0wa/cov_wawa
    cov_wpwp = cov_w0w0 - np.power(cov_w0wa,2)/cov_wawa

    wp = w0 + wa * one_minus_ap

    print '\n'
    print '\n > 1-ap = ',one_minus_ap
    print '\n > zp = ',one_minus_ap/(1-one_minus_ap)
    print '\n > sqrt(cov_wpwp)/sqrt(cov_w0w0) = ',np.sqrt(cov_wpwp)/np.sqrt(cov_w0w0)
    print '\n'
    return wp,"cosmological_parameters--wp"

'''
def derive_s8_fixed_alpha(chain):
    h=chain['cosmological_parameters--h0']
    return h*100,"cosmological_parameters--hubble"

def derive_hubble(chain):
    h=chain['cosmological_parameters--h0']
    return h*100,"cosmological_parameters--hubble"


def derive_s8_fixed_alpha(chain):
    alpha=0.586
    #0.50
    omega_m=chain['cosmological_parameters--omega_m']
    try:
        sigma_8=chain['COSMOLOGICAL_PARAMETERS--SIGMA_8']
    except KeyError:
        sigma_8=chain['COSMOLOGICAL_PARAMETERS--SIGMA_8']
    s8 = sigma_8 * (omega_m/0.3)**alpha
    return s8,"cosmological_parameters--s8_%.3f"%alpha

def derive_s8_fixed_alpha_kilbinger(chain):
    omega_m=chain['cosmological_parameters--omega_m']
    try:
        sigma_8=chain['COSMOLOGICAL_PARAMETERS--SIGMA_8']
    except KeyError:
        sigma_8=chain['COSMOLOGICAL_PARAMETERS--SIGMA_8']
    s8 = sigma_8 * (omega_m/0.27)**0.6
    return s8,"cosmological_parameters--s8_kilbinger"

def s8_col(sigma_8,omega_m,alpha):
    return sigma_8 * (omega_m/0.3)**alpha

def pca_min_direction(col1,col2,weights):
    samples_vector=np.array([col1,col2]).T
    deltas=(samples_vector-np.average(samples_vector.T,axis=1,weights=weights))
    cov=np.dot(deltas.T*weights,deltas)/np.sum(weights)
    e,v=np.linalg.eig(cov)
    smallest=np.argmin(e)
    return v[1,smallest]/v[0,smallest]

def derive_s8_find_alpha_pca(chain):
    omega_m,sigma_8=chain['cosmological_parameters--omega_m'],chain['COSMOLOGICAL_PARAMETERS--SIGMA_8']
    log_weights=np.zeros_like(omega_m)
    print( "Deriving ... ", chain.colnames)
    if 'old_weight' in chain.colnames :
        print( 'Log weights + old weight used')
        log_weights+=np.log(chain['old_weight'])+chain['log_weight']
    elif 'weight' in chain:
        log_weights+=np.log(chain['weight'])
    elif 'log_weight' in chain:
        log_weights+=chain['log_weight']
    log_weights -= log_weights.max()
    weights=np.exp(log_weights)
    alpha_pca = pca_min_direction(np.log(chain['COSMOLOGICAL_PARAMETERS--SIGMA_8']),
                                  np.log(chain['cosmological_parameters--omega_m']/0.3),
                                  weights)
    return s8_col(sigma_8,omega_m,alpha_pca), "cosmological_parameters--s8_%.3f"%alpha_pca                                                                 

