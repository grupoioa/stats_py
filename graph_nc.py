import sys
from netCDF4 import Dataset
import numpy as np
from plot_st import plot_stat


if __name__ == "__main__":
    filenames=sys.argv[1:]
    for filename in filenames:
        with Dataset(filename, "r", format="NETCDF4") as rootgrp: 
            print(rootgrp['T2'])
            data=np.array(rootgrp['T2'])
        print(data.shape)

        plot_stat(data[0],
            #"Temperatura máxima por mes intervalo 1980-2016\n"+"marzo",
            "Temperatura máxima por mes intervalo 1980-2016\n"+filename.split('/')[-1],
            filename.split('/')[-1].split('.')[0]+".png",
            )
