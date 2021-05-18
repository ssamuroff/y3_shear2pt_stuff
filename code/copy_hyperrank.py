import numpy as np
import fitsio as fi


f = fi.FITS('sim_3x2pt_withsompz_TATT_half_noisy.fits', 'rw')
f0 = fi.FITS('2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits')

for i,h in enumerate(f0[1:]):
    hdr = h.read_header()
    name = hdr['EXTNAME']
    if not 'nz_source_realisation' in name:
        continue

    r = f0[name].read()

    f.write(r)
    f[-1].write_key('EXTNAME',name)

    print(i)

f0.close()
f.close()
print('Done')

    

    
