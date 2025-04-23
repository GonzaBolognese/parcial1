import csv

RUTA = r'.\capturas_maritimas_pba_2010-2024.csv'

def leer_archivo(archivo):
    f = open(archivo, 'rt', encoding='utf-8')
    rows = csv.reader(f)
    especies = dict()
    headers = next(rows)
    for row in rows:
        try:
            record = dict(zip(headers, row))
            if record['especie'].lower() not in especies:
                especies[record['especie'].lower()] = dict()
            especies[record['especie'].lower()][record['año']] = record['toneladas']           
        except:
            return('El archivo ingresado no es valido')
    return especies
def info_por_especie(especie_analizada):
    año_mas = 0
    año_menos = 0
    total = 0.00
    for k in especie_analizada:
            try:
                if type(float(especie_analizada[k])) != str:
                    if  año_mas ==0 or especie_analizada[año_mas]<especie_analizada[k]:
                        año_mas = k
                    if año_menos == 0 or especie_analizada[año_menos]> especie_analizada[k]:
                        año_menos = k
                    total += float(especie_analizada[k])
            except:
                print('Error en formato del csv')
    return [año_mas, año_menos, total]

def info_por_año(especies, fecha):
    especies_pescadas = dict()
    mas_pescada = ''
    menos_pescada = ''
    total = 0
    for e in especies:
        try:
            if fecha in especies[e]:
                if type(float(especies[e][fecha])) != str and especies[e][fecha] != '0.00':
                    especies_pescadas[e]=especies[e][fecha]
        except:
            print(f'El valor de toneladas de {e} en el año {fecha} no es valido')
    for e in especies_pescadas:
        if mas_pescada == '' or especies_pescadas[e] > especies_pescadas[mas_pescada]:
            mas_pescada = e
        if menos_pescada == '' or especies_pescadas[e] < especies_pescadas[menos_pescada]:
            menos_pescada = e
        total += float(especies_pescadas[e])
        
    return [mas_pescada, menos_pescada, total]

def frecuencia(especies):
    especies_concurrentes=list()
    unicas = list()
    for e in especies:
        if len(e)==15:
            especies_concurrentes.append(e)
        if len(e) == 1:
            unicas.append(e)
    return [especies_concurrentes,unicas]

def listado_mas_pescados (especies):
    especie_mas_pescada = ''
    datos_especie_mas = dict()
    especie_menos_pescada = ''
    datos_especie_menos = dict()
    for e in especies:
        informe_especie = info_por_especie(especies[e.lower()])
        if especie_mas_pescada == '' or datos_especie_mas[2] < informe_especie[2]:
            especie_mas_pescada = e
            datos_especie_mas = informe_especie
        if especie_menos_pescada == '' or datos_especie_menos[2] > informe_especie[2]:
            especie_menos_pescada = e
            datos_especie_menos = informe_especie

    return [especie_mas_pescada, especie_menos_pescada]

def año_mas_pescados (especies):
    año_mas = ''
    info_año_mas=list()
    año_menos = ''
    info_año_menos=list()
    años = list(range(2010, 2026))
    for a in años:
        informe_año = info_por_año(especies, str(a))
        if año_mas == '' or info_año_mas[2] < informe_año[2]:
            año_mas = a
            info_año_mas = informe_año
        if año_menos == '' or info_año_menos[2] > informe_año[2]:
            año_menos = a
            info_año_menos = informe_año
    return[año_mas, año_menos]
        

    


def informe_año(archivo, especie='', fecha=''):
    especies = leer_archivo(archivo)
    informe = {
    }
    if especie !='' or fecha !='':
        if especie !='':
            informe_especie = info_por_especie(especies[especie.lower()])
            informe['Año mas pescado']=informe_especie[0]
            informe['Año menos pescado']=informe_especie[1]
            informe['Cantidad (acumulada) de pescado obtenida en total']=informe_especie[2]
            print(informe)
        if fecha != '':
            informe_especies_año = info_por_año(especies, fecha)
            informe[f'Especie mas pescada en {fecha}']=informe_especies_año[0]
            informe[f'Especie menos pescada en {fecha}']=informe_especies_año[1]
            informe[f'Total pescado en {fecha}']=informe_especies_año[2]            
    else:
        absolutos = frecuencia(especies)
        informe['Especies que se pescan absolutamente todos los años'] = absolutos[0]
        informe['Especies que aparecieron una única vez'] = absolutos[1]
        cantidades = listado_mas_pescados(especies)
        informe['Especie mas pescada'] = cantidades[0]
        informe['Especie menos pescada'] = cantidades[1]
        años_record = año_mas_pescados(especies)
        informe['Año en que mas se pescó'] = años_record[0]
        informe['Año en que menos se pescó'] = años_record[1]
    
    print(informe)


#Prueba sin aclarar especie, ni año
informe_año(RUTA)
#Prueba sin aclarar año
informe_año(RUTA,'ABADEJO')
#Prueba sin aclarar especie
informe_año(RUTA, '', '2020')
