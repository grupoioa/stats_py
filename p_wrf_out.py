#author: Miguel Angel Robles Roldan

'''
Procesamiento de datos NETCDF de salidas de pronóstico por día.
Toma como parámetros fecha de inicio, fecha de fin y ruta
    python by_day.py 19810101 19811231 /CHACMOOL/DATOS/

'''

import sys
import multiprocessing as mpk
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

#crea arreglos de salidas
#ocupa menos RAM si no es función
def create_out(data_vars, ops, tempo, años):
    '''
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
                        elif v=='WIND':
                            data_out[v][op+t][m]=np.zeros(80, dtype=np.uint32)
                            
                    #data_out[v][op+t][m] = np.copy(init_a)
    return data_out

def cal_max(data, d_var, data_out,mydate):
    '''
    Calcula máximos para cada intervalo, para todas las temporalidades
    data: arreglo de datos a procesar
    d_var:variable
    data_out: diccionario de salida
    mydate: fecha de los datos
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

itime=time.time()
#variables a procesar
 
data_vars=(
        "T2",#Temperatura
        "RH",#Humedad Relativa
        #"RAIN",#lluvia
        "W",#viento
        "SWDOWN",#Radiación de onda corta
        "GLW",# Radiación de onda larga
        "QFX",#Evaporación
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
print(idate,edate)
#diccionarios de salidas
años=(idate.strftime("%Y"),edate.strftime("%Y"))
data_out=create_out(data_vars,ops,tempo,años)
result = subprocess.check_output(['bash','-c', 'free -m']).decode('utf-8')
print(result)
print('init:',time.time()-itime)
#carpeta de datos
path=sys.argv[3]
proc_time=[]
#ciclo de procesamiento por archivo
pdate=idate
file_count=0
err_count=0
while pdate<=edate:
    dayfile=path+pdate.strftime(fmtdate)
    itime=time.time()
    cals_time=0
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
    #file opening
    with Dataset(dayfile,'r') as root:
        #var loading
        for var in data_vars:
            if var=='RH':
                P=np.array(root['PSFC'][:])
                Q=np.array(root['Q2'][:])
                T=np.array(root['T2'][:])
                itimec=time.time()
                data['RH']=(0.263*P*Q)/np.exp(17.67*(T-273.15)/(T-29.65))
                np.clip(data['RH'],0,100,out=data['RH'])
                cals_time+=time.time()-itimec
            elif var=='W':
                U=np.array(root['U10'][:])
                V=np.array(root['V10'][:])
                itimec=time.time()
                data['W']=np.sqrt(np.square(V)+np.square(U))
                cals_time+=time.time()-itimec
            else:
                data[var]=np.array(root[var][:])
    #except:
    file_count+=1

    rtime=time.time()-itime
    itime=time.time()
    #Data processing
    for var in data_vars:
        if var=='T2':
            data[var]-=273.15
        st_ops.st_max(data[var],var,data_out,pdate)
        st_ops.st_min(data[var],var,data_out,pdate)
        st_ops.st_acc(data[var],var,data_out,pdate)
        #data_histo[var]=np.histogram(data[var],bins=10)
    proc_time.append([rtime,time.time()-itime])
    pdate+=dt.timedelta(days=1)
    print(proc_time[-1], 'cals:',cals_time)
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
