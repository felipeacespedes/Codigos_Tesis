# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 12:24:14 2026

@author: felip
"""

import matplotlib.pyplot as plt
import numpy as np

# Datos extraídos del párrafo de tu tesis
dates = [1955, 1964, 1966, 1966, 1977, 1981, 1995, 2004, 2006, 2008, 2009]
events = [
    "ENAP Aconcagua\n(Refinería petróleo)",
    "ENAMI Ventanas\n(Fundición cobre)",
    "Central Ventanas I\n(Termoeléctrica carbón)",
    "Puerto Ventanas\nChilgener",
    "Central Ventanas II\n(Termoeléctrica carbón)",
    "Terminal marítimo\nOXIQUIM",
    "Terminal marítimo\nGASMAR",
    "Planta lubricantes\nCOPEC",
    "Central Nueva Ventanas\n(Termoeléctrica carbón)",
    "Central Campiche\n(Termoeléctrica carbón)",
    "Terminal marítimo\nGNL Quintero"
]

#%% Crear figura y eje

fig, ax = plt.subplots(figsize=(10, 4), constrained_layout=True)
ax.set_title("Llegada de Industrias a la Macrozona Concón-Quintero-Puchuncaví", fontsize=14, fontweight="bold", pad=30)

# Línea base (la línea de tiempo principal) - zorder bajo (capa 1)
ax.axhline(0, color="black", linewidth=2, zorder=1)

# Crear niveles alternados para las etiquetas
levels = np.array([2.5, -2.5, 4.5, -4.5, 2.5, -2.5, 4.5, -4.5, 2.5, -2.5, 4.5])

# Dibujar las líneas verticales (trazos) y los puntos en la línea de tiempo - zorder medio (capas 2 y 3)
ax.vlines(dates, 0, levels, color="tab:blue", linestyles="dashed", alpha=0.7, zorder=2)
ax.plot(dates, np.zeros_like(dates), "-o", color="black", markerfacecolor="white", markersize=8, zorder=3)

# Añadir los años LIGERAMENTE SOBRE la línea de tiempo e INCLINADOS 45° - zorder ALTO (capa 10)
for d in dates:
    # d es el año (coordenada x), 0.2 es el desplazamiento vertical hacia arriba.
    ax.text(d, 0.2, str(d), 
            horizontalalignment='left', # Alineación a la izquierda para que 'nazca' desde el punto
            verticalalignment='bottom', 
            fontsize=10, 
            fontweight='bold', 
            rotation=45, # Inclinación de 45 grados
            zorder=10)

# Añadir los cuadros de texto (los globos de empresa) - zorder MUY ALTO (capa 15)
# Aumenté ligeramente levels y xytext para dar espacio a los años inclinados.
for d, l, r in zip(dates, levels, events):
    ax.annotate(r, xy=(d, l),
                xytext=(0, np.sign(l)*8), textcoords="offset points",
                horizontalalignment="center",
                verticalalignment="bottom" if l > 0 else "top",
                fontsize=9,
                bbox=dict(boxstyle="round,pad=0.4", fc="aliceblue", ec="steelblue", lw=1),
                zorder=15)

# Formatear el eje X: Eliminar las marcas (ticks) y etiquetas originales de abajo
ax.set_xticks([]) # Elimina las marcas y etiquetas por defecto del eje
ax.set_xlim(1952, 2012)
ax.set_ylim(-6, 6) # Ajustar límites verticales para dar aire

# Ocultar el eje Y y los bordes innecesarios
ax.yaxis.set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False) 

# Guardar la figura en alta resolución
plt.savefig('linea_tiempo_CQP_anhos_inclinados.png', dpi=300, bbox_inches='tight')
plt.show()