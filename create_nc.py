from netCDF4 import Dataset

metadata={}
metadata['T2']={
        'units':'C',
        'standard_name':'Air temperature',
        'long_name':'Air temperature',
        'description': ' Air Temperature at 2 m',
        'dtype':"f8",
        }
metadata['U10']={
        'units':'m s-1',
        'standard_name':'eastward_wind',
        'long_name':'eastward_wind',
        'description': 'U at 10 m',
        'dtype':"f8",
        }
metadata['V10']={
        'units':'m s-1',
        'standard_name':'northward_wind',
        'long_name':'northward_wind',
        'description': 'V at 10 m',
        'dtype':"f8",
        }
metadata['PREC2']={
        'units':'mm',
        'standard_name':'Precipitation',
        'long_name':'Precipitation',
        'description': 'Precipitation',
        'dtype':"f8",
        }
metadata['RH']={
        'units':'%',
        'standard_name':'Relative Humidity',
        'long_name':'Relative Humidity',
        'description': 'Relative Humidity',
        'dtype':"f8",
        }
#metadata['']={
        #'units':'',
        #'standard_name':'',
        #'long_name':'',
        #'description': '',
        #'dtype':"f8",
        #}

def create_empty(filename,data_size=(348,617)):
    '''
    crea archivo .nc
    agrega lat y lon
    '''
    with Dataset(filename, 'w', format="NETCDF4") as rootgrp:
        #dimensiones
        time=rootgrp.createDimension("Time",None)
        lat=rootgrp.createDimension("south_north", data_size[0])
        lon=rootgrp.createDimension("west_east",data_size[1])
        #Atributos
        rootgrp.description="Cálculo de estadísticos"
    return 0

def create_all( tempo, data_out, path='./', metadata=metadata):
    '''
    crea un archivo por temporalidad y los llena con los datos en data_out
    tempo, temporalidades
    data_out, diccionario con datos
    path, carpeta/prefijo donde se almacenaran los archivos
    '''
    for t in tempo:
        filename=path+'st'+t+'.nc'
        create_empty(filename)
        for nvar in data_out.keys():
            #filtro para operación actual
            ops = [op for op in data_out[nvar].keys() if t in op] 
            for op_data in ops:
                #crea una variable 
                var_name=nvar+'_'+op_data
                with Dataset(filename,'a',format="NETCDF4") as root:
                    var=root.createVariable(
                            var_name,#nombre
                            metadata[nvar]['dtype'],#tipo de dato
                            ("Time","south_north","west_east"),#dimensiones
                            )
                    #atrr
                    var.units=metadata[nvar]['units']
                    var.standard_name=metadata[nvar]['standard_name']
                    var.long_name=metadata[nvar]['long_name']
                    var.description=metadata[nvar]['description']
                    for i,k_tempo in enumerate(sorted(data_out[nvar][op_data].keys())):
                        var[i,:,:]=data_out[nvar][op_data][k_tempo]

    return 0

