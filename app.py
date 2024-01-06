# Aqui voy a tener todas las funciones que hacen parte de la api
from fastapi import FastAPI
import pandas as pd
import numpy as np
from typing import Union


app = FastAPI()

@app.get('/playTimeGenre/{genero:str}')
def PlayTimeGenre(genero:Union[str, None] = None):
    '''Debe regresar el año con más tiempo de juego según el genero que se esté trayendo.'''
    if genero == None:
        return '{"message":"Es necesario el genero para seguir con su consulta"}'
    

    pass

@app.get('/userForGenre/{genero:str}')
def UserForGenre(genero: Union[str,None] = None):
    '''Retorna el usuario con más horas jugadas por genero, desglozado en las horas que jugó por año.'''
    if genero == None:
        return '{"message":"Es necesario el genero para seguir con su consulta"}'
    

    pass
# Fin
# Comienzo
@app.get('/userRecommend/{year:int}')
def UserRecommend(year: Union[int,None] = None):
    '''Retorne el top 3 de juegos más recomendados según el parámetro de año.'''
    if year == None:
        return '{"message":"Es necesario el año para seguir con su consulta"}'
    
    games = pd.read_parquet('DatasetFinal/games.parquet')
    recomendacion = pd.read_parquet('DatasetFinal/recomendacion.parquet')

    games_year = games[games['año'] == str(year)]

    if games_year.empty:
        return {'error':f'No existen juegos en el año seleccionado. Año:{year}'}

    recomendaciones = []
    for i in games_year['id']:
        scores = recomendacion[recomendacion['item_id'] == i]
        value = scores['recommend'].value_counts()
        if value.__len__() == 0:
            continue
        else:
            if value.__len__() == 1:
                j = value.keys()
                for k in j:
                    if k:
                        recomendaciones.append({"id":i,"value":value[True]})
    
    recomendaciones = sorted(recomendaciones, reverse=True, key= lambda x:x['value'])
    nombres = []
    for i in recomendaciones[0:3]:
        df = games_year[games_year['id'] == i['id']]
        nombres.append(df['title'].values)

    return {"mensaje":f'Los juegos mas recomendados en {year} son: 1: {nombres[0][0]}, 2: {nombres[1][0]}, 3: {nombres[2][0]}'}
# Fin
# Comienzo
@app.get('/usersWorstDeveloper/{year:int}')
def UsersWorstDeveloper(year: Union[int,None] = None):
    '''A partir del parámetro de año retorna el top 3 peores desarrolladores según las recomendaciones de los usuarios'''
    if year == None:
        return '{"message":"Es necesario el año para seguir con su consulta"}'
    
    developer = pd.read_parquet('DatasetFinal/games.parquet')
    recomendacion = pd.read_parquet('DatasetFinal/recomendacion.parquet')

    developer_year = developer[developer['año'] == str(year)]

    if developer_year.empty:
        return {'error':f'No existen juegos en el año seleccionado. Año:{year}'}

    recomendaciones = []
    for i in developer_year['id']:
        scores = recomendacion[recomendacion['item_id'] == i]
        value = scores['recommend'].value_counts()
        if value.__len__() == 0:
            continue
        else:
            if value.__len__() == 1:
                j = value.keys()
                for k in j:
                    if (not k):
                        recomendaciones.append({"id":i,"value":value[False]})
    
    recomendaciones = sorted(recomendaciones, reverse=True, key= lambda x:x['value'])
    nombres = []
    for i in recomendaciones[0:3]:
        df = developer_year[developer_year['id'] == i['id']]
        nombres.append(df['developer'].values)

    return {"mensaje":f'Los desarrolladores menos recomendados en {year} son: 1: {nombres[0][0]}, 2: {nombres[1][0]}, 3: {nombres[2][0]}'}
# Fin
# Comienzo
@app.get('/sentimentAnalysis/{eDesarrolladora:str}')
def SentimentAnalysis(eDesarrolladora: Union[str,None] = None):
    '''Se necesita el nombre de la empresa desarrolladora para retornar un diccionario que contenga una lista de la categorización de los reviews que los usuarios le ha dado a la misma de manera tal que: [positivo=,neutro=,negativo=]'''
    if eDesarrolladora == None:
        return '{"message":"Es necesario el nombre de la empresa desarrolladora para seguir con su consulta"}'
    
    developer = pd.read_parquet('DatasetFinal/games.parquet')
    recomendacion = pd.read_parquet('DatasetFinal/recomendacion.parquet')

    developer_year = developer[developer['developer'] == eDesarrolladora]

    if developer_year.empty:
        return {'error':f'No existen el desarrollador seleccionado. Año:{eDesarrolladora}'}
    # verificar que existe la empresa que se está mandando

    # buscar en el archivo donde se tienen los datos limpios

    # retornar resultado
    # return {eDesarrolladora:f'Negativo:{sal['neg']}, Neutro:{sal['neu']}, Positivo:{sal['pos']}'}
    pass
# Fin
# Comienzo