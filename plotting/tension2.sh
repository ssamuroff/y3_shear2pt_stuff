#!/bash

export BASE=/physics2/ssamurof/cosmosis/sws/ias/chains/NG/

export DES=$BASE"/multicolour/real/tatt/out_mixed-3x2pt-tatt-cov_v16-sortofNG-multinest.txt"
export COMB="/physics2/ssamurof/y1cosmicshear/code/out_jointlike-mixed-3x2pt-tatt+planck15.txt"
export PLANCK=/home/ssamurof/misc/other_peoples_datasets/planck15/chains/out_planck15_TTTEEE-mnu-multinest.txt

cd /home/ssamurof/cosmosis
source config/setup-cosmosis

cd $BASE"/plotting/scripts"

postprocess -o tension-multicolour-tatt --factor-kde 1.2 --no-plots -f pdf --extra tension-tatt.py $DES $PLANCK $COMB