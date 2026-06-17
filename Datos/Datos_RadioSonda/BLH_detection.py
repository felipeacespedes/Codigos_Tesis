# -*- coding: utf-8 -*-
"""
Created on Tue May 26 15:52:07 2026

@author: felip
"""

import os
import pandas as pd
from datetime import datetime, timedelta

# Define the start and end dates for your analysis
start_date = datetime(2022, 1, 1, 0)   # Jan 1, 2022, 00:00
end_date = datetime(2023, 12, 31, 12)  # Dec 31, 2023, 12:00

# Directory where your daily text files are stored 
# (Leave as '.' if they are in the same folder as this script)
data_directory = 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_RadioSonda/data' 
output_filename = 'BLH.txt'

# Open the output file once before starting the loop
with open(output_filename, 'w') as outfile:
    # Optional: Write a header line for your output file
    outfile.write("date,BLH\n")
    
    current_date = start_date
    
    while current_date <= end_date:
        # Format the datetime into your specific naming convention: yyyymmdd_hh.txt
        date_str = current_date.strftime('%Y%m%d')
        hour_str = current_date.strftime('%H')
        filename = f"{date_str}_{hour_str}.txt"
        filepath = os.path.join(data_directory, filename)
        
        # Check if the file exists for this specific 12-hour interval
        if os.path.exists(filepath):
            
            with open(filepath, 'r') as f:
                lines = f.readlines()
                data_start = None
                for i, line in enumerate(lines):
                    if "PRES   HGHT   TEMP" in line:
                        data_start = i + 3
                        break
            # Cargamos archivo a DF
            df = pd.read_csv(filepath, skiprows=data_start, sep='\\s+',
                             names=["PRES", "HGHT", "TEMP", "DWPT", "RELH", "MIXR",
                                    "DRCT", "SKNT", "THTA", "THTE", "THTV"],
                             na_values=['*****', '99999', 'NaN', 'NaN*', ''])
            
            # Creamos pendiente de Temperatura según altura
            d1_T = df['TEMP'].diff(periods=-1) / df['HGHT'].diff(periods=-1)
            H = df['HGHT']
            
            # Calculo cambio positivo en pendiente
            for i in range(len(H)):
                if d1_T[i] > 0:
                    blh = H[i]
                    # print('BLH = '+str(blh))
                    break
                elif H[i] > 2000:
                    blh = 'nan'
                    break
                elif i == len(H)-1: 
                    print('No se encontró pendiente positiva')

        else:
            # If the file is missing, set parameter to 'nan'
            blh = 'nan'
            
        # Write the result to your output file
        # Formatted as: YYYY-MM-DD HH:00, blh
        outfile.write(f"{current_date.strftime('%Y-%m-%d %H:00')},{blh}\n")
        
        # Increment the time by exactly 12 hours
        current_date += timedelta(hours=12)

print(f"Processing complete. Results saved to {output_filename}")