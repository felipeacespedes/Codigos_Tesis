
# Código para visualizar contaminantes con paquete OpenAir ----------------


# Cargamos librerías ------------------------------------------------------

library(readr)
library(openair)
library(dplyr)
library(lubridate)
library(ggplot2)

# Primera aproximación ----------------------------------------------------

# Cargamos datos
path <- 
  "C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Estaciones/Centro_Quintero/Cont/"
HCNM <- read_delim(paste(path,"HCNM.csv", sep = ""), 
                  delim = ";", escape_double = FALSE, col_types = 
                    cols(...6 = col_skip(), 
                  `FECHA (YYMMDD)` = col_date(format = "%y%m%d"), 
                  `HORA (HHMM)` = col_time(format = "%H %M"), 
                  `Registros no validados` = col_number(), 
                  `Registros preliminares` = col_skip(), 
                  `Registros validados` = col_skip()), 
                  locale = locale(decimal_mark = ","), 
                  trim_ws = TRUE)

# Rename columns
colnames(HCNM) <- c("date", "time", "HCNM")

# Combine Date and Time columns into a single datetime column
HCNM$date <- as.POSIXct(paste(HCNM$date, HCNM$time), format="%Y-%m-%d %H:%M:%S")

# Remove Date and Time columns
HCNM <- subset(HCNM, select = c("date", "HCNM"))

# View HCNM
View(HCNM)

# Use timeVariation function
timeVariation(HCNM, pollutant = "HCNM", 
              main = "Time Variation of HCNM Air Concentration")

# Use summaryPlot, QUEDA PENDIENTE!!
summaryPlot( HCNM, pollutant = 'HCNM', period = 'months')

# Use calendarPlot
calendarPlot( HCNM, pollutant = 'HCNM', main = 'HCNM', year = 2022, month = c(8,9))


# DFs por estación con contaminantes --------------------------------------

# Lista con estaciones, contaminantes y unidades
Est = list('Ventanas','Los_Maitenes','Centro_Quintero','Loncura'
           ,'Sur','Junta_Vecinos','Concón','Gaviotas','Colmo')
Cont = list('HCNM','MP25','CO')

Und = list('ppm','ppm','$$\\mu g/m^{3}$$')

Dic = list(Est = Est, Cont = Cont, Und = Und)

rm(Est,Cont,Und)

# Ciclo for para asignar columna con fechas de interés
Est = list()
# fechas
Fi = "2019-01-01 00:00:00"
Ff = "2023-12-31 23:00:00"
date = seq(as.POSIXct(Fi, tz = "America/Santiago")
           , as.POSIXct(Ff, tz = "America/Santiago")
           , by = "hour")


Est <- lapply(Dic$Est, function(e) {
  data.frame(date = date)
})

# Assign names to the list
names(Est) <- Dic$Est

# Borramos variables de sobra
rm(date, Fi, Ff)

# Read and merge data for each station and contaminant
for (e in Dic$Est) {
  for (c in Dic$Cont) {
    # Construct the file path
    file_path <- paste("C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/",
                       "Estaciones/", e, "/Cont/", c, ".csv", sep = "")
    print(e)
    
    # Check if the directory exists
    if (dir.exists(dirname(file_path))) {
      # Use tryCatch to catch and ignore errors
      tryCatch({
        # Read the file only if the directory exists
        df_ec <- read_delim(
          file_path,
          delim = ";",
          escape_double = FALSE, 
          col_types = cols(...6 = col_skip(), 
                           `FECHA (YYMMDD)` = col_date(format = "%y%m%d"), 
                           `HORA (HHMM)` = col_time(format = "%H %M"), 
                           `Registros no validados` = col_number(), 
                           `Registros preliminares` = col_skip(), 
                           `Registros validados` = col_skip()), 
          locale = locale(decimal_mark = ","), 
          trim_ws = TRUE
        )
        
        # Rename columns
        colnames(df_ec) <- c("date", "time", c)
        
        # Combine Date and Time columns into a single datetime column
        df_ec$date <- as.POSIXct(paste(df_ec$date, df_ec$time)
                                 , format="%Y-%m-%d %H:%M:%S")
        
        # Remove Date and Time columns
        df_ec <- select(df_ec, date, c)
        
        # Merge data frames based on datetime column
        Est[[e]] <- left_join(Est[[e]], df_ec, by = "date")
      }, error = function(err) {
        # Print a message or take other action if an error occurs
        print(paste("Error leyendo el archivo para: ", e, "/", c
                    ,", ",err,sep=""))
      })
    }
  }
}


# Ploteamos Variables  ----------------------------------------------------
ei = 1
for (e in Est) {
  # Creamos variable para dataframe
  df_est = e
  df_est$doy <- yday(df_est$date)
  
  # Create a time variation plot: NO FUNCIONA :(
  #file = paste("/TimeVariation/",
  #              Est[e],".png",sep='')
  #png(file=file)
  timeVariation(df_est,
                pollutant = colnames(df_est)
                [-c(1, ncol(df_est))],
                normalise = TRUE,
                main=Dic$Est[ei]
                )
  #dev.off
  ei = ei+1
}


# ploteamos polar plots

