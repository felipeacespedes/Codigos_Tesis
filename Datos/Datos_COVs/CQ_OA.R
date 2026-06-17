# Instalamos e importmaos librerías
library(openair)
library(readr)
library(dplyr)
library(lubridate)

CQ_file <- "CQ_ContMet1823_OpenAirFormat.csv"

CQ <- read_delim( CQ_file, name_repair = "minimal",
                   delim = ";", escape_double = FALSE,
                   col_types = cols(date = col_datetime
                                    (format = "%d/%m/%Y %H:%M:%S")),
                   trim_ws = TRUE)

CQ$HCNM <- CQ$HCNM
# CQ$HCT <- CQ$HCT/3
# CQ$CH4 <- CQ$CH4/3

### timeVariation ###
# NO, NO2, O3
timeVariation(CQ, pollutant = c('HCNM','NO','NO2','O3'),
              ylab='[ppb]',
              normalise=TRUE,
              main='NO, NO2 y O3 en Centro Quintero entre 2018 y 2023.'
              )
# CH4, HCNM, HCT
timeVariation(CQ, pollutant = c('CH4','HCNM','HCT'),
              ylab='[ppb]',
              # normalise=TRUE,
              main='CH4, HCNM y HCT en Centro Quintero entre 2018 y 2023.'
              )
# HCNM, CO, NO2
timeVariation(CQ, pollutant = c('HCNM','CO','NO2'),
              # ylab='[ppb]',
              normalise=TRUE,
              main='HCNM, CO y NO2 en Centro Quintero entre 2018 y 2023.'
              )

### polarAnulus ###
# HCNM, CO, NO
polarAnnulus( CQ, pollutant = 'HCNM',
              period = 'hour', 
              main='HCNM en Centro Quintero entre 2018 y 2023.',
              statistic = 'mean'
              # normalise=TRUE
              )
polarAnnulus( CQ, pollutant = 'CO',
              period = 'hour', 
              main='CO en Centro Quintero entre 2018 y 2023.',
              statistic = 'mean'
              # normalise=TRUE
              )
polarAnnulus( CQ, pollutant = 'NO',
              period = 'hour', 
              main='NO en Centro Quintero entre 2018 y 2023.',
              statistic = 'mean'
              # normalise=TRUE
              )

### Percentile Rose ###

perc <- c(25, 50, 75, 90, 95, 99)

# PRs de contaminantes con percentiles perc.
percentileRose(CQ, pollutant = 'HCNM',
               key.position = "bottom",
               percentile = perc,
               normalise=TRUE
               )
percentileRose(CQ, pollutant = 'CO',
               key.position = "bottom",
               percentile = perc,
               normalise=TRUE
               )
percentileRose(CQ, pollutant = 'NO',
               key.position = "bottom",
               percentile = perc,
               normalise=TRUE
               )

### CorPlot ###
corPlot(CQ, main='Centro Quintero entre 2018 y 2023.')
corPlot(CQ, cluster = TRUE, main= 'Centro Quintero entre 2018 y 2023.')
CP_dendro <- corPlot(CQ, dendrogram = TRUE)


### Calendar plot for campaign ###

calendarPlot(CQ,pollutant = 'NO', year=2022, month=c(8,9,10,11),
             limits = c(0, 50),statistic = 'max',main='NO')
calendarPlot(CQ,pollutant = 'NO2', year=2022, month=c(8,9,10,11),
             limits = c(0, 50),statistic = 'max',main='NO2')
calendarPlot(CQ,pollutant = 'HCNM', year=2022, month=c(8,9,10,11),
             limits = c(0, 1000),statistic = 'max',main='HCNM')

