import sys
from netCDF4 import Dataset
import numpy as np
from plot_st import plot_stat


if __name__ == "__main__":
    filename=sys.argv[1]
    with Dataset(filename, "r") as rootgrp: 
        data=np.array(rootgrp['T2'])

    for i in range(12):
        filename2="nc/T2max_per_m{:02}.nc".format(i+1)
        with Dataset(filename2, "r") as rootgrp: 
            data2=np.array(rootgrp['T2'])
        print(data.shape,data2.shape)
        plot_stat(data[i]-data2[0],
            "Diferencia de Temperatura máxima por mes intervalo 1980-2016\nMes "+str(i+1),
            "T2dif_max_per_m{:02}.png".format(i+1),
            )
