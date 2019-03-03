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
#srun python p_wrf_out.py 19800101 20161231 '/CHACMOOL/DATOS/'
#srun python graph_nc.py nc/T2max_per_m*.nc
srun python graph_nc.py /home/rmedina/out/maximasMes/meses/Maximas_Mes_Rv4_*
#conda deactivate
