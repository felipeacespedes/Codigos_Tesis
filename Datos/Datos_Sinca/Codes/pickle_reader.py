# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 13:59:33 2024

@author: felip
"""

import pandas as pd

def read_pickle_file(file):
    pickle_data = pd.read_pickle(file)
    return pickle_data