#!/bash

export BASE=/Users/hattifattener/Documents/y3cosmicshear

export D0M0=$BASE"/chains/ias_fid/fidm/mnla_dtatt/chain_1x2pt_hyperrank_2pt_SOMPZWZsamples_pit_goodlowz_shifted_1000samples_ramped.055_PITfix_sim_noiseless_GCharSmail_SIMULATED.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt"
export D0M1=$BASE"/chains/ias_fid/fidm/mtatt_dtatt/chain_1x2pt_hyperrank_2pt_SOMPZWZsamples_pit_goodlowz_shifted_1000samples_ramped.055_PITfix_sim_noiseless_GCharSmail_SIMULATED.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt"
export D1M0=$BASE"/chains/ias_fid/fidm/mnla_dnla/chain_1x2pt_hyperrank_2pt_SOMPZWZsamples_pit_goodlowz_shifted_1000samples_ramped.055_PITfix_sim_noiseless_GCharSmail_SIMULATED_NLA.fits_scales_3x2pt_0.5_8_6_v0.4.ini_lcdm.txt"


cd /Users/hattifattener/cosmosis
source config/setup-cosmosis

cd /Users/hattifattener/Documents/y3cosmicshear

postprocess -o sim_iatest --factor-kde 1.1 --no-plots -f pdf --extra plotting/cosmosis_iatest.py $D0M0 $D0M1 $D1M0