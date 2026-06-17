# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 15:16:55 2023

@author: felip
"""
# Libirerías 
import folium
import zipfile
import io

from fastkml import kml

#%% Plot KML file from a KMZ file

# read KML content 
kmz = zipfile.ZipFile("Australia_KMZ/Australia.kmz", 'r')  # extract zip file first, then read kmz file inside the extracted folder
kml_content = kmz.open('doc.kml', 'r').read()  # kml content

# create KML object
k = kml.KML()
k.from_string(kml_content)

# read features from docs to folders to records and then extract geometries - in my case, Shapely points
docs = list(k.features())
folders = []
for d in docs:
    folders.extend(list(d.features()))
records = []
for f in folders:
    records.extend(list(f.features()))
geoms = [element.geometry for element in records]  # extract geometry

# plot the geoms - latitude (y), longitude (x)
import folium
mapit = folium.Map()
for geom in geoms:
    folium.Marker(location=(geom.y, geom.x), fill_color='#43d9de', radius=2).add_to(mapit)
mapit.save('map.html')