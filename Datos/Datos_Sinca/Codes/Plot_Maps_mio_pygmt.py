# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 17:45:15 2025

@author: felip
"""

# librerías
import pygmt
import geopandas as gpd
# from cartopy.io.shapereader import Reader
# from cartopy.feature import ShapelyFeature
# import cartopy.crs as ccrs



# Importamos mapas vectoriales de la BCN y KML de Zona Industrial

# Regiones
path_reg = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Regiones/'+\
            'Regional.shp'

# Zonas Urbanas
path_urb = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Areas_Pobladas/'+\
            'Areas_Pobladas.shp'
# urb = ShapelyFeature(Reader(path_urb).geometries(), ccrs.Mercator.GOOGLE)

# Zona Industrial
path_zi = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Zona_Industrial/web/'\
            +'Zona_Industrial.shp'
            
# Oleoducto
path_od = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Zona_Industrial/IDE/'\
            +'Oleoducto.shp'
            
# Gasoducto
path_gd = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Zona_Industrial/IDE/'\
            +'Gasoducto.shp'

# Prueba    
path_t = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Zona_Industrial/IDE/'\
            +'Bloque_ENAP.shp'

Dic = {
    'Estaciones': ['Ventanas','Centro_Quintero','Concón','Colmo'],
    'Abreviación_Estaciones': ['VE','CQ','CC','CO'],
    'Lon': [-71.480928,-71.532226,-71.515441,-71.440576],
    'Lat': [-32.741822,-32.787721,-32.924531,-32.929497]
}

region = [-71.6, -71.4, -32.95, -32.7]

def map_topo_pygmt(output_file):
    """
    Create a topographic map using PyGMT.
    
    Parameters:
    - grid_file: Path to NetCDF (topography) file
    - stations: List of (lon, lat, name) tuples
    - urban_area_shp: Path to urban shapefile
    - industrial_area_shp: Path to industrial shapefile
    - output_file: Path to save figure
    - region: [west, east, south, north]
    """
    # link archivo nc
    path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
    nc = path+'QUINTERO.nc'
    
    fig = pygmt.Figure()

    # Set the color palette
    pygmt.makecpt(cmap="geo", series=[0, 700])
    
    # Plot topography
    proj = "M5/5/5c"
    frame = ["af","+glightblue"]
    nc_clipped = pygmt.grdclip(grid=nc, below=[0.01, float("NaN")])
    fig.basemap(region=region, projection=proj, frame=frame)
    fig.grdimage(grid=nc_clipped, region=region, projection=proj, 
                 frame=frame, shading=False,nan_transparent=True)


    # Plot urban areas
    zu = gpd.read_file(path_urb)
    # Reproyectar a WGS84 lat/lon
    zu= zu.to_crs("EPSG:4326")
    # Filtrar para Quintero, Puchuncavi y Concon
    zu = zu[(zu['comuna'] == 'Quintero') | (zu['comuna'] == 'PUCHUNCAVI') \
            | (zu['comuna'] == 'Concón')]
    fig.plot(data=zu, pen="0.8p,blue")

    # Plot industrial areas
    fig.plot(data=path_zi, pen="0.8p,red")
    
    # Plot oleoductos
    od = gpd.read_file(path_od)
    od = od[od['COMBUSTIBL']=='PETROLEO CRUDO']
    # od = od[od['COMBUSTIBL']=='GASOLINA 93/97 - KEROSENE DOMESTICO - DIESEL']
    # od = od[od['COMBUSTIBL']=='GASOLINA 93/97  - MEZCLA PROPANO-BUTANO LICUADO']
    # od = od[od['COMBUSTIBL']=='FUEL OIL N5']
    # od = od[od.index==0]
    fig.plot(data=od, pen="0.8p,dimgrey")
    
    # Plot gasoducto
    gd = gpd.read_file(path_gd)
    gd = gd[gd['NOMBRE']=='GASODUCTO QUINTERO-QUILLOTA 24 PULGADAS']
    # gd = gd[gd.index==0]
    fig.plot(data=gd, pen="0.8p,grey")

    # # Plot test: red vial
    # t = gpd.read_file(path_t)
    # # Reproyectar a WGS84 lat/lon
    # t= t.to_crs("EPSG:4326")
    # # Filtrar para Quintero, Puchuncavi y Concon
    # t = t[(t['Cod_Region']==5)&(t['Clase_Ruta']==1)]
    # fig.plot(data=t, pen="0.8p,orange")
    
    # Plot test: bloque ENAP
    # fig.plot(data=path_t, pen="10p,orange")

    
    # Style de las estaciones
    style="c0.2c"

    # Plot SINCA stations (white points)
    for i in range(4):
        offset = "-0.3c/-0.2c" if i==1 else "0.25c/0.25c"
        fig.plot(x=Dic['Lon'][i], y=Dic['Lat'][i], style=style, fill="white", 
                 pen="black")
        fig.text(x=Dic['Lon'][i], y=Dic['Lat'][i],
                 text=Dic['Abreviación_Estaciones'][i],
                 font="8p,Helvetica-Bold,black", offset=offset)
    
    # Plot PTR station
    ptr_cord = [-71.526988, -32.781688]
    fig.plot(x=ptr_cord[0], y=ptr_cord[1], style=style, fill="magenta", 
             pen="black")
    fig.text(x=ptr_cord[0], y=ptr_cord[1],
             text='PTR',
             font="8p,Helvetica-Bold,black", offset="0.1c/0.25c")
    # Plot DMC station
    dmc_cord = [-71.52278, -32.78417]
    fig.plot(x=dmc_cord[0], y=dmc_cord[1], style=style, fill="cyan", 
             pen="black")
    fig.text(x=dmc_cord[0], y=dmc_cord[1],
             text='DMC',
             font="8p,Helvetica-Bold,black", offset="0.35c/-0.25c")
    # Plot NF
    nf_cord = [-71.408510, -32.719072]
    fig.plot(x=nf_cord[0], y=nf_cord[1], style=style, fill="orange", 
             pen="black")
    fig.text(x=nf_cord[0], y=nf_cord[1],
             text='NF',
             font="8p,Helvetica-Bold,black", offset="-0.25c/-0.25c") 
    
    # Add city tags
    fig.text(text=["Bahía de","Quintero-Puchuncaví"],
             font="6p,Helvetica-Bold,black",
             x=[-71.545,-71.545], y=[-32.747,-32.755])
    fig.text(text="Concón",
             font="6p,Helvetica-Bold,black",
             x=-71.55, y=-32.915)


    # Add colorbar
    pygmt.config(FONT_ANNOT_PRIMARY="8,Helvetica,black")
    pygmt.config(FONT_LABEL="8p,Helvetica,black")
    fig.colorbar(position="jTR+o-0.5/0.3+w2.5/0.15c+v",
                 frame=["x+lTopography [m]"])


    # Add inset globe
    with fig.inset(position="jBR+w2.7c+o-1.7/1c", margin=0):
        fig.coast(
            region="g",
            projection="G-65/-20/?",
            land="gray",
            water="white",
            dcw="Chile+gforestgreen",
            frame='g30'
        )
        x = [-105]  # x vector coordinates
        y = [-27.5]  # y vector coordinates
        d = [0]  # direction of vectors
        l = [0.5]  # length of vectors
        # Cartesian vectors (v) with red fill and pen (+g, +p), vector head at the end (+e), and
        # 40 degree angle (+a) with no indentation for the vector head (+h)
        style = "v0.15c+e+a40+gred+h0+p1p,red"
        fig.plot(x=x, y=y, style=style, pen="1p,red", direction=[d, l])
        # Estrella en Quintero
        fig.plot(x=-71,y=-32,style="a0.2c", pen="0.1p,black", fill="red")
        
    fig.show()
    # Save
    fig.savefig(output_file, dpi=600)
