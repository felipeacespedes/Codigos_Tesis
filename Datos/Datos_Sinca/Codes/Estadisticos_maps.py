# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 11:48:22 2023

@author: felip

Estadisticos_maps entrega mapas para el dominio de zona industrial Concón-
Quintero-Puchuncaví, con valores estadísticos por estación de: 
    - media
    - mediana
    - perc. 25 y 70
    - std
    - min y max
, tomando una variable y etsación de Dic.
"""

# librerías

import cartopy
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as pl
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import os
from import_var import import_var
import sys
from windrose import WindroseAxes, plot_windrose
from netCDF4 import Dataset


# Creamos diccionarios a usar

# Diccionario
Dic = {}

Dic['Estaciones'] = ['Ventanas','Los_Maitenes','Centro_Quintero','Loncura' \
                     ,'Sur','Junta_Vecinos','Concón','Gaviotas','Colmo']

Dic['Abreviación_Estaciones'] = ['VE','LM','CQ','LO' \
                                 ,'SU','JV','CC','GA','CO']

    
Dic['Lat'] = [-32.741822,-32.764257,-32.787721,-32.794914,-32.801052
              ,-32.935160,-32.924531,-32.915544,-32.929497]

Dic['Lon'] = [-71.480928,-71.454400,-71.532226,-71.496420,-71.483406
              ,-71.525804,-71.515441,-71.481469,-71.440576]

Dic['Variables'] = ['SO2','CH4','HCNM','HCT','CO','MP25','MP10' \
                    ,'Vel','Dir']

Dic['Unidades'] = ['ppb', 'ppm', 'ppm', 'ppm', 'ppm'\
                   , r'$\mathbf{\mu g/m^{3}}$', r'$\mathbf{\mu g/m^{3}}$'\
                   , 'm/s', '°']

Dic['CoM'] = ['Cont', 'Cont', 'Cont', 'Cont', 'Cont', 'Cont', 'Cont' \
              , 'Meteo', 'Meteo']
    
Dic['Estadísticos'] = ['count','mean','std','5%','25%','50%','75%','95%'\
                       ,'99.8%','min','max','mediana', 'IQR']


# Importamos mapas vectoriales de la BCN y KML de Zona Industrial

# Regiones
path_reg = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Regiones/'+\
            'Regional.shp'
reg = ShapelyFeature(Reader(path_reg).geometries(), ccrs.Mercator.GOOGLE)

# Zonas Urbanas
path_urb = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Areas_Pobladas/'+\
            'Areas_Pobladas.shp'
urb = ShapelyFeature(Reader(path_urb).geometries(), ccrs.Mercator.GOOGLE)

# Zona Industrial
path_zi = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Zona_Industrial/py/'\
            +'Zona_Industrial.shp'
zi = ShapelyFeature(Reader(path_zi).geometries(), ccrs.PlateCarree())

del path_reg, path_urb, path_zi


# Cremaos funciones:
    
######## Función create_map: crea mapa 
def create_map(ax, le, Lon, Lat, colors, cmap, num_sections, estd, wd):
    # Set extent
    region = [-71.6, -71.4, -32.95, -32.7]
    ax.set_extent(region)

    # Regiones (linea de costa)
    ax.add_feature(reg, alpha=0.8, linewidth=.8, facecolor='gray' \
                   ,edgecolor='black',zorder=1)
    
    # Zonas urbanas
    ax.add_feature(urb, alpha=0.9, linewidth=.8, facecolor='yellow' \
                   ,edgecolor='black', zorder=2)
    
    # Zonas Industriales
    ax.add_feature(zi, alpha=0.9, linewidth=.8, facecolor='green' \
                   ,edgecolor='black', zorder=3)
        
    # Nombramos cada una de las zonas 
    legend_handles = [
        mpatches.Patch(color='yellow', label='Zonas Urbanas'),
        mpatches.Patch(color='green', label='Zonas Industriales')
        ]

    # Set up gridlines
    gl = ax.gridlines(draw_labels=True, dms=False, alpha=0.5, zorder=4\
                      , x_inline=False, y_inline=False, crs=ccrs.PlateCarree()\
                      , linewidth=0.5)
    gl.top_labels = False
    gl.left_labels = True
    gl.right_labels = False
    # Set label style to display coordinates in decimal format
    gl.xformatter = cartopy.mpl.gridliner.LONGITUDE_FORMATTER
    gl.yformatter = cartopy.mpl.gridliner.LATITUDE_FORMATTER
    gl.xlocator = mticker.FixedLocator([-71.60, -71.55, -71.50, -71.45\
                                        , -71.40])

    # Estaciones y sus nombres
    sc = ax.scatter(Lon, Lat, s=130, c=colors, cmap=cmap, transform=\
                    ccrs.PlateCarree(),edgecolors='black',zorder=6)

    for e in le:
        ei = Dic['Estaciones'].index(e)
        ax.text(Dic['Lon'][ei],Dic['Lat'][ei]+0.004\
                ,Dic['Abreviación_Estaciones'][ei], fontsize=10\
                ,weight='bold',zorder=6)             
    del e, ei
    
    # # Dirección de viento usando quiver
    # if type(wd) == pd.core.frame.DataFrame:
    #     wd = wd.fillna(0)
    #     ax.quiver( wd['Lon'].values, wd['Lat'].values\
    #              , wd['U'].values, wd['V'].values)


    # Nombramos cada una de las zonas 
    legend_handles = [
        mpatches.Patch(color='yellow', label='Zonas Urbanas'),
        mpatches.Patch(color='green', label='Zonas Industriales')
        ]
    # Add legend to the plot
    ax.legend(handles=legend_handles, loc='upper left')


    # Add city markers and names
    city_names = ['Concón', 'Quintero', 'Puchuncaví']
    city_coords = [(-71.541875, -32.936387), (-71.533682, -32.771999)\
                   , (-71.486326, -32.731778)]

    for name, (lon, lat) in zip(city_names, city_coords):
        add = 0
        if name == 'Puchuncaví':
            add = 0.02
        ax.text(lon - 0.04 - add, lat , name, color='black', fontsize=10\
                , transform=ccrs.PlateCarree())

    return sc

########## Función para  identificar numero de ceros y 2 cifras importantes
def process_number(number):
    
    # Puede que haya que cheaquear si dato en nan y hacer algo
    if number == 0.0: 
        return 0, 0
    else: 
        pass
    
    # Convert the number to a string
    num_str = str(abs(number))

    # Initialize variables to count leading zeros and store the result
    zeros_count = 0
    result_digits = 0
    
    # Check sign of number
    if number >= 0:
        sign = 1
    else:
        sign = -1
    
    # Check relevant 2 digits and zeros
    if abs(number) >= 1.0:
        # Check exponent
        zeros_count = len(str(int(float(num_str))))-2
        # Get first 2 digits
        result_digits = int(num_str.replace('.','')[0:2])
    elif abs(number) < 1.0:
        num_str_dec = num_str[2:None]
        # print('num_str_dec: '+str(num_str_dec))
        for char in num_str_dec:
            if char == '0':
                # Increment leading_zeros_count if the character is '0'
                zeros_count += 1
            elif char.isdigit():
                result_digits = int(num_str_dec[zeros_count:zeros_count+2])\
                    if len(num_str_dec[zeros_count:None])>=2 else \
                    int(num_str_dec[zeros_count]+'0')
                zeros_count = (zeros_count+2)*-1
                break

    return zeros_count, result_digits*sign


############# Función CB_params()
def CB_params(var):
    # Contamos valores negativos
    vn = sum(n < 0 for n in var)
    
    # Valores positivos
    if vn == 0:
        vmin = 0; v = var.max()
        [ncs, vmax] = process_number(v)
        extend = 'max'
        cmap  =  plt.colormaps.get_cmap('Blues')
        
        # Hacemos que vmax sea siempre multiplo de 10
        vmax = ((int(vmax/10))*10) + 10
        
        # Queremos que la cantidad de secciones sea impar para 
        # que la cantidad de ticks sea par.
        n_sect = int(vmax/10) if vmax > 50 else int(vmax/5) \
                              if vmax > 20 else int(vmax/2) \
                              if vmax > 10 else int(vmax)

    # Valores negativos
    elif vn == len(var):
        vmax = 0
        [ncs, vmin] = process_number(var.min())
        extend = 'min'
        cmap = plt.colormaps.get_cmap('Reds_r')

        # Hacemos que vmax sea siempre multiplo de 10
        vmin = ((int(vmin/10))*10) + 10
        
        # Queremos que la cantidad de secciones sea impar para 
        # que la cantidad de ticks sea par.
        n_sect = int(vmin/10) if vmin > 50 else int(vmin/5) \
                              if vmin > 20 else int(vmin/2) \
                              if vmin > 10 else int(vmin)
        
    # Valores mixtos: puede que mno esté tan bueno cómo los otros dos
    else:
        sup = max([abs(var.min()),abs(var.max())])
        [ncs, vmax] = process_number(sup)
        extend = 'both'
        cmap = plt.colormaps.get_cmap('RdBu_r')
        
        # Hacemos que vmax sea siempre multiplo de 10
        vmax = ((int(vmax/10))*10) + 10
        vmin = -1*vmax
        
        # Queremos que la cantidad de secciones sea impar para 
        # que la cantidad de ticks sea par.
        n_sect = int(vmax/10) if vmax > 50 else int(vmax/5) \
                              if vmax > 20 else int(vmax/2) \
                              if vmax > 10 else int(vmax)
            
    # Ahora, entregamos las variables 
    return [vmin, vmax, cmap, extend, n_sect, ncs]


############# Función Est_maps(): crea serie de mapas
def est_maps( le, lv, lestd, Fi , Ff, dire):
    # Variables:
        
        # le: lista de estaciones a plotear.
        
        # lv: lista de variables a plotear.
                
        # lestd: lista de estadísticos a plotear.
        
        # Fi: Fecha inicial en formato '2018-01-01'
        
        # Ff: Fecha final en formato '2023-12-31'
        
        # dire: dirección para guardar plots
        
    # T: vector de tiempo
    T = pd.date_range(Fi+' 00:00:00',Ff+' 23:00:00',freq='h')
    
    # Obtenemos Lat y Lon de estaciones seleccionadas
    Lon = []
    Lat = []
    for e in le:
        Lon.append( Dic['Lon'][Dic['Estaciones'].index(e)])
        Lat.append( Dic['Lat'][Dic['Estaciones'].index(e)])

    
    # Chequeamos si las variables, estaciones y estadísticos
    # ingresadas existen o están bien escritas
    for v in lv:
        if v in Dic['Variables']:
            print(v+' included.')
        else:
            sys.exit(v+' está mal escrito o no existe.')

    for e in le:
        if e in Dic['Estaciones']:
            print(e+' included.')
        else:
            sys.exit(e+' está mal escrito o no existe.')
            
    for estd in lestd:
        if estd in Dic['Estadísticos']:
            print(estd+' included.')
        else:
            sys.exit(estd+' está mal escrito o no existe.')


    ## Importamos todas las variables y estaciones a usar
    
    # Creamos diccionario de estaciones
    Var= {}

    # Creamos array con Nans para rellenar las variables que no existan
    nan = np.empty(len(T)); nan[:] = np.nan
            
    # Importamos variables de contaminantes a dataframe de cada estación
    lv.extend(['Dir','Vel'])
    for v in range(len(lv)):
        Var[lv[v]] = pd.DataFrame({'T': T})
        Var[lv[v]] = Var[lv[v]].set_index('T')
        for e in range(len(le)):
            
            file_c = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'\
            +'Estaciones/'+le[e]+'/Cont/'+lv[v]+'.csv'
            file_m = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'\
            +'Estaciones/'+le[e]+'/Meteo/'+lv[v]+'.csv'
            if os.path.isfile(file_c) == True:
                Var[lv[v]][le[e]] = import_var(\
                    le[e],'Cont',lv[v],Fi,Ff)
                    
            elif os.path.isfile(file_m) == True:
                Var[lv[v]][le[e]] = import_var(\
                    le[e],'Meteo',lv[v],Fi,Ff)
            else:
                Var[lv[v]][le[e]] = nan
                
            del file_c, file_m
            
    lv.remove('Dir')
    lv.remove('Vel')

    
    # Ploteamos por estación, variable y estadístico
    for v in lv:
        for estd in lestd:
            
            # Calculate the specified statistic for each station                
            if estd in ['min', 'max']:
                # Creamos variable
                var = Var[v].apply(lambda col: getattr(col, estd)())
                
                if estd == 'max':
                    print('aun no creado para max chileno loco')
                    sys.exit()
                elif estd == 'min':
                    print('aun no creado para min chileno loco')
                    sys.exit()

                wd = None
            
            elif estd in ['count','std','mean']:
                # Define var, the value of the stat in each station
                var = Var[v].apply(lambda col: col.describe()).loc[estd]
                wd = None
                
            else: # si es un percentil
                # Define var, the value of the stat in each station
                var = Var[v].apply(lambda col: col.describe\
                        (percentiles=[float(estd.strip('%'))/100])).loc[estd]
                # Number of percentiles to take in each direction
                prc = 2.0  
                # Define the inferior and superior values to compare
                prc_inf = (float(estd.strip('%'))-prc)
                var_inf = Var[v].apply(lambda col: col.describe\
                (percentiles=[prc_inf/100])).loc[str(int(prc_inf))+'%'] 
                prc_sup = (float(estd.strip('%'))+prc)
                var_sup = Var[v].apply(lambda col: col.describe\
                (percentiles=[prc_sup/100])).loc[str(int(prc_sup))+'%']
                    
                # Save the moments of interest
                estd_moments = Var[v][(var_inf <= Var[v]) &\
                                         (Var[v] <= var_sup)] 
            
                # Calculamos estadisticos y vientos
                # Dataframe to save wind direction and speed by station
                wd = pd.DataFrame(columns = ['Dir','Vel','U','V','Lon','Lat']\
                                  , index = le )
                # Dictionary to save the values that were averaged
                wd_vals = {}
                ws_vals = {}
                
                # Start figure with subplots of windroses
                fig = plt.figure(figsize=(15,15))
                # Filter wind direction and speed DataFrame using boolean 
                # indexing for the specific station
                                
                ei = 1
                for e in le: 
                    wd_vals[e] = Var['Dir'].loc[estd_moments[e].notna(),e]
                    ws_vals[e] = Var['Vel'].loc[estd_moments[e].notna(),e]
                    
                    # Aqui debemos inspeccionar qué ocurre con el uso de loc
                    # y estd_moments:

                    # Add Lat and Lon to the df
                    wd.loc[e,'Lat'] = Dic['Lat'][ei-1]
                    wd.loc[e,'Lon'] = Dic['Lon'][ei-1]
                    
                    # Calculate the average wind direction for moments 
                    # with the same statistic value for a specific station
                    wd.loc[e,'U'] = np.nanmean(np.sin(np.deg2rad\
                                                      (wd_vals[e])))*-1
                    wd.loc[e,'V'] = np.nanmean(np.cos(np.deg2rad\
                                                      (wd_vals[e])))*-1
                    # Assign Speed to wd dataframe
                    wd.loc[e,'Vel'] = np.nanmean(ws_vals[e])
                    wd.loc[e,'Dir'] = np.rad2deg(np.arctan(\
                                      wd.loc[e,'U']/wd.loc[e,'V']))
                    
                    # Plot each wind rose
                    # windrose
                    print(e)
                    ax = fig.add_subplot(int('33'+str(ei)), projection="windrose")
                    ax.contourf(wd_vals[e], Var[v].loc[estd_moments[e].notna(),e] \
                                #ws_vals[e]\
                                #, bins=np.arange(0, 8, 1)
                                , bins=np.linspace(0,0.3,7), cmap=cm.hot)
                    ax.set_legend()
                    ax.set_title(e)
                    
                    # Add 1 to index ei
                    ei += 1
                    
                # Apply tight layout and show plot
                fig.suptitle(estd)
                fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
                plt.show()
                
                
                # Verificamos existencia de path y creamos directorios si no existe
                if os.path.isdir(dire) == False:
                    os.makedirs(dire)
                
                # Save fig
                fig.savefig(dire+v+'_'+estd+'_wr.png', dpi=300)
                
                
                # return ws_vals, wd_vals, estd_moments
                # sys.exit()
                # del ws_vals, wd_vals, estd_moments

            # retornamos las variables wd para poder verificar si suman 1
            # print(v)
            # print(estd)
            # return wd, wd_vals, ws_vals
            
            # Get parameters for colorbar
            [v_inf, v_sup, cmap, ext, num_sections, ncs] = CB_params(var)
            
            # Creamos figuras
            fig, ax = plt.subplots(figsize=(6.5,6.5), subplot_kw={'projection':\
                                                        ccrs.PlateCarree()})
            
            # Create maps
            if estd in ['5%','25%','50%','75%','95%','min','max']:
                sc = create_map(ax, le, Lon, Lat, [var*eval(f'10**({ncs})')]
                                , cmap, num_sections, estd, wd)
            else:
                sc = create_map(ax, le, Lon, Lat, [var*eval(f'10**({ncs})')]
                                , cmap, num_sections, estd, wd)   

            
            # Create a BoundaryNorm to discretize the colorbar
            norm = pl.colors.BoundaryNorm(np.linspace(v_inf, v_sup\
                                          , num_sections + 1)\
                                          , cmap.N, clip=True)
            
            # Create a ScalarMappable object
            sc_mappable = pl.cm.ScalarMappable(cmap=cmap, norm=norm)
            sc_mappable.set_array(var*eval(f'10**({ncs})'))
            
            # Create the shared colorbar
            cbar = fig.colorbar(sc_mappable, ax=ax, extend=ext\
                                , aspect=15, shrink=0.96)
            if estd != 'count':
                cbar.set_label(label=estd+' ['+Dic['Unidades'][Dic['Variables']\
                                .index(v)]+']',weight='bold')
            else:
                cbar.set_label(label='Hourly values available [n°]'\
                               ,weight='bold')
                
            if ncs != 0:
                ax.text(-71.37,-32.705,'e'+str(ncs),color='black'\
                    , fontsize=11, transform=ccrs.PlateCarree()) 
            
            # Adjust layout
            fig.tight_layout(pad=1.5)
            fig.suptitle(v)
            
            # Show the plot
            plt.show()
            
            # Verificamos existencia de path y creamos directorios si no existe
            if os.path.isdir(dire) == False:
                os.makedirs(dire)
            
            # Save fig
            fig.savefig(dire+v+'_'+estd+'.png', dpi=300)

    

############# Función Est_maps_df(): crea serie de mapas para df
def est_maps_df( var_str, df, lestd, Fi , Ff, dire):
    # Variables:
        # var_str: string de variable.
        
        # df: dataframe series de tiempo por estación e índice temporal.
                
        # lestd: lista de estadísticos a plotear.
        
        # Fi: Fecha inicial en formato '2018-01-01'
        
        # Ff: Fecha final en formato '2023-12-31'
        
        # dire: dirección para guardar plots
        
    # T: vector de tiempo
    T = pd.date_range(Fi+' 00:00:00',Ff+' 23:00:00',freq='h')
    
    # Cortamos df entre fechas a utilizar
    i = df.index.get_loc(Fi+' 00:00:00')
    f = df.index.get_loc(Ff+' 23:00:00')
    df = df.iloc[i:f+1]# f+1
    
    # lista de estaciones
    le = list(df.columns)
    
    # Obtenemos Lat y Lon de estaciones seleccionadas
    Lon = []
    Lat = []
    for e in le:
        Lon.append( Dic['Lon'][Dic['Estaciones'].index(e)])
        Lat.append( Dic['Lat'][Dic['Estaciones'].index(e)])


    ## Importamos variables meteo
    # Definimos DFs WD y WS
    WD = pd.DataFrame(columns=le)
    WD['T'] = T
    WD = WD.set_index('T')
    WS = pd.DataFrame(columns=le)
    WS['T'] = T
    WS = WS.set_index('T')
    # creamos vector Nan para rellenar columnas vacias
    nan = np.empty(len(T)); nan[:] = np.nan
    # Iteramos por estación
    for e in le:
        path_vel = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'\
        +'Estaciones/'+e+'/Meteo/Vel.csv'
        path_dir = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'\
        +'Estaciones/'+e+'/Meteo/Dir.csv'
        # importamos dir
        if os.path.isfile(path_dir) == True:
            WD[e] = import_var(e,'Meteo','Dir',Fi,Ff)
        else:
            WD[e] = nan
        # importamos vel
        if os.path.isfile(path_vel) == True:
            WS[e] = import_var(e,'Meteo','Vel',Fi,Ff)
        else: 
            WD[e] = nan
        # borramos variables
        del path_vel, path_dir
        
        
    # Aquí la idea es usar estadisticos de percentiles 
    for estd in lestd:
        
        
        if estd in ['5%','50%','95%']:    
            # Calculamos estadisticos y vientos
            # Dataframe to save wind direction and speed by station
            wd = pd.DataFrame(columns = ['Dir','Vel','U','V','Lon','Lat']\
                              , index = le )
            # Dictionary to save the values that were averaged
            wd_vals = {}
            ws_vals = {}
            
            # Number of percentiles to take in each direction
            prc = 5.0
            
            # Define var, the value of the stat in each station
            var = df.apply(lambda col: col.describe\
                    (percentiles=[float(estd.strip('%'))/100])).loc[estd]
            var = var.astype(float)
            
            # Define the inferior and superior values to compare
            prc_inf = (float(estd.strip('%'))-prc)
            inf = df.apply(lambda col: col.describe\
            (percentiles=[prc_inf/100])).loc[str(int(prc_inf))+'%'] 
            inf = inf.astype(float)
            prc_sup = (float(estd.strip('%'))+prc)
            sup = df.apply(lambda col: col.describe\
            (percentiles=[prc_sup/100])).loc[str(int(prc_sup))+'%']
            sup = sup.astype(float)
            
            print(estd)
            print(inf)
            print(sup)
                
            # Save the moments of interest
            estd_moments = df[(inf <= df) & (df <= sup)]
                
            # Start figure with subplots of windroses
            fig = plt.figure(figsize=(15,15))
            # Filter wind direction and speed DataFrame using boolean 
            # indexing for the specific station
            ei = 1
            for e in le: 
                wd_vals[e] = WD.loc[estd_moments[e].notna(),e]
                ws_vals[e] = WS.loc[estd_moments[e].notna(),e]
                
                # Add Lat and Lon to the df
                wd.loc[e,'Lat'] = Dic['Lat'][Dic['Estaciones'].index(e)]
                wd.loc[e,'Lon'] = Dic['Lon'][Dic['Estaciones'].index(e)]
                
                # Calculate the average wind direction for moments 
                # with the same statistic value for a specific station
                wd.loc[e,'U'] = np.nanmean(np.sin(np.deg2rad\
                                                  (wd_vals[e])))*-1
                wd.loc[e,'V'] = np.nanmean(np.cos(np.deg2rad\
                                                  (wd_vals[e])))*-1
                # Assign Speed to wd dataframe
                wd.loc[e,'Vel'] = np.nanmean(ws_vals[e])
                wd.loc[e,'Dir'] = np.rad2deg(np.arctan(\
                                  wd.loc[e,'U']/wd.loc[e,'V']))
                
                # Plot each wind rose
                # windrose
                print(e)
                ax = fig.add_subplot(int('33'+str(ei)), projection="windrose")
                ax.contourf(wd_vals[e], ws_vals[e], bins=np.arange(0, 8, 1)\
                            , cmap=cm.hot)
                ax.set_legend()
                ax.set_title(e)
                
                # Add 1 to index ei
                ei += 1
            
            # Apply tight layout and show plot
            fig.suptitle(estd)
            fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
            plt.show()
            
            # Verificamos existencia de path y creamos directorios si no existe
            if os.path.isdir(dire) == False:
                os.makedirs(dire)
            # Save fig
            fig.savefig(dire+var_str+'_'+estd+'_wr_mod.png', dpi=300)
        

        else:
            # Define var, the value of the stat in each station
            var = df.apply(lambda col: col.describe()).loc[estd]
            var = var.astype(float)
            wd = None
        
        # Get parameters for colorbar
        [v_inf, v_sup, cmap, ext, num_sections, ncs] = CB_params(var)
        
        # Creamos figuras
        fig, ax = plt.subplots(figsize=(8,8), subplot_kw={'projection':\
                                                    ccrs.PlateCarree()})
        
        # Create maps
        if estd in ['5%','25%','50%','75%','95%','min','max']:
            sc = create_map(ax, df, Lon, Lat, [var*eval(f'10**({ncs})')]
                            , cmap, num_sections, estd, wd)
        else:
            sc = create_map(ax, le, Lon, Lat, [var*eval(f'10**({ncs})')]
                            , cmap, num_sections, estd, wd)   

        
        # Create a BoundaryNorm to discretize the colorbar
        norm = pl.colors.BoundaryNorm(np.linspace(v_inf, v_sup\
                                      , num_sections + 1)\
                                      , cmap.N, clip=True)
        
        # Create a ScalarMappable object
        sc_mappable = pl.cm.ScalarMappable(cmap=cmap, norm=norm)
        sc_mappable.set_array(var*eval(f'10**({ncs})'))
        
        # Create the shared colorbar
        cbar = fig.colorbar(sc_mappable, ax=ax, extend=ext\
                            , aspect=15, shrink=0.96)
        if estd != 'count':
            cbar.set_label(label=estd+' ['+Dic['Unidades'][Dic['Variables']\
                            .index(var_str)]+']',weight='bold')
        else:
            cbar.set_label(label='Hourly values available [n°]'\
                           ,weight='bold')
            
        if ncs != 0:
            ax.text(-71.37,-32.705,'e'+str(ncs),color='black'\
                , fontsize=11, transform=ccrs.PlateCarree()) 
        
        # Adjust layout
        fig.tight_layout(pad=1.5)
        fig.suptitle(var_str)
        
        # Show the plot
        plt.show()
        
        # Verificamos existencia de path y creamos directorios si no existe
        if os.path.isdir(dire) == False:
            os.makedirs(dire)
        
        # Save fig
        fig.savefig(dire+var_str+'_'+estd+'_mod.png', dpi=300)
    
    
    
# est_maps_df_entrepercs
def windrose_df_entrepercs( var_str, df, Fi , Ff, Pi, Pf, dire, le):
    # Variables:
        # var_str: string de variable.
        
        # df: dataframe series de tiempo por estación e índice temporal.
                        
        # Fi: Fecha inicial en formato '2018-01-01'
        
        # Ff: Fecha final en formato '2023-12-31'
        
        # Pi: percentil inicial
        
        # Pf: percentil final
        
        # dire: dirección para guardar plots
        
        
    # T: vector de tiempo
    T = pd.date_range(Fi+' 00:00:00',Ff+' 23:00:00',freq='h')
    
    # Cortamos df entre fechas a utilizar
    i = df.index.get_loc(Fi+' 00:00:00')
    f = df.index.get_loc(Ff+' 23:00:00')
    df = df.iloc[i:f+1]

    # lista de estaciones
    # le = list(df.columns)
    
    # Dictionary to save the values that are between the percentiles of choice
    wd_vals = {}
    ws_vals = {}

    ## Importamos variables meteo
    # Definimos DFs WD y WS
    WD = pd.DataFrame(columns=le)
    WD['T'] = T
    WD = WD.set_index('T')
    WS = pd.DataFrame(columns=le)
    WS['T'] = T
    WS = WS.set_index('T')
    # creamos vector Nan para rellenar columnas vacias
    nan = np.empty(len(T)); nan[:] = np.nan
    # Iteramos por estación
    for e in le:
        path_vel = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'\
        +'Estaciones/'+e+'/Meteo/Vel.csv'
        path_dir = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'\
        +'Estaciones/'+e+'/Meteo/Dir.csv'
        # importamos dir
        if os.path.isfile(path_dir) == True:
            WD[e] = import_var(e,'Meteo','Dir',Fi,Ff)
        else:
            WD[e] = nan
        # importamos vel
        if os.path.isfile(path_vel) == True:
            WS[e] = import_var(e,'Meteo','Vel',Fi,Ff)
        else: 
            WD[e] = nan
        # borramos variables
        del path_vel, path_dir
        
    
    # Define the inferior and superior values to compare
    prc_inf = (float(Pi.strip('%')))
    inf = df.apply(lambda col: col.describe\
    (percentiles=[prc_inf/100])).loc[str(int(prc_inf))+'%'] 
    inf = inf.astype(float)
    prc_sup = (float(Pf.strip('%')))
    sup = df.apply(lambda col: col.describe\
    (percentiles=[prc_sup/100])).loc[str(int(prc_sup))+'%']
    sup = sup.astype(float)
    
        
    # Save the moments of interest
    estd_moments = df[(inf <= df) & (df <= sup)]

    
    # Start figure with subplots of windroses
    fig = plt.figure(figsize=(10,13))
    # Filter wind direction and speed DataFrame using boolean 
    # indexing for the specific station
    ei = 1

    # ahora ploteamos los valores entre percentiles de interés
    for e in le: 
        wd_vals[e] = WD.loc[estd_moments[e].notna(),e]
        ws_vals[e] = WS.loc[estd_moments[e].notna(),e]
        
        
        # Plot each wind rose
        # windrose
        print(e)
        ax = fig.add_subplot(int('32'+str(ei)), projection="windrose")
        ax.contourf(wd_vals[e], ws_vals[e], bins=np.arange(0, 6, 1)\
                    , cmap=cm.autumn_r)
        ax.set_legend()
        ax.set_title(e)
        
        # Add 1 to index ei
        ei += 1
    
    # Apply tight layout and show plot
    fig.suptitle('WRs para valores de '+var_str+' entre percentiles '\
                 +Pi+' - '+Pf)
    fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
    plt.show()
    
    # Verificamos existencia de path y creamos directorios si no existe
    if os.path.isdir(dire) == False:
        os.makedirs(dire)
    # Save fig
    fig.savefig(dire+var_str+'_'+Pi+'-'+Pf+'_wr_mod.png', dpi=300)
    
    
    
######### Mapas estadísticos con topografía ##########

def custom_colormap():
    # Define blue color for zero or lesser values
    blue_color = (0.541, 0.722, 0.961)
    
    # Create a terrain colormap starting from green
    terrain_cmap = plt.cm.get_cmap('terrain')
    terrain_colors = terrain_cmap(np.linspace(0.26, 1, 256))  # Start from green
    
    # Combine the blue color and the terrain colormap
    colors = [blue_color] + list(terrain_colors)
    cmap = mcolors.LinearSegmentedColormap.from_list('custom_colormap', colors, N=256)
    
    return cmap


def plot_topo_colorbar(estd, lestd, dire, vmin, vmax, n):
    if estd == lestd[0]: 
        # Create a figure and axis for the color bar
        fig, ax = plt.subplots(figsize=(1, 20))
        
        # Define colormap and bounds
        cmap = custom_colormap()
        bounds = np.linspace(vmin, vmax, n+1)
        ticks = np.linspace(vmin, vmax, 10+1)

        # Add colorbar of contourf
        norm = mcolors.BoundaryNorm(bounds, cmap.N, extend='both')        
        cb = plt.colorbar(plt.cm.ScalarMappable(norm=norm,cmap=cmap)\
                          , cax=ax, orientation='vertical',ticks=ticks\
                          , format='%1.f', aspect = 100)
                        #, fraction=0.01, pad=0.05 , alpha=0.5)
        cb.set_label('Altitud [m]')
        
        # cbar = plt.colorbar(ax=ax, cmap=cmap, levels=levels \
        #                     , orientation='vertical', fraction=0.03\
        #                     , pad=0.05 , alpha=0.5, fmt='%1.f')
        # cbar.set_label('Altitud [m]')
    
        # Save the color bar as an image
        plt.savefig(dire+'topo_colorbar.png', dpi=300, bbox_inches='tight')
    
        # Show the color bar
        plt.show()
        
        # Inform png saved
        print('Topography colorbar for estd == '+estd+' saved in: '+dire)
        
    else:
        print('Topography colorbar not saved for '+estd)


def create_map_topo(fig, ax, le, Lon, Lat, colors, cmap, num_sections, estd\
                    , lestd, wd, nc, dire):
    ##### NC FILE ######
    # Load NetCDF file
    nc_file = Dataset(nc)
    # Extract data from NetCDF file
    x_range = nc_file['x_range'][:]
    y_range = nc_file['y_range'][:]
    z_range = nc_file['z_range'][:]
    spacing = nc_file['spacing'][:]
    dimension = nc_file['dimension'][:]
    z = nc_file['z'][:]

    # Calculate the grid coordinates
    x = np.arange(x_range[0], x_range[1], spacing[0])
    x = x[0:len(x)-1]
    y = np.arange(y_range[0], y_range[1], spacing[1])[::-1]

    # Create a meshgrid
    X, Y = np.meshgrid(x, y)

    # Reshape the 'z' data based on 'dimension'
    z_data = z.reshape(len(y), len(x))
    
    ####### MAP #######
    # Set extent
    region = [-71.6, -71.4, -32.95, -32.7]
    ax.set_extent(region)
    
    # Linea de Costa
    bc = ax.contour(X, Y, z_data, levels=[0.1], colors='black', linewidths=1\
                    , transform=ccrs.PlateCarree())
    # Zonas Urbanas
    color_urb = 'cyan'#(0.384, 0.98, 0.831, 1) 
    ax.add_feature(urb, linewidth=2.5, facecolor=(1,1,1,0)\
                    ,edgecolor=color_urb, zorder=2)
    # Zonas Industriales
    color_zi = 'lightcoral'#(0.961, 0.455, 0.318, 1) # 
    ax.add_feature(zi, linewidth=2.5, facecolor=(1,1,1,0)\
                    ,edgecolor=color_zi, zorder=3)

    # Set up gridlines
    gl = ax.gridlines(draw_labels=True, dms=False, alpha=0.9, zorder=4\
                      , x_inline=False, y_inline=False, crs=ccrs.PlateCarree()\
                      , linewidth=0.7)
    gl.top_labels = False
    gl.left_labels = True
    gl.right_labels = False
    # Set label style to display coordinates in decimal format
    gl.xformatter = cartopy.mpl.gridliner.LONGITUDE_FORMATTER
    gl.yformatter = cartopy.mpl.gridliner.LATITUDE_FORMATTER
    gl.xlocator = mticker.FixedLocator([-71.60, -71.55, -71.50, -71.45\
                                        , -71.40])
        
    # Contourf: ploteamos topografía
    vmin=0.1; vmax=500.1; n=50
    levels = np.linspace(vmin, vmax, n+1)
    cmap_c = custom_colormap() #'terrain'
    c = ax.contourf(X, Y, z_data, cmap=cmap_c, levels=levels, extend='both' \
                    , transform=ccrs.PlateCarree())
    # plot_topo_colorbar(estd, lestd, dire,vmin,vmax,n)

    # Add colorbar of contourf
    ticks = np.linspace(vmin, vmax, 5+1)
    cbar = plt.colorbar(c, ax=ax, orientation='horizontal', location='top',
                         pad=0.021, ticks=ticks, format='%1.f',
                         aspect=35, fraction=0.0209, anchor=(0.25,1))
    cbar.set_label('Altitud [m]')

    # Estaciones y sus nombres
    sc = ax.scatter(Lon, Lat, s=130, c=colors, cmap=cmap, transform=\
                    ccrs.PlateCarree(),edgecolors='black',zorder=6)

    for e in le:
        ei = Dic['Estaciones'].index(e)
        ax.text(Dic['Lon'][ei],Dic['Lat'][ei]+0.004\
                ,Dic['Abreviación_Estaciones'][ei], fontsize=10\
                ,weight='bold',zorder=6)             
    del e, ei

    # Nombramos cada una de las zonas 
    legend_handles = [
        mpatches.Patch(color=color_urb, label='Zonas Urbanas'),
        mpatches.Patch(color=color_zi, label='Zonas Industriales')
        ]

    # Add legend to the plot
    ax.legend(handles=legend_handles, loc='upper left')

    # Add city markers and names
    city_names = ['Concón', 'Quintero', 'Puchuncaví']
    city_coords = [(-71.541875, -32.936387), (-71.533682, -32.771999)\
                   , (-71.486326, -32.731778)]

    for name, (lon, lat) in zip(city_names, city_coords):
        add_lon = 0
        add_lat = 0
        if name == 'Puchuncaví':
            add_lon = 0.023
            add_lat = 0.005
        elif name =='Quintero':
            add_lon = 0.005
        elif name =='Concón':
            add_lon = -0.025
            add_lat = -0.02


        ax.text(lon - 0.04 - add_lon, lat - add_lat , name, color='black'
                , fontsize=11, transform=ccrs.PlateCarree(),zorder=7)

    return sc


############# Función Est_maps_topo(): crea serie de mapas para df
def est_maps_topo( var_str, df, lestd, Fi , Ff, dire, nc):
    # Variables:
        # var_str: string de variable.
        
        # df: dataframe series de tiempo por estación e índice temporal.
                
        # lestd: lista de estadísticos a plotear.
        
        # Fi: Fecha inicial en formato '2018-01-01'
        
        # Ff: Fecha final en formato '2023-12-31'
        
        # dire: dirección para guardar plots
        
    # T: vector de tiempo
    T = pd.date_range(Fi+' 00:00:00',Ff+' 23:00:00',freq='h')
    
    # Cortamos df entre fechas a utilizar
    i = df.index.get_loc(Fi+' 00:00:00')
    f = df.index.get_loc(Ff+' 23:00:00')
    df = df.iloc[i:f+1]
    
    # lista de estaciones
    le = list(df.columns)
    
    # Obtenemos Lat y Lon de estaciones seleccionadas
    Lon = []
    Lat = []
    for e in le:
        Lon.append( Dic['Lon'][Dic['Estaciones'].index(e)])
        Lat.append( Dic['Lat'][Dic['Estaciones'].index(e)])

    #### ESTÁ MODIFICADO PARA NO VER VIENTO ####
    ## Importamos variables meteo
    # Definimos DFs WD y WS
    # WD = pd.DataFrame(columns=le)
    # WD['T'] = T
    # WD = WD.set_index('T')
    # WS = pd.DataFrame(columns=le)
    # WS['T'] = T
    # WS = WS.set_index('T')
    # creamos vector Nan para rellenar columnas vacias
    # nan = np.empty(len(T)); nan[:] = np.nan
    # # Iteramos por estación
    # for e in le:
    #     path_vel = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'\
    #     +'Estaciones/'+e+'/Meteo/Vel.csv'
    #     path_dir = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'\
    #     +'Estaciones/'+e+'/Meteo/Dir.csv'
    #     # importamos dir
    #     if os.path.isfile(path_dir) == True:
    #         WD[e] = import_var(e,'Meteo','Dir',Fi,Ff)
    #     else:
    #         WD[e] = nan
    #     # importamos vel
    #     if os.path.isfile(path_vel) == True:
    #         WS[e] = import_var(e,'Meteo','Vel',Fi,Ff)
    #     else: 
    #         WD[e] = nan
    #     # borramos variables
    #     del path_vel, path_dir
        
        
    # Aquí la idea es usar estadisticos de percentiles 
    for estd in lestd:
        #### ESTÁ MODIFICADO PARA NO VER VIENTO ####
        # if estd in ['5%','50%','95%']:    
            # # Calculamos estadisticos y vientos
            # # Dataframe to save wind direction and speed by station
            # wd = pd.DataFrame(columns = ['Dir','Vel','U','V','Lon','Lat']\
            #                   , index = le )
            # # Dictionary to save the values that were averaged
            # wd_vals = {}
            # ws_vals = {}
            
            # # Number of percentiles to take in each direction
            # prc = 5.0
            
            # # Define var, the value of the stat in each station
            # var = df.apply(lambda col: col.describe\
            #         (percentiles=[float(estd.strip('%'))/100])).loc[estd]
            # var = var.astype(float)
            
            # # Define the inferior and superior values to compare
            # prc_inf = (float(estd.strip('%'))-prc)
            # inf = df.apply(lambda col: col.describe\
            # (percentiles=[prc_inf/100])).loc[str(int(prc_inf))+'%'] 
            # inf = inf.astype(float)
            # prc_sup = (float(estd.strip('%'))+prc)
            # sup = df.apply(lambda col: col.describe\
            # (percentiles=[prc_sup/100])).loc[str(int(prc_sup))+'%']
            # sup = sup.astype(float)
            
            # print(estd)
            # print(inf)
            # print(sup)
                
            # # Save the moments of interest
            # estd_moments = df[(inf <= df) & (df <= sup)]
                
            # # Start figure with subplots of windroses
            # fig = plt.figure(figsize=(15,15))
            # # Filter wind direction and speed DataFrame using boolean 
            # # indexing for the specific station
            # ei = 1
            # for e in le: 
            #     wd_vals[e] = WD.loc[estd_moments[e].notna(),e]
            #     ws_vals[e] = WS.loc[estd_moments[e].notna(),e]
                
            #     # Add Lat and Lon to the df
            #     wd.loc[e,'Lat'] = Dic['Lat'][Dic['Estaciones'].index(e)]
            #     wd.loc[e,'Lon'] = Dic['Lon'][Dic['Estaciones'].index(e)]
                
            #     # Calculate the average wind direction for moments 
            #     # with the same statistic value for a specific station
            #     wd.loc[e,'U'] = np.nanmean(np.sin(np.deg2rad\
            #                                       (wd_vals[e])))*-1
            #     wd.loc[e,'V'] = np.nanmean(np.cos(np.deg2rad\
            #                                       (wd_vals[e])))*-1
            #     # Assign Speed to wd dataframe
            #     wd.loc[e,'Vel'] = np.nanmean(ws_vals[e])
            #     wd.loc[e,'Dir'] = np.rad2deg(np.arctan(\
            #                       wd.loc[e,'U']/wd.loc[e,'V']))
                
            #     # Plot each wind rose
            #     # windrose
            #     print(e)
            #     ax = fig.add_subplot(int('33'+str(ei)), projection="windrose")
            #     ax.contourf(wd_vals[e], ws_vals[e], bins=np.arange(0, 8, 1)\
            #                 , cmap=cm.hot)
            #     ax.set_legend()
            #     ax.set_title(e)
                
            #     # Add 1 to index ei
            #     ei += 1
            
            # # Apply tight layout and show plot
            # fig.suptitle(estd)
            # fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
            # plt.show()
            
            # # Verificamos existencia de path y creamos directorios si no existe
            # if os.path.isdir(dire) == False:
            #     os.makedirs(dire)
            # # Save fig
            # fig.savefig(dire+var_str+'_'+estd+'_wr_mod.png', dpi=300)
            
        # IQR
        if estd == 'IQR':
            # Define var, the value of the stat in each station
            p25 = df.describe().loc['25%'] 
            p75 = df.describe().loc['75%']
            var = p75 - p25
            wd = None
        
        # percentiles no incluidos en .describe() 
        elif estd[-1] == '%' and estd not in ['25%','50%','75%']:
            prct = float(estd.strip('%'))/100
            var = df.apply(lambda col: col.describe(percentiles=[prct])).loc[estd]
            var = var.astype(float)
            wd = None
        # resto de estadísticos que deberían estar en .describe() 
        elif estd in df.describe().index.values:  
            # Define var, the value of the stat in each station
            var = df.describe().loc[estd]
            wd = None
            
        # estd no definido
        else:
            sys.exit('Estadístico "'+estd+'" no definido. Deben ser:\n'+\
                     '- '+str(df.describe().index.values)+'\n'+\
                    '- Cualquier percentil entero o con decimal,'+\
                    ' que termine en signo porcentaje del tipo "99.8%"\n'+\
                    '- "IQR" (rango intercuantil)')
        
        print(estd)
        print(var)
        # Get parameters for colorbar
        [v_inf, v_sup, cmap, ext, num_sections, ncs] = CB_params(var)
        
        # Creamos figuras
        fig, ax = plt.subplots(figsize=(6,6), subplot_kw={'projection':\
                                                    ccrs.PlateCarree()})
        
        # Create maps
        sc = create_map_topo(fig, ax, le, Lon, Lat, var.values*eval(f'10**({ncs})')
                        , cmap, num_sections, estd, lestd, wd, nc, dire)   

        
        # Create a BoundaryNorm to discretize the colorbar
        norm = pl.colors.BoundaryNorm(np.linspace(v_inf, v_sup\
                                      , num_sections + 1)\
                                      , cmap.N, clip=True)
        
        # Create a ScalarMappable object
        sc_mappable = pl.cm.ScalarMappable(cmap=cmap, norm=norm)
        sc_mappable.set_array(var*eval(f'10**({ncs})'))
        
        # Create the shared colorbar
        cbar = fig.colorbar(sc_mappable, ax=ax, extend=ext\
                            , aspect=15, shrink=0.96)
        if estd == 'count':
            cbar.set_label(label='Hourly values available [n°]'\
                           ,weight='bold')
        elif estd == '50%':
            cbar.set_label(label='Mediana ['+Dic['Unidades'][Dic['Variables']\
                            .index(var_str)]+']',weight='bold')
        else:
            cbar.set_label(label=estd+' ['+Dic['Unidades'][Dic['Variables']\
                            .index(var_str)]+']',weight='bold')
            
        if ncs != 0:
            ax.text(-71.37,-32.705,'e'+str(ncs),color='black'\
                , fontsize=11, transform=ccrs.PlateCarree()) 
        
        # Adjust layout
        fig.tight_layout(pad=0.1)
        

        # Verificamos existencia de path y creamos directorios si no existe
        if os.path.isdir(dire[0:len(dire)-1]) == False:
            os.makedirs(dire[0:len(dire)-1])
        
        print(f"Saving to: {os.getcwd()}")
        
        if estd[-1]=='%':
            estd=estd[0:len(estd)-1]
        if '.' in estd:
            estd = estd.replace('.','')
        
        # Save fig
        fig.savefig(dire+'mapa_'+var_str+'_'+estd+'.png', dpi=300)
    
    
    