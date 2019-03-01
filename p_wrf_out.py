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
import subprocess
from plot_st import plot_stat

#genera keys para dict de días
def gen_d():
    idate=dt.datetime(2020,1,1)
    mydays=[]
    for i in range(366):
        mydate=idate+dt.timedelta(days=i)
        mydays.append(mydate.strftime("%m%d"))
    return tuple(mydays)

#genera keys para horas por mes
def gen_h():
    hrs=[]
    for i in range(12):
        for j in range(24):
            hrs.append("{:02}{:02}".format(i+1,j))
    return tuple(hrs)

#genera keys para dict de mes
def gen_m():
    m=[]
    for i in range(12):
        m.append("{:02}".format(i+1))
    return tuple(m)

#genera keys para dict de años
def gen_y(year,end_year):
    y=[]
    for i in range(year,end_year+1):
        y.append(str(i))
    return tuple(y)

#crea arreglos de salidas
#ocupa menos RAM si no es función
def create_out(data_vars, ops, tempo):
    data_out={}
    for v in data_vars:
        data_out[v]={}
        for op in ops:
            for t in tempo:
                data_out[v][op+t]={}
                if op=='max':
                    init_a=np.full(data_size,np.NINF,dtype=np.float)
                elif op=='min':
                    init_a=np.full(data_size,np.PINF,dtype=np.float)
                elif op=='acc':
                    init_a=np.zeros(data_size,dtype=np.float)
                else:
                    init_a=[]
                if t=='_per_h':
                    my_keys=gen_h()
                elif t=='_per_d':
                    my_keys=gen_d()

                elif t=='_per_m':
                    my_keys=gen_m()
                elif t=='_per_y':
                    my_keys=gen_y(1979,2017)

                for m in my_keys:
                    data_out[v][op+t][m] = np.copy(init_a)
    return data_out

def cal_max(data, d_var, data_out,mydate):
    '''
    Calcula máximos para cada intervalo
    '''
#hora
    if 'max_per_h' in data_out[d_var]:
        for my_h in range(24):
            my_k=mydate.strftime('%m')+"{:02}".format(my_h)
            data_out[d_var]['max_per_h'][my_k]=\
                np.amax([data_out[d_var]['max_per_h'][my_k],data[my_h]],
                        axis=0)

    data_max=np.amax(data, axis=0)
#reducir usando una función
#día
    if 'max_per_d' in data_out[d_var]:
        data_out[d_var]['max_per_d'][mydate.strftime('%m%d')]=\
                np.amax([data_out[d_var]['max_per_d'][mydate.strftime('%m%d')],data_max],
                        axis=0,
                        )
#mes
    if 'max_per_m' in data_out[d_var]:
        data_out[d_var]['max_per_m'][mydate.strftime('%m')]=\
                np.amax([data_out[d_var]['max_per_m'][mydate.strftime('%m')],data_max],
                        axis=0)
#año
    if 'max_per_y' in data_out[d_var]:
        data_out[d_var]['max_per_y'][mydate.strftime('%Y')]=\
                np.amax([data_out[d_var]['max_per_y'][mydate.strftime('%Y')],data_max],
                        axis=0)

def cfile(filename,data):
    print(data.shape)
    with Dataset(filename, "w", format="NETCDF4") as rootgrp:
        #tamaños
        time=rootgrp.createDimension("Time",None)
        lat=rootgrp.createDimension("south_north", data.shape[0])
        lon=rootgrp.createDimension("west_east",data.shape[1])
        #variables
        temp=rootgrp.createVariable(
                "T2",#nombre
                "f8",#tipo de dato
                ("Time","south_north","west_east"),#dimensiones
                )
        #Atributos
        rootgrp.description="TEst example"
        temp.units='C'
        #save data
        temp[0,:,:]=data
    return 0

itime=time.time()
#variables a procesar
 
data_vars=(
        "T2",#Temperatura
        #"RH",#Humedad Relativa
        #"RAIN",#lluvia
        #"U10",#viento componente U
        #"V10",#viento componente V
        #"SWDOWN",#Radiación de onda corta
        #"GLW",# Radiación de onda larga
        #"QFX",#Evaporación
        #"PBLH",#Altura de capa límite
        )
#vars=(
        #"T2",#Temperatura
        #"RAINC",#lluvia ??
        #"RAINNC",
        #"U10",#viento componente U
        #"V10",#viento componente V
        #"SWDOWN",#Radiación de onda corta
        #"GLW",# Radiación de onda larga
        #"QFX",#Evaporación
        ##"P",# perturbación de la presión
        #"PSFC",#Presión en superficie
        ##"PBLH",#Altura de capa límite
        #)
#tamaño de datos, leer de algún archivo?
data_size=(348,617)
#operaciones
ops=(
        'max',
        #'min',
        #'acc',
        #'per',
        #'his',
        )
#temporalidad de salidas
tempo=(
        '_per_h',
        '_per_d',
        '_per_m',
        #'_per_y',
        )
#diccionarios de salidas
data_out=create_out(data_vars,ops,tempo)
result = subprocess.check_output(['bash','-c', 'free -m']).decode('utf-8')
print(result)
print('init:',time.time()-itime)
#carpeta de datos
path=sys.argv[3]
data_n={}
proc_time=[]
#inicializa acumulador
for var in data_vars:
    data_n[var]=0
#formato de nombres de archivos
fmtdate= "a%Y/salidas/wrfout_c1h_d01_%Y-%m-%d_%H:%M:%S.a%Y"
#idate=dt.datetime(1982,1,1)
#edate=dt.datetime(1982,12,31)
#convierte intervalo de fechas
infmt="%Y%m%d"
idate=dt.datetime.strptime(sys.argv[1],infmt)
edate=dt.datetime.strptime(sys.argv[2],infmt)
print(idate,edate)
#ciclo de procesamiento por archivo
pdate=idate
file_count=0
err_count=0
while pdate<=edate:
    dayfile=path+pdate.strftime(fmtdate)
    print(dayfile)
    itime=time.time()
    data={}
    #file opening
    try:
        with Dataset(dayfile,'r') as root:
            #var loading
            for var in data_vars:
                data[var]=np.array(root[var][:])
    except:
        print('Error en la lectura')
        err_count+=1
        continue
    file_count+=1

    rtime=time.time()-itime
    itime=time.time()
    #Data processing
    for var in data_vars:
        if var=='T2':
            data[var]-=273.15
        cal_max(data[var],var,data_out,pdate)
        #data_max[var]=np.max(data[var],axis=0)
        #data_acc[var]=np.sum(data[var],axis=0)
        #data_n[var]+=data[var].shape[0]
        #data_perc[var]=np.percentile(data[var],[0.1,1,5,10,90,95,99,99.9])
        #data_histo[var]=np.histogram(data[var],bins=10)
    #T2max=np.sum(T2,axis=0)
    proc_time.append([rtime,time.time()-itime])
    pdate+=dt.timedelta(days=1)
    print(proc_time[-1])
    #print('data_max:', len(data_max), data_max["T2"].shape)
    #print('data_prom:', len(data_prom), data_prom["T2"].shape)
    #print('data_perc:', len(data_perc), data_perc["T2"].shape)
    #print('data_histo:',len(data_histo), data_histo["T2"])
    #print('data_n:', data_n)
#print('data:',data_out)

result = subprocess.check_output(['bash','-c', 'free -m']).decode('utf-8')
print(result)
#guardando tiempos
with open("time_rec.csv",'w') as tfile:
    pass
for d in proc_time:
    with open("time_rec.csv",'a') as tfile:
        print(d[0],d[1],sep=',',file=tfile)

print(file_count,"archivos procesados")
print(err_count,"archivos con errores")
itime=time.time()
#grafica por mes
for i in gen_m():
    plot_stat(data_out["T2"]["max_per_m"][i],
        "Temperatura máxima mes "+i+"\n1980-2016",
        "tmax_"+i+".png",
        )
#grafica por hora, enero
for i in range(24):
    j= "01{:02}".format(i)
    plot_stat(data_out["T2"]["max_per_h"][j],
        "Temperatura máxima enero, hora:  "+str(i)+"\n1980-2016",
        "tmax_"+j+".png",
        )
print("graficación:",time.time()-itime)
#guardando datos en archivo nc
for nvar in data_out.keys():
    for op_data in data_out[nvar].keys():
        for i in data_out[nvar][op_data].keys():
            nc_file='nc/'+nvar+op_data+i+'.nc'
            print(nc_file)
            cfile(nc_file,data_out[nvar][op_data][i])
