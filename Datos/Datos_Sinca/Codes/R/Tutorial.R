# añadimos librería dplyr
install.packages('dplyr')
library(dplyr)

ages <- c(5,6)
names <- c('Juan','Luis')

friends <- data.frame(names,ages)
View(friends)

friends$names
str(friends)

friends[1,]
friends[,1]

data()
View(CO2)


# install library tidyverse
install.packages('tidyverse')
library('tidyverse')


CO2 %>% 
  filter(conc > 30 & uptake < 50) %>%
  mutate(conc_by_10 = conc*10) %>% 
  select(conc_by_10, uptake) %>% 
  arrange(uptake) %>% 
  # View()
  plot()

## Explore data set

# data set mamals
data(msleep)
View(msleep)

# quick overview
glimpse(msleep)

# nombres de columnas
head(msleep)

# clase
class(msleep)

# Largo de DF
length(msleep)

# Largo de columna name en msleep
length(msleep$name)

# Nombres de las variables 
names(msleep)

# Entrega categorias unicas en columna
unique(msleep$vore)

# complete entrega filas en que no hay NAn
# al usar ! se hace lo contrario
missing <- !complete.cases(msleep)

# entrega objeto booleano a indice de filas de df
msleep[missing, ]

## Cleaning data

# Select variables
starwars %>% 
  select(name, height, mass)

# Select indexes of columns
starwars %>% 
  select(1:3)

# Select variable that ends with 'color'
starwars %>% 
  select(ends_with('color')) %>% 
  View()
# , también se puede usar start_with y contains

# Select para cambiar orden de variables
starwars %>% 
  select(name, mass, height, everything())

# Cambiar nombre de variable
starwars %>% 
  rename('characters' = 'name') %>% 
  head()

# cambiar clase/tipo de variable
class(starwars$hair_color)
starwars$hair_color <- as.factor(starwars$hair_color)
class(starwars$hair_color)

# Cambiar clase con tidyverse
starwars %>% 
  mutate(hair_color = as.character(hair_color)) %>% 
  glimpse()

# cambiar nivel de factor
df <- starwars
df$sex <- as.factor(df$sex)

levels(df$sex)

df <- df %>% 
  mutate(sex = factor(sex,
                      levels = c('male',
                                 'female',
                                 'hermaphroditic',
                                 'none')))
levels(df$sex)


# Filtar filas requeridas
starwars %>% 
  select(mass,sex) %>% 
  filter(mass<55 & sex=='male') %>% 
  arrange(mass)

# cambiar nombre de variables
starwars %>% 
  select(sex) %>% 
  mutate(sex = recode(sex,
                      'male'='man',
                      'female'='woman'))

# Tratando con datos Nan
mean(starwars$height) # no sabe que hay Nans
mean(starwars$height, na.rm = TRUE) # remueve Nans
# drop_na()

# Tratando datos duplicados
Names <- c('Peter','John','Andrew','Peter')
Age <- c(22,33,44,22)

friends <- data.frame(Names,Age)
glimpse(friends)

friends %>% 
  distinct()

# lo mismo que 
distinct(friends)

## Manipulate
#################

# Crear o cambiar variable con mutate()
starwars %>% 
  mutate(height_m = height/100) %>% 
  select(name,height,height_m)

# Categorizar alturas por alto y bajo
starwars %>% 
  mutate(height_m = height/100) %>% 
  select(name,height,height_m) %>% 
  mutate(tallness = if_else(height_m<1,'short','tall'))


## Reordenar datos
install.packages('gapminder')
library(gapminder)
View(gapminder)

# Creamos nuevo df con varibales de interés (datos "Largos")
data <- select(gapminder,country,year,lifeExp)
View(data)

# Creamos nuevo df reordenando data, de manera de obtener
# los años como nombres de columnas y las esperanzas de vida
# como valores, creamos datos "anchos"
wide_data <- data %>% 
  pivot_wider(names_from = year, values_from = lifeExp)

View(wide_data)

# Ahora podemos reinvertir el proceso creando datos "Largos"
# , para esto reordenaremos nuevamente por expectativa de vida
# y valores se dejaran cómo años
long_data <- wide_data %>% 
  pivot_longer(2:13,
               names_to='year',
               values_to='lifeExp')

View(long_data)


# Describir datos
#####################
View(msleep)

# Estadisticos
min(msleep$awake)
max(msleep$awake)
range(msleep$awake)
IQR(msleep$awake)

mean(msleep$awake)
median(msleep$awake)
var(msleep$awake)

# summary
summary(msleep$awake)

# summary para 2 variables
msleep %>% 
  select(awake,sleep_total) %>% 
  summary()

# resume tus datos 
msleep %>% 
  drop_na(vore) %>% 
  group_by(vore) %>% 
  summarise(Lower = min(sleep_total),
            Average = mean(sleep_total),
            Upper = max(sleep_total),
            Difference = 
              max(sleep_total)-min(sleep_total)) %>% 
  arrange(Average) %>% 
  View()


