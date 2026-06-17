# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 15:32:10 2024

@author: felip

Código para crear archivo .txt con lista de links FNL. Los links tendran las 
fechas de descarga de cada un delta designado. El link original es:
 https://data.rda.ucar.edu/ds083.3/2024/202404/gdas1
.fnl0p25.2022082500.f00.grib2  \
"""

import pandas as pd

#%% Seteamos variables

# path de archivo txt
path = 'C:/Users/felip/Desktop/U/Tesis/Corrida_WRF/WPS/'

# año y mes actual
año = '2024'
mes = '09'

# seteamos fecha inical, final y delta
Fi = '2022-09-25 00:00:00'
Ff = '2022-10-10 00:00:00'
delta = '6H'

# creamos pandas date_range
dates = pd.date_range(Fi,Ff,freq = delta)

#%% Creamos lista de strings 

## Link antiguo 
# date_links = []
# for d in dates:
#     # creamos parte inicial y final de link
#     link_i = 'https://data.rda.ucar.edu/ds083.3/'+str(d.year)+'/'+str(d.year)\
#               +d.strftime('%m')+'/gdas1.fnl0p25.'
#     link_f = '.f00.grib2'
#     date_links.append(link_i+d.strftime('%Y%m%d%H')+link_f)


## Link nuevo
# https://data.rda.ucar.edu/d083003/2022/202208/gdas1.fnl0p25.2022080212.f00.grib2
date_links = []
for d in dates:
    # creamos parte inicial y final de link
    link_i = 'https://data.rda.ucar.edu/d083003/'+str(d.year)+'/'+str(d.year)\
              +d.strftime('%m')+'/gdas1.fnl0p25.'
    link_f = '.f00.grib2'
    date_links.append(link_i+d.strftime('%Y%m%d%H')+link_f)

#%% Creamos archivo .txt

with open(path+"FNL_date_links.txt", "w") as textFile:
    for link in date_links:
        textFile.write("  "+link+"  \\ "+ "\n")
    print(link)


