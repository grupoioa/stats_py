import sys
from netCDF4 import Dataset
import numpy as np
from plot_st import plot_stat


if __name__ == "__main__":
    filename=sys.argv[1]
    with Dataset(filename, "r", format="NETCDF4") as rootgrp: 
        print(rootgrp['T2'])
        data=np.array(rootgrp['T2'])
    print(data.shape)

    for i in range(12):
        plot_stat(data[i],
            "Temperatura máxima por mes intervalo 1980-2016\n"+str(i+1),
            "T2max_per_m{:02}_ncl.png".format(i+1),
            )
