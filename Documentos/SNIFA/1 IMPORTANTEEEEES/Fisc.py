# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 15:39:32 2025

@author: felip
"""

import pandas as pd

#%% Cargamos datos de Fiscalizaciones

path = 'C:/Users/felip/Desktop/U/Tesis/Documentos/SNIFA/Fiscalizaciones.csv'
Fisc_df = pd.read_csv(path)

#%% Tomamos solo las de interés

#%% Concón-Quintero-Puchuncací
mask = (Fisc_df['ComunaNombre']=='Concón') |\
       (Fisc_df['ComunaNombre']=='Quintero') |\
       (Fisc_df['ComunaNombre']=='Puchuncaví')
CQP_df = Fisc_df.loc[mask]

#%% Enap Terminal Maritimo Quintero
mask = (Fisc_df['UnidadFiscalizableId']==2784)
ENAP_TM = Fisc_df.loc[mask]

#%% Oxiquim Terminal Maritimo Quintero
mask = (Fisc_df['UnidadFiscalizableId']==1648)
Oxiq_TM = Fisc_df.loc[mask]
