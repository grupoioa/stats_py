'''
Biblioteca de funciones de operaciones para estadísticos
'''

import numpy as np

def st_max(data, d_var, data_out,mydate):
    '''
    Calcula máximos para cada intervalo, para todas las temporalidades
    data: arreglo de datos a procesar
    d_var:variable
    data_out: diccionario de salida
    mydate: fecha de los datos
    '''
    tempos=[te for te in data_out[d_var].keys() if 'max' in te]
    #máximo del día
    data_max=np.amax(data, axis=0)
    for tempo in tempos:
        #define keys
        #día
        if 'max_per_d'==tempo:
            my_k=mydate.strftime('%m%d')
        #mes
        if 'max_per_m'==tempo:
            my_k=mydate.strftime('%m')
        #año
        if 'max_per_y'==tempo:
            my_k=mydate.strftime('%Y')
        #hora
        if 'max_per_h'==tempo:
            #para cada hora
            for my_h in range(24):
                my_k=mydate.strftime('%m')+"{:02}".format(my_h)
                #máximo entre el calculado y la hora actual
                np.fmax(data_out[d_var]['max_per_h'][my_k],
                        data[my_h],
                        out=data_out[d_var]['max_per_h'][my_k],
                        )
        else:
            np.fmax(data_out[d_var][tempo][my_k],
                    data_max,
                    out=data_out[d_var][tempo][my_k],
                    )

def st_min(data, d_var, data_out, mydate):
    '''
    Calcula mínimos para cada intervalo, para todas las temporalidades
    data: arreglo de datos a procesar
    d_var:variable
    data_out: diccionario de salida
    mydate: fecha de los datos
    '''
    tempos=[te for te in data_out[d_var].keys() if 'min' in te]
    #mínimo del día
    data_min=np.amin(data, axis=0)
    for tempo in tempos:
        #define keys
        #día
        if 'min_per_d' == tempo:
            my_k=mydate.strftime('%m%d')
        #mes
        if 'min_per_m'==tempo:
            my_k=mydate.strftime('%m')
        #año
        if 'min_per_y'==tempo:
            my_k=mydate.strftime('%Y')
        #hora
        if 'min_per_h'==tempo:
            #para cada hora
            for my_h in range(24):
                my_k=mydate.strftime('%m')+"{:02}".format(my_h)
                #mínimo entre el calculado y la hora actual
                np.fmin(data_out[d_var]['min_per_h'][my_k],
                        data[my_h],
                        out=data_out[d_var]['min_per_h'][my_k],
                        )
        else:
            np.fmin(data_out[d_var][tempo][my_k],
                    data_min,
                    out=data_out[d_var][tempo][my_k],
                    )

def st_acc(data, d_var, data_out, mydate):
    '''
    Calcula acumulado para cada intervalo, para todas las temporalidades
    data: arreglo de datos a procesar
    d_var:variable
    data_out: diccionario de salida
    mydate: fecha de los datos
    '''
    tempos=[te for te in data_out[d_var].keys() if 'acc' in te]
    #acumulado del día
    data_acc=np.sum(data, axis=0)
    for tempo in tempos:
        #define keys
        #día
        if 'acc_per_d' == tempo:
            my_k=mydate.strftime('%m%d')
        #mes
        if 'acc_per_m'==tempo:
            my_k=mydate.strftime('%m')
        #año
        if 'acc_per_y'==tempo:
            my_k=mydate.strftime('%Y')
        #hora
        if 'acc_per_h'==tempo:
            #para cada hora
            for my_h in range(24):
                my_k=mydate.strftime('%m')+"{:02}".format(my_h)
                #acumulado entre el calculado y la hora actual
                np.add(data_out[d_var]['avg_per_h'][my_k],
                        data[my_h],
                        out=data_out[d_var]['avg_per_h'][my_k],
                        )
                
                data_out[d_var]['cnt'+tempo[3:]][my_k]+=1
        else:
            np.add(data_out[d_var][tempo][my_k],
                    data_acc,
                    out=data_out[d_var][tempo][my_k],
                    )
            data_out[d_var]['cnt'+tempo[3:]][my_k]+=data.shape[0]

def st_avg(data_out):

    for d_var in data_out.keys():
        tempos=[te for te in data_out[d_var].keys() if 'avg' in te]
        for tempo in tempos:
            for k in data_out[d_var][tempo].keys():
                data_out[d_var][tempo][k]=data_out[d_var]['acc'+tempo[3:]][k]/data_out[d_var]['cnt'+tempo[3:]][k]
                #print('ndata:',tempo,data_out[d_var]['cnt'+tempo[3:]][k])
            del(data_out[d_var]['cnt'+tempo[3:]] )

def st_his(data, d_var, data_out, mydate):
    '''
    Calcula histograma para cada intervalo, para todas las temporalidades
    data: arreglo de datos a procesar
    d_var:variable
    data_out: diccionario de salida
    mydate: fecha de los datos
    '''
    tempos=[te for te in data_out[d_var].keys() if 'prc' in te]
    #acumulado del día
    data_acc=np.sum(data, axis=0)
    for tempo in tempos:
        #define keys
        #día
        if 'avg_per_d' == tempo:
            my_k=mydate.strftime('%m%d')
        #mes
        if 'avg_per_m'==tempo:
            my_k=mydate.strftime('%m')
        #año
        if 'avg_per_y'==tempo:
            my_k=mydate.strftime('%Y')
        #hora
        if 'avg_per_h'==tempo:
            #para cada hora
            for my_h in range(24):
                my_k=mydate.strftime('%m')+"{:02}".format(my_h)
                #acumulado entre el calculado y la hora actual
                np.add(data_out[d_var]['avg_per_h'][my_k],
                        data[my_h],
                        out=data_out[d_var]['avg_per_h'][my_k],
                        )
                
                data_out[d_var]['cnt'+tempo[3:]][my_k]+=1
        else:
            np.add(data_out[d_var][tempo][my_k],
                    data_acc,
                    out=data_out[d_var][tempo][my_k],
                    )
            data_out[d_var]['cnt'+tempo[3:]][my_k]+=data.shape[0]

