# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 21:07:54 2024

@author: felip
"""

# Importamos librerías
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import seaborn as sns
from datetime import datetime
import sys


## Ajustes heatmaps
# COLORMAP
CMAP = 'turbo'
# CMAP = 'nipy_spectral'
# LINEAS GRILLA
LW = 0.08
LC = (1, 1, 1, 0.3)






# Plot_Prod:
def Plot_Prod(PrR,name_str,sn,fs,n,skip,xtick_delta,date_1,date_2,d0,n_steps):
    # Variables
    # - PrR: Matriz de production rates para compuesto.
    # - name_str: nombre entendible de compuesto (str).
    # - sn: nombre de specie, según MCM.
    # - fs: fig size, formato (l,w).
    # - n: número de reacciónes a mostrar.
    # - skip: número de reacciones a saltar.
    # - xtick_delta: delta en número de minutos a saltar para mostrar en ticks.
    # - date_1/date_2: strings de datetimes inicial y final de figura.
    # - n_steps: numero de steps.
    # Separamos reacciones que producen cov
    PrR_cov = PrR.loc[PrR['speciesName']==sn,:].reset_index()
    PrR_cov = PrR_cov.drop(['index','speciesNumber',
                            'speciesName','Unnamed: 7'],axis=1)
    res = len(PrR_cov.index[PrR_cov.time==d0])
    
    # return PrR_cov, res
    # sys.exit()
    

    # Variables
    PR_cov = pd.to_numeric(PrR_cov.rate.values).reshape([n_steps,res])
    time = pd.to_datetime(PrR_cov.time.values.reshape([n_steps,res])[:,0])
    reaction_name = PrR_cov.reaction.values.reshape([n_steps,res])[0,:]
    reaction_num = PrR_cov.reactionNumber.values.reshape([n_steps,res])[0,:]
    
    # hacer df reaction y poner labels a plot de reacciones correspondientes
    # Creamos DF para reacciones
    react_df = pd.DataFrame({'number':reaction_num,'name':reaction_name})
    react_df = react_df.set_index('number')
    
    # Creamos Dataframe
    PR_df = pd.DataFrame(data=PR_cov, index=time, columns=reaction_num)
    PR_df = PR_df.loc[date_1:date_2,:]
    # Ordenamos por n reacciones más importantes
    PR_df = PR_df.reindex(PR_df.sum().sort_values(ascending=False).index, axis=1)
    del reaction_name, reaction_num, time
                     
    # Creamos caso para cuando el número de reacciones es mayor a 50
    if len(react_df.index)>n:        
        # Cortamos las n necesarias
        PR_df = PR_df.iloc[:,0+skip:n+skip]
    else:
        print('El número de reacciones totales es menor que '+str(n))
    
    # Ploteamos
    fig = plt.subplots(figsize = fs, layout='constrained')

    ax = sns.heatmap(PR_df.transpose(),cmap = CMAP,
                     linewidths=LW,linecolor=LC,
                     xticklabels=xtick_delta)

    ax.set_xticklabels(PR_df.index[ax.get_xticks().astype(int)]\
                       .strftime('%m-%d %H:%M'),rotation=10)
    ax.set_yticklabels(react_df.loc[PR_df.columns,'name'].values,rotation=0)
    ax.set_title("Rates de producción "+name_str+f" por reacción, {date_2[0:10]}.")
    ax.set_xlabel('Hora')
    ax.set_ylabel('Reacciones [ordenadas por relevancia]')
    fig[0].text(0.02,0.96,'+ relevancia',fontsize=11,fontstyle='italic',
                fontweight='bold')
    fig[0].text(0.02,0.03,'- relevancia',fontsize=11,fontstyle='italic',
                fontweight='bold')
    
    # Colorbar
    colorbar = ax.collections[0].colorbar
    colorbar.ax.set_ylabel(r'Rate de producción [$moléculas \ s^{-1}$]', rotation=270, labelpad=20)
    fig[0].get_layout_engine().set(w_pad=0.2, h_pad=0.2)

    
# Plot_Loss:
def Plot_Loss(LoR,name_str,sn,fs,n,skip,xtick_delta,date_1,date_2,d0,n_steps):
    # Variables
    # - LoR: Matriz de loss rates para compuesto.
    # - name_str: nombre entendible de compuesto (str).
    # - sn: nombre de specie, según MCM.
    # - fs: fig size, formato (l,w).
    # - n: número de reacciónes a mostrar.
    # - skip: número de reacciones a saltar.
    # - xtick_delta: delta en número de minutos a saltar para mostrar en ticks.
    # - date_1/date_2: strings de datetimes inicial y final de figura.
    # - n_steps: número de pasos.
    # Separamos reacciones que producen cov
    LoR_cov = LoR.loc[LoR['speciesName']==sn,:].reset_index()
    LoR_cov = LoR_cov.drop(['index','speciesNumber',
                            'speciesName','Unnamed: 7'],axis=1)
    res = len(LoR_cov.index[LoR_cov.time==d0])

    # Variables
    LR_cov = pd.to_numeric(LoR_cov.rate.values).reshape([n_steps,res])
    time = pd.to_datetime(LoR_cov.time.values.reshape([n_steps,res])[:,0])
    reaction_name = LoR_cov.reaction.values.reshape([n_steps,res])[0,:]
    reaction_num = LoR_cov.reactionNumber.values.reshape([n_steps,res])[0,:]
    
    # hacer df reaction y poner labels a plot de reacciones correspondientes
    # Creamos DF para reacciones
    react_df = pd.DataFrame({'number':reaction_num,'name':reaction_name})
    react_df = react_df.set_index('number')
    
    # Creamos Dataframe
    LR_df = pd.DataFrame(data=LR_cov, index=time, columns=reaction_num)
    # Ordenamos por n reacciones más importantes
    LR_df = LR_df.reindex(LR_df.sum().sort_values(ascending=False).index, axis=1)
    
    del reaction_name, reaction_num, time
                     
    # Creamos caso para cuando el número de reacciones es mayor a 50
    if len(react_df.index)>n:        
        # Cortamos las n necesarias
        LR_df = LR_df.iloc[:,0+skip:n+skip]
    else:
        print('El número de reacciones totales es menor que '+str(n))
    
    # Ploteamos
    fig = plt.subplots(figsize = fs, layout='constrained')

    ax = sns.heatmap(LR_df.transpose(),cmap = CMAP,
                     linewidths=LW,linecolor=LC,
                     xticklabels=xtick_delta)

    ax.set_xticklabels(LR_df.loc[date_1:date_2,:].index[ax.get_xticks()\
                                                        .astype(int)]\
                       .strftime('%m-%d %H:%M'),rotation=10)
    ax.set_yticklabels(react_df.loc[LR_df.columns,'name'].values,rotation=0)
    ax.set_title("Rates de perdida "+name_str+f" por reacción, {date_2[0:10]}.")
    ax.set_xlabel('Hora')
    ax.set_ylabel('Reacciones [ordenadas por relevancia]')
    fig[0].text(0.02,0.96,'+ relevancia',fontsize=11,fontstyle='italic',
                fontweight='bold')
    fig[0].text(0.02,0.03,'- relevancia',fontsize=11,fontstyle='italic',
                fontweight='bold')

    # Colorbar
    colorbar = ax.collections[0].colorbar
    colorbar.ax.set_ylabel(r'Rate de perdida [$moléculas \ s^{-1}$]', rotation=270, labelpad=20)
    fig[0].get_layout_engine().set(w_pad=0.2, h_pad=0.2)
    
    
# Plot_Prod_find:
def Plot_Prod_find(PrR,name_str,sn,fn,fs,n,skip,xtick_delta,date_1,date_2,d0,n_steps):
    # Variables
    # - PrR: Matriz de production rates para compuesto.
    # - name_str: nombre entendible de compuesto (str).
    # - sn: nombre de specie, según MCM.
    # - fn: nombre de specie a encontrar, según MCM.
    # - fs: fig size, formato (l,w).
    # - n: número de reacciónes a mostrar.
    # - skip: número de reacciones a saltar.
    # - xtick_delta: delta en número de minutos a saltar para mostrar en ticks.
    # - date_1/date_2: strings de datetimes inicial y final de figura.
    # - n_steps: numero de steps.
    # Separamos reacciones que producen cov
    PrR_cov = PrR.loc[PrR['speciesName']==sn,:].reset_index()
    PrR_cov = PrR_cov.drop(['index','speciesNumber',
                            'speciesName','Unnamed: 7'],axis=1)
    res = len(PrR_cov.index[PrR_cov.time==d0])
    

    # Variables
    PR_cov = pd.to_numeric(PrR_cov.rate.values).reshape([n_steps,res])
    time = pd.to_datetime(PrR_cov.time.values.reshape([n_steps,res])[:,0])
    reaction_name = PrR_cov.reaction.values.reshape([n_steps,res])[0,:]
    reaction_num = PrR_cov.reactionNumber.values.reshape([n_steps,res])[0,:]
    
    # hacer df reaction y poner labels a plot de reacciones correspondientes
    # Creamos DF para reacciones
    react_df = pd.DataFrame({'number':reaction_num,'name':reaction_name})
    react_df = react_df.set_index('number')
    # Creamos Dataframe
    PR_df = pd.DataFrame(data=PR_cov, index=time, columns=reaction_num)
    
    ######################################################################
    ## Seleccionamos solo reacciones que contengan el compuesto buscado ##
    rname_split = react_df['name'].str.split(r"\+|\=")
    rname_bool = rname_split.apply(lambda x: fn in x).tolist()
    if sum(rname_bool)==0:
        return('No se encontró '+fn+' en las reacciones de '+sn)
    PR_df = PR_df.iloc[:,rname_bool]

    # Ordenamos por n reacciones más importantes
    PR_df = PR_df.loc[date_1:date_2,:]
    PR_df = PR_df.reindex(PR_df.sum().sort_values(ascending=False).index, axis=1)
    del reaction_name, reaction_num, time
               
    # Creamos caso para cuando el número de reacciones es mayor a 50
    if len(react_df.index)>n:        
        # Cortamos las n necesarias
        PR_df = PR_df.iloc[:,0+skip:n+skip]
    else:
        print('El número de reacciones totales es menor que '+str(n))
    
    # Ploteamos
    fig = plt.subplots(figsize = fs, layout='constrained')

    ax = sns.heatmap(PR_df.transpose(),cmap = CMAP,
                     linewidths=LW,linecolor=LC,
                     xticklabels=xtick_delta)

    ax.set_xticklabels(PR_df.index[ax.get_xticks().astype(int)]\
                       .strftime('%m-%d %H:%M'),rotation=10)
    ax.set_yticklabels(react_df.loc[PR_df.columns,'name'].values,rotation=0)
    ax.set_title("Rates de producción "+name_str+f" por reacción, {date_2[0:10]}.")
    ax.set_xlabel('Hora')
    ax.set_ylabel('Reacciones [ordenadas por relevancia]')
    fig[0].text(0.02,0.96,'+ relevancia',fontsize=11,fontstyle='italic',
                fontweight='bold')
    fig[0].text(0.02,0.03,'- relevancia',fontsize=11,fontstyle='italic',
                fontweight='bold')
    
    # Colorbar
    colorbar = ax.collections[0].colorbar
    colorbar.ax.set_ylabel(r'Rate de producción [$moléculas \ s^{-1}$]', rotation=270, labelpad=20)
    fig[0].get_layout_engine().set(w_pad=0.2, h_pad=0.2)
    
# Plot_Loss_find:
def Plot_Loss_find(LoR,name_str,sn,fn,fs,n,skip,xtick_delta,date_1,date_2,d0,n_steps):
    # Variables
    # - LoR: Matriz de loss rates para compuesto.
    # - name_str: nombre entendible de compuesto (str).
    # - sn: nombre de specie, según MCM.
    # - fn: nombre de specie a encontrar, según MCM.
    # - fs: fig size, formato (l,w).
    # - n: número de reacciónes a mostrar.
    # - skip: número de reacciones a saltar.
    # - xtick_delta: delta en número de minutos a saltar para mostrar en ticks.
    # - date_1/date_2: strings de datetimes inicial y final de figura.
    # - n_steps: número de pasos.
    # Separamos reacciones que producen cov
    LoR_cov = LoR.loc[LoR['speciesName']==sn,:].reset_index()
    LoR_cov = LoR_cov.drop(['index','speciesNumber',
                            'speciesName','Unnamed: 7'],axis=1)
    res = len(LoR_cov.index[LoR_cov.time==d0])

    # Variables
    LR_cov = pd.to_numeric(LoR_cov.rate.values).reshape([n_steps,res])
    time = pd.to_datetime(LoR_cov.time.values.reshape([n_steps,res])[:,0])
    reaction_name = LoR_cov.reaction.values.reshape([n_steps,res])[0,:]
    reaction_num = LoR_cov.reactionNumber.values.reshape([n_steps,res])[0,:]
    
    # hacer df reaction y poner labels a plot de reacciones correspondientes
    # Creamos DF para reacciones
    react_df = pd.DataFrame({'number':reaction_num,'name':reaction_name})
    react_df = react_df.set_index('number')
    
    # Creamos Dataframe
    LR_df = pd.DataFrame(data=LR_cov, index=time, columns=reaction_num)
    
    ######################################################################
    ## Seleccionamos solo reacciones que contengan el compuesto buscado ##
    rname_split = react_df['name'].str.split(r"\+|\=")
    rname_bool = rname_split.apply(lambda x: fn in x).tolist()
    if sum(rname_bool)==0:
        return('No se encontró '+fn+' en las reacciones de '+sn)
    LR_df = LR_df.iloc[:,rname_bool]
    
    # Ordenamos por n reacciones más importantes
    LR_df = LR_df.loc[date_1:date_2,:]
    LR_df = LR_df.reindex(LR_df.sum().sort_values(ascending=False).index, axis=1)
    
    del reaction_name, reaction_num, time
                     
    # Creamos caso para cuando el número de reacciones es mayor a 50
    if len(react_df.index)>n:        
        # Cortamos las n necesarias
        LR_df = LR_df.iloc[:,0+skip:n+skip]
    else:
        print('El número de reacciones totales es menor que '+str(n))
    
    # Ploteamos
    fig = plt.subplots(figsize = fs, layout='constrained')

    ax = sns.heatmap(LR_df.transpose(),cmap = CMAP,
                     linewidths=LW,linecolor=LC,
                     xticklabels=xtick_delta)

    ax.set_xticklabels(LR_df.loc[date_1:date_2,:].index[ax.get_xticks()\
                                                        .astype(int)]\
                       .strftime('%m-%d %H:%M'),rotation=10)
    ax.set_yticklabels(react_df.loc[LR_df.columns,'name'].values,rotation=0)
    ax.set_title("Rates de perdida "+name_str+f" por reacción, {date_2[0:10]}.")
    ax.set_xlabel('Hora')
    ax.set_ylabel('Reacciones [ordenadas por relevancia]')
    fig[0].text(0.02,0.96,'+ relevancia',fontsize=11,fontstyle='italic',
                fontweight='bold')
    fig[0].text(0.02,0.03,'- relevancia',fontsize=11,fontstyle='italic',
                fontweight='bold')

    # Colorbar
    colorbar = ax.collections[0].colorbar
    colorbar.ax.set_ylabel(r'Rate de perdida [$moléculas \ s^{-1}$]', rotation=270, labelpad=20)
    fig[0].get_layout_engine().set(w_pad=0.2, h_pad=0.2)
    
    
# Return_Prod:
def Return_Prod(PrR,sn,d0,date_1,date_2,n_steps):
    # Variables
    # - PrR: Matriz de production rates para compuesto.
    # - sn: nombre de specie, según MCM.
    # - n_steps: numero de steps.
    # Separamos reacciones que producen cov
    PrR_cov = PrR.loc[PrR['speciesName']==sn,:].reset_index()
    PrR_cov = PrR_cov.drop(['index','speciesNumber',
                            'speciesName','Unnamed: 7'],axis=1)
    res = len(PrR_cov.index[PrR_cov.time==d0])


    # Variables
    PR_cov = pd.to_numeric(PrR_cov.rate.values).reshape([n_steps,res])
    time = pd.to_datetime(PrR_cov.time.values.reshape([n_steps,res])[:,0])
    reaction_name = PrR_cov.reaction.values.reshape([n_steps,res])[0,:]
    reaction_num = PrR_cov.reactionNumber.values.reshape([n_steps,res])[0,:]
    
    # hacer df reaction y poner labels a plot de reacciones correspondientes
    # Creamos DF para reacciones
    react_df = pd.DataFrame({'number':reaction_num,'name':reaction_name})
    react_df = react_df.set_index('number')
    
    # Creamos Dataframe
    PR_df = pd.DataFrame(data=PR_cov, index=time, columns=reaction_num)
    # Cortamos para ordenar en base a ventana escogida
    PR_df = PR_df.loc[date_1:date_2,:]
    # Ordenamos por n reacciones más importantes
    PR_df = PR_df.reindex(PR_df.sum().sort_values(ascending=False).index, axis=1)

    del reaction_name, reaction_num, time
    
    return PR_df, react_df

# Return_Loss:
def Return_Loss(LoR,sn,d0,date_1,date_2,n_steps):
    # Variables
    # - LoR: Matriz de loss rates para compuesto.
    # - d0: fecha inicial de archivo
    # - sn: nombre de specie, según MCM.
    # - n_steps: numero de steps.
    # Separamos reacciones que producen cov
    LoR_cov = LoR.loc[LoR['speciesName']==sn,:].reset_index()
    LoR_cov = LoR_cov.drop(['index','speciesNumber',
                            'speciesName','Unnamed: 7'],axis=1)
    res = len(LoR_cov.index[LoR_cov.time==d0])

    # Variables
    LR_cov = pd.to_numeric(LoR_cov.rate.values).reshape([n_steps,res])
    time = pd.to_datetime(LoR_cov.time.values.reshape([n_steps,res])[:,0])
    reaction_name = LoR_cov.reaction.values.reshape([n_steps,res])[0,:]
    reaction_num = LoR_cov.reactionNumber.values.reshape([n_steps,res])[0,:]
    
    # hacer df reaction y poner labels a plot de reacciones correspondientes
    # Creamos DF para reacciones
    react_df = pd.DataFrame({'number':reaction_num,'name':reaction_name})
    react_df = react_df.set_index('number')
    
    # Creamos Dataframe
    LR_df = pd.DataFrame(data=LR_cov, index=time, columns=reaction_num)
    # Cortamos para ordenar en base a ventana escogida
    LR_df = LR_df.loc[date_1:date_2,:]
    # Ordenamos por n reacciones más importantes
    LR_df = LR_df.reindex(LR_df.sum().sort_values(ascending=False).index, axis=1)
    
    del reaction_name, reaction_num, time
    
    return LR_df, react_df
                     

    
# DF_reacts:
def DF_reacts(PoL,sn,n_steps,d0,date_1,date_2):
    # Variables
    # - PoL: Matriz de production or loss rates para compuesto.
    # - sn: nombre de specie, según MCM.
    # - n_steps: número de pasos.

    
    # Separamos reacciones que producen cov
    PoL_cov = PoL.loc[PoL['speciesName']==sn,:].reset_index()
    PoL_cov = PoL_cov.drop(['index','speciesNumber',
                            'speciesName','Unnamed: 7'],axis=1)
    res = len(PoL_cov.index[PoL_cov.time==d0])

    # Variables
    PL_cov = pd.to_numeric(PoL_cov.rate.values).reshape([n_steps,res])
    time = pd.to_datetime(PoL_cov.time.values.reshape([n_steps,res])[:,0])
    reaction_name = PoL_cov.reaction.values.reshape([n_steps,res])[0,:]
    reaction_num = PoL_cov.reactionNumber.values.reshape([n_steps,res])[0,:]
    
    # hacer df reaction y poner labels a plot de reacciones correspondientes
    # Creamos DF para reacciones
    react_df = pd.DataFrame({'number':reaction_num,'name':reaction_name})
    react_df = react_df.set_index('number')
    
    # Creamos Dataframe
    PL_df = pd.DataFrame(data=PL_cov, index=time, columns=reaction_num)
    # Cortamos fechas para ordenar en base a ventana escogida
    PL_df = PL_df.loc[date_1:date_2,:]
    # Ordenamos por n reacciones más importantes
    PL_df = PL_df.reindex(PL_df.sum().sort_values(ascending=False).index, axis=1)
    
    del reaction_name, reaction_num, time
    
    return PL_df, react_df
    
    
# Concentration
def Plot_Conc(CCS, comp, fs, log, vmin, vmax, cp, d_h,date_1,date_2):
    # Variables
    # - CCS: DataFrame de concentraciones
    # - comp: lista de strings de compuestos a plotear
    # - fs: figsize en formato (n,m).
    # - log: Booleano para plotear heatmap en escala logaritmica.
    # - vmin: valor mínimo de colorbar.
    # - vmax: valor máximo de colorbar.
    # - cp: color palette
    # - n_steps: número de pasos.
    

    fig = plt.subplots(figsize = fs, layout='constrained')
    
    if log == True:
        ax = sns.heatmap(CCS.loc[date_1:date_2,comp].transpose(),
                         cmap =cp,
                         linewidths=LW,linecolor=LC,
                         cbar_kws={"pad": -0.01},
                         norm=LogNorm(vmin=vmin,vmax=vmax))
    else:
        ax = sns.heatmap(CCS.loc[date_1:date_2,comp].transpose(),
                         cmap =cp,
                         linewidths=LW,linecolor=LC,
                         vmin=vmin,vmax=vmax,cbar_kws={"pad": -0.01})

    # tomamos largo de index
    len_ind = len(CCS.loc[date_1:date_2].index)
    step = d_h*60
    ax.set_xticks(np.arange(0,len_ind,1)[0:len_ind:step])
    ax.set_xticklabels(CCS.index[0:len_ind:step].strftime('%m-%d %H:%M'),
                       rotation=10)
    ax.set_title(f"Concentración por compuesto, {date_2[0:10]}.")
    ax.set_xlabel('Hora')
    ax.set_ylabel('Compuestos')
    # Colorbar
    cax = ax.collections[0].colorbar.ax
    cax.set_ylabel('Concentración [mol/cm3]', rotation=270, labelpad=20)
    fig[0].get_layout_engine().set(w_pad=0.2, h_pad=0.2)
    
# Calc_Prod:
def Calc_Prod(PrR,sn,d0,date_1,date_2,n_steps):
    # Variables
    # - PrR: Matriz de production rates para compuesto.
    # - sn: nombre de specie, según MCM.
    # - rn: nombre de reacción, según MCM.
    # - n_steps: numero de steps.
    # Separamos reacciones que producen cov
    PrR_cov = PrR.loc[PrR['speciesName']==sn,:].reset_index()
    PrR_cov = PrR_cov.drop(['index','speciesNumber',
                            'speciesName','Unnamed: 7'],axis=1)
    res = len(PrR_cov.index[PrR_cov.time==d0])


    # Variables
    PR_cov = pd.to_numeric(PrR_cov.rate.values).reshape([n_steps,res])
    time = pd.to_datetime(PrR_cov.time.values.reshape([n_steps,res])[:,0])
    reaction_name = PrR_cov.reaction.values.reshape([n_steps,res])[0,:]
    reaction_num = PrR_cov.reactionNumber.values.reshape([n_steps,res])[0,:]
    
    # hacer df reaction y poner labels a plot de reacciones correspondientes
    # Creamos DF para reacciones
    react_df = pd.DataFrame({'number':reaction_num,'name':reaction_name})
    react_df = react_df.set_index('number')
    
    # Creamos Dataframe
    PR_df = pd.DataFrame(data=PR_cov, index=time, columns=reaction_num)
    
    # Calculamos segundos
    date_1 = pd.to_datetime(date_1)
    date_2 = pd.to_datetime(date_2)
    
    # Hacemos la suma de producción de moleculas entre fechas
    PR_df = PR_df.loc[date_1:date_2].sum()*300
    PR_sum = pd.DataFrame({'sum':PR_df,'prct':(PR_df/PR_df.sum())*100,
                           'name':reaction_name,'number':reaction_num})
    sum_row = pd.Series({'sum':PR_sum['sum'].sum(),'prct':100
                         ,'name':'Total','number':0})
    PR_sum = pd.concat([PR_sum,sum_row.to_frame().T],ignore_index=True)
    PR_sum = PR_sum.sort_values(by='sum',ascending=False).reset_index(drop=True)
    PR_sum = PR_sum.astype(dtype= {"sum":"float64","prct":"float64",
                                   "name":"object","number":"int64"})
    return PR_sum
    
# Calc_Loss:
def Calc_Loss(LoR,sn,d0,date_1,date_2,n_steps):
    # Variables
    # - LoR: Matriz de loss rates para compuesto.
    # - d0: fecha inicial de archivo
    # - sn: nombre de specie, según MCM.
    # - n_steps: numero de steps.
    # Separamos reacciones que producen cov
    LoR_cov = LoR.loc[LoR['speciesName']==sn,:].reset_index()
    LoR_cov = LoR_cov.drop(['index','speciesNumber',
                            'speciesName','Unnamed: 7'],axis=1)
    res = len(LoR_cov.index[LoR_cov.time==d0])

    # Variables
    LR_cov = pd.to_numeric(LoR_cov.rate.values).reshape([n_steps,res])
    time = pd.to_datetime(LoR_cov.time.values.reshape([n_steps,res])[:,0])
    reaction_name = LoR_cov.reaction.values.reshape([n_steps,res])[0,:]
    reaction_num = LoR_cov.reactionNumber.values.reshape([n_steps,res])[0,:]
    
    # hacer df reaction y poner labels a plot de reacciones correspondientes
    # Creamos DF para reacciones
    react_df = pd.DataFrame({'number':reaction_num,'name':reaction_name})
    react_df = react_df.set_index('number')
    
    # Creamos Dataframe
    LR_df = pd.DataFrame(data=LR_cov, index=time, columns=reaction_num)
    
    # Calculamos segundos
    date_1 = pd.to_datetime(date_1)
    date_2 = pd.to_datetime(date_2)
    
    # Hacemos la suma de producción de moleculas entre fechas
    LR_df = LR_df.loc[date_1:date_2].sum()*300
    LR_sum = pd.DataFrame({'sum':LR_df,'prct':(LR_df/LR_df.sum())*100,
                           'name':reaction_name,'number':reaction_num})
    sum_row = pd.Series({'sum':LR_sum['sum'].sum(),'prct':100
                         ,'name':'Total','number':0})
    LR_sum = pd.concat([LR_sum,sum_row.to_frame().T],ignore_index=True)
    LR_sum = LR_sum.sort_values(by='sum',ascending=False).reset_index(drop=True)
    LR_sum = LR_sum.astype(dtype= {"sum":"float64","prct":"float64",
                                   "name":"object","number":"int64"})
    return LR_sum

# Calc_find:
def Calc_find(LoR,sn,find,but,RoP,d0,date_1,date_2,n_steps):
    # Variables
    # - LoR: Matriz de loss rates para compuesto.
    # - sn: nombre de specie, según MCM.
    # - find: string con diferenciadores a sumar. Caracteres especiales deben
    #         como "+.{}"... deben llevar un '\' antes. El '.' marca inicio y fin.
    # - RoP: string  o lista de strings con 'R' o 'P' para reactante o producto.
    # - d0: fecha inicial de archivo.
    # - date_1/2: fecha inicial/final a usar para el calculo.
    # - n_steps: numero de steps.
    # Separamos reacciones que producen cov
    LoR_cov = LoR.loc[LoR['speciesName']==sn,:].reset_index()
    LoR_cov = LoR_cov.drop(['index','speciesNumber',
                            'speciesName','Unnamed: 7'],axis=1)
    res = len(LoR_cov.index[LoR_cov.time==d0])

    # Variables
    LR_cov = pd.to_numeric(LoR_cov.rate.values).reshape([n_steps,res])
    time = pd.to_datetime(LoR_cov.time.values.reshape([n_steps,res])[:,0])
    reaction_name = LoR_cov.reaction.values.reshape([n_steps,res])[0,:]
    reaction_num = LoR_cov.reactionNumber.values.reshape([n_steps,res])[0,:]
    
    # hacer df reaction y poner labels a plot de reacciones correspondientes
    # Creamos DF para reacciones
    react_df = pd.DataFrame({'number':reaction_num,'name':reaction_name})
    react_df = react_df.set_index('number')
    
    # Creamos Dataframe
    LR_df = pd.DataFrame(data=LR_cov, index=time, columns=reaction_num)
    
    # Calculamos segundos
    date_1 = pd.to_datetime(date_1)
    date_2 = pd.to_datetime(date_2)
    
    # Hacemos la suma de producción de moleculas entre fechas
    LR_df = LR_df.loc[date_1:date_2].sum()*300
    LR_sum = pd.DataFrame({'sum':LR_df,'prct':(LR_df/LR_df.sum())*100,
                           'name':reaction_name,'number':reaction_num})
    LR_sum = LR_sum.sort_values(by='sum',ascending=False).reset_index(drop=True)
    LR_name = LR_sum['name']
    cols = LR_sum['name'].str.split('=',expand=True)
    cols[0] = '.'+cols[0].astype(str)+'='
    cols[1] = '='+cols[1].astype(str)+'.'

    # Sumamos las reacciones de interés
    if type(find) == str:
        if RoP == 'R':
            inc = cols[0].str.contains(find,regex=True)
            exc = ~cols[0].str.contains(but,regex=True)
            lsum = LR_sum.loc[inc & exc,'sum'].sum()
        elif RoP == 'P':
            inc = cols[1].str.contains(find,regex=True)
            exc = ~cols[1].str.contains(but,regex=True)
            lsum = LR_sum.loc[inc & exc,'sum'].sum()
        else:
            sys.exit("PoR debe ser un string 'R' o 'P', de reactante o producto.")
    else:
        sys.exit("find debe ser un string.")
        
    # Agregamos la fila de suma
    sum_row = pd.Series({'sum':lsum,'prct':(lsum/LR_df.sum())*100,
                         'name':'suma','number':0})
    LR_sum = pd.concat([sum_row.to_frame().T,LR_sum],ignore_index=True)
    LR_sum = LR_sum.sort_values(by='sum',ascending=False).reset_index(drop=True)
    LR_sum = LR_sum.astype(dtype= {"sum":"float64","prct":"float64",
                                   "name":"object","number":"int64"})

    
    return LR_sum, LR_name.loc[inc & exc]


    