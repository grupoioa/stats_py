import sys
from netCDF4 import Dataset
import numpy as np
from plot_st import plot_stat


if __name__ == "__main__":
    filenames=sys.argv[1:]
    print(filenames)
    for i,filename in enumerate(filenames):
        print(filename)
        k='PREC2_MAX' #para raul v4
        #k='T2'# para el mío
        with Dataset(filename, "r", format="NETCDF4") as rootgrp: 
            data=np.array(rootgrp[k])
        print(data.shape)

        plot_stat(data[0],
            #"Temperatura máxima por mes intervalo 1980-2016\n"+"marzo",
            "Temperatura máxima por mes intervalo 1980-2016\n"+filename.split('/')[-1],
            filename.split('/')[-1].split('.')[0]+".png",
            )
