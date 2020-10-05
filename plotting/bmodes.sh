
cd /home/ssamurof/cosmosis
source config/setup-cosmosis

cd /physics2/ssamurof/y3_shear2pt_stuff/chains/

export B0=out_Y3-Bmodes-1x2pt.txt
export B1=out_Y3-Bmodes-1x2pt-withbmodes-fidparams.txt

postprocess --factor-kde=1.1 -o ~/tmp/y3_bmodes --no-plots --extra ../plotting_scripts/bmodes.py $B0 $B1

postprocess --factor-kde=1.1 -o ~/tmp/y3_bmodes --no-plots --extra ../plotting_scripts/bmodes_ia.py $B0 $B1 


