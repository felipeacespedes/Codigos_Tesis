# Lucas Castillo Elmes
# lcastilloelmes@gmail.com
# Codigo original por Camilo Menares
# En caso de querer acceder a codigo original, tanto este cómo el de R se 
# encuentran en la carpeta Tesis/Datos/datos_Lucas

#? Librerias
import requests
import os
import numpy as np

#? Lista de estaciones

est_name = {'RV': [ 'Ventanas','Los Maitenes','Centro Quintero','Loncura' \
     ,'Sur','Junta de Vecinos','Concón','Las Gaviotas','Colmo']}
est_id = {'RV': ['548','504','539','547','506','535','509','512','511']}

#est_name = {'RV': [ 'Los Andes',  'La Palma', 'San Pedro'], 'RM': ['Cerrillos', 'Cerrillos I', 'Cerro Navia', 'El Bosque', 'Independencia', 'La Florida', 'Las Condes', 'Pudahuel', 'Puente Alto', 'Quilicura', 'Quilicura I', "Parque O'Higgins", 'Talagante'], 'RVI': ['San Fernando'], 'RVII': ['La Florida'], 'RVIII': ['Kingston College', 'Hualqui'], 'RXI': ['Coyhaique II']}
#est_id = {'RV': ['532','515', '514'], 'RM': ['D31', 'D16', 'D18', 'D17', 'D11', 'D12', 'D13', 'D15', 'D27', 'D30', 'D29', 'D14', 'D28'], 'RVI': ['612'], 'RVII': ['703'], 'RVIII': ['827', '841'], 'RXI': ['B04']}

#est_name = {'RXV': ['Arica'], 'RI': ['Alto Hospicio'], 'RII': ['Antofagasta', 'Playa Blanca', 'Rendic', 'Sur', 'Chiu Chiu', 'Club Deportivo 23 de Marzo', 'Colegio Pedro Vergara Keller', 'Estacion Centro', 'Hospital el Cobre', 'Nueva ChiuChiu', 'Oasis', 'Servicio Medico Legal', 'Aukahuasi', 'San Jose', 'Villa Caspana', 'Hospital', 'Iglesia', 'Jardin Infantil Integra', 'Juan Jose Latorre', 'Compañia de Bomberos', 'Ferrocarriles', 'Sierra Gorda', 'Paposo', 'Punto de Maximo Impacto', 'Bomberos', 'Gobernacion', 'Super Site', 'Tres Marias', 'Escuela E-10', 'Centro', 'Escuela E-12', 'Escuela Gabriela Mistral', 'Sur'], 'RIII': ['Copiapo Sivica', 'Copiapo', 'Los Volcanes', 'Paipote', 'San Fernando', 'CAP', 'Cine Inca', 'Dona Ines', 'Intelec', 'SM6', 'SM7', 'SM8', 'Huasco Sivica', '21 de Mayo', 'EME F', 'EME M', 'EME ME', 'Huasco II', 'SM1', 'SM2', 'SM3', 'SM4', 'SM5', 'Tierra Amarilla', 'Pabellon'], 'RIV': ['Andacollo', 'Chepiquilla', 'El Sauce', 'Hospital', 'Urmeneta - Plaza Centenario', 'Coquimbo', 'La Serena', 'Caimanes', 'Chacay', 'El Mauro', 'Punta Chungo', 'Cuncumen', 'Camisas', 'Coiron', 'Hotel Mina', 'Quelen Alto'], 'RV': ['La Cruz, Colbun', 'La Calera', 'Rural 1', 'Catemu', 'Chagres Meteorologia', 'Romeral', 'Santa Margarita', 'Concon MMA', 'Colmo', 'Concon', 'Junta de Vecinos', 'Las Gaviotas', 'Concon sur', 'La Cruz, Melon', 'Los Andes', 'Lo Campo', 'Puchuncavi', 'Campiche', 'La Greda', 'Los Maitenes', 'Ventanas', 'Meteorologica Principal', 'Terminal Concentrados', 'Cuerpo de Bomberos', 'La Palma', 'San Pedro', 'Manzanar', 'Quilpue', 'ARMAT', 'Centro Quintero', 'Loncura', 'Central Quintero', 'Quintero', 'Sur', 'Valle Alegre', 'Valparaiso', 'Vina del Mar'], 'RM': ['Cerrillos', 'Cerrillos I', 'Cerro Navia', 'El Bosque', 'Independencia', 'La Florida', 'Las Condes', 'Pudahuel', 'Puente Alto', 'Quilicura', 'Quilicura I', "Parque O'Higgins", 'Talagante'], 'RVI': ['Codegua', 'Subestacion Candelaria', 'Cauquenes', 'Cipreses', 'Coya Poblacion', 'Sewell', 'Casas de Peuco', 'San Francisco de Mostazal', 'Rancagua I', 'Rancagua II', 'Rengo', 'MVC', 'Totihue', 'San Fernando'], 'RVII': ['Cauquenes Sivica', 'Curico', 'El Boldo', 'Linares', 'La Florida', 'U.C. Maule', 'Universidad de Talca', 'Teno, CEMENTOS BIO BIO', 'Teno, ENLASA'], 'RVIII': ['Colicheu', 'Punteras', 'Meteorologica, Chiguayante', 'INIA, Chillan', 'Puren', 'Kingston College', 'Cerro Merquin', 'Calabozo', 'Coronel Norte', 'Coronel Sur', 'Escuadron, ENEL', 'Escuadron, ENESA', 'Lagunillas, ENEL', 'Lota rural', 'Lota urbana', 'Balneario Curanilahue', 'Bocatoma', 'ENAP Price', 'JUNJI', 'Hualqui', 'Laja', '21 de mayo', 'Los Angeles Oriente', 'CESFAM, Los Angeles', 'Club de Empleados', 'Entre Rios', 'Lautaro', 'Cayumanqui', 'Quillon', 'Nueva Aldea','San Carlos', 'MASISA Mapal', 'Consultorio - San Vicente', 'Libertad', 'San Vicente, Bomberos', 'Indura', 'Inpesca', 'Nueva Libertad', 'Liceo Polivalente'], 'RIX': ['Padre Las Casas II', 'Padre Las Casas', 'Las Encinas Temuco', 'Nielol', 'Museo Ferroviario'], 'RXIV': ['CESFAM Lago Ranco', 'La Union', 'Consultorio Mafil', 'Fundo La Ribera', 'Vivero Los Castanos', 'Valdivia', 'Valdivia 2'], 'RX': ['Osorno', 'Entre Lagos', 'Alerce', 'Mirasol', 'Trapen Norte', 'Trapen Sur', 'Puerto Varas'], 'RXI': ['Vialidad', 'Coyhaique', 'Coyhaique II'], 'RXII': ['Punta Arenas']}
#est_id = {'RXV': ['F01'], 'RI': ['117'], 'RII': ['237', '226', '225', '213', '228', '233', '235', '236', '217', '253', '234', '227', '219', '220', '218', '210', '211', '209', '252', '221', '207', '204', '216', '215', '230', '201', '251', '231', '222', '205', '203', '202', '206'], 'RIII': ['332', '311', '315', '314', '313', '320', '0', '321', '0', '306', '307', '308', '333', '330', '310', '309', '324', '329', '301', '302', '303', '304', '305', '312', '316'], 'RIV': ['420', '411', '412', '414', '415', '426', '425', '407', '402', '406', '408', '424', '405', '404', '401', '409'], 'RV': ['534', '517', '518', '522', '0', '523', '524', '560', '511', '509', '535', '512', '510', '519', '532', '521', '505', '501', '503', '504', '548', '0', '502', '513', '515', '514', '533', '549', '525', '539', '547', '0', '540', '506', '507', '550', '529'], 'RM': ['D31', 'D16', 'D18', 'D17', 'D11', 'D12', 'D13', 'D15', 'D27', 'D30', 'D29', 'D14', 'D28'], 'RVI': ['601', '0', '606', '605', '604', '608', '603', '602', '609', '615', '611', '613', '614', '612'], 'RVII': ['714', '709', '706', '713', '703', '710', '711', '704', '705'], 'RVIII': ['876', '854', '833', '810', '873', '827', '831', '809', '878', '816', '880', '881', '879', '859', '860', '832', '805', '838', '804', '841', '826', '875', '874', '836', '818', '852', '870', '871', '850', '846','884', '819', '802', '803', '801', '807', '806', '837', '830'], 'RIX': ['902', '903', '901', '905', '904'], 'RXIV': ['E06', 'E04', 'E01', 'E05', 'E02', 'E03', 'E08'], 'RX': ['A01', 'A04', 'A08', 'A07', 'A02', 'A03', 'A09'], 'RXI': ['B05', 'B03', 'B04'], 'RXII': ['C05']}
    

#? Descargar datos contaminacion SINCA
def sinca_aq(i, f, R, c_aq):

    fecha_i = i[2:4] + i[5:7] + i[8:10]
    fecha_f = f[2:4] + f[5:7] + f[8:10]

    c_id = ['PM25' , 'PM10' ,'0003' , '0NOX' , '0001' , '0008' ,'0004' \
            ,'0002','0CH4','NMHC'] 
    c_name = ['PM25' , 'PM10' ,'NO2' , 'NOx' , 'SO2' , 'O3' ,'CO' \
              , 'NO' , 'CH4','NMHC'] 
    c_dic = {'PM25':'PM25','PM10':'PM10', 'NO2':'0003','NOx':'0NOX'\
             ,'SO2':'0001','O3':'0008','CO':'0004','NO':'0002','CH4':'0CH4'\
                 ,'NMHC':'NMHC'}
        
    reg = ['RXV','RI','RII','RIII','RIV','RV','RM','RVI','RVII','RVIII'\
           ,'RIX','RXIV','RX','RXI','RXII']
    
    est_name = {'RV': [ 'Ventanas','Los Maitenes','Centro Quintero','Loncura'\
                ,'Sur','Junta de Vecinos','Concón','Las Gaviotas','Colmo']\
              , 'RM': ['Cerrillos', 'Cerrillos I', 'Cerro Navia', 'El Bosque'\
                       , 'Independencia', 'La Florida', 'Las Condes'\
                       , 'Pudahuel', 'Puente Alto', 'Quilicura', 'Quilicura I'\
                       , "Parque O'Higgins", 'Talagante']\
              , 'RVI': ['San Fernando']\
              , 'RVII': ['La Florida']\
              , 'RVIII': ['Kingston College', 'Hualqui']\
              , 'RXI': ['Coyhaique II']}
    est_id = {'RV': ['548','504','539','547','506','535'\
                     ,'509','512','511']\
              , 'RM': ['D31', 'D16', 'D18', 'D17', 'D11', 'D12', 'D13', 'D15'\
                       , 'D27', 'D30', 'D29', 'D14', 'D28']\
              , 'RVI': ['612']\
              , 'RVII': ['703']\
              , 'RVIII': ['827', '841']\
              , 'RXI': ['B04']}

    n_reg = len(est_name[R])
    reg_iso = {'RXV':['AP'],'RI':['TA'],'RII':['AN'],'RIII':['AT']\
               ,'RIV':['CO'],'RV':['VS'],'RM':['RM'],'RVI':['LI']\
               ,'RVII':['ML'],'RVIII':['BI'],'RIX':['AR'],'RXIV':['LR']\
               ,'RX':['LL'],'RXI':['AI'],'RXII':['MA']}

    for i in c_aq:
        n_iso = 1
        for j in range(n_reg):

            nn = str(n_iso).zfill(2)
            url = 'http://sinca.mma.gob.cl/cgi-bin/APUB-MMA/apub.tsindico2.cgi?outtype=xcl&macro=./' + R + '/' + est_id[R][j] + '/Cal/' + c_dic[i] + '//' + c_dic[i] + '.horario.horario.ic&from=' + fecha_i + '&to=' + fecha_f + '&path=/usr/airviro/data/CONAMA/&lang=esp&rsrc=&macropath=';
            fileName = 'CL' + reg_iso[R][0] + nn + '_' + est_name[R][j] + '_' + i + '.csv'
            print('Descarga: ' + fileName)
            req = requests.get(url)
            file = open(fileName, 'wb')
            for chunk in req.iter_content(100000):
                file.write(chunk)
            file.close()
            n_iso = n_iso + 1

    return(url)

#? Descargar datos meteorologicos SINCA
# hacer vector con alturas para iterar 
alt = []
for i in range(16):
    alt.append(str(i).zfill(3))


def sinca_met(i, f, R, c_met):
    
    fecha_i = i[2:4] + i[5:7] + i[8:10]
    fecha_f = f[2:4] + f[5:7] + f[8:10]

    c_id = ['WDIR','WSPD','TEMP', 'RHUM']
    c_name = ['WDIR','WSPD','TEMP', 'RHUM']
    c_dic = {'WDIR':'WDIR','WSPD':'WSPD','TEMP':'TEMP','RHUM':'RHUM'}
        
    reg = ['RXV','RI','RII','RIII','RIV','RV','RM','RVI','RVII','RVIII','RIX','RXIV','RX','RXI','RXII']
    
    est_name = {'RV': [ 'Ventanas','Los Maitenes','Centro Quintero','Loncura'\
                ,'Sur','Junta de Vecinos','Concón','Las Gaviotas','Colmo']\
                , 'RM': ['Cerrillos', 'Cerrillos I', 'Cerro Navia', 'El Bosque'\
                         , 'Independencia', 'La Florida', 'Las Condes'\
                             , 'Pudahuel', 'Puente Alto', 'Quilicura'\
                                 , 'Quilicura I', "Parque O'Higgins"\
                                     , 'Talagante']\
                , 'RVI': ['San Fernando'], 'RVII': ['La Florida']\
                , 'RVIII': ['Kingston College', 'Hualqui']\
                , 'RXI': ['Coyhaique II']}
    est_id = {'RV': ['548','504','539','547','506','535','509','512','511']\
              , 'RM': ['D31', 'D16', 'D18', 'D17', 'D11', 'D12', 'D13', 'D15'\
                       , 'D27', 'D30', 'D29', 'D14', 'D28'], 'RVI': ['612']\
              , 'RVII': ['703'], 'RVIII': ['827', '841'], 'RXI': ['B04']}

    n_reg = len(est_name[R])

    reg_iso = {'RXV':['AP'],'RI':['TA'],'RII':['AN'],'RIII':['AT']\
               ,'RIV':['CO'],'RV':['VS'],'RM':['RM'],'RVI':['LI']\
               ,'RVII':['ML'],'RVIII':['BI'],'RIX':['AR'],'RXIV':['LR']\
               ,'RX':['LL'],'RXI':['AI'],'RXII':['MA']}

    for i in c_met:
        n_iso = 1
        for j in range(n_reg):
            for a in alt:

                nn = str(n_iso).zfill(2)

                if i == 'WDIR':
                    url = 'https://sinca.mma.gob.cl/cgi-bin/APUB-MMA/apub.tsindico2.cgi?outtype=xcl&macro=./' + R + '/' + est_id[R][j] + '/Met/' + c_dic[i] + '//horario_' + a + '_spec.ic&from=' + fecha_i + '&to=' + fecha_f + '&path=/usr/airviro/data/CONAMA/&lang=esp&rsrc=&macropath=';
                else:
                    url = 'https://sinca.mma.gob.cl/cgi-bin/APUB-MMA/apub.tsindico2.cgi?outtype=xcl&macro=./' + R + '/' + est_id[R][j] + '/Met/' + c_dic[i] + '//horario_' + a + '.ic&from=' + fecha_i + '&to=' + fecha_f + '&path=/usr/airviro/data/CONAMA/&lang=esp&rsrc=&macropath=';

                fileName = 'CL' + reg_iso[R][0] + nn + '_' + est_name[R][j] + '_' + i + '_' + a + '.csv'
                print('Descarga: ' + fileName)
                
                req = requests.get(url)
                file = open(fileName, 'wb')
                for chunk in req.iter_content(100000):
                    file.write(chunk)
                file.close()
            n_iso = n_iso + 1

    return(url)

#? Input
# os.chdir('C:/Users/felip/Desktop/U/Tesis/Datos/Datos_Sinca/Download_code')
# i = '1997-01-01'
# f = '2023-12-31'
# R = ['RM']
# c_aq = ['O3','NO','NO2','NOx','CO']

# for j in R:
#     print(j)
#     sinca_aq(i,f,j,c_aq)
 
