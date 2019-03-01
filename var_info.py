#author: Miguel Angel Robles Roldan

'''
Info de variables, parámetros: nombre de archivo.
    python var_info.py /CHACMOOL/DATOS/abc.nc

'''

import sys
from netCDF4 import Dataset
import numpy as np
import time
import datetime as dt

#variables a procesar
vars=(
        "T2",#Temperatura
        "RAINC",#lluvia ??
        "RAINNC",
        "U10",#viento componente U
        "V10",#viento componente V
        "SWDOWN",#Radiación de onda corta
        "GLW",# Radiación de onda larga
        "QFX",#Evaporación
        "P",# perturbación de la presión
        "PSFC",#Presión en superficie
        #"PBLH",#Altura de capa límite
        )
filename=sys.argv[1]
#file opening
root = Dataset(filename,'r')
#file info
print(root.data_model)
print(root.dimensions)
print(root.variables.keys())
#var loading
for var in vars:
    print(var, root[var][:].shape)
root.close()

