# Instalamos e importmaos librerías
library(openair)
library(readr)
library(dplyr)
library(lubridate)
library(vtable)
# librerías para running correlation
library(zoo)
library(runner)



# lista de estaciones
lei <- c('Ventanas','Los_Maitenes','Centro_Quintero','Loncura',
        'Sur','Junta_Vecinos','Concón','Gaviotas','Colmo')
lef <-c('Ventanas','Centro_Quintero','Concón','Colmo')
      #c('Colmo','Gaviotas','Concón','Centro_Quintero','Ventanas')
      

# queda verificar si el dataframe tiene los datos de viento, y en caso contario 
# , asignarlos

# Importamos datos originales, modificados y modificados con LOD
path <- 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
HCNM_m <- read_delim(paste(path,'HCNM_mod_df.csv',sep=''))



HCNM_or <- read_delim(paste(path,'HCNM_orig_df.csv',sep=''))
HCNM_m_lod <- read_delim(paste(path,'HCNM_mod_lod_df.csv',sep=''))
WD <- read_delim(paste(path,'WD_df.csv',sep=''))
WS <- read_delim(paste(path,'WS_df.csv',sep=''))


View(HCNM_or)
View(HCNM_m)
View(HCNM_m_lod)


# Seleccionamos periodo a inspeccionar
per <- HCNM_m_lod %>% 
  filter( 10<=month(date) & month(date)<=11 & year(date)==2019)
View(per)


##########################
### Tabla Estadísticos ###
##########################

## Replace "ó" with "o"
lec <- c('Ventanas','Centro_Quintero','Concon','Colmo')
colnames(HCNM_m) <- gsub("ó", "o", colnames(HCNM_m))

# Seleccionamos solo estaciones que usamos
HCNM_m <- HCNM_m[c('date','Ventanas','Centro_Quintero','Concon',
                           'Colmo')]

# Modificamos HCNM_m a periodo de tesis final [2019-2023]
HCNM_m <- HCNM_m %>% 
  filter( 2019<=year(date) & year(date)<=2023 )
View(HCNM_m)




## sumtable agregando columna de porcentaje de datos:

# ** ASEGURARSE DE: remplazar "ó" con "o" y seleccionar solo las 5 estaciones

# Define the total possible number of observations
start_time <- min(HCNM_m$date, na.rm = TRUE)
end_time <- max(HCNM_m$date, na.rm = TRUE)
total_time_points <- as.numeric(difftime(end_time, start_time, units = "mins")) / 60  # Assuming hourly data

# Column selection vector (assuming 'lec' defines which columns to analyze)
# Make sure lec is defined earlier like: lec <- c("Concón", "OtherStation", ...) 
# and that they match column names in HCNM_m_lod
availability <- colSums(!is.na(HCNM_m[lec])) / total_time_points * 100  # Convert to %
availability <- signif(availability, digits = 3)

# perc. 99.8
P998 <- apply(HCNM_m[lec], 2, quantile, probs =0.998, na.rm=TRUE)
P998 <- signif(P998, digits = 3)



cols <- c('notNA(x)', 'mean(x)', 'sd(x)', 'median(x)', 'pctile(x)[75]-pctile(x)[25]','min(x)',
          'pctile(x)[25]', 'pctile(x)[75]', 'pctile(x)[90]','max(x)' )

cols_nm <- c('N','Media','Std','Mediana','IQR','Min','Pctl 25','Pctl 75',
             'Pctl 90','Max') 

# Run sumtable and extract summary
summary_table <- sumtable(HCNM_m[lec],summ=cols,summ.names = cols_nm, digits = 3, out = "return")


# Add "Data Availability (%)" and "95th Percentile" as new rows
summary_table <- cbind(summary_table,
                       'Porcentaje' = availability,
                       'Pctl 99.8' = P998)

# Convert matrix to dataframe
summary_df <- as.data.frame(summary_table)


# Reordenamos columnas
cols_no <- c('N','Porcentaje','Media','Std','Mediana','IQR','Min','Pctl 25','Pctl 75',
                     'Pctl 90','Pctl 99.8','Max')
summary_df <- summary_df[,cols_no]



# Save as CSV
path <- 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
write.csv(summary_df, paste0(path, "summary_table.csv"), row.names = TRUE)




##############
## CorrPlot ##
##############

# normal 
corPlot(HCNM_m_lod, cluster = TRUE, main= 'Estaciones SINCA')

# discriminando por percentil
HCNM_p90<- cbind(HCNM_m_lod[1], sapply(HCNM_m_lod[-1], function(i) 
  replace(i, i < quantile(i, 0.75,na.rm=TRUE), NA)))
corPlot(HCNM_p90, cluster = TRUE, main= 'Estaciones SINCA')


##################
## rolling corr ##
##################

# Definition of stations
est1 = HCNM_m_lod$Centro_Quintero
est2 = HCNM_m_lod$Concón

# Create a vector to store correlations
lags <- -6:6
correlations <- numeric(length(lags))

# Loop over each lag/lead
for (i in seq_along(lags)) {
  lag <- lags[i]
  if (lag < 0) {
    # Shift est1 backward (lead)
    x <- est1[1:(nrow(HCNM_m_lod) + lag)]
    y <- est2[(1 - lag):nrow(HCNM_m_lod)]
  } else if (lag > 0) {
    # Shift est1 forward (lag)
    x <- est1[(1 + lag):nrow(HCNM_m_lod)]
    y <- est2[1:(nrow(HCNM_m_lod) - lag)]
  } else {
    # No shift
    x <- est1
    y <- est2
  }
  
  # Calculate correlation, use complete.obs to handle NA
  correlations[i] <- cor(x, y, use = "complete.obs")
}

# Create a data frame of results
lag_correlation_df <- data.frame(
  Lag = lags,
  Correlation = correlations
)

# View the results
print(lag_correlation_df)

# Optional: plot the correlation vs lag
library(ggplot2)
ggplot(lag_correlation_df, aes(x = Lag, y = Correlation)) +
  geom_line() +
  geom_point() +
  theme_minimal() +
  labs(title = "Lagged Correlation: Est1 vs Est2",
       x = "Lag (hours)",
       y = "Correlation")


##################
## summaryPlot ##
#################

summaryPlot(HCNM_or)
summaryPlot(HCNM_m)
summaryPlot(HCNM_m_lod, poll=lef)
summaryPlot(per,period='months',lwd=2)


###################
## timeVariation ##
###################

timeVariation(WD, pollutant = lef, statistic = 'mean',
              normalise=FALSE, ylab="[°]")

# plots por separado
TV <- timeVariation(HCNM_m_lod, poll = c('Ventanas','Centro_Quintero'),
                    normalise = FALSE, col = openColours("Set2",10)[c(2,4)],
                    ylab='[ppm]', statistic = 'median')
## just the diurnal variation
plot(TV, subset = "hour")
## day and hour
plot(TV, subset ="day.hour")
## weekday variation
plot(TV, subset = "day")
## monthly variation
plot(TV, subset = "month")

# plots por separado
TV <- timeVariation(HCNM_m_lod, poll = c('Concón','Colmo'),
                    normalise = FALSE, col=openColours("Set2", 10)[c(3,5)],
                    ylab='[ppm]', statistic = 'median')
## just the diurnal variation
plot(TV, subset = "hour")
## day and hour
plot(TV, subset ="day.hour")
## weekday variation
plot(TV, subset = "day")
## monthly variation
plot(TV, subset = "month")


## por dirección de viento 

##make a field called "south and fill: make all values = "other"
CQ$south <-"other"
##now find which indexes correspond to southerly conditions > 4m/s ws
id <-which(with(CQ,ws > 2 & wd > 135 & wd <= 225 ))
##use the ids to update the site column
##there are now two values in site: "other" and "southerly"
CQ$south[id] <-"southerly"
timeVariation(CQ, pollutant ="HCNM", group = "south", ylab = "HCNM(ppm)",
              difference = TRUE)

## por percentil

##make a field called "P90" and fill: make all values = "other"
CQ$P90 <-"other"
##now find which indexes correspond to values greater ther percentile 90%
id <-which(with(CQ,HCNM > quantile(HCNM,probs=0.90, na.rm=TRUE)))
##use the ids to update the site column
##there are now two values in site: "other" and "prct_90"
CQ$P90[id] <-"prct_90"
timeVariation(CQ, pollutant ="HCNM", group = "P90", ylab = "HCNM(ppm)",
              difference = TRUE)




#################
## calendarPlot##
#################

# periodos de interés
calendarPlot(HCNM_m_lod, poll='Ventanas', year=2022, month=c(8,9))
calendarPlot(HCNM_m_lod, poll='Centro_Quintero', year=2022, month=c(8,9))
calendarPlot(HCNM_m_lod, poll='Concón', year=2022, month=c(8,9))
calendarPlot(HCNM_m_lod, poll='Colmo', year=2022, month=c(8,9))
calendarPlot(HCNM_m_lod, poll='Gaviotas', year=2022, month=c(8,9))

# calendarPlot: inspección
calendarPlot(HCNM_m_lod, poll='Centro_Quintero', year=2019)

##############################
## Estaciones en particular ##

# Importamos datos modificados y con LOD
path <- 'C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/'
VE <- read_delim(paste(path,'VE_df.csv',sep=''))
CQ <- read_delim(paste(path,'CQ_df.csv',sep=''))
CC <- read_delim(paste(path,'CC_df.csv',sep=''))
CO <- read_delim(paste(path,'CO_df.csv',sep=''))

# Creamos DF añadiendo las concentraciones de Concón a Centro Quintero
CQ_cc = CQ
CQ_cc$Centro_Quintero <- CQ$HCNM
CQ_cc$Concón <- CC$HCNM
# creamos ratio
CQ_cc <- transform(CQ_cc, ratio = Concón / Centro_Quintero)



## time variation ##
# Wd
timeVariation(VE, poll='wd',main='Ventanas')
timeVariation(CQ, poll='wd',main='Centro Quintero')
timeVariation(CC, poll='wd',main='Concón')
timeVariation(CO, poll='wd',main='Colmo')
# Ws
timeVariation(VE, poll='ws',main='Ventanas')
timeVariation(CQ, poll='ws',main='Centro Quintero')
timeVariation(CC, poll='ws',main='Concón')
timeVariation(CO, poll='ws',main='Colmo')

## polarAnnulus ##

# mean
polarAnnulus(VE, poll='HCNM', period='hour',main='Ventanas')
polarAnnulus(CQ, poll='HCNM', period='hour',main='Centro_Quintero',
             statistic = 'max')
polarAnnulus(CC, poll='HCNM', period='hour',main='Concón',
             statistic = 'mean')
polarAnnulus(GA, poll='HCNM', period='hour',main='Las_Gaviotas',
             statistic = 'mean')

polarAnnulus(CO, poll='HCNM', period='hour',main='Colmo',
             statistic = 'mean')

# max

polarAnnulus(VE, poll='HCNM', period='hour',main='Ventanas',
             statistic = 'max')
polarAnnulus(CQ, poll='HCNM', period='hour',main='Centro_Quintero',
             statistic ='max')
polarAnnulus(CC, poll='HCNM', period='hour',main='Concón',
             statistic = 'max')
polarAnnulus(GA, poll='HCNM', period='hour',main='Las_Gaviotas',
             statistic = 'max')
polarAnnulus(CO, poll='HCNM', period='hour',main='Colmo',
             statistic = 'max')

# Percentile
polarAnnulus(VE, poll='HCNM', period='hour',main='Ventanas',
             statistic = 'cpf',percentile = , min.bin = 2, width = 'fat')
polarAnnulus(CQ, poll='HCNM', period='hour',main='Centro_Quintero',
             statistic = 'cpf',percentile = 90, min.bin = 2, width = 'fat')
polarAnnulus(CC, poll='HCNM', period='hour',main='Concón',
             statistic = 'cpf',percentile = 90, min.bin = 2, width = 'fat')
polarAnnulus(GA, poll='HCNM', period='hour',main='Gaviotas',
             statistic = 'cpf',percentile = 90, min.bin = 2, width = 'fat')
polarAnnulus(CO, poll='HCNM', period='hour',main='Colmo',
             statistic = 'cpf',percentile = 90, min.bin = 2, width = 'fat')

# Season
polarAnnulus(VE, poll='HCNM', period='hour', type='season', 
             statistic='cpf', percentile=90,
             hemisphere = 'southern', width='fat',
             main='Ventanas')
polarAnnulus(CQ, poll='HCNM', period='hour', type='season', 
             statistic='cpf', percentile=90,
             hemisphere = 'southern', width='fat',
             main='Centro_Quintero')
polarAnnulus(CC, poll='HCNM', period='hour', type='season', 
             statistic='cpf', percentile=90,
             hemisphere = 'southern', width='fat',
             main='Concón')
polarAnnulus(GA, poll='HCNM', period='hour', type='season', 
             statistic='cpf', percentile=90,
             hemisphere = 'southern', width='fat',
             main='Gaviotas')
polarAnnulus(CO, poll='HCNM', period='hour', type='season', 
             statistic='cpf', percentile=90,
             hemisphere = 'southern', width='fat',
             main='Colmo')

# PolarAnnulus sobre una velocidad de viento 
# (para evitar alta variabilidad en bajas velocidades)
polarAnnulus(subset(CQ,ws > 1),poll='HCNM',period='hour', main='Centro_Quintero')
# Polar Annulus sobre un percentil de HCNM
polarAnnulus(subset(CQ,HCNM > quantile(HCNM,probs=0.9, na.rm=TRUE)),
             poll='HCNM',period='hour', main='Centro_Quintero')


####################################################################
####################################################################

# Los postulantes a los plots que necesito son los siguientes:


######################
## Percentile Roses ##
######################

# Común
percentileRose(VE, poll='HCNM', main = 'Ventanas', key.position = "right",
               percentile = c( 25, 50, 75, 90), mean=FALSE)
percentileRose(CQ, poll='HCNM', main = 'Centro_Quintero', key.position = "right",
               percentile = c( 25, 50, 75, 90), mean=FALSE)
percentileRose(CC, poll='HCNM', main = 'Concón', key.position = "right",
               percentile = c( 25, 50, 75, 90), mean=FALSE)
percentileRose(CO, poll='HCNM', main = 'Colmo', key.position = "right",
               percentile = c( 25, 50, 75, 90), mean=FALSE)

# Estación del año
percentileRose(VE, poll='HCNM', main = 'Ventanas', key.position = "right",
               percentile = c( 25, 50, 75, 90),mean = FALSE,
               type='month',hemisphere='southern')
percentileRose(CQ, poll='HCNM', main = 'Centro_Quintero', key.position = "right",
               percentile = c( 25, 50, 75, 90),mean = FALSE,
               type='month',hemisphere='southern')
percentileRose(CC, poll='HCNM', main = 'Concón', key.position = "right",
               percentile = c( 25, 50, 75, 90),mean = FALSE,
               type='month',hemisphere='southern')
percentileRose(CO, poll='HCNM', main = 'Colmo', key.position = "right",
               percentile = c( 25, 50, 75, 90),mean = FALSE,
               type='month',hemisphere='southern')

# Con percentiles #  c(25, 50, 75, 90, 95, 99, 99.9)
percentileRose(CQ, poll='HCNM', main = 'Centro_Quintero', key.position = "right",
               percentile = c(90, 95, 99.8))

# Smooth con percentiles
percentileRose(CQ, poll='HCNM', main = 'Centro_Quintero', key.position = "right",
               percentile = c(25, 50, 75, 90, 95, 99),
               col = "default", smooth = TRUE)

# Estación y Día-Noche
percentileRose(CQ, pollutant = 'HCNM', type = c("season", "daylight"),
               hemisphere='southern', latitude = -32.78, longitude = -71.53 ,
               mean =FALSE, percentile = c(0, 50, 75, 90))


#################
## Polar Freqs ##
#################

# frecuencia de dirección y velocidad de viento
polarFreq(CQ)

# aporte a concentración media
polarFreq(CQ, pollutant = "HCNM",statistic = "median",min.bin = 2)
polarFreq(VE, pollutant = "HCNM", type = "year",statistic = "mean",min.bin = 2)

# aporte a concentración media pesado por frecuencia
polarFreq(CQ, pollutant = "HCNM", statistic = "weighted.mean", 
          type='season', hemisphere='southern')

# aporte por estación y día-noche
polarFreq(CQ, type = c("season", "daylight"),
          hemisphere='southern', latitude = -32.78, longitude = -71.53 )

# aporte por hora del día
polarFreq(CQ, type = c('season','hour'),
          hemisphere='southern', latitude = -32.78, longitude = -71.53 )

###############
## Wind Rose ##
###############

# Normal
windRose(CQ)

# Por Estación
windRose(VE, type='season', hemisphere='southern')
windRose(CQ, type='season', hemisphere='southern')
windRose(CC, type='season', hemisphere='southern')
windRose(CO, type='season', hemisphere='southern')


windRose(CQ, type='hour')



# Por Año
windRose(CQ, type='year', hemisphere='southern')

# Por Cuantil
windRose(CQ, type='HCNM')



####################
## Pollution Rose ##
####################

# Normal
pollutionRose(VE,pollutant = 'HCNM')
pollutionRose(CQ,pollutant = 'HCNM')
pollutionRose(CC,pollutant = 'HCNM')
pollutionRose(CO,pollutant = 'HCNM')

# Contribución proporcional a la media
pollutionRose(CQ,pollutant = 'HCNM', stat='prop.')

# Por hora: Normalizado y sin línea de segmentación
pollutionRose(CQ,pollutant = 'HCNM',normalise=FALSE,seg=1,
              type = 'hour', hemisphere='southern',layout=c(6,4))

# Por estación del año: no Normalizado y sin línea de segmentación
pollutionRose(VE,pollutant = 'HCNM',seg=1,main='Ventanas',
              type = 'season', hemisphere='southern',layout=c(2,2))
pollutionRose(CQ,pollutant = 'HCNM',seg=1,main='Centro_Quintero',
              type = 'season', hemisphere='southern',layout=c(2,2))
pollutionRose(CC,pollutant = 'HCNM',seg=1,main='Concón',
              type = 'season', hemisphere='southern',layout=c(2,2))
pollutionRose(GA,pollutant = 'HCNM',seg=1,main='Gaviotas',
              type = 'season', hemisphere='southern',layout=c(2,2))
pollutionRose(CO,pollutant = 'HCNM',seg=1,main='Colmo',
              type = 'season', hemisphere='southern',layout=c(2,2))


## Estaciones condicionadas:

# Centro Quintero condicionada por Concón (Crear CQ_cc)
pollutionRose(CQ_cc, pollutant = "Centro_Quintero", 
              type = "Concón", layout = c(2, 2))



#################
## Polar Plots ##
#################

# Normal
polarPlot( CQ, poll = 'HCNM')

# Entre percentiles
polarPlot( CQ, poll = 'HCNM', stati = "cpf", percentile = c(50,60), 
           normalise = FALSE)
polarPlot( CQ, poll = 'HCNM', stati = "cpf", percentile = c(60,70), 
           normalise = FALSE)
polarPlot( CQ, poll = 'HCNM', stati = "cpf", percentile = c(70,80), 
           normalise = FALSE)
polarPlot( CQ, poll = 'HCNM', stati = "cpf", percentile = c(80,90), 
           normalise = FALSE)
polarPlot( CQ, poll = 'HCNM', stati = "cpf", percentile = c(90,100), 
           normalise = FALSE)

# Sobre percentil
polarPlot( VE, poll = 'HCNM', stati = "cpf", percentile = 90,
           main='Ventana', hemisphere='southern', type='season')
polarPlot( CQ, poll = 'HCNM', stati = "cpf", percentile = 75,
           main='Centro_Quintero', hemisphere='southern', type='season')
polarPlot( CC, poll = 'HCNM', stati = "cpf", percentile = 90,
           main='Concón', hemisphere='southern', type='season')
polarPlot( GA, poll = 'HCNM', stati = "cpf", percentile = 90,
           main='Gaviotas', hemisphere='southern', type='season')
polarPlot( CO, poll = 'HCNM', stati = "cpf", percentile = 90,
           main='Colmo', hemisphere='southern', type='season')

# NWR
polarPlot( CQ, poll = 'HCNM', statistic = 'nwr',
           main='Centro_Quintero', hemisphere='southern', type='season')
polarPlot( CQ, poll = 'HCNM', statistic = 'nwr',
           main='Centro_Quintero')
polarPlot( selectByDate( CQ, year = 2019), poll = 'HCNM', statistic = 'nwr',
           ws_spread = 0.5, wd_spread = 4)


# condicionado
polarPlot(CQ_cc, pollutant = 'ratio', stati = "cpf", percentile = 90,
          main = 'ratio Concón/Centro_Quintero')



#####################
### Polar Cluster ###
#####################

library(gridExtra)
library(latticeExtra)
nclust = 10
clust = 8
polarCluster(CQ,pollutant = 'HCNM',n.clusters = nclust,cols = 'Set2',
             normalise = TRUE)
results <- polarCluster(CQ, pollutant='HCNM', n.clusters=nclust,
                        cols= "Set2")
results <- results[['data']]


# ploteamos serie de tiempo de cluster
timeProp(results,
  #subset(results, cluster %in% c("C4")), 
  pollutant = "HCNM",
  proportion = "cluster", 
  avg.time = '1 hour',
  col = openColours("Set2", nclust),#[clust], 
  key.position = 'top', 
  key.columns = nclust, 
  date.breaks = 10
  )

############################
## Selección de Episodios ##
############################

# Permite seleccionar periodos en los que se sobrepasa un umbral por un cierto
# número de valores consecutivos

episode <- selectRunning(CQ, pollutant = "HCNM", threshold = 0.39, run.len = 2)
ep <- episode[episode$criterion == 'yes', ]

nrow(CQ)
nrow(episode)

polarPlot(CQ, pollutant = 'HCNM',min.bin=2)
polarPlot(episode[episode$criterion == 'yes', ], pollutant = 'HCNM',min.bin=1)

# Eventos 2018
timeProp(selectByDate(episode,start ='21/08/2018',end ='28/11/2018'),
         pollutant = 'HCNM', avg.time = 'hour',
         proportion = 'criterion', date.breaks = 12, key.position = 'top',
         key.columns = 2, ylab = 'HCNM [ppm]',cols = c('blue','red'))
# Campaña Septiembre-Octubre 2022
timeProp(selectByDate(episode,start ='27/08/2022',end ='03/11/2022'),
         pollutant = 'HCNM', 
         proportion = 'criterion', date.breaks = 12, key.position = 'top',
         key.columns = 2, ylab = 'HCNM [ppm]',cols = c('blue','red'))
# Eventos 2023 
timeProp(selectByDate(episode,start ='14/03/2023',end ='01/04/2023',hour=5:11),
         pollutant = 'HCNM', avg.time = 'day',
         proportion = 'criterion', date.breaks = 4, key.position = 'top',
         key.columns = 2, ylab = 'HCNM [ppm]',cols = c('blue','red'))

#################################
## Time Series con Wind Arrows ##
#################################

## Ploteamos eventos 2018 con direcciones
DATE1 <- as_datetime("2018-08-21 00:00:00")
DATE2 <- as_datetime("2018-11-28 00:00:00")

## Ploteamos campaña Septiembre-Octubre 2022 con direcciones
DATE1 <- as_datetime("2022-10-04 00:00:00")
DATE2 <- as_datetime("2022-10-04 12:00:00")

## Ploteamos eventos 2023 con direcciones
DATE1 <- as_datetime("2023-03-15 22:00:00")
DATE2 <- as_datetime("2023-03-16 08:00:00")

# Ventanas
VE_ts <- VE %>% dplyr::filter(DATE1<=date & date<=DATE2)
timePlot(VE_ts, pollutant = 'HCNM', lwd = 2, ylab = NULL,
         main = 'Ventanas',strip=FALSE,
         windflow = list(scale = 0.05, lwd = 1.5, col = "turquoise4"))

# Centro Quintero
CQ_ts <- CQ %>% dplyr::filter(DATE1<=date & date<=DATE2)
timePlot(CQ_ts, pollutant = 'HCNM', lwd = 2, ylab = NULL,
         main = 'Centro Quintero',strip=FALSE,
         windflow = list(scale = 0.05, lwd = 1.5, col = "turquoise4"))

# Concón
CC_ts <- CC %>% dplyr::filter(DATE1<=date & date<=DATE2)
timePlot(CC_ts, pollutant = 'HCNM', lwd = 2, ylab = NULL,
         main = 'Concón',strip=FALSE,
         windflow = list(scale = 0.05, lwd = 1.5, col = "turquoise4"))

# Colmo
CO_ts <- CO %>% dplyr::filter(DATE1<=date & date<=DATE2)
timePlot(CO_ts, pollutant = 'HCNM', lwd = 2, ylab = NULL,
         main = 'Colmo',strip=FALSE,
         windflow = list(scale = 0.05, lwd = 1.5, col = "turquoise4"))

