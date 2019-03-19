#!/bin/bash
#SBATCH -J test
#SBATCH -p workq2
##SBATCH -N 1
##SBATCH --ntask-per-node 1
#SBATCH -o graph.out
#SBATCH -e graph.err
module load herramientas/python/3.6

PATH=/home/mroldan/.conda/envs/carto/bin:$PATH

srun python graph_dif2.py /home/rmedina/out/maximasMes/Maximas_Mes-Promedio_Maximas_Mes_Rv4.nc ./st_per_m.nc QFX_MAX QFX_max_per_m
srun python graph_dif2.py /home/rmedina/out/promediosMes/Promedios_Mes_Rv4.nc ./st_per_m.nc QFX QFX_avg_per_m
#srun python graph_dif2.py /home/rmedina/out/maximasMes/Maximas_Mes-Promedio_Maximas_Mes_Rv4.nc ./st_per_m.nc MAGNITUD_VIENTO_MAX W_max_per_m
#srun python graph_dif2.py /home/rmedina/out/promediosMes/Promedios_Mes_Rv4.nc ./st_per_m.nc MAGNITUD_VIENTO W_avg_per_m
#srun python graph_dif2.py /home/rmedina/out/promediosMes/Promedios_Mes_Rv4_RH.nc ./st_per_m.nc RH RH_avg_per_m
#srun python graph_dif2.py /home/rmedina/out/maximasMes/Maximas_Mes-Promedio_Maximas_Mes_Rv4.nc ./st_per_m.nc RH_MAX RH_max_per_m
#srun python graph_dif2.py /home/rmedina/out/minimasMes/Minimas_Mes-Promedio_Minimas_Mes_Rv4.nc ./st_per_m.nc
#srun python graph_dif2.py /./home/rmedina/out/promediosMes/Promedios_Mes_Rv4.nc st_per_m.nc
