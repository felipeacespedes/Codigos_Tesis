# -*- coding: utf-8 -*-
"""
Created on Fri Jan  2 20:39:31 2026

@author: felip
"""

import pandas as pd

df = pd.read_csv('table.csv')

# Defining the mapping of MCM names to IUPAC and Formula
# Format: (Name-part)radical
# Formula: CxHyOz

mapping = {
    'HYPROPO2': {'IUPAC': '(1-Hydroxypropane-2-ylperoxy)radical', 'Formula': 'C3H7O3'},
    'HYPROPO': {'IUPAC': '(1-Hydroxypropane-2-yloxy)radical', 'Formula': 'C3H7O2'},
    'IPROPOLO2': {'IUPAC': '(2-Hydroxypropylperoxy)radical', 'Formula': 'C3H7O3'},
    'IPROPOLO': {'IUPAC': '(2-Hydroxypropoxy)radical', 'Formula': 'C3H7O2'},
    'NBUTOLAO2': {'IUPAC': '(1-Hydroxybutan-2-ylperoxy)radical', 'Formula': 'C4H9O3'},
    'NBUTOLAO': {'IUPAC': '(1-Hydroxybutan-2-yloxy)radical', 'Formula': 'C4H9O2'},
    'HO3C4O2': {'IUPAC': '(2-Hydroxybutan-1-ylperoxy)radical', 'Formula': 'C4H9O3'},
    'HO3C4O': {'IUPAC': '(2-Hydroxybutan-1-yloxy)radical', 'Formula': 'C4H9O2'},
    'IBUTOLBO2': {'IUPAC': '[2-Hydroxy-2-methylpropylperoxy]radical', 'Formula': 'C4H9O3'}, # Wait, IBUTOLBO2 InChI is 1-hydroxy-2-methyl-2-peroxy
    'IBUTOLBO': {'IUPAC': '(1-Hydroxy-2-methylpropan-2-yloxy)radical', 'Formula': 'C4H9O2'},
    'TBUTOLO2': {'IUPAC': '(2-Hydroxy-2-methylpropylperoxy)radical', 'Formula': 'C4H9O3'},
    'TBUTOLO': {'IUPAC': '(2-Hydroxy-2-methylpropyloxy)radical', 'Formula': 'C4H9O2'},
    'PE1ENEAO2': {'IUPAC': '(1-Hydroxypentan-2-ylperoxy)radical', 'Formula': 'C5H11O3'},
    'PE1ENEAO': {'IUPAC': '(1-Hydroxypentan-2-yloxy)radical', 'Formula': 'C5H11O2'},
    'PE1ENEBO2': {'IUPAC': '(2-Hydroxypentan-1-ylperoxy)radical', 'Formula': 'C5H11O3'},
    'PE1ENEBO': {'IUPAC': '(2-Hydroxypentan-1-yloxy)radical', 'Formula': 'C5H11O2'}
}

# Refine IBUTOLBO2 based on MCM
# IBUTOLBO2 (InChI: InChI=1S/C4H9O3/c1-4(2,7-6)3-5/h5H,3H2,1-2H3)
# -> 2-methyl-2-peroxypropan-1-ol?
# -> (1-hydroxy-2-methylpropan-2-ylperoxy)radical
mapping['IBUTOLBO2'] = {'IUPAC': '(1-Hydroxy-2-methylpropan-2-ylperoxy)radical', 'Formula': 'C4H9O3'}

# Update the DataFrame
for index, row in df.iterrows():
    mcm_name = row['MCM']
    if mcm_name in mapping:
        df.at[index, 'IUPAC'] = mapping[mcm_name]['IUPAC']
        df.at[index, 'Formula'] = mapping[mcm_name]['Formula']

df.to_csv('table_updated.csv', index=False)
print(df)