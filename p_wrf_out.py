#author: Miguel Angel Robles Roldan

'''
Procesamiento de datos NETCDF de salidas de pronóstico por día.
Toma como parámetros fecha de inicio, fecha de fin y ruta de datos de entrada
    python by_day.py 19810101 19811231 /CHACMOOL/DATOS/

'''

import sys
import multiprocessing as mp
from netCDF4 import Dataset
import numpy as np
import time
import datetime as dt
import subprocess
import create_nc as nc
import st_ops 

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

def create_out(data_vars, ops, tempo, años):
    '''
    Crea arreglo para almacenar datos de salida
    data_vars: variables
    ops: operaciones
    tempo: temporalidades
    dt: (año inicio,año fin)
    '''
    data_out={}
    for v in data_vars:
        data_out[v]={}
        for op in ops:
            for t in tempo:
                data_out[v][op+t]={}
                if t=='_per_h':
                    my_keys=gen_h()
                elif t=='_per_d':
                    my_keys=gen_d()

                elif t=='_per_m':
                    my_keys=gen_m()
                elif t=='_per_y':
                    my_keys=gen_y(años[0],años[1])

                for m in my_keys:
                    if op=='max':
                        data_out[v][op+t][m]=np.full(data_size,np.NINF,dtype=np.float)
                    elif op=='min':
                        data_out[v][op+t][m]=np.full(data_size,np.PINF,dtype=np.float)
                    elif op=='avg':
                        data_out[v][op+t][m]=np.zeros(data_size,dtype=np.float)
                    elif op=='cnt':
                        data_out[v][op+t][m]=np.zeros(1, dtype=np.uint16)
                    elif op=='prc':
                        if v=='T2':
                            data_out[v][op+t][m]=np.zeros(70, dtype=np.uint32)
                        elif v=='RAIN':
                            data_out[v][op+t][m]=np.zeros(80, dtype=np.uint32)
                        elif v=='WS':
                            data_out[v][op+t][m]=np.zeros(80, dtype=np.uint32)
                            
                    #data_out[v][op+t][m] = np.copy(init_a)
    return data_out

def load_data(dayfile, data_vars ):
    '''
    lee datos del archivo de entrada y los carga en el diccionario de salida
    data_vars: diccionario de salida
    dayfile: archivo de entrada 
    return: tupla de tiempos (lectura,procesamiento)
    '''
    tread=0
    tproc=0
    #file opening
    with Dataset(dayfile,'r') as root:
        for var in data_vars:
            tread_i=time.time()
            if var=='T2':
                data['T2']=np.array(root['T2'][:])
                tproc_i=time.time()
                tread+=tread_i-tproc_i
                data['T2']-=273.15
                tproc+=tproc_i-time.time()

            if var=='RH':
                P=np.array(root['PSFC'][:])
                Q=np.clip(np.array(root["Q2"][:]),a_min=0,a_max=None,)
                T=np.array(root['T2'][:])
                tproc_i=time.time()
                tread+=tread_i-tproc_i
                ez=611.2
                eps=0.622
                Es=ez*np.exp(17.67*(T-273.15)/(T-29.65))
                Qvs=eps*Es/(P-(1-eps)*Es)
                data['RH']=100*Q/Qvs
                np.clip(data['RH'],0,100,out=data['RH'])
                tproc+=tproc_i-time.time()
            elif var=='WS':
                U=np.array(root['U10'][:])
                V=np.array(root['V10'][:])
                tproc_i=time.time()
                tread+=tread_i-tproc_i
                data['WS']=np.sqrt(np.square(V)+np.square(U))
                tproc+=tproc_i-time.time()
            else:
                data[var]=np.array(root[var][:])
                tread+=tread_i-time.time()
    return (tread,tproc)

itime=time.time()
#variables a procesar
 
data_vars=(
        "T2",#Temperatura
        "RH",#Humedad Relativa
        #"RAIN",#lluvia
        "WS",#viento
        "SWDOWN",#Radiación de onda corta
        "GLW",# Radiación de onda larga
        "QFX",#Evaporación
        #"PBLH",#Altura de capa límite
        )
#tamaño de datos, leer de algún archivo?
data_size=(348,617)
#operaciones
ops=(
        'max',
        'min',
        'avg',
        'cnt',
        #'prc',
        #'his',
        )
#temporalidad de salidas
tempo=(
        '_per_h',
        '_per_d',
        '_per_m',
        #'_per_y',
        )
#formato de nombres de archivos
fmtdate= "a%Y/salidas/wrfout_c1h_d01_%Y-%m-%d_%H:%M:%S.a%Y"
#convierte intervalo de fechas
infmt="%Y%m%d"
idate=dt.datetime.strptime(sys.argv[1],infmt)
edate=dt.datetime.strptime(sys.argv[2],infmt)
print('Procesando intervalo:',idate,edate)
#diccionarios de salida
años=(idate.strftime("%Y"),edate.strftime("%Y"))
data_out=create_out(data_vars,ops,tempo,años)
#consumo de RAM
result = subprocess.check_output(['bash','-c', 'free -m']).decode('utf-8')
print(result)

#tiempo
print('tiempo de inicialización:',time.time()-itime)
proc_time=[]

#carpeta de datos de entrada
path=sys.argv[3]
#ciclo de procesamiento por archivo
pdate=idate
file_count=0
err_count=0
while pdate<=edate:
    #tiempos
    itime=time.time()
    cals_time=0

    dayfile=path+pdate.strftime(fmtdate)
    data={}
    #file test
    try:
        with open(dayfile,'r') as pfile:
            print(dayfile)
    except:
        print('Archivo no encontrado: ',dayfile)
        err_count+=1
        pdate+=dt.timedelta(days=1)
        continue
    init_time=time.time()-itime
    #data loading
    rtime,ptime=load_data(dayfile,data_vars)

    itime=time.time()
    file_count+=1
    #Data processing
    for var in data_vars:
        st_ops.st_max(data[var],var,data_out,pdate)
        st_ops.st_min(data[var],var,data_out,pdate)
        st_ops.st_acc(data[var],var,data_out,pdate)
        #data_histo[var]=np.histogram(data[var],bins=10)
    pdate+=dt.timedelta(days=1)
    #guarda tiempos (inicial,lectura,procesamiento)
    proc_time.append([init_time, rtime, ptime+time.time()-itime])
    print(proc_time[-1])
st_ops.st_avg(data_out)
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
#guardando datos en archivo nc
itime=time.time()

#create files
nc.create_all(tempo,data_out,)
print("guardado:",time.time()-itime)
