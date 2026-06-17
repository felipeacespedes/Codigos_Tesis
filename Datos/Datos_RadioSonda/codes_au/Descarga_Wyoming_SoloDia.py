#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:54:37 2023

@author: au
"""

import requests
import re


# Función para formatear la fecha en el formato "yyyymmdd"
def format_date(year, month, day):
    return f"{year:04d}{month:02d}{day:02d}"

# Ingresar la fecha manualmente
year = int(input("Ingrese el año: "))
month = int(input("Ingrese el mes: "))
day = int(input("Ingrese el día: "))

try:
    # Desactivar la verificación del certificado SSL
    requests.packages.urllib3.disable_warnings()

    # Construir la URL para el día específico (FROM y TO iguales)
    # url = f"https://weather.uwyo.edu/cgi-bin/sounding?region=samer&TYPE=TEXT%3ALIST&YEAR={year}&MONTH={month:02d}&FROM={day:02d}12&TO={day:02d}12&STNM=85586"
    # url = f"https://weather.uwyo.edu/wsgi/sounding?datetime={year}-{month:02d}-{day:02d}%2012:00:00&id=85586&type=TEXT:CSV&src=BUFR"
    url = f"https://weather.uwyo.edu/cgi-bin/sounding?region=samer&TYPE=TEXT%3ALIST&YEAR={year}&MONTH={month:02d}&FROM={day:02d}12&TO={day:02d}12&STNM=85586"
    # Obtener la fecha formateada en el nombre del archivo
    date_str = format_date(year, month, day)
    path = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_RadioSonda/'
    filename = f"{date_str}_12.txt"

    # Descargar los datos
    response = requests.get(url, verify=False)
    
    # Path
    path = "data/"

    if response.status_code == 200:
        # Buscar la línea de "Station information and sounding indices"
        data = response.text
        texto_index = data.find("Station information and sounding indices")

        if texto_index != -1:
            data = data[:texto_index]  # Obtener solo la parte anterior a la línea

            # Eliminar etiquetas HTML del contenido
            data = re.sub("<[^<]+>", "", data)

            with open(path+filename, "w") as file:
                file.write(data.strip())

            print(f"Datos descargados exitosamente en {filename}.")
        else:
            print(f"No se encontró la línea 'Station information and sounding indices' en {filename}.")
    else:
        print(f"Error al hacer la solicitud HTTP para {filename}.")

finally:
    # Restaurar la verificación del certificado SSL
    requests.packages.urllib3.disable_warnings(False)