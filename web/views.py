from django.shortcuts import render
import json, urllib3
import random

host_prod = 'https://viztool2020.herokuapp.com'
host_dev = 'http://localhost:8095'

host = host_prod

def html_color():
    return "#" + "%06x" % random.randint(0, 0xFFFFFF)

def index(request):

    # carga de programas de universidad
    http = urllib3.PoolManager()

    response = http.request('GET', f'{host}/apicmp/programa/')
    data_json = response.data.decode('utf-8')
    data = json.loads(data_json)


    programas = {}
    colores = {}
    pesos = {}
    for x in data:
        if x['pesos']:
            programas[x['id']]=x['nombre']
            colores[x['id']] = html_color() # genera colores aleatorios
            pesos[x['id']]= {z['area']:[z['min'], z['max']] for z in x['pesos']}


    # carga de datos de las areas
    response = http.request('GET', f'{host}/apicmp/area/')
    data_json = response.data.decode('utf-8')
    data = json.loads(data_json)
    
    areas = {}
    for x in data:
        areas[x['id']]= [x['numeral'], x['nombre']]


    response = http.request('GET', f'{host}/apicmp/universidad/')
    data_json = response.data.decode('utf-8')
    data = json.loads(data_json)
    
    universidades = {}
    for x in data:
        universidades[x['id']]= x['nombre']

    #carga de programas de universidades
    response = http.request('GET', f'{host}/apicmp/programau/')
    data_json = response.data.decode('utf-8')
    data = json.loads(data_json)

    programasu = {}
    pesosu = {}
    coloresu = {}
    for x in data:
        # carga de pesos min y max para cada programa
        if x['pesosu']:
            programasu[x['id']]='{}-{}'.format(universidades.get(x['universidad'],''),x['nombre'])
            coloresu[x['id']] = html_color() # genera colores aleatorios
            pesosu[x['id']]= {z['area']:[z['min'], z['max']] for z in x['pesosu']}
    

    context = { 'programas': programas,
                'pesos': pesos,
                'universidades': universidades,
                'programasu': programasu,                
                'pesosu': pesosu,
                'colores': colores,
                'coloresu': coloresu,
                'areas': areas,

            }



    return render(request, 'web/form1.html', context)