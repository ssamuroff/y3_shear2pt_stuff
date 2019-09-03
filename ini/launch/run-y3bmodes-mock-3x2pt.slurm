#!/bin/bash 
#SBATCH -J Y3-Bmodes-3x2pt
#SBATCH -N 2
#SBATCH --ntasks-per-node=16
#SBATCH --constraint intel_e5_v4 
#SBATCH --partition long
#SBATCH -t 80:00:00
#SBATCH -o /home/ssamurof/logs/y3-all-mock-3x2pt-bmodes.log

cd /home/ssamurof/cosmosis/
source config/setup-cosmosis
cd /physics2/ssamurof/y3_shear2pt_stuff/chains

export DATAFILE=../data/simulated_y3_tatt_c1_1_c2_m5_alpha1_1_alpha2_1_bmodes.fits
export SAVEFILE=$SLURM_JOB_NAME
export VALUESFILE=../ini/params/values-y3-tatt.ini
export PRIORSFILE=../ini/prios/priors-y3.ini

export PARAMFILE=../ini/params/params-3x2pt-tatt-bmodes.ini

mpiexec -n 32 cosmosis $PARAMFILE --mpi -p runtime.sampler=multinest output.lock=F multinest.resume=F 