import matplotlib.pyplot as plt
from matplotlib import cm
from netCDF4 import Dataset
import numpy as np

from cartopy import config
import cartopy.crs as ccrs
from cartopy.feature import NaturalEarthFeature
from cartopy import feature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
#from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib as mpl

import time

def plot_stat(data,title, ofilename):
    itime=time.time()
#coordinate file 
    cname='/CHACMOOL/DATOS/a1980/salidas/wrfout_c_anio_d01_1980-01-01_00:00:00.a1980'
    cdataset=Dataset(cname)
    lats = cdataset.variables['XLAT'][0,:]
    lons = cdataset.variables['XLONG'][0,:]
    print('data:',data.shape)
    print('load coors:',time.time()-itime)
    itime=time.time()
#extract data
    print('load data:',time.time()-itime)
    itime=time.time()

#plot config
#dpi=100
#plt.figure(figsize=(1024/100,768/100),
    plt.figure(figsize=(1130/100,720/100),
            #tight_layout=True,
            )
    plt.subplots_adjust(left=0.03,right=1.0,top=0.89,bottom=-0.03)
#ax = plt.axes(projection=ccrs.Mercator())
    ax = plt.axes(projection=ccrs.PlateCarree())
    states = NaturalEarthFeature(category="cultural", scale="10m",
                 facecolor="none",
                 name='admin_1_states_provinces_lines',
                 )
#name="admin_0_scale_rank")
    ax.add_feature(feature.BORDERS,)
    ax.add_feature(states, edgecolor='gray')
    print('load features:',time.time()-itime)
    itime=time.time()
#Plot
    normi = mpl.colors.Normalize(vmin=0, vmax=1000)
    dmap=plt.contourf(lons, lats, data, 30,
                         transform=ccrs.PlateCarree(),
                         #cmap=cm.gist_ncar,
                         cmap=cm.tab20c,
                         #T2
                         #vmin=-20,
                         #vmax=50,
                         #RAIN
                         norm=normi,
                         #extend='both',
                         )
    
#dmap.set_clim(-20.0,50.0)
    ax.coastlines()
#ax.set_yticks(range(5,40,5),crs=ccrs.PlateCarree())
    g1=ax.gridlines(crs=ccrs.PlateCarree(),
            draw_labels=True,
            linestyle='--',
            )
    g1.xlabels_bottom=False
    g1.ylabels_right=False
    g1.xlocator=mticker.FixedLocator(range(-70,-135,-5))
    g1.xformatter=LONGITUDE_FORMATTER
    g1.ylocator=mticker.FixedLocator(range(5,40,5))
    g1.yformatter=LATITUDE_FORMATTER
# Add color bar
    cbar=plt.colorbar(dmap,ax=ax,
            shrink=0.95,
            orientation="horizontal",
            aspect=50,
            #spacing="uniform",
            #spacing='proportional',
            #pad=0.03,
            #fraction=0.1,
            pad=0.01,
            ticks=range(0,600,50)#RAIN
            #ticks=range(-20,50,5)#T2
            #ticks=range(-20,20,1),

            )
    #RAIN
    cbar.set_label("Precipitación [mm/?]")
    dmap.set_clim(0,300)
    #T2
    #cbar.set_label("Temperatura [C]")
    ##cbar.set_clim(-19.0,20.0)
    #dmap.set_clim(-20.0,50.0)

    plt.title(title,
            pad=25,
            )
    print('plot:',time.time()-itime)
    itime=time.time()
#plt.savefig('test_fig.png', bbox_inches='tight')
    plt.savefig(ofilename )
    plt.close()
    print('save:',time.time()-itime)
