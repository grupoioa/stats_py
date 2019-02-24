#author: Miguel Angel Robles Roldan

'''
Procesamiento de datos NETCDF de salidas de pronóstico por día.
Toma como parámetros fecha de inicio, fecha de fin y ruta
    python by_day.py 19810101 19811231 /CHACMOOL/DATOS/

'''

import sys
import multiprocessing as mp
from netCDF4 import Dataset
import numpy as np
import time
import datetime as dt

filenames=sys.argv[1:]
vars=(
        "T2",#Temperatura
        "RAINC",#lluvia ??
        "RAINNC",
        "U10",#viento componente U
        "V10",#viento componente V
        "SWDOWN",#Radiación de onda corta
        "GLW",# Radiación de onda larga
        "QFX",#Evaporación
        "P",
        "PSFC",
        #"PBLH",#Altura de capa límite
        )
data={}
data_max={}
data_acc={}
data_n={}
data_perc={}
data_histo={}
proc_time=[]
for var in vars:
    data_n[var]=0

try:
    path=sys.argv[3]
except:
    path='/CHACMOOL/DATOS/'
fmtdate= "a%Y/salidas/wrfout_c1h_d01_%Y-%m-%d_%H:%M:%S.a%Y"
#idate=dt.datetime(1982,1,1)
#edate=dt.datetime(1982,12,31)
infmt="%Y%m%d"
idate=dt.datetime.strptime(sys.argv[1],infmt)
edate=dt.datetime.strptime(sys.argv[1],infmt)
print(idate,edate)

pdate=idate
while pdate<=edate:
#for n,dayfile in enumerate(filenames[:10]):
    dayfile=path+pdate.strftime(fmtdate)
    print(dayfile)
    itime=time.time()
    #file opening
    root = Dataset(dayfile,'r')
    #file info
    #print(root.data_model)
    #print(root.dimensions)
    #print(root.variables.keys())
    #var loading
    for var in vars:
        data[var]=np.array(root[var][:])

    root.close()
    rtime=time.time()-itime
    itime=time.time()
    #Data processing
    for var in vars:
        data_max[var]=np.max(data[var],axis=0)
        data_acc[var]=np.sum(data[var],axis=0)
        data_n[var]+=data[var].shape[0]
        data_perc[var]=np.percentile(data[var],[0.1,1,5,10,90,95,99,99.9])
        data_histo[var]=np.histogram(data[var],bins=10)
    #T2max=np.sum(T2,axis=0)
    proc_time.append([rtime,time.time()-itime])
    pdate+=dt.timedelta(days=1)
    print(proc_time[-1])
    print('data:',len(data))
    print('data_max:', len(data_max), data_max["T2"].shape)
    #print('data_prom:', len(data_prom), data_prom["T2"].shape)
    #print('data_perc:', len(data_perc), data_perc["T2"].shape)
    #print('data_histo:',len(data_histo), data_histo["T2"])
    #print('data_n:', data_n)

#saving times
with open("time_rec.csv",'w') as tfile:
    pass
for d in proc_time:
    with open("time_rec.csv",'a') as tfile:
        print(d[0],d[1],sep=',',file=tfile)

