# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 17:45:15 2025

@author: felip
"""

# librerías
# from cartopy.io.shapereader import Reader
# from cartopy.feature import ShapelyFeature

import pygmt
from pygmt.params import Position, Box, Axis, Frame, Pattern
# import cartopy.crs as ccrs
import geopandas as gpd



# Importamos mapas vectoriales de la BCN y KML de Zona Industrial

# Regiones
path_reg_bcn = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Regiones/'+\
            'Regional.shp'
path_reg_dpa = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/DPA_2023/REGIONES/'+\
            'REGIONES_v1.shp'

# Zonas Urbanas
path_urb = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Areas_Pobladas/'+\
            'Areas_Pobladas.shp'
# urb = ShapelyFeature(Reader(path_urb).geometries(), ccrs.Mercator.GOOGLE)

# Zona Industrial
path_zi = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/Zona_Industrial/web/'\
            +'Zona_Industrial.shp'

# Estaciones Supercitio
Dic = {
    'Estaciones': ['Ventanas','Quintero','Concón'],
    'Abreviación_Estaciones': ['VE','QN','CC'],
    'Lon': [-71.485704,-71.535295,-71.515825],
    'Lat': [-32.741703,-32.772393,-32.936796],
    'offset': ['0.25c/0.25c','0.25c/0.25c','0.25c/-0.25c']
}
# Estaciones SMA BETX
Dic_SMA = {
    'Lon': [-71.48586392070062,
            -71.48036410484943,
            -71.50366726242898,
            -71.5327853233008,
            -71.53284181843453,
            -71.51628113173922,
            -71.43932727591744
            ],
    'Lat': [-32.74252173748857, 
            -32.74206174002564, 
            -32.78839578699402, 
            -32.78771030403182, 
            -32.77534792447901, 
            -32.9333449593504,  
            -32.93364995472767
            ]
    }

# Estaciones SINCA HCNM

Dic_SINCA = {
    'Lon': [-71.48085631867254,
            -71.45464196561922,
            -71.48355425242353,
            -71.49617226623195,
            -71.53282374950032,
            -71.52578110544918,
            -71.51552560084303,
            -71.48144813507038,
            -71.44042240832609
            ],
    'Lat': [-32.741832288558555, 
            -32.763920427216554, 
            -32.801575883510445, 
            -32.794915743661484, 
            -32.78771166503232,  
            -32.93510884542938,  
            -32.92448811127461,  
            -32.915200544992786, 
            -32.92952100195035
            ]
}


# Región a plotear
region_a = [-71.63, -71.39, -32.98, -32.68]

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
    path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Plot_Map/'
    nc = path+'QUINTERO.nc'
    
    fig = pygmt.Figure()
    pygmt.config(FORMAT_GEO_MAP="ddd.xx",MAP_FRAME_TYPE="plain")

    # Set the color palette
    # pygmt.makecpt(cmap="geo", series=[0, 600])
    # pygmt.makecpt(cmap="world", series=[-400, 600])
    # pygmt.makecpt(cmap="dem4", series=[0, 600])
    # pygmt.makecpt(cmap="gmt/relief", series=[0, 600])
    # pygmt.makecpt(cmap="gmt/globe", series=[0, 600])
    # pygmt.makecpt(cmap="cmocean/topo", series=[0, 600])
    # pygmt.makecpt(cmap="gmt/etopo1", series=[0, 600])



    
    ### Plot topography ###
    proj = "M5/5/5c"
    ## BCN:
    pygmt.makecpt(cmap="geo", series=[0, 600])
    frame = ["af","+gcornflowerblue"]
    nc_clipped = pygmt.grdclip(grid=nc, below=[0.001, float("NaN")])
    shade = pygmt.grdgradient(grid=nc_clipped, azimuth=(0,270), normalize="cauchy", norm_amp=1)
    fig.basemap(region=region_a, projection=proj, frame=frame)
    fig.grdimage(grid=nc_clipped, region=region_a, projection=proj,
                 frame=frame,
                 shading=shade,
                 nan_transparent=True)

    ## Load earth relief:
    # grid = pygmt.datasets.load_earth_relief(data_source="igpp",use_srtm=False,
    #                                         resolution="01s", region=region_a)
    # shade = pygmt.grdgradient(grid=grid, azimuth=(0,270), normalize="cauchy", norm_amp=1)
    # fig.grdimage(grid=grid, region=region_a, projection=proj,shading=shade,
    #              cmap="gmt/geo")

    ### Region como linea de costa ###

    ## Plot regiones: BCN
    # lr = gpd.read_file(path_reg_bcn)
    # # Reproyectar a WGS84 lat/lon
    # lr= lr.to_crs("EPSG:4326")
    # # Filtrar para Quintero, Puchuncavi y Concon
    # lr = lr[(lr['codregion'] == 5)]
    # fig.plot(data=lr, pen="0.5p,dimgrey,solid",transparency=5)

    ## Plot regiones: DPA
    # lr = gpd.read_file(path_reg_dpa)
    # # Reproyectar a WGS84 lat/lon
    # lr= lr.to_crs("EPSG:4326")
    # # Filtrar para Región de Coquimbo, Metropolitana, Valparaíso y O'Higgins
    # lr = lr[(lr['CUT_REG'] == '05') | (lr['CUT_REG'] == '13') \
    #         | (lr['CUT_REG'] == '06')| (lr['CUT_REG'] == '04')]
    # fig.plot(data=lr, pen="0.5p,dimgrey,solid",transparency=5)

    ### Urban and industrial areas ###
    trans = 40
    # Plot urban areas
    color_urb = "blue"
    zu = gpd.read_file(path_urb)
    # Reproyectar a WGS84 lat/lon
    zu= zu.to_crs("EPSG:4326") # 4226
    # Filtrar para Quintero, Puchuncavi y Concon
    zu = zu[(zu['comuna'] == 'Quintero') | (zu['comuna'] == 'PUCHUNCAVI') \
            | (zu['comuna'] == 'Concón')]
    
    fig.plot(data=zu, fill=color_urb, transparency=trans) # pen="0.05p,"+color_urb,

    # Plot industrial areas
    color_ind = "orange"
    fig.plot(data=path_zi, fill=color_ind, transparency=trans-10) # pen="0.05p,"+color_ind,

    # Plot stations (points)
    for i in range(3):
        fig.plot(x=Dic['Lon'][i], y=Dic['Lat'][i], style="c0.2c", fill="whitesmoke", 
                 pen="black")
        fig.text(x=Dic['Lon'][i], y=Dic['Lat'][i],
                 text=Dic['Abreviación_Estaciones'][i],
                 font="8p,Helvetica-Bold,black", offset=Dic['offset'][i])

    # # Plot stations SMA BETX
    # for i in range(len(Dic_SMA['Lon'])):
    #     fig.plot(x=Dic_SMA['Lon'][i], y=Dic_SMA['Lat'][i], style="c0.1c", fill="cyan", 
    #              pen="black")

    # Plot stations SINCA HCNM 
    for i in range(len(Dic_SINCA['Lon'])):
        fig.plot(x=Dic_SINCA['Lon'][i], y=Dic_SINCA['Lat'][i], style="d0.13c", fill="whitesmoke", 
                 pen="black")
        
    # Add city tags
    fig.text(text=["Quintero-Puchuncavi"," Bay"],
             font="5.8p,Helvetica-Bold,black",
             x=[-71.552,-71.552], y=[-32.747,-32.755])
    # fig.text(text=["Bahía de","Quintero-Puchuncaví"],
    #          font="6p,Helvetica-Bold,black",
    #          x=[-71.545,-71.545], y=[-32.745,-32.753])
    fig.text(text="Concon",
             font="5.8p,Helvetica-Bold,black",
             x=-71.55, y=-32.915)


    # Add colorbar
    pygmt.config(FONT_ANNOT_PRIMARY="13,Helvetica,black")
    pygmt.config(FONT_LABEL="13p,Helvetica,black")
    fig.colorbar(position="jTR+o-1.5/0.3+w3/0.2c+v",
                 frame=["x+lTopography [m]"])

    # Plot north arrow
    fig.image(
            imagefile=path+"north_arrow.png",
            position="jTR+w0.5c+o0.1c/0.1c",  # jTR = Top Right; +w = width (1.2cm); +o = offset (x/y)
            )

    # Plot scale bar
    with pygmt.config(FONT_ANNOT_PRIMARY="6p,Helvetica-Narrow-Bold,black",
                      FONT_LABEL="6p,Helvetica-Narrow-Bold,black"):
        fig.scalebar(length="5k", height="2.8p",fancy=True, unit=True,
                    #  label_alignment='bottom',label='5 km',
                     position=Position("TL", anchor="TL",offset=(0.3,0.2)))


    # Create an inset map, placing it in the Bottom Right (BR) corner with x- and y-offsets
    # of 0.1 cm, respectively. The inset map contains the Chile main land. "U54S/3c" means
    # UTM projection with a map width of 3 cm. The inset width and height are automatically
    # calculated from the specified ``region`` and ``projection`` parameters. Draws a
    # rectangular box around the inset with a fill color of "white" and a pen of "1p".
    region_b = [-72.1, -70, -34.3, -31.7]
    proj = "M2c"
    with fig.inset(
        position=Position("BR", offset=(-2.5,0.5)),
        box=Box(fill="white", pen="1p"),
        region=region_b,#[-72.34, -69.9, -34.2, -31.98],#[129, 146, 30, 46],
        projection=proj,
    ):
        # Highlight the Chile area in "lightbrown" and draw its outline with a pen of "0.2p"
        # fig.coast(dcw="CL+glightbrown+p0.2p", area_thresh=10000)

        grid = pygmt.datasets.load_earth_relief(resolution="30s", region=region_b)
        shade = pygmt.grdgradient(grid=grid, azimuth=(0,270), normalize="cauchy", norm_amp=0.5)

        fig.grdimage(grid=grid,  
                     shading=shade,

                    #  cmap="gmt/relief",
                    # cmap="gmt/dem2",
                    # cmap="SCM/fes",
                    cmap="gmt/terra"

                    )
        # Fronteras y limites regionales
        # fig.coast(
        #         resolution="f",  # 'f' = full resolution (máxima precisión para mapas regionales)
        #         transparency=2,
        #         projection=proj,
        #         region=region_b,
        #         dcw='CL+c',
        #         borders=[
        #             "1/0.8p,dimgrey,solid",  # Frontera nacional (Chile-Argentina): línea negra de 1pt
        #             "2/0.8p,dimgrey,4_2:2p",  # Frontera nacional (Chile-Argentina): línea negra de 1pt

        #         ],
        #     )

        # Plot regiones: BCN
        lr = gpd.read_file(path_reg_bcn)
        # Reproyectar a WGS84 lat/lon
        lr= lr.to_crs("EPSG:4326")
        # Filtrar para Quintero, Puchuncavi y Concon
        lr = lr[(lr['codregion'] == 5) | (lr['codregion'] == 13) \
                | (lr['codregion'] == 6)| (lr['codregion'] == 4)]
        fig.plot(data=lr, pen="0.5p,dimgrey,solid",transparency=0)


        # Plot regiones: DPA
        # lr = gpd.read_file(path_reg_dpa)
        # # Reproyectar a WGS84 lat/lon
        # lr= lr.to_crs("EPSG:4326")
        # # Filtrar para Región de Coquimbo, Metropolitana, Valparaíso y O'Higgins
        # lr = lr[(lr['CUT_REG'] == '05') | (lr['CUT_REG'] == '13') \
        #         | (lr['CUT_REG'] == '06')| (lr['CUT_REG'] == '04')]
        # fig.plot(data=lr, pen="0.8p,dimgrey,solid",transparency=5)

        # Plot urban areas
        zu = gpd.read_file(path_urb)
        # Reproyectar a WGS84 lat/lon
        zu= zu.to_crs("EPSG:4326") # 4326
        # Filtrar para Quintero, Puchuncavi y Concon
        zu = zu[(zu['Entidad'] == 'Ciudad') | (zu["Entidad"] == "Pueblo")]
        fig.plot(data=zu, fill=color_urb, transparency=trans) # pen="0.03p,"+color_urb,


        # Plot a rectangle ("r") in the inset map to show the area of the main figure.
        # "+s" means that the first two columns are the longitude and latitude of the bottom
        # left corner of the rectangle, and the last two columns the longitude and latitude
        # of the upper right corner.
        rect_pen = "1.3p,black"
        rectangle = [[region_a[0], region_a[2], region_a[1], region_a[3]]]
        fig.plot(data=rectangle, style="r+s", pen=rect_pen)

        # Define cities with abbreviations
        cities = [
            {"name": "LA", "lon": -70.5969, "lat": -32.8336, "just": "ML", "offset": "0.1c/0c"},
            {"name": "SA", "lon": -70.6693, "lat": -33.4489, "just": "ML", "offset": "0.1c/0c"},
            # {"name": "VA", "lon": -71.6127, "lat": -33.0472, "just": "TL", "offset": "-0.1c/-0.2c"},
            {"name": "VM", "lon": -71.5518, "lat": -33.0245, "just": "TL", "offset": "0.1c/0c"}
        ]
        
        # Plot each city
        for city in cities:
            fig.plot(x=city["lon"], y=city["lat"], style="a0.13c", fill="red")
            fig.text(
                x=city["lon"],
                y=city["lat"], 
                text=city["name"], 
                font="7p,Helvetica-Bold,black", 
                justify=city["just"], 
                offset=city["offset"]
            )

        with pygmt.config(FONT_ANNOT_PRIMARY="5p,Helvetica-Narrow-Bold,black",
                          FONT_LABEL="5p,Helvetica-Narrow-Bold,black"):
            fig.scalebar(length="100k", height="3p",fancy=True, unit=True,
                        #  label_alignment='bottom',label='50 km',
                         position=Position("TR", anchor="TR",offset=(0.3,0.15)))

    # Line 1: Top-Right of main map -> Top-Right of red box in inset
    fig.plot(
        x=[5.0, 5.97],   # [Main map X_edge, Inset red box X] in cm
        y=[7.4, 2.3],   # [Main map Y_top,  Inset red box Y] in cm
        projection="x1c",
        region=[0, 15, 0, 15],
        pen=rect_pen+",4_2:2p",
        no_clip=True,
    )

    # Line 2: Bottom-Right of main map -> Bottom-Left/Right of red box in inset
    fig.plot(
        x=[5.0, 5.97],   # [Main map X_edge, Inset red box X] in cm
        y=[0.0, 2.05],   # [Main map Y_bottom, Inset red box Y] in cm
        projection="x1c",
        region=[0, 15, 0, 15],
        pen=rect_pen+",4_2:2p",
        no_clip=True,
    )
        
    fig.show()
    # Save
    fig.savefig(output_file, dpi=600)





    # # Add inset globe
    # with fig.inset(position="jBR+w2.7c+o-1.7/1c", margin=0):
    #     fig.coast(
    #         region="g",
    #         projection="G-65/-20/?",
    #         land="gray",
    #         water="white",
    #         dcw="Chile+gforestgreen",
    #         frame='g30'
    #     )
    #     x = [-105]  # x vector coordinates
    #     y = [-27.5]  # y vector coordinates
    #     d = [0]  # direction of vectors
    #     l = [0.5]  # length of vectors
    #     # Cartesian vectors (v) with red fill and pen (+g, +p), vector head at the end (+e), and
    #     # 40 degree angle (+a) with no indentation for the vector head (+h)
    #     style = "v0.15c+e+a40+gred+h0+p1p,red"
    #     fig.plot(x=x, y=y, style=style, pen="1p,red", direction=[d, l])
    #     # Estrella en Quintero
    #     fig.plot(x=-71,y=-32,style="a0.2c", pen="0.1p,black", fill="red")



    # # Add zoomed-out inset map
    # with fig.inset(position="jBRR+w3c+o-1c/1c", margin=0):
        
    #     # Force a plain (non-zebra) frame, drawn with a 1p black pen
    #     with pygmt.config(MAP_FRAME_TYPE="plain", MAP_FRAME_PEN="1p,black"):
            
    #         zoom_region = [-72.34, -69.9, -34.2, -31.98]
            
    #         # Plot basemap
    #         # frame="tbrl" will now correctly draw the plain black border on all 4 sides
    #         fig.coast(
    #             region=zoom_region,
    #             projection="M?", 
    #             land="#E6E6E6",
    #             water="#D4E6F1",
    #             shorelines="1/0.3p,black",
    #             borders="1/0.1p,black",
    #             frame="tbrl"
    #         )
            
    #     # Draw the red rectangle for the Quintero-Puchuncaví Bay area bounds[cite: 2]
    #     box_x = [-71.6, -71.4, -71.4, -71.6, -71.6]
    #     box_y = [-32.95, -32.95, -32.7, -32.7, -32.95]
    #     fig.plot(x=box_x, y=box_y, pen="1.2p,red")
        
    #     # Define cities with abbreviations
    #     cities = [
    #         {"name": "LA", "lon": -70.5969, "lat": -32.8336, "just": "ML", "offset": "0.1c/0c"},
    #         {"name": "SA", "lon": -70.6693, "lat": -33.4489, "just": "ML", "offset": "0.1c/0c"},
    #         {"name": "VA", "lon": -71.6127, "lat": -33.0472, "just": "TL", "offset": "-0.08c/-0.05c"},
    #         {"name": "VM", "lon": -71.5518, "lat": -33.0245, "just": "ML", "offset": "0.08c/0c"}
    #     ]
        
    #     # Plot each city
    #     for city in cities:
    #         fig.plot(x=city["lon"], y=city["lat"], style="c0.08c", fill="black")
    #         fig.text(
    #             x=city["lon"], 
    #             y=city["lat"], 
    #             text=city["name"], 
    #             font="7p,Helvetica-Bold,black", 
    #             justify=city["just"], 
    #             offset=city["offset"]
    #         )
