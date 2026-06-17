# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 10:50:08 2026

@author: felip
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

path_data = 'C:/Users/felip/Desktop/U/Tesis/Datos/Inventarios_Emisiones/'
path_fig = 'C:/Users/felip/Desktop/U/Tesis/Figs/Overleaf/introduccion/Emisiones/'

# Configuración global de estilo
plt.rcParams['axes.axisbelow'] = True # Asegura que la grilla quede detrás

def procesar_y_graficar(nombre_archivo, nombre_columna_valor, incluir_total=False, n_top=10):
    """
    Args:
        nombre_archivo (str): Prefijo del archivo (ej. 'COVs').
        nombre_columna_valor (str): Nombre de la columna (ej. 'COVs (T/año)').
        incluir_total (bool): True para graficar la fila 'TOTAL', False para excluirla.
        n_top (int): Número de instalaciones a mostrar (las N con mayores emisiones).
    """
    
    # --- 1. Carga y Limpieza ---
    # Cargamos 2022
    path_2022 = f"{path_data}2022/{nombre_archivo}_2022.csv"
    df_22 = pd.read_csv(path_2022)
    
    if 'SO2' in nombre_archivo:
        df_22.iloc[:,1] = df_22.iloc[:,1].astype(str).str.replace('.', '', regex=False)
    df_22.iloc[:,1] = df_22.iloc[:,1].astype(str).str.replace(',', '.', regex=False).astype(float)
    df_22 = df_22.rename(columns={df_22.columns[1]: '2022'})
    
    # Cargamos 2023
    path_2023 = f"{path_data}2023/{nombre_archivo}_2023.csv"
    df_23 = pd.read_csv(path_2023)
    
    if 'SO2' in nombre_archivo:
        df_23.iloc[:,1] = df_23.iloc[:,1].astype(str).str.replace('.', '', regex=False)
    df_23.iloc[:,1] = df_23.iloc[:,1].astype(str).str.replace(',', '.', regex=False).astype(float)
    df_23 = df_23.rename(columns={df_23.columns[1]: '2023'})

    # --- 2. Unificación ---
    df_merged = pd.merge(df_22, df_23, on='INSTALACIÓN', how='outer')
    
    # --- 3. Filtrado de TOTAL ---
    if not incluir_total:
        df_merged = df_merged[df_merged['INSTALACIÓN'].str.upper().str.strip() != 'TOTAL']

    # --- 4. Ordenamiento y Corte (Top N) ---
    df_merged['Max_Emision'] = df_merged[['2022', '2023']].max(axis=1)
    df_sorted = df_merged.sort_values(by='Max_Emision', ascending=True).tail(n_top)
    
    # CAMBIO AQUÍ: Seleccionamos 2023 PRIMERO para que se dibuje abajo
    df_plot = df_sorted.set_index('INSTALACIÓN')[['2023', '2022']]
    
    # --- 5. Textos y Gráfico ---
    partes_nombre = nombre_columna_valor.split(' ', 1)
    titulo = partes_nombre[0]
    unidad = partes_nombre[1] if len(partes_nombre) > 1 else ""

    fig, ax = plt.subplots(figsize=(7, max(4, n_top * 0.5)))
    
    # CAMBIO AQUÍ: Colores invertidos (Naranja primero, Azul segundo) para coincidir con el orden de columnas
    df_plot.plot(kind='barh', ax=ax, color=['tab:orange', 'tab:blue'], width=0.8)
    
    ax.set_title(f"Emisiones de {nombre_archivo}", fontsize=12, pad=10)#(Top {n_top})"
    ax.set_xlabel(unidad, fontsize=12)
    ax.set_ylabel("", fontsize=12)
    ax.grid(zorder=0, alpha=0.2)
    
    # CAMBIO AQUÍ: Invertir el orden de la leyenda para que muestre 2022 arriba
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(reversed(handles), reversed(labels), title="Año",loc='lower right')
    
    plt.tight_layout()
    plt.savefig(path_fig+nombre_archivo,dpi=300)
