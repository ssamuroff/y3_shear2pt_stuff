import numpy as np



def derive_a1delta(chain):
    alpha=0.50
    A1 = chain['intrinsic_alignment_parameters--a1']
    try:
        b = chain['intrinsic_alignment_parameters--bias_ta']
    except:
        b = 0.

    return A1*b,"intrinsic_alignment_parameters---a1delta"


