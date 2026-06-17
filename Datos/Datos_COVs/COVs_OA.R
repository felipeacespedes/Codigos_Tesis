# Instalamos e importmaos librerías
library(conflicted)
library(openair)
library(readr)
library(dplyr)
library(lubridate)
library(tidyverse)
library(vtable)
library(dendextend)


# Importamos archivo csv
cov_file <- "datos_inv/MasterDF_inv_data_1min.csv"
# cov_file <- "datos_ver/ver_data_1min.csv"

COV <- read_delim( cov_file, name_repair = "minimal",
                  delim = ";", escape_double = FALSE,
                  col_types = cols(date = col_datetime
                                    (format = "%d/%m/%Y %H:%M:%S")),
                                    trim_ws = TRUE)



# Seleccionamos contaminantes y variables meteo de interés
BTE <- select(COV,'date','Benzene','Toluene','Ethyl.benzene_Xylenes')

MET <- select(COV,'date','p','t','rh','ws','wd')

COV_MET <- select(COV,'date','Butenes','Acetaldehyde','Methanol',
                  'Acetone_propanal','Propene_Cyclopropane','sr')


# Definimos contaminantes relevantes a utilizar 
btex <- c('Benzene','Toluene','Ethyl.benzene_Xylenes')
cov_int1 <- c('Butenes','Acetaldehyde',
              'Propene_Cyclopropane','Acetone_propanal')
cov_int2 <- c('Methacrolein_MVK','Butanone_Butanal')
cov_int3 <- c('Butenes','Acetaldehyde','Propene_Cyclopropane',
              'Acetone_propanal','Methanol','Toluene')
cov_int4 <- c('Methanol','Toluene',
              'Formaldehyde','Ethanol')
              
cov_int5 <- c('CO','NO2','NO','O3')



# extraemos lista de contaminantes (para no incluir variables meteo)
lc_sm <- names(COV[1:25])


## Time Plot ##
###############

## promedio horario
# benzene
Benzene_hr <- timeAverage(select(COV,'date','Benzene'), avg.time = "hour")
timePlot(Benzene_hr, pollutant = 'Benzene', lwd = 2, ylab = NULL,
         main = 'Benzene, hourly',strip=FALSE,marker)
## serie og
# methanol
dia <- selectByDate( COV, start = '2022-08-31', end = '2022-09-11')
timePlot(dia, pollutant = 'Methanol', lwd = 2, ylab = NULL,
         main = 'Methanol',strip=FALSE)

## serie con vectores viento
# DATE1 <- as_datetime("2022-09-13 06:00:00")
# DATE2 <- as_datetime("2022-09-13 16:00:00")
# DATE1 <- as_datetime("2022-09-13 10:00:00")
# DATE2 <- as_datetime("2022-09-13 12:00:00")
# DATE1 <- as_datetime("2022-10-03 00:00:00")
# DATE2 <- as_datetime("2022-10-08 00:00:00")


DATE1 <- as_datetime("2022-09-12 05:00:00")
DATE2 <- as_datetime("2022-09-12 11:00:00")
# DATE1 <- as_datetime("2022-10-04 00:00:00")
# DATE2 <- as_datetime("2022-10-04 23:00:00")
# DATE1 <- as_datetime("2022-10-07 05:00:00")
# DATE2 <- as_datetime("2022-10-07 11:00:00")
DATE <- COV %>% dplyr::filter(DATE1<=date & date<=DATE2)
timePlot(DATE, pollutant = cov_int4, #avg.time = 'hour',
         windflow = list(scale = 0.05, lwd = 1,
                         col = "grey30"),#strip=FALSE,
         lwd = 2, group = FALSE, y.relation = 'free', 
         ylab = "[ppb]",main='Evento 12/09, 05:00 a 11:00')



## Summary Plot ##
##################

# plotear toda la serie
summaryPlot(COV, period = 'months', normalise = TRUE)
summaryPlot(BTE, period = 'months', normalise = TRUE)

# ploteamos dias en párticular
dia <- selectByDate( COV, start = '2022-08-28', end = '2022-09-03')
summaryPlot( dia, period = 'days', lwd = 3, avg.time = 'hour')
summaryPlot( dia,pollutant = cov_int, period = 'days', lwd = 3, 
             avg.time = 'hour')

# plotear toda la serie, pero en histograma sin outliers
summaryPlot(BTE, period = 'months', 
            clip=TRUE, percentile = .99)

# plotear toda la serie, pero en histograma con outliers y con función
# de densidad
summaryPlot(BTE, period = 'months', 
            clip=TRUE, percentile = .99, type='density')
summaryPlot(MET, period = 'months', 
            clip=TRUE, percentile = .99, type='density')




## TimeVariation ##
###################

# Visualisamos la variación temporal de alguna variables con ayuda de 
# la función timeVariation()
timeVariation( COV, pollutant = c('Benzene','Toluene','Ethyl.benzene_Xylenes'),
               normalise = TRUE)
timeVariation( COV, pollutant = c('Butenes','Acetaldehyde','Methanol',
                                  'Acetone_propanal','Propene_Cyclopropane','sr'),
               normalise = TRUE)

# Variables meteo
plot(timeVariation(COV, pollutant = 'ws'), subset="hour")


plot(timeVariation(COV, pollutant = 'p',col='blue',ylab='hPa'), subset="hour")
plot(timeVariation(COV, pollutant = 't',col='orange',ylab='°C'), subset="hour")
plot(timeVariation(COV, pollutant = 'rh',col='green',ylab='%'), subset="hour")
plot(timeVariation(COV, pollutant = 'sr',col='red',ylab='W/m2'), subset="hour")
plot(timeVariation(COV, pollutant = 'ws',col='purple',ylab='m/s'), subset="hour")
plot(timeVariation(COV, pollutant = 'wd',col='brown',ylab='°'), subset="hour")


# Seleccionamos una día
dia <- COV %>% filter(month(date)==8 & day(date)==31)
View(dia)

## Polar Plot ##
################
polarPlot( COV, pollutant = 'Benzene', main = 'Benzene')


## Polar Annulus ##
###################
# día
polarAnnulus( dia, pollutant = 'Benzene', period = 'hour', main = 'Hour')
polarAnnulus( dia, pollutant = 'Toluene', period = 'hour', main = 'Hour')
polarAnnulus( dia, pollutant = 'Ethyl.benzene_Xylenes', 
              period = 'hour', main = 'Hour')

# todos los días, mean

# conjuntos
polarAnnulus( COV, pollutant = bte, period = 'hour', main = 'BTEX',
              statistic = 'max')
polarAnnulus( COV, pollutant = cov_int, period = 'hour', main = 'Paper',
              statistic = 'max')

# particulares
polarAnnulus( COV, pollutant = 'Benzene', period = 'hour', main = 'Benzene')
polarAnnulus( COV, pollutant = 'Toluene', period = 'hour', main = 'Toluene')
polarAnnulus( COV, pollutant = 'Ethyl.benzene_Xylenes', 
              period = 'hour', main = 'Ethylbenzene Xylenes')
polarAnnulus( COV, pollutant = 'Butenes', period = 'hour', main = 'Butenes')
polarAnnulus( COV, pollutant = 'Propene_Cyclopropane', period = 'hour',
              main = 'Propene_Cyclopropane')



# todos los días, max

# conjuntos
polarAnnulus( COV, pollutant = bte, period = 'hour', main = 'BTEX',
              statistic = 'max')
polarAnnulus( COV, pollutant = cov_int, period = 'hour', main = 'Paper',
              statistic = 'max')

# particulares
polarAnnulus( COV, pollutant = 'Benzene', period = 'hour', main = 'Benzene',
              statistic = 'max')
polarAnnulus( COV, pollutant = 'Toluene', period = 'hour', main = 'Toluene',
              statistic = 'max')
polarAnnulus( COV, pollutant = 'Ethyl.benzene_Xylenes', period = 'hour', 
              main = 'Ethylbenzene Xylenes', statistic = 'max')
polarAnnulus( COV, pollutant = 'Butenes', period = 'hour', main = 'Butenes',
              stati = 'max')
polarAnnulus( COV, pollutant = 'Propene_Cyclopropane', period = 'hour',
              main = 'Propene_Cyclopropane', statistic = 'max')


# ploteamos para cada día de la semana
polarAnnulus( COV, pollutant = 'Propene_Cyclopropane', period = 'hour', 
              main = 'Weekday',type = 'weekday',statistic = 'max')


## Scatter Plot ##
##################
## con Meteo

# Para todo el periodo
scatterPlot(COV, x = 'Benzene', y = 'Toluene', z = 'wd')
scatterPlot(COV, x = 'Methacrolein_MVK', y = 'Propene_Cyclopropane', z = 'wd')
scatterPlot(COV, x = 'Butenes', y = 'Propene_Cyclopropane', z = 'wd')

# Para cada día de la semana
scatterPlot(COV, x = 'Benzene', y = 'Toluene', z = 'wd',
            type = 'weekday')
scatterPlot(COV, x = 'Butenes', y = 'Propene_Cyclopropane', z = 'wd',
            type = 'weekday')


# Para cada hora del día
scatterPlot(COV, x = 'Benzene', y = 'Toluene', z = 'wd',
            type = 'hour')
scatterPlot(COV, x = 'Butenes', y = 'Propene_Cyclopropane', z = 'wd',
            type = 'hour')
scatterPlot(COV, x = 'Furan', y = 'Isoprene', z = 'wd',
            type = 'hour')

## sin Meteo y seleccionando más de una variables en eje y ##

# select the variables of interest
subdat <- select(COV, 'date', 'Dimethyl.sulfide',
                 'Benzene','Ethyl.benzene_Xylenes','Toluene')
# calculate weekly averages
#subdat <- timeAverage(subdat, avg.time = "hour")
# reshape so we have two variable columns
subdat <- pivot_longer(subdat, cols = c('Benzene','Ethyl.benzene_Xylenes','Toluene'), 
                       names_to = "pollutant")
head(subdat)

# ahora filtramos por día para ver episodios
DATE1 <- as_datetime("2022-01-11 07:20:00")
DATE2 <- as_datetime("2022-01-11 07:50:00")
dia0111 <- subdat %>% filter(DATE1<=date & date<=DATE2)

view(dia0111)                            

# Para todo el periodo
scatterPlot(dia0111, x = "Dimethyl.sulfide", y = "value", 
            group = "pollutant", 
            pch = c(21,22,24), cex = 1.5, 
            fill = c("dodgerblue", "tomato","forestgreen"), 
            col = "white", 
            linear = TRUE, 
            xlab = "DMS (ppbv)", 
            ylab = "BTEX (ppbv)",
            main = "Verano, 11/01, 07-08 hrs")



## Calendar Plot ##
###################

# plot simple de 2 meses
calendarPlot( BTE, pollutant = 'Benzene', main = 'Benzene')
calendarPlot( BTE, pollutant = 'Toluene', main = 'Toluene')
calendarPlot( BTE, pollutant = 'Ethyl.benzene_Xylenes', 
              main = 'Ethyl.benzene_Xylenes')
calendarPlot( COV_0309, pollutant = 'Benzene', main = 'Benzene')
calendarPlot( COV_0309, pollutant = 'Toluene', main = 'Toluene')
calendarPlot( COV_0309, pollutant = 'Ethyl.benzene_Xylenes', 
              main = 'Ethyl.benzene_Xylenes')

# Butenes
calendarPlot( COV, 
              pollutant = 'Butenes',
              main = 'Butenes',
              statistic = 'max',
              limits = c(0, 100))
# Acetaldehyde
calendarPlot( COV, 
              pollutant = 'Acetaldehyde',
              main = 'Acetaldehyde',
              statistic = 'max',
              limits = c(0, 100))
# Propene_Cyclopropane
calendarPlot( COV, 
              pollutant = 'Propene_Cyclopropane',
              main = 'Propene_Cyclopropane',
              statistic = 'max',
              limits = c(0, 100))
# Acetone_Propanal
calendarPlot( COV, 
              pollutant = 'Acetone_propanal',
              main = 'Acetone_propanal',
              statistic = 'max',
              limits = c(0, 100))
# Methanol
calendarPlot( COV, 
              pollutant = 'Methanol',
              main = 'Methanol',
              statistic = 'max',
              limits = c(0, 50))
# Styrene
calendarPlot( COV, 
              pollutant = 'Styrene',
              main = 'Styrene',
              statistic = 'max',
              limits = c(0, 30))


### Polar Freq ###

polarFreq(COV,pollutant = 'Butenes',type='weekday',statistic = 'weighted.mean',
          min.bin=2)

## Percentile Rose ##
#####################

# percentiles
perc <- c(25, 50, 75, 90, 95, 99)

# PRs de BTE con percentiles perc.
percentileRose(COV, pollutant = bte, key.position = "bottom", percentile = perc)



### Correlation matrix ###
##########################

corPlot(COV, cluster = TRUE, main= 'Invierno completo')
CP_dendro <- corPlot(COV, dendrogram = TRUE)


# Plot the dendrogram
par(mar=c(12,3,1,1))
plot(as.dendrogram(CP_dendro$clust))
# abline(h = 2, lty = 2)


# Tanglegram
CP_dendrov <- corPlot(VER, dendrogram = TRUE, main= 'Verano')
CP_dendroi <- corPlot(INV, dendrogram = TRUE, main= 'Invierno')
dendro_ver <- as.dendrogram(CP_dendrov$clust)
dendro_inv <- as.dendrogram(CP_dendroi$clust)
dl <- dendlist(
  dendro_ver %>% 
    set("labels_col", value = c("skyblue", "orange", "grey"), k=3) %>%
    set("branches_lty", 1) %>%
    set("branches_k_color", value = c("skyblue", "orange", "grey"), k = 3),
  dendro_inv %>%
    set("labels_col", value = c("skyblue", "orange", "grey"), k=3) %>%
    set("branches_lty", 1) %>%
    set("branches_k_color", value = c("skyblue", "orange", "grey"), k = 3))
tanglegram(dl, 
           common_subtrees_color_lines = TRUE, highlight_distinct_edges  = FALSE,
           highlight_branches_lwd=FALSE, 
           margin_inner=11,
           lwd=2, sort = TRUE
)


# Estudio por contaminante
g1 <- c('Naphthalene','Benzonitrile','Phenol','Dimethyl.sulfide',
        'Benzofuran','Cresol','Monoterpenes')
g2 <- c('Isoprene','Furan','Acetonitrile','Benzene')

g3 <- c('Butanone_Butanal','Methacrolein_MVK','C9_Aromatics',
        'Ethyl.benzene_Xylenes','Formaldehyde')
g4 <- c('Toluene','Methanol','Butenes','Propene_Cyclopropane',
        'Acetone_propanal','Acetaldehyde')
cont <- 'Benzonitrile'


### Polar plot ###
##################

# Percentiles
polarPlot(COV, poll = g4, stati = "cpf", percentile = c(10, 20),normalise = TRUE)
polarPlot(COV, poll = g4, stati = "cpf", percentile = c(20, 30),normalise = TRUE)
polarPlot(COV, poll = g4, stati = "cpf", percentile = c(30, 40),normalise = TRUE)
polarPlot(COV, poll = g4, stati = "cpf", percentile = c(40, 50),normalise = TRUE)
polarPlot(COV, poll = g4, stati = "cpf", percentile = c(50, 60),normalise = TRUE)
polarPlot(COV, poll = g4, stati = "cpf", percentile = c(50, 60),normalise = TRUE)
polarPlot(COV, poll = g4, stati = "cpf", percentile = c(60, 70),normalise = TRUE)
polarPlot(COV, poll = g4, stati = "cpf", percentile = c(70, 80),normalise = TRUE)
polarPlot(COV, poll = g4, stati = "cpf", percentile = c(80, 90),normalise = TRUE)
polarPlot(COV, poll = g4, stati = "cpf", percentile = c(90, 100),normalise = TRUE)
polarPlot(COV, poll = g1, stati = "cpf", percentile = c(99, 100),normalise = TRUE)

polarPlot(COV, poll = g4, stati = "cpf", percentile = c(80, 100),normalise = TRUE)


### Polar Cluster ###
#####################
library(gridExtra)
library(latticeExtra)
polarCluster(COV,pollutant = g4,n.clusters = 4:8,cols = 'Set2', normalise = TRUE)
results <- polarCluster(COV, pollutant=g4, n.clusters=8, cols= "Set2", normalise = TRUE)
results <- results[['data']]

# Acetone
timeProp(
  subset(results, cluster %in% c("C4")), 
  pollutant = "Acetone_propanal", 
  proportion = "cluster", 
  avg.time = '1 hour',
  col = openColours("Set2", 8)[4], 
  key.position = 'top', 
  key.columns = 1, 
  date.breaks = 10
)
# Acetaldehyde
timeProp(
  subset(results, cluster %in% c("C4")), 
  pollutant = "Acetaldehyde", 
  proportion = "cluster", 
  avg.time = '1 hour',
  col = openColours("Set2", 8)[4], 
  key.position = 'top', 
  key.columns = 1, 
  date.breaks = 10
)
# Butenes
timeProp(
  subset(results, cluster %in% c("C4")), 
  pollutant = "Butenes", 
  proportion = "cluster", 
  avg.time = '1 hour',
  col = openColours("Set2", 8)[4], 
  key.position = 'top', 
  key.columns = 1, 
  date.breaks = 10
)
# Propene/Cyclopropane
timeProp(
  subset(results, cluster %in% c("C4")), 
  pollutant = "Propene_Cyclopropane", 
  proportion = "cluster", 
  avg.time = '1 hour',
  col = openColours("Set2", 8)[4], 
  key.position = 'top', 
  key.columns = 1, 
  date.breaks = 10
)
# Toluene
timeProp(
  subset(results, cluster %in% c("C4")), 
  pollutant = "Toluene", 
  proportion = "cluster", 
  avg.time = '1 hour',
  col = openColours("Set2", 8)[4], 
  key.position = 'top', 
  key.columns = 1, 
  date.breaks = 10
)

# Methanol
timeProp(
  subset(results, cluster %in% c("C4")), 
  pollutant = "Methanol", 
  proportion = "cluster", 
  avg.time = '1 hour',
  col = openColours("Set2", 8)[4], 
  key.position = 'top', 
  key.columns = 1, 
  date.breaks = 10
)

# Aggregating concentrations across all pollutants in the group
results$average_concentration <- rowMeans(results[, g4], na.rm = TRUE)

# Then use the aggregated column in timeProp
timeProp(
  subset(results, cluster %in% c("C3")), 
  pollutant = "average_concentration", 
  proportion = "cluster", 
  avg.time = '60 min',
  col = openColours("Set2", 5)[3], 
  key.position = 'top', 
  key.columns = 1, 
  date.breaks = 20
)


### calendar plot cluster 4 ###

# Methanol
calendarPlot( subset(results, cluster %in% c("C4")), 
              pollutant = "Methanol",
              main = "Methanol",
              proportion = "cluster",
              avg.time = '1 hour')
# Ethanol
calendarPlot( subset(results, cluster %in% c("C4")), 
              pollutant = "Ethanol",
              main = "Ethanol",
              proportion = "cluster",
              avg.time = '1 hour')

# Butenes
calendarPlot( subset(results, cluster %in% c("C4")), 
              pollutant = "Butenes",
              main="Butenes",
              proportion = "cluster",
              avg.time = '1 hour')

# Acetaldehyde
calendarPlot( subset(results, cluster %in% c("C4")), 
              pollutant = "Acetaldehyde",
              main = "Acetaldehyde",
              proportion = "cluster",
              avg.time = '1 hour')
              
# Propene_Cyclopropane
calendarPlot( subset(results, cluster %in% c("C4")), 
              pollutant = "Propene_Cyclopropane",
              main = "Propene_Cyclopropane",
              proportion = "cluster",
              avg.time = '1 hour')

# Acetone_propanal
calendarPlot( subset(results, cluster %in% c("C4")), 
              pollutant = "Acetone_propanal",
              main = "Acetone_propanal",
              proportion = "cluster",
              avg.time = '1 hour')

# Benzene
calendarPlot( subset(results, cluster %in% c("C4")), 
              pollutant = "Benzene",
              main = "Benzene",
              proportion = "cluster",
              avg.time = '1 hour')
# Toluene
calendarPlot( subset(results, cluster %in% c("C4")), 
              pollutant = "Toluene",
              main = "Toluene",
              proportion = "cluster",
              avg.time = '1 hour')

# Ethyl.benzene_Xylenes
calendarPlot( subset(results, cluster %in% c("C4")), 
              pollutant = "Ethyl.benzene_Xylenes",
              main = "Ethyl.benzene_Xylenes",
              proportion = "cluster",
              avg.time = '1 hour')


### PollutionRose ###
#####################

# normal
pollutionRose(COV,pollutant = 'Butenes')

# condicionada por otro contaminante


### Tabla Estadísticos ###
##########################

st <- sumtable(COV,title='Mediciones minutarias (ppb) PTR-TOF-MS 27-08 al 03-11 del 2022')


### Scatterplot de contaminates y series en particular ###
##########################################################

### DMS

# select the variables of interest
subdat_raw <- select(COV, 'date', 'Dimethyl.sulfide',
                     'Benzene','Ethyl.benzene_Xylenes','Toluene')
# calculate weekly averages
# subdat <- timeAverage(subdat, avg.time = "hour")

# reshape so we have two variable columns
subdat <- pivot_longer(subdat_raw, cols = c('Benzene','Ethyl.benzene_Xylenes','Toluene'), 
                       names_to = "pollutant")
head(subdat)

## Ploteamos todo el periodo
timePlot(subdat_raw, pollutant = c('Dimethyl.sulfide','Benzene',
                                   'Ethyl.benzene_Xylenes','Toluene'), lwd = 2, ylab = NULL,
         main = 'Dimethyl.sulfide',strip=FALSE)
scatterPlot(subdat, x = "Dimethyl.sulfide", y = "value", 
            group = "pollutant", 
            pch = c(21,22,24), cex = 1.5, 
            fill = c("dodgerblue", "tomato","forestgreen"), 
            col = "white", 
            linear = TRUE, 
            xlab = "DMS (ppbv)",
            ylab = "BTEX (ppbv)",
            main = "Dimethyl.sulfide",
            ylim = c(-2,50))


## Acetonitrilo

# select the variables of interest
subdat_raw <- select(COV, 'date', 'Acetonitrile',
                     'Benzene','Ethyl.benzene_Xylenes','Toluene')
# calculate weekly averages
# subdat_raw <- timeAverage(subdat_raw, avg.time = "20 min")

# reshape so we have two variable columns
subdat <- pivot_longer(subdat_raw, cols = c('Benzene','Ethyl.benzene_Xylenes','Toluene'), 
                       names_to = "pollutant")
head(subdat)

## Ploteamos todo el periodo
timePlot(subdat_raw, pollutant = c('Acetonitrile','Benzene',
                                   'Ethyl.benzene_Xylenes','Toluene'), lwd = 2, ylab = NULL,
         main = 'Acetonitrile',strip=FALSE)
scatterPlot(subdat, x = "Acetonitrile", y = "value", 
            group = "pollutant", 
            pch = c(21,22,24), cex = 1.5, 
            fill = c("dodgerblue", "tomato","forestgreen"), 
            col = "white", 
            linear = TRUE, 
            xlab = "Acetonitrile (ppbv)", 
            ylab = "BTEX (ppbv)",
            main = "Acetonitrile",
            ylim = c(-2,50))



## Propene_Cyclopropane

# select the variables of interest
subdat_raw <- select(COV, 'date', 'Propene_Cyclopropane',
                     'Benzene','Ethyl.benzene_Xylenes','Toluene')#,'wd','ws')
# calculate weekly averages
# subdat_raw <- timeAverage(subdat_raw, avg.time = "20 min")

# reshape so we have two variable columns
subdat <- pivot_longer(subdat_raw, cols = c('Benzene','Ethyl.benzene_Xylenes','Toluene'), 
                       names_to = "pollutant")
head(subdat)

## Ploteamos todo el periodo
timePlot(subdat_raw, pollutant = c('Propene_Cyclopropane','Benzene',
                                   'Ethyl.benzene_Xylenes','Toluene'), lwd = 2, ylab = NULL,
         main = 'Propene_Cyclopropane',strip=FALSE)
scatterPlot(subdat, x = "Propene_Cyclopropane", y = "value", 
            group = "pollutant", 
            pch = c(21,22,24), cex = 1.5, 
            fill = c("dodgerblue", "tomato","forestgreen"), 
            col = "white", 
            linear = TRUE, 
            xlab = "Propene_Cyclopropane (ppbv)", 
            ylab = "BTEX (ppbv)",
            main = "Propene_Cyclopropane",
            ylim = c(-2,30))



## Isoprene

# select the variables of interest
subdat_raw <- select(COV, 'date', 'Isoprene',
                     'Benzene','Ethyl.benzene_Xylenes','Toluene')#,'wd','ws')
# calculate weekly averages
# subdat_raw <- timeAverage(subdat_raw, avg.time = "20 min")

# reshape so we have two variable columns
subdat <- pivot_longer(subdat_raw, cols = c('Benzene','Ethyl.benzene_Xylenes','Toluene'), 
                       names_to = "pollutant")
head(subdat)

## Ploteamos todo el periodo
timePlot(subdat_raw, pollutant = c('Isoprene','Benzene',
                                   'Ethyl.benzene_Xylenes','Toluene'), lwd = 2, ylab = NULL,
         main = 'Isoprene',strip=FALSE)
scatterPlot(subdat, x = "Isoprene", y = "value", 
            group = "pollutant", 
            pch = c(21,22,24), cex = 1.5, 
            fill = c("dodgerblue", "tomato","forestgreen"), 
            col = "white", 
            linear = TRUE, 
            xlab = "Isoprene (ppbv)", 
            ylab = "BTEX (ppbv)",
            main = "Isoprene",
            ylim = c(-2,50))




## Butenes

# select the variables of interest
subdat_raw <- select(COV, 'date', 'Butenes',
                     'Benzene','Ethyl.benzene_Xylenes','Toluene')#,'wd','ws')
# calculate weekly averages
# subdat_raw <- timeAverage(subdat_raw, avg.time = "20 min")

# reshape so we have two variable columns
subdat <- pivot_longer(subdat_raw, cols = c('Benzene','Ethyl.benzene_Xylenes','Toluene'), 
                       names_to = "pollutant")
head(subdat)

## Ploteamos todo el periodo
timePlot(subdat_raw, pollutant = c('Butenes','Benzene',
                                   'Ethyl.benzene_Xylenes','Toluene'), lwd = 2, ylab = NULL,
         main = 'Butenes',strip=FALSE)
scatterPlot(subdat, x = "Butenes", y = "value", 
            group = "pollutant", 
            pch = c(21,22,24), cex = 1.5, 
            fill = c("dodgerblue", "tomato","forestgreen"), 
            col = "white", 
            linear = TRUE, 
            xlab = "Butenes (ppbv)", 
            ylab = "BTEX (ppbv)",
            main = "Butenes")




## Furan

# select the variables of interest
subdat_raw <- select(COV, 'date', 'Furan',
                     'Benzene','Ethyl.benzene_Xylenes','Toluene')#,'wd','ws')
# calculate weekly averages
# subdat_raw <- timeAverage(subdat_raw, avg.time = "20 min")

# reshape so we have two variable columns
subdat <- pivot_longer(subdat_raw, cols = c('Benzene','Ethyl.benzene_Xylenes','Toluene'), 
                       names_to = "pollutant")
head(subdat)

## Ploteamos todo el periodo
timePlot(subdat_raw, pollutant = c('Furan','Benzene',
                                   'Ethyl.benzene_Xylenes','Toluene'), lwd = 2, ylab = NULL,
         main = 'Furan',strip=FALSE)
scatterPlot(subdat, x = "Furan", y = "value", 
            group = "pollutant", 
            pch = c(21,22,24), cex = 1.5, 
            fill = c("dodgerblue", "tomato","forestgreen"), 
            col = "white", 
            linear = TRUE, 
            xlab = "Furan (ppbv)", 
            ylab = "BTEX (ppbv)",
            main = "Furan",
            ylim = c(-2,50))




## Cresol

# select the variables of interest
subdat_raw <- select(COV, 'date', 'Cresol',
                     'Benzene','Ethyl.benzene_Xylenes','Toluene')#,'wd','ws')
# calculate weekly averages
# subdat_raw <- timeAverage(subdat_raw, avg.time = "20 min")

# reshape so we have two variable columns
subdat <- pivot_longer(subdat_raw, cols = c('Benzene','Ethyl.benzene_Xylenes','Toluene'), 
                       names_to = "pollutant")
head(subdat)

## Ploteamos todo el periodo
timePlot(subdat_raw, pollutant = c('Cresol','Benzene',
                                   'Ethyl.benzene_Xylenes','Toluene'), lwd = 2, ylab = NULL,
         main = 'Cresol',strip=FALSE)
scatterPlot(subdat, x = "Cresol", y = "value", 
            group = "pollutant", 
            pch = c(21,22,24), cex = 1.5, 
            fill = c("dodgerblue", "tomato","forestgreen"), 
            col = "white", 
            linear = TRUE, 
            xlab = "Cresol (ppbv)", 
            ylab = "BTEX (ppbv)",
            main = "Cresol")


## Phenol

# select the variables of interest
subdat_raw <- select(COV, 'date', 'Phenol',
                     'Benzene','Ethyl.benzene_Xylenes','Toluene')#,'wd','ws')
# calculate weekly averages
# subdat_raw <- timeAverage(subdat_raw, avg.time = "20 min")

# reshape so we have two variable columns
subdat <- pivot_longer(subdat_raw, cols = c('Benzene','Ethyl.benzene_Xylenes','Toluene'), 
                       names_to = "pollutant")
head(subdat)

## Ploteamos todo el periodo
timePlot(subdat_raw, pollutant = c('Phenol','Benzene',
                                   'Ethyl.benzene_Xylenes','Toluene'), lwd = 2, ylab = NULL,
         main = 'Phenol',strip=FALSE)
scatterPlot(subdat, x = "Phenol", y = "value", 
            group = "pollutant", 
            pch = c(21,22,24), cex = 1.5, 
            fill = c("dodgerblue", "tomato","forestgreen"), 
            col = "white", 
            linear = TRUE, 
            xlab = "Phenol (ppbv)", 
            ylab = "BTEX (ppbv)",
            main = "Phenol")

## C9_Aromatics

# select the variables of interest
subdat_raw <- select(COV, 'date', 'C9_Aromatics',
                     'Benzene','Ethyl.benzene_Xylenes','Toluene')#,'wd','ws')
# calculate weekly averages
# subdat_raw <- timeAverage(subdat_raw, avg.time = "20 min")

# reshape so we have two variable columns
subdat <- pivot_longer(subdat_raw, cols = c('Benzene','Ethyl.benzene_Xylenes','Toluene'), 
                       names_to = "pollutant")
head(subdat)

## Ploteamos todo el periodo
timePlot(subdat_raw, pollutant = c('C9_Aromatics','Benzene',
                                   'Ethyl.benzene_Xylenes','Toluene'), lwd = 2, ylab = NULL,
         main = 'C9_Aromatics',strip=FALSE)
scatterPlot(subdat, x = "C9_Aromatics", y = "value", 
            group = "pollutant", 
            pch = c(21,22,24), cex = 1.5, 
            fill = c("dodgerblue", "tomato","forestgreen"), 
            col = "white", 
            linear = TRUE, 
            xlab = "C9_Aromatics (ppbv)", 
            ylab = "BTEX (ppbv)",
            main = "C9_Aromatics")

## Methacrolein_MVK

# select the variables of interest
subdat_raw <- select(COV, 'date', 'Methacrolein_MVK',
                     'Benzene','Ethyl.benzene_Xylenes','Toluene')#,'wd','ws')
# calculate weekly averages
# subdat_raw <- timeAverage(subdat_raw, avg.time = "20 min")

# reshape so we have two variable columns
subdat <- pivot_longer(subdat_raw, cols = c('Benzene','Ethyl.benzene_Xylenes','Toluene'), 
                       names_to = "pollutant")
head(subdat)

## Ploteamos todo el periodo
timePlot(subdat_raw, pollutant = c('Methacrolein_MVK','Benzene',
                                   'Ethyl.benzene_Xylenes','Toluene'), lwd = 2, ylab = NULL,
         main = 'Methacrolein_MVK',strip=FALSE)
scatterPlot(subdat, x = "Methacrolein_MVK", y = "value", 
            group = "pollutant", 
            pch = c(21,22,24), cex = 1.5, 
            fill = c("dodgerblue", "tomato","forestgreen"), 
            col = "white", 
            linear = FALSE, 
            xlab = "Methacrolein_MVK (ppbv)", 
            ylab = "BTEX (ppbv)",
            main = "Methacrolein_MVK")



