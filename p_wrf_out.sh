#!/bin/bash
#SBATCH -J test
#SBATCH -p workq2
##SBATCH -N 1
##SBATCH --ntask-per-node 1
#SBATCH -o ptest.out
#SBATCH -e ptest.err
module load herramientas/python/3.6

PATH=/home/mroldan/.conda/envs/carto/bin:$PATH

#conda activate carto
srun python p_wrf_out.py 19790101 20171231 '/CHACMOOL/DATOS/'
#srun python p_wrf_out.py 19800101 19801231 '/CHACMOOL/DATOS/'
#conda deactivate
