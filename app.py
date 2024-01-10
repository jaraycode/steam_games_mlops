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
    try:
        playtime = pd.read_parquet('DatasetFinal/playtime.parquet')

        playtime = playtime[playtime['genero'] == genero]

        playtime = playtime.sort_values(by='horas',ascending=False)

        return {f"Año de lanzamiento con más horas jugadas del genero {genero}":f"{playtime['año'].values[0]}"}
    except:
        return {"Error":"El genero no existe dentro del dataset"}

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
    recomendacion = pd.read_parquet('DatasetFinal/reviews.parquet')

    games_year = games[games['año'] == str(year)]

    if games_year.empty:
        return {'error':f'No existen juegos en el año seleccionado. Año:{year}'}

    recomendaciones = []
    for i in games_year['id']:
        scores = recomendacion[recomendacion['item_id'] == i]
        value = scores['recommend'].value_counts()
        sentiment = scores['sentiment'].value_counts()
        if sentiment.empty:
            if value.empty:
                continue
            else:
                if value.__len__() == 1:
                    j = value.keys()
                    for k in j:
                        if k:
                            recomendaciones.append({"id":i,"value":value[True]})
                else:
                    recomendaciones.append({"id":i,"value":value[True]})
        else:
            if value.empty:
                continue
            else:
                if value.__len__() == 1:
                    j = value.keys()
                    s = sentiment.keys()
                    aux = 0
                    for s2 in s:
                        if s2 == 1 | s2 == 2:
                           aux = sentiment[1] + sentiment[2] 
                    for k in j:
                        if k:
                            recomendaciones.append({"id":i,"value":value[True] + aux})
                else:
                    s = sentiment.keys()
                    aux = 0
                    for s2 in s:
                        if s2 == 1 | s2 == 2:
                           aux = sentiment[1] + sentiment[2] 
                    recomendaciones.append({"id":i,"value":value[True] + aux})
    recomendaciones = sorted(recomendaciones, reverse=True, key= lambda x:x['value'])
    nombres = []
    for i in recomendaciones[0:3]:
        df = games_year[games_year['id'] == i['id']]
        nombres.append(df['title'].values)

    return [{'Puesto 1': nombres[0][0]}, {'Puesto 2': nombres[1][0]}, {'Puesto 3': nombres[2][0]}]
# Fin
# Comienzo
@app.get('/usersWorstDeveloper/{year:int}')
def UsersWorstDeveloper(year: Union[int,None] = None):
    '''A partir del parámetro de año retorna el top 3 peores desarrolladores según las recomendaciones de los usuarios'''
    if year == None:
        return '{"message":"Es necesario el año para seguir con su consulta"}'
    
    developer = pd.read_parquet('DatasetFinal/games.parquet')
    recomendacion = pd.read_parquet('DatasetFinal/reviews.parquet')

    developer_year = developer[developer['año'] == str(year)]

    if developer_year.empty:
        return {'error':f'No existen juegos en el año seleccionado. Año:{year}'}

    recomendaciones = []
    for i in developer_year['id']:
        scores = recomendacion[recomendacion['item_id'] == i]
        value = scores['recommend'].value_counts()
        sentiment = scores['sentiment'].value_counts()
        if sentiment.empty:
            if value.empty:
                continue
            else:
                if value.__len__() == 1:
                    j = value.keys()
                    for k in j:
                        if (not k):
                            recomendaciones.append({"id":i,"value":value[False]})
                else:
                    recomendaciones.append({"id":i,"value":value[False]})
        else:
            if value.empty:
                continue
            else:
                if value.__len__() == 1:
                    j = value.keys()
                    s = sentiment.keys()
                    aux = 0
                    for s2 in s:
                        if s2 == 0:
                           aux = sentiment[0] 
                    for k in j:
                        if (not k):
                            recomendaciones.append({"id":i,"value":value[False] + aux})
                else:
                    s = sentiment.keys()
                    aux = 0
                    for s2 in s:
                        if s2 == 0:
                           aux = sentiment[0] 
                    recomendaciones.append({"id":i,"value":value[False] + aux})
    
    recomendaciones = sorted(recomendaciones, reverse=True, key= lambda x:x['value'])
    nombres = []
    for i in recomendaciones[0:3]:
        df = developer_year[developer_year['id'] == i['id']]
        nombres.append(df['developer'].values)
    return [{'Puesto 1': nombres[0][0]}, {'Puesto 2': nombres[1][0]}, {'Puesto 3': nombres[2][0]}]
# Fin
# Comienzo
@app.get('/sentimentAnalysis/{eDesarrolladora:str}')
def SentimentAnalysis(eDesarrolladora: Union[str,None] = None):
    '''Se necesita el nombre de la empresa desarrolladora para retornar un diccionario que contenga una lista de la categorización de los reviews que los usuarios le ha dado a la misma de manera tal que: [positivo=,neutro=,negativo=]'''
    if eDesarrolladora == None:
        return '{"message":"Es necesario el nombre de la empresa desarrolladora para seguir con su consulta"}'
    
    developer = pd.read_parquet('DatasetFinal/games.parquet')
    recomendacion = pd.read_parquet('DatasetFinal/reviews.parquet')

    developer_year = developer[developer['developer'] == eDesarrolladora]

    if developer_year.empty:
        return {'error':f'No existen el desarrollador seleccionado. Año:{eDesarrolladora}'}
    
    developer_filtered = developer[developer['developer'] == eDesarrolladora]

    if developer_filtered.empty:
        return {'error': f'La empresa desarrolladora no existe en los datos actuales. Empresa {eDesarrolladora}'}
    
    sentiment_total = []
    for game in developer_filtered['id']:
        scores = recomendacion[recomendacion['item_id'] == game]
        sentiment = scores['sentiment'].value_counts()
        if sentiment.empty:
            continue
        else:
            print(sentiment)
            pos = 0
            neg = 0
            neu = 0
            if sentiment.__len__() == 3:
                sentiment_total.append({"neg":sentiment[0],"neu":sentiment[1],"pos":sentiment[2]})
            elif sentiment.__len__() < 3:
                for s in sentiment:
                    if s == 2:
                        pos = s
                    elif s == 1:
                        neu = s
                    elif s == 0:
                        neg = s
                sentiment_total.append({"neg":neg,"neu":neu,"pos":pos})

    neutro = 0
    positivo = 0
    negativo = 0

    for s in sentiment_total:
        neutro += s['neu']
        positivo += s['pos']
        negativo += s['neg']

    return {f'{eDesarrolladora}': [f'Negativo = {negativo}', f'Neutro = {neutro}', f'Positivo = {positivo}']}
# Fin
# Comienzo