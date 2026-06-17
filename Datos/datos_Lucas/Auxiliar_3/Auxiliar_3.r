# Auxiliar 3
# Lucas Castillo  
# lcastilloelmes@gmail.com

# Importar Librerias
library(lubridate)
library(tidyverse)
library(openair)

# Preparar datos ----------------------------------------------
# Creamos una seccion con muchos guiones '#-----'

# Leer datos
# Podemos ocupar cualquier funcion de readr (tidyverse), me gusta usar
# esta porque es mas general, necesitamos el nombre del archivo
# que tiene que estar en la misma carpeta, el delimitador que depende
# del archivo (coma, puntocoma, tab, etc) y cuales son nuestros valores NA.
# Datos horarios de SINCA, estacion Puente Alto
O3 = read_delim('O3.csv', delim = ';', na = c('', 'NA'))
WDIR = read_delim('WDIR.csv', delim = ';', na = c('', 'NA'))
WSPD = read_delim('WSPD.csv', delim = ';', na = c('', 'NA'))
NOX = read_delim('NOX.csv', delim = ';', na = c('', 'NA'))

# Alternativamente, para saltarnos lineas usamos "skip" si todas las lineas
# que queremos saltarnos tienen un denominador en comun podemos usar comment = '#'
# donde # es el comentario (este simbolo puede cambiar)
O3_Alt = read_delim('O3_CLVS15_2018-2021.csv', delim = ';', skip = 27, na = c(-999, 'NA'))

# Encontrar un factor en comun
# Un dataframe es como una tabla donde cada columna se llama con un $
# Paste es para juntar dos strings con una separacion especifica
O3$date = paste(O3$`FECHA (YYMMDD)`,O3$`HORA (HHMM)`, sep = '')
WDIR$date = paste(WDIR$`FECHA (YYMMDD)`,WDIR$`HORA (HHMM)`, sep = '')
WSPD$date = paste(WSPD$`FECHA (YYMMDD)`,WSPD$`HORA (HHMM)`, sep = '')
NOX$date = paste(NOX$`FECHA (YYMMDD)`,NOX$`HORA (HHMM)`, sep = '')

# Ignorar columnas que no sirven
# Lo hacemos con select, podemos usar el numero de la columna o el nombre
# Si queremos todas las columnas menos algunas, usamos un numero negativo
# El vector se crea con c(,) que significa "combine"
# Con colnames cambiamos los nombres de las columnas, esto nos ayuda a ordenar
O3 = select(O3, c(7,3))
colnames(O3) = c('date','O3')

WDIR = select(WDIR, c(5,3))
colnames(WDIR) = c('date','WDIR')

WSPD = select(WSPD, c(5,3))
colnames(WSPD) = c('date','WSPD')

NOX = select(NOX, c(7,3))
colnames(NOX) = c('date','NOX')

# Juntar columnas con full_join de tidyverse
# Hay otro tipos de join tambien, ver la documentacion https://www.tidyverse.org/packages/
data = full_join(full_join(full_join(O3, NOX), WDIR), WSPD)

# Arreglar fechas
# La clase fecha se llama POSIXct, siempre es recomendable usar este paso
# El formato es como vienen las fechas en un archivo
# Ver las opciones aca https://www.rdocumentation.org/packages/base/versions/3.6.2/topics/strptime
data$date = as.POSIXct(data$date, format = '%y%m%d%H%M')

# Lo siguiente lo hacemos usando la libreria openair
# La documentacion es https://davidcarslaw.github.io/openair/

# Serie de tiempo
# En este caso nuestro eje x siempre son las fechas (llamadas "date")
# Y nuestro eje y los pollutants
# El eje y puede tener la misma escala (same) o unica para cada uno (free)
timePlot(data, pollutant = c('O3','NOX'), y.relation = 'free')

# Tendencia
# Recuerden desestacionalizar si es necesario, lo vimos en clases!
# Recuerden tambien las tres partes de la serie de tiempo.
TheilSen(data, pollutant = 'O3', deseason = TRUE)
smoothTrend(data, pollutant = 'O3', deseason = TRUE)

# Variacion temporal
# Podemos extrar los ciclos asignando una variable
# A = timeVariation(), A$data$hour es el ciclo diario entre otros
timeVariation(data, pollutant = c('O3','NOX'))


# Polar Plot
# Necesitamos direccionn y velocidad de viento ademas de concentracion
# Ver documentacion para ver que se requiere
polarPlot(data, pollutant = 'O3', wd = 'WDIR', x = 'WSPD')

# Calcular MDA8
# Es el Maximo diario del promedio movil de 8 horas, nos sirve para
# cosas de salud.

# Sacamos el promedio movil con una ventana de 8 horas
roll = rollingMean(data, pollutant = 'O3', width = 8, new.name = 'rolling', data.thresh = 0)

# Separamos por dia (es el default de time average, esto se puede cambiar)
# y usamos el estadistico del maximo (es decir, dame el maximo de cada dia)
mda8 = timeAverage(roll, statistic = 'max')

# Ordenamos
mda8 = select(mda8, c('date','rolling'))

# Para plotear quiero que los que cumplen con la norma sean verdes y
# los que no, rojo, por eso separamos en dos con un condicional.
# Si se cumple lo primero, agregarlo a YES o NO.
mda8$NO = ifelse(mda8$rolling < 61,NA,mda8$rolling)
mda8$YES = ifelse(mda8$rolling >= 61,NA,mda8$rolling)


# Ploteamos con timePlot, con group hacemos que ambas columnas se dibujen en un solo plot
# a diferencia del primer ejemplo.
# Con cols elejimos los colores.
# Con pch (point character) elegimos el tipo de punto (guglear las opciones)
# Con lty (line type) elegimos la linea, en este caso, ninguna (tambien guglear)
# OpenAir plotea con la libreria "Lattice" que viene en la base
# Las variables pch y lty (entre otras) son de lattice no de openair
# Asi que buscar documentacion de lattice si se quiere cambiar mucho un grafico
# Para cambiar titulos, labels, etc tambien buscar documentacion de lattice.
timePlot(mda8, pollutant = c('YES','NO'), group = TRUE, cols = c('green','red'), pch = c(20,20), lty = c(0,0))

