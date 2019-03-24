# IOA python stats (V0.1.0)

Generación de estadísticos: mínimas, máximas, promedios y percentiles de las salidas del WRF generadas en el grupo IOA. 


## Primeros pasos
Estas rutinas están diseñadas para correr en el cluster, con acceso a los datos desde él (actualmente en /CHACMOOL/DATOS/).
Se debe verificar que se encuentran instaladas las bibliotecas necesarias, las cuales se especifican en [Prerrequisitos](#Prerrequisitos).
En caso de no encontrar las bibliotecas es recomendable instalarlas mediante un ambiente en conda.
Para instalar un ambiente en conda se debe ejecutar:

*conda create --name myenv*

### Prerrequisitos
Se requieren las siguientes bibliotecas
* numpy
* netCDF4

#### Instalación
Se pueden instalar mediante pip o mediante [conda](https://conda.io) (recomendado)

##### Para numpy:
*conda install -c anaconda numpy*

o para instalar en un ambiente (p. ej. myenv):

*conda install -n myenv -c anaconda numpy*

##### Para netCDF4:
*conda install -c anaconda netcdf4*

o para instalar en un ambiente (p. ej. myenv):

*conda install -n myenv -c anaconda netcdf4*

## Deployment

El archivo p_wrf_out.sh ejecuta el script p_wrf_out.py en el cluster. 
Dentro de p_wrf_out.sh se configura la ejecución y se establece la fecha de inicio, fecha de fin y la carpeta donde se encuentran los datos. Por ejemplo, la instrucción:

*srun python p_wrf_out.py 19800101 19801231 '/CHACMOOL/DATOS/'*

Ejecuta el script para el intervalo del 1 de enero de 1980 al 31 de diciembre de 1980, con los datos en */CHACMOOL/DATOS/*

## Para contribuir

Para información sobre cómo ayudar o publicar errores vea [CONTRIBUTING.md](https://github.com/grupoioa/stats_py/blob/master/CONTRIBUTING.md).

## Autores

* **Miguel Ángel Robles R.** 

Vea también la lista de [colaboradores](https://github.com/grupoioa/stats_py/graphs/contributors)

## Agradecimientos
La primera versión de este código fue hecha en NCL y publicada en [https://github.com/rmedina09/HitoAtlasGolfoMexico](https://github.com/rmedina09/HitoAtlasGolfoMexico), agradecemos a Raul Medina por facilitar detalles sobre el código. Asímismo agradecemos a Olmo Zavala por su contribución en el desarrollo del proyecto.
