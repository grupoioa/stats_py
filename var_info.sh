#!/bin/bash
#SBATCH -J test
#SBATCH -p workq2
##SBATCH -N 1
##SBATCH --ntask-per-node 1
#SBATCH -o info.out
#SBATCH -e info.err
module load herramientas/python/3.6

PATH=/home/mroldan/.conda/envs/carto/bin:$PATH

#conda activate carto
ls /KRAKEN/DATOS/a1979/salidas/wrfout_c1h*
srun python var_info.py "/CHACMOOL/DATOS/a1979/salidas/wrfout_c1h_d01_1979-12-01_00:00:00.a1979"
#conda deactivate
