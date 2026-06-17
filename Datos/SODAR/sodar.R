# Lucas Castillo Elmes

# Librerias
library(tidyverse)
library(openair)
library(lattice)
library(lubridate)


# Datos SODAR
dir = './RawSodar/' # Directorio de los datos
files =  list.files(path = dir) # Busca todos los archivos en el directorio
files = paste0(dir, files) 

data_s = read_tsv(files, skip = 10, na = c('*', NA)) # Lee archivos
data_s = filter(data_s, z == 100) # Filtra archivos solo con z = 100

colnames(data_s)[1] = 'date' # Cambio el nombre de la columna time para que sea igual

# Datos COV
data_cov = read_csv('VOC_Q.csv')

# Juntar datos
data = full_join(data_s, data_cov, by = 'date')

# Graficos

pol = 'Benzene'
paleta = 'default'

data2 = dplyr::select(data, c('date', pol, 'speed', 'dir'))
colnames(data2) = c('date', pol, 'ws', 'wd')


polarFreq(data2, pollutant = pol, statistic = 'mean', type = 'daylight',
          latitude = -32.78, longitude = -71.52,
          key.position = 'bottom', trans = F, cols = paleta,
          key = list(plot.style = c("ticks", "border"), fit = "all"))

f = polarPlot(data, pollutant = pol, x = 'speed', wd = 'dir', statistic = 'mean',
          type = 'daylight',  latitude = -32.78, longitude = -71.52,
          key.position = 'bottom', key.footer= paste0(pol, ', ppbv'), 
          key.header = '', cols = paleta,  
          strip = FALSE,
          key = list(plot.style = c("ticks", "border"), fit = "all"),
          par.settings=list(fontsize=list(text=12)))
          

# strip.custom(factor.levels = c('Day','Night'))



