# Lucas Castillo Elmes

# Librerias
library(tidyverse)

# Input
dir = 'C:\\Users\\felip\\Desktop\\U\\Tesis\\Datos\\AtChem\\output041022\\'
files = list.files(path = dir, pattern = 'productionRates', recursive = T)
files = paste0(dir, files)

# Datos
data = read_csv(files, id = 'id')
data$id = substr(data$id, 56, 62)
data$PERIOD = substr(data$id, 1,3)
data$RUN = substr(data$id, 5,8)
data$id = NULL
data$...1 = NULL
data$...8 = NULL
data$speciesNumber = NULL
data$type = 'loss'

jan_date = as.POSIXct('2021-01-29 00:00:00', tz = 'UTC')
data$DATE = ifelse(data$PERIOD == 'Jan', jan_date + data$time, data$time)
mar_date = as.POSIXct('2021-03-17 00:00:00', tz = 'UTC')
data$DATE = ifelse(data$PERIOD == 'Mar', mar_date + data$time, data$DATE)
data$DATE = as.POSIXct(data$DATE, tz = 'UTC')
data$DATE = with_tz(data$DATE, tz = 'America/Santiago')

colnames(data) = tolower(colnames(data))
data = dplyr::select(data, c('date', 'period', 'run', 'speciesname', 'rate', 'reaction', 'reactionnumber'))

write_csv(data, 'mar_prod.csv')

