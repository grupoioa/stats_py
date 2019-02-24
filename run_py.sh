#!/bin/bash
##SBATCH -J test
##SBATCH -p workq2
##SBATCH -N 1
##SBATCH --ntask-per-node 5
##SBATCH -t 0-2:00
##SBATCH -o slurm.%x.%j.out
##SBATCH -e slurm.%x.%j.err

module load herramientas/python/3.6 

#srun --cpus-per-task=1 -pworkq2 -l python by_day.py /CHACMOOL/DATOS/a1982/salidas/wrfout_c1h*
srun --cpus-per-task=1 -pworkq2 -l -o by_day.out python by_day.py 

