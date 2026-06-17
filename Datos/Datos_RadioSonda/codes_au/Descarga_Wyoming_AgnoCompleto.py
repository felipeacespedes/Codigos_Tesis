#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:03:35 2023

@author: au
"""

import requests
import re


# DEFINIR PARAMETROS
year = 2023
max_retries = 2  # Cantidad máxima de reintentos en caso de error
hh = '12' # '00' ó '12'
path = "data/"

# Función para formatear la fecha en el formato "yyyymmdd"
def format_date(year, month, day):
    return f"{year:04d}{month:02d}{day:02d}"

# Descargamos archivos hh para año year 
try:
    # Desactivar la verificación del certificado SSL
    requests.packages.urllib3.disable_warnings()

    # Iterar por los meses del año
    for month in range(1, 13):
        # Obtener la cantidad de días en el mes actual
        if month in [1, 3, 5, 7, 8, 10, 12]:
            days_in_month = 31
        elif month in [4, 6, 9, 11]:
            days_in_month = 30
        else:  # February
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                days_in_month = 29
            else:
                days_in_month = 28
        
        
        # Iterar por los días del mes actual
        for day in range(1, days_in_month + 1):
            # Construir la URL para el día específico (FROM y TO iguales)
            url = f"https://weather.uwyo.edu/cgi-bin/sounding?region=samer&TYPE=TEXT%3ALIST&YEAR={year}&MONTH={month:02d}&FROM={day:02d}{hh}&TO={day:02d}{hh}&STNM=85586"

            # Obtener la fecha formateada en el nombre del archivo
            date_str = format_date(year, month, day)
            filename = f"{date_str}_{hh}.txt"

            # Intentar realizar la solicitud HTTP con reintentos
            for retry in range(max_retries):
                response = requests.get(url, verify=False)

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
                        
                        
                    break  # Salir del bucle de reintentos si se logra descargar exitosamente
                else:
                    print(f"Error al hacer la solicitud HTTP para {filename}. Reintentando...")

            else:
                # Si no se logra descargar después de max_retries intentos, imprimir un mensaje y continuar con el siguiente día
                print(f"Error al hacer la solicitud HTTP para {filename} después de {max_retries} intentos. Continuando con el siguiente día.")


finally:
    # Restaurar la verificación del certificado SSL
    requests.packages.urllib3.disable_warnings(False)
