# Instalamos e importmaos librerías
library(openair)
library(readr)
library(dplyr)
library(lubridate)
library(vtable)

# Importamos DF
path <- 'C:/Users/felip/Desktop/U/Tesis/Datos/Intoxicados/'
DF_h <- read_delim(paste(path,'DF_h.csv',sep=''))
DF_d <- read_delim(paste(path,'DF_d.csv',sep=''))
colnames(DF_h)[colnames(DF_h) == "ws_CQ"] <- "ws"
colnames(DF_h)[colnames(DF_h) == "wd_CQ"] <- "wd"
colnames(DF_d)[colnames(DF_d) == "ws_CQ"] <- "ws"
colnames(DF_d)[colnames(DF_d) == "wd_CQ"] <- "wd"

# definimos variables
var <- c(
        'O3_CQ','NO2_CQ','NO_CQ','HCNM_CQ',
        'MP25_CQ','MP10_CQ','CO_CQ','SO2_CQ'
        
        # 'HCNM_VE','SO2_VE','NO2_VE','NO_VE','O3_VE',
        # 'MP25_VE','MP10_VE',
        )

## Polar plot
polarPlot(DF_h,poll='HCNM_VE',main='O3_CQ',stat='max')

# Discriminando
polarPlot(subset(DF_h,T59 > 0),poll='HCNM_CQ', main='CQ', stati ='nwr',normalise=FALSE)

# Percentiles
df <- subset(DF_h,evento > 0)
polarPlot(df, poll = var, stati = "cpf", percentile = c(10, 20),normalise = TRUE)
polarPlot(df, poll = var, stati = "cpf", percentile = c(20, 30),normalise = TRUE)
polarPlot(df, poll = var, stati = "cpf", percentile = c(30, 40),normalise = TRUE)
polarPlot(df, poll = var, stati = "cpf", percentile = c(40, 50),normalise = TRUE)
polarPlot(df, poll = var, stati = "cpf", percentile = c(50, 60),normalise = TRUE)
polarPlot(df, poll = var, stati = "cpf", percentile = c(50, 60),normalise = TRUE)
polarPlot(df, poll = var, stati = "cpf", percentile = c(60, 70),normalise = TRUE)
polarPlot(df, poll = var, stati = "cpf", percentile = c(70, 80),normalise = TRUE)
polarPlot(df, poll = var, stati = "cpf", percentile = c(80, 90),normalise = TRUE)
polarPlot(df, poll = var, stati = "cpf", percentile = c(90, 100),normalise = TRUE)


## Polar Annulus
polarAnnulus(DF_h,poll='O3_CQ',main='O3_CQ', stati ='max')

# Polar Annulus discriminando 
polarAnnulus(subset(DF_h,evento > 0),poll=var,period='hour', main='CQ', stati ='mean',normalise=TRUE)

### Polar Cluster ###
#####################
library(gridExtra)
library(latticeExtra)
nclust = 9
clust = 7
polarCluster(subset(DF_h,evento > 0),pollutant = 'HCNM_CQ',n.clusters = nclust,cols = 'Set2',
             normalise = FAL)
results <- polarCluster(DF_h, pollutant='HCNM_CQ', n.clusters=nclust,
                        cols= "Set2",year=2023)
results <- results[['data']]


# ploteamos serie de tiempo de cluster
timeProp(results,
         # subset(results, cluster %in% c("C7")),
         pollutant = "HCNM_CQ",
         proportion = "cluster", 
         avg.time = '1 day',
         col = openColours("Set2", nclust),#[clust], 
         key.position = 'top', 
         key.columns = nclust, 
         date.breaks = 10,
)

# Corrplot
corPlot(subset(DF_d,T59 > 50), cluster=TRUE )
