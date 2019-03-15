# IOA python stats (V0.1.0)

Generación de estadísticos: mínimas, máximas, promedios y percentiles de las salidas del WRF generadas en el grupo IOA . 


## Primeros pasos
Estas rutinas están diseñadas para correr en el cluster y con los datos en la carpeta /CHACMOOL/DATOS/ y se debe verificar que se encuentran instaladas las bibliotecas necesarias.
En caso de no encontrar las bibliotecas es recomendable instalarlas mediante un ambiente en conda.
Para instalar un ambiente en conda se debe ejecutar:

*conda create --name myenv*

### Prerrequisitos
Se requieren las siguientes bibliotecas
* numpy
* netCDF4

#### Instalación
Se pueden instalar mediante pip o mediante conda (recomendado)

##### Para numpy:
*conda install -c anaconda numpy*

o para instalar en un ambiente (p. ej. myenv):

*conda install -n myenv -c anaconda numpy*

##### Para netCDF4:
*conda install -c anaconda netcdf4*

o para instalar en un ambiente (p. ej. myenv):

*conda install -n myenv -c anaconda netcdf4*

## Probando

El archivo p_wrf_out.sh ejecuta el script p_wrf_out.py en el cluster. 
Dentro de p_wrf_out.sh se configura la ejecución y se establece la fecha de inicio, fecha de fin y la carpeta donde se encuentran los datos. Por ejemplo, la instrucción:

*srun python p_wrf_out.py 19800101 19801231 '/CHACMOOL/DATOS/'*

Ejecuta el script para el intervalo del 1 de enero de 1980 al 31 de diciembre de 1980, con los datos en */CHACMOOL/DATOS/*

## Deployment

???
Agregue notas adicionales sobre cómo implementar esto en un sistema en vivo

## Para contribuir

Link a los estándares para contribuir, como referencia se puede usar este link [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426)
Debe ser para obtener detalles sobre nuestro código de conducta y el proceso para enviar pull request.


## Autores

* **Miguel Ángel Robles R.** *Initial work*

Vea también la lista de [colaboradores]

## Licencia

Este proyecto está licenciado bajo la licencia MIT; consulte el archivo [LICENSE.md] (LICENSE.md) para obtener detalles

## Colaboradores/Agradecimientos??

* *Raul Medina*
* *Sam*
* *Olmo*
* ???
