#!/bash

export BASE=/Users/hattifattener/Documents/y3cosmicshear

export NLA_1x2pt='/Volumes/groke/work/chains/y3/real/robustnesstests/chain_1x2pt_nla.txt'
export TATT_1x2pt='/Volumes/groke/work/chains/y3/real/chain_1x2pt_lcdm.txt'
export NLA_3x2pt='/Volumes/groke/work/chains/y3/real/robustnesstests/chain_3x2pt_nla.txt'
export TATT_3x2pt='/Volumes/groke/work/chains/y3/real/chain_3x2pt_lcdm.txt'

cd /Users/hattifattener/cosmosis
source config/setup-cosmosis

cd /Users/hattifattener/Documents/y3cosmicshear

postprocess -o ia_models_3x2pt --factor-kde 1.1 --no-plots -f pdf --extra plotting/all-models-3x2pt-TATT-S8.py $NLA_3x2pt $TATT_3x2pt

postprocess -o ia_models_1x2pt --factor-kde 1.1 --no-plots -f pdf --extra plotting/all-models-1x2pt-TATT-S8.py $NLA_1x2pt $TATT_1x2pt